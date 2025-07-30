from fastapi import APIRouter, Depends, HTTPException
from app.schemas.automation import SignupPayload
from app.internal.automation.run import run_ai_driven_signup
from app.internal.dolphin_api.api import DolphinAPI
from app.core.config import settings
from playwright.async_api import async_playwright
import os
import time

router = APIRouter()

def get_dolphin_api():
    return DolphinAPI(api_token=settings.DOLPHIN_API_TOKEN)

@router.post("/signup")
async def automate_signup(payload: SignupPayload, dolphin_api: DolphinAPI = Depends(get_dolphin_api)):
    # --- Get the next proxy ---
    proxy_dir = f"proxies/{payload.proxy_username}"
    if not os.path.isdir(proxy_dir):
        raise HTTPException(status_code=404, detail=f"No proxy directory found for username: {payload.proxy_username}")

    proxy_file = None
    for f in os.listdir(proxy_dir):
        if f.endswith(".txt") and f != "last_used_port.txt":
            proxy_file = os.path.join(proxy_dir, f)
            break

    if not proxy_file:
        raise HTTPException(status_code=404, detail=f"No proxy file found for username: {payload.proxy_username}")

    with open(proxy_file, "r") as f:
        proxies_from_file = [line.strip() for line in f.readlines()]

    if not proxies_from_file:
        raise HTTPException(status_code=404, detail=f"No proxies found in file for username: {payload.proxy_username}")

    state_file = os.path.join(proxy_dir, "last_used_port.txt")
    last_used_port = None
    if os.path.exists(state_file):
        with open(state_file, "r") as f:
            last_used_port = f.read().strip()

    next_proxy_str = None
    if last_used_port:
        last_used_index = -1
        for i, proxy_str in enumerate(proxies_from_file):
            if last_used_port in proxy_str:
                last_used_index = i
                break

        if last_used_index != -1:
            next_index = (last_used_index + 1) % len(proxies_from_file)
            next_proxy_str = proxies_from_file[next_index]
        else:
            next_proxy_str = proxies_from_file[0]
    else:
        next_proxy_str = proxies_from_file[0]

    try:
        credentials, host_port = next_proxy_str.split("@")
        login, password = credentials.split(":")
        host, port_str = host_port.split(":")
        port = int(port_str)
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid proxy format in file.")

    proxy_details = {
        "type": "socks5",
        "host": host,
        "port": port,
        "login": login,
        "password": password,
        "name": f"socks5://{login}:{password}@{host}:{port}",
        "changeIpUrl": "",
    }

    # --- Create Dolphin profile ---
    # Read the country from the file
    country_file_path = os.path.join(proxy_dir, "country.txt")
    country = "XX" # Default country
    if os.path.exists(country_file_path):
        with open(country_file_path, "r") as f:
            country = f.read().strip()

    profile_name = f"{payload.type.upper()}_{country.upper()}_{time.strftime('%d%m%Y')}"
    profile_id = dolphin_api.create_profile(name=profile_name, proxy_details=proxy_details)
    if not profile_id:
        raise HTTPException(status_code=500, detail="Failed to create Dolphin profile")

    # --- Update last used port state ---
    with open(state_file, "w") as f:
        f.write(str(port))

    # --- Run automation ---
    ws_endpoint, _ = dolphin_api.start_profile_automation(profile_id)
    if not ws_endpoint:
        raise HTTPException(status_code=500, detail="Failed to start Dolphin profile")

    async with async_playwright() as p:
        await run_ai_driven_signup(p, ws_endpoint, payload)

    dolphin_api.stop_profile(profile_id)
    return {"status": "completed", "profile_id": profile_id}