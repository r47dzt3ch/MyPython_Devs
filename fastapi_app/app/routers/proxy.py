from fastapi import APIRouter, Depends, HTTPException
from app.internal.proxy_manager.api import ProxyManager
from app.core.config import settings
from app.schemas.proxy import ResidentialProxyRequest
import os
import json
import zipfile
import io
import time

router = APIRouter()

def get_proxy_manager():
    return ProxyManager(config={'key': settings.PROXY_API_KEY})

@router.get("/geo")
async def get_geo_data(proxy_manager: ProxyManager = Depends(get_proxy_manager)):
    try:
        geo_data = proxy_manager.residentGeo()
        # The geo data is returned as a zip file in binary format.
        # I need to unzip it and return the JSON content.
        
        with zipfile.ZipFile(io.BytesIO(geo_data), 'r') as zip_ref:
            # I'm assuming there's a single JSON file in the zip.
            json_file_name = zip_ref.namelist()[0]
            with zip_ref.open(json_file_name) as json_file:
                return json.load(json_file)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch GEO data: {e}")

@router.get("/next-residential")
async def get_next_residential_proxy(username: str):
    proxy_dir = f"proxies/{username}"
    if not os.path.isdir(proxy_dir):
        raise HTTPException(status_code=404, detail=f"No proxy directory found for username: {username}")

    # Find the proxy list file
    proxy_file = None
    for f in os.listdir(proxy_dir):
        if f.endswith(".txt") and f != "last_used_port.txt" and f != "country.txt":
            proxy_file = os.path.join(proxy_dir, f)
            break

    if not proxy_file:
        raise HTTPException(status_code=404, detail=f"No proxy file found for username: {username}")

    with open(proxy_file, "r") as f:
        proxies_from_file = [line.strip() for line in f.readlines()]

    if not proxies_from_file:
        raise HTTPException(status_code=404, detail=f"No proxies found in file for username: {username}")

    # State file to store the last used port
    state_file = os.path.join(proxy_dir, "last_used_port.txt")
    last_used_port = None
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            last_used_port = f.read().strip()

    next_proxy_str = None
    if last_used_port:
        # Find the index of the last used port
        last_used_index = -1
        for i, proxy_str in enumerate(proxies_from_file):
            if last_used_port in proxy_str:
                last_used_index = i
                break

        if last_used_index != -1:
            next_index = (last_used_index + 1) % len(proxies_from_file)
            next_proxy_str = proxies_from_file[next_index]
        else:
            # If the last used port is not in the list, start from the beginning
            next_proxy_str = proxies_from_file[0]
    else:
        # If no last used port, start from the beginning
        next_proxy_str = proxies_from_file[0]

    try:
        credentials, host_port = next_proxy_str.split("@")
        login, password = credentials.split(":")
        host, port = host_port.split(":")

        return {
            "host": host,
            "port": int(port),
            "login": login,
            "password": password,
        }
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid proxy format in file.")

@router.post("/create-residential")
async def create_residential_proxy(payload: ResidentialProxyRequest, proxy_manager: ProxyManager = Depends(get_proxy_manager)):
    
    title = f"{payload.country.upper()}_{payload.type.upper()}_{time.strftime('%d%m%Y')}"
    
    try:
        creation_params = {
            "country": payload.country,
            "region": payload.region,
            "city": payload.city,
            "isp": payload.isp,
            "title": title
        }
        created_proxy = proxy_manager.residentCreate(**creation_params)
        
        if not created_proxy:
            raise HTTPException(status_code=500, detail="Failed to create residential proxy or invalid response.")
            
        proxy_id = created_proxy.get("id")
        login = created_proxy.get("login")
        
        if not proxy_id or not login:
            raise HTTPException(status_code=500, detail="Invalid response from proxy creation API.")

        exported_proxies = proxy_manager.residentExport(proxy_id)
        
        if not exported_proxies:
            raise HTTPException(status_code=500, detail="Failed to export proxy list.")

        proxy_dir = f"proxies/{login}"
        os.makedirs(proxy_dir, exist_ok=True)
        
        # Save the proxy list
        file_path = os.path.join(proxy_dir, "proxy_list.txt")
        with open(file_path, "w") as f:
            f.write(exported_proxies.decode('utf-8'))
            
        # Save the country
        country_file_path = os.path.join(proxy_dir, "country.txt")
        with open(country_file_path, "w") as f:
            f.write(payload.country)
            
        return {"status": "success", "message": f"Proxy list saved to {file_path}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create residential proxy: {e}")