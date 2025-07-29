from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import random
import json
import requests
from playwright.async_api import async_playwright, Playwright
import google.generativeai as genai
from bs4 import BeautifulSoup
from proxy_seller_user_api import Api as ProxySellerApi
import os
import time
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# --- CONFIGURATION ---
DOLPHIN_API_TOKEN = os.getenv("DOLPHIN_API_TOKEN")
DOLPHIN_API_URL = os.getenv("DOLPHIN_API_URL")
DOLPHIN_API_LOCAL = os.getenv("DOLPHIN_API_LOCAL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Residential Proxy Credentials
PROXY_API_KEY = os.getenv("PROXY_SELLER_API_KEY")
# --- Pydantic Models ---
class SignupPayload(BaseModel):
    name: str
    email: str
    password: str
    proxy_username: str
    type: str # e.g., "AMZ", "FB"

class ProfileResponse(BaseModel):
    profile_id: int
    status: str

class AutomationRequest(BaseModel):
    profile_id: int

class ResidentialProxyRequest(BaseModel):
    country: str
    region: str
    city: str
    isp: str
    type: str # e.g., "AMZ", "FB"

class ProxyManager:
    """Manages residential proxies from Proxy-Seller using the SDK."""

    def __init__(self, api_key):
        self.api = ProxySellerApi({'key': api_key})

    def get_residential_proxies(self):
        """Fetches the list of residential proxies."""
        print("Fetching residential proxies...")
        try:
            return self.api.residentList()
        except Exception as e:
            print(f"Error fetching residential proxies: {e}")
            return None

class DolphinAPI:
    """A simple wrapper for the Dolphin {anty} API."""

    def __init__(self, api_token):
        self.api_token = api_token
        self.cloud_headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
        self.local_headers = {"Content-Type": "application/json"}

    def create_profile(self, name="Test-Profile", proxy_details=None):
        """Creates a new browser profile with a proxy."""
        print(f"Creating a new Dolphin anty browser profile named '{name}'...")
        
        payload = {
            "name": f"{name}-{random.randint(1000, 9999)}",
            "tags": ["Test"],
            "platform": "macos",
            "browserType": "anty",
            "mainWebsite": "",
            "useragent": {
                "mode": "manual",
                "value": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            "proxy": proxy_details,
            # Add other profile settings as needed from the original script
        }

        try:
            response = requests.post(
                f"{DOLPHIN_API_URL}/browser_profiles",
                headers=self.cloud_headers,
                json=payload,
            )
            response.raise_for_status()
            profile_data = response.json()
            
            profile_id = profile_data.get("id") or profile_data.get("browserProfileId")

            if profile_id:
                print(f"Successfully created profile. ID: {profile_id}")
                return profile_id
            else:
                print(f"Failed to create profile: {response.text}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error creating Dolphin profile: {e}")
            if e.response:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response body: {e.response.text}")
            return None

    def get_profiles(self):
        """Fetches all browser profiles."""
        print("Fetching all browser profiles...")
        try:
            response = requests.get(
                f"{DOLPHIN_API_URL}/browser_profiles",
                headers=self.cloud_headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Dolphin profiles: {e}")
            return None

    def get_profile_details(self, profile_id):
        """Fetches details for a specific profile."""
        print(f"Fetching details for profile {profile_id}...")
        try:
            response = requests.get(
                f"{DOLPHIN_API_URL}/browser_profiles/{profile_id}",
                headers=self.cloud_headers,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching profile details: {e}")
            return None

    def start_profile_automation(self, profile_id):
        """Starts the browser profile in automation mode."""
        print(f"Starting profile {profile_id} in automation mode...")
        time.sleep(5)
        try:
            url = f"{DOLPHIN_API_LOCAL}/v1.0/browser_profiles/{profile_id}/start?automation=1"
            response = requests.get(url, headers=self.local_headers)
            response.raise_for_status()
            data = response.json()
            if data.get("success") and "automation" in data:
                port = data["automation"]["port"]
                ws_endpoint = data["automation"]["wsEndpoint"]
                full_ws_endpoint = f"ws://127.0.0.1:{port}{ws_endpoint}"
                print(f"Profile started. CDP WebSocket endpoint: {full_ws_endpoint}")
                return full_ws_endpoint, port
            else:
                print(f"Failed to start profile or get automation endpoint: {data}")
                return None, None
        except requests.exceptions.RequestException as e:
            print(f"Error starting Dolphin profile: {e}")
            return None, None


@app.get("/profiles")
async def list_profiles():
    dolphin = DolphinAPI(DOLPHIN_API_TOKEN)
    profiles = dolphin.get_profiles()
    if profiles:
        return profiles
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch profiles")

@app.get("/proxies/geo")
async def get_geo_data():
    proxy_manager = ProxyManager(PROXY_API_KEY)
    try:
        geo_data = proxy_manager.api.residentGeo()
        # The geo data is returned as a zip file in binary format.
        # I need to unzip it and return the JSON content.
        import zipfile
        import io
        
        with zipfile.ZipFile(io.BytesIO(geo_data), 'r') as zip_ref:
            # I'm assuming there's a single JSON file in the zip.
            json_file_name = zip_ref.namelist()[0]
            with zip_ref.open(json_file_name) as json_file:
                return json.load(json_file)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch GEO data: {e}")

@app.get("/proxies/next-residential")
async def get_next_residential_proxy(username: str):
    proxy_dir = f"proxies/{username}"
    if not os.path.isdir(proxy_dir):
        raise HTTPException(status_code=404, detail=f"No proxy directory found for username: {username}")

    # Find the proxy list file
    proxy_file = None
    for f in os.listdir(proxy_dir):
        if f.endswith(".txt") and f != "last_used_port.txt" and f != "last_used_port.txt":
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

@app.post("/proxies/create-residential")
async def create_residential_proxy(payload: ResidentialProxyRequest):
    proxy_manager = ProxyManager(PROXY_API_KEY)
    
    title = f"{payload.country.upper()}_{payload.type.upper()}_{time.strftime('%d%m%Y')}"
    
    try:
        creation_params = {
            "country": payload.country,
            "region": payload.region,
            "city": payload.city,
            "isp": payload.isp,
            "title": title
        }
        created_proxy = proxy_manager.api.residentCreate(creation_params)
        
        if not created_proxy:
            raise HTTPException(status_code=500, detail="Failed to create residential proxy or invalid response.")
            
        proxy_id = created_proxy.get("id")
        login = created_proxy.get("login")
        
        if not proxy_id or not login:
            raise HTTPException(status_code=500, detail="Invalid response from proxy creation API.")

        exported_proxies = proxy_manager.api.residentExport(proxy_id)
        
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

@app.get("/")
async def root():
    return {"message": "Amazon Automator API is running"}


class GeminiAI:
    """Gemini AI integration for intelligent site analysis"""
    
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def _get_clean_html(self, html_content: str) -> str:
        """Clean HTML using BeautifulSoup to improve AI analysis."""
        soup = BeautifulSoup(html_content, 'lxml')
        # Remove script and style tags
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        return soup.get_text(separator='\n', strip=True)

    async def analyze_signup_page(self, html_content: str) -> dict:
        """Analyze the signup page to find form elements."""
        clean_html = await self._get_clean_html(html_content)
        prompt = f"""
        Analyze the following HTML of an Amazon registration page and identify the CSS selectors for the form fields.
        I need to fill out the following fields: 'customer_name', 'email', 'password', and 'password_check'.
        Return a JSON object with the selectors.

        HTML:
        {clean_html[:4000]}

        JSON Response format:
        {{
            "customer_name_selector": "...",
            "email_selector": "...",
            "password_selector": "...",
            "password_check_selector": "...",
            "submit_button_selector": "..."
        }}
        """
        try:
            response = await self.model.generate_content_async(prompt)
            response_text = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(response_text)
        except Exception as e:
            print(f"Error analyzing signup page with Gemini: {e}")
            return {}

    async def find_navigation_element(self, html_content: str, text_to_find: str) -> dict:
        """Find a navigation element (like 'Sign In' or 'Create Account') on the page."""
        clean_html = await self._get_clean_html(html_content)
        prompt = f"""
        Analyze the following HTML and find the CSS selector for the element that contains the text "{text_to_find}".
        This is likely a link (<a>) or a button (<button>).

        HTML:
        {clean_html[:4000]}

        JSON Response format:
        {{
            "selector": "..."
        }}
        """
        try:
            response = await self.model.generate_content_async(prompt)
            response_text = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(response_text)
        except Exception as e:
            print(f"Error finding navigation element with Gemini: {e}")
            return {}


async def run_ai_driven_signup(playwright: Playwright, ws_endpoint: str, signup_payload: SignupPayload):
    """Connects to the browser and uses AI to automate Amazon signup with fallback logic."""
    print("Connecting to the browser via Playwright...")
    ai = GeminiAI()
    browser = None
    try:
        browser = await playwright.chromium.connect_over_cdp(ws_endpoint)
        context = browser.contexts[0]
        page = context.pages[0]

        # --- Primary Strategy: Go directly to registration ---
        try:
            print("Attempting to navigate directly to registration page...")
            await page.goto("https://www.amazon.com/ap/register", timeout=60000)
            await page.wait_for_selector("#ap_customer_name", timeout=15000)
            print("Successfully loaded registration page directly.")
        except Exception as e:
            print(f"Direct navigation failed: {e}. Initiating fallback strategy...")
            
            # --- Fallback Strategy: Navigate from homepage ---
            await page.goto("https://www.amazon.com", timeout=60000)
            
            # 1. Find and click "Sign In"
            print("AI is looking for the 'Sign In' link...")
            html_content = await page.content()
            nav_selectors = await ai.find_navigation_element(html_content, "Hello, sign in")
            if not nav_selectors.get("selector"):
                raise Exception("AI could not find the 'Sign In' link.")
            
            await page.click(nav_selectors["selector"])
            await page.wait_for_load_state("networkidle")
            
            # 2. Find and click "Create Account"
            print("AI is looking for the 'Create Account' button...")
            html_content = await page.content()
            create_selectors = await ai.find_navigation_element(html_content, "Create your Amazon account")
            if not create_selectors.get("selector"):
                raise Exception("AI could not find the 'Create Account' button.")
                
            await page.click(create_selectors["selector"])
            await page.wait_for_load_state("networkidle")
            print("Successfully navigated to registration page via fallback.")

        # --- Analyze and Fill Form ---
        print("Analyzing registration page with Gemini AI...")
        html_content = await page.content()
        form_selectors = await ai.analyze_signup_page(html_content)
        if not all(form_selectors.values()):
             # Fallback to default selectors if AI fails
            form_selectors = {
                "customer_name_selector": "#ap_customer_name", "email_selector": "#ap_email",
                "password_selector": "#ap_password", "password_check_selector": "#ap_password_check",
                "submit_button_selector": "#continue"
            }
            print("AI analysis failed, using default selectors.")

        print(f"Using selectors: {form_selectors}")
        await page.fill(form_selectors["customer_name_selector"], signup_payload.name)
        await page.fill(form_selectors["email_selector"], signup_payload.email)
        await page.fill(form_selectors["password_selector"], signup_payload.password)
        await page.fill(form_selectors["password_check_selector"], signup_payload.password)
        await page.click(form_selectors["submit_button_selector"])
        print("Form submitted.")

    except Exception as e:
        print(f"An error occurred during AI-driven Playwright automation: {e}")
    finally:
        if browser and browser.is_connected():
            print("Closing browser connection...")
            await browser.close()


@app.post("/automations/signup")
async def automate_signup(payload: SignupPayload):
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
    dolphin = DolphinAPI(DOLPHIN_API_TOKEN)
    # Read the country from the file
    country_file_path = os.path.join(proxy_dir, "country.txt")
    country = "XX" # Default country
    if os.path.exists(country_file_path):
        with open(country_file_path, "r") as f:
            country = f.read().strip()

    profile_name = f"{payload.type.upper()}_{country.upper()}_{time.strftime('%d%m%Y')}"
    profile_id = dolphin.create_profile(name=profile_name, proxy_details=proxy_details)
    if not profile_id:
        raise HTTPException(status_code=500, detail="Failed to create Dolphin profile")

    # --- Update last used port state ---
    with open(state_file, "w") as f:
        f.write(str(port))

    # --- Run automation ---
    ws_endpoint, _ = dolphin.start_profile_automation(profile_id)
    if not ws_endpoint:
        raise HTTPException(status_code=500, detail="Failed to start Dolphin profile")

    async with async_playwright() as p:
        await run_ai_driven_signup(p, ws_endpoint, payload)

    dolphin.stop_profile(profile_id)
    return {"status": "completed", "profile_id": profile_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,)