import asyncio
import random
import json
import requests
from playwright.async_api import async_playwright, Playwright
import google.generativeai as genai
from bs4 import BeautifulSoup
import os
import time
from dotenv import load_dotenv
load_dotenv()
# --- CONFIGURATION ---
# It's recommended to load these from a .env file or environment variables in a real application.
DOLPHIN_API_TOKEN = os.getenv("DOLPHIN_API_TOKEN")
DOLPHIN_API_URL = os.getenv("DOLPHIN_API_URL")
DOLPHIN_API_LOCAL = os.getenv("DOLPHIN_API_LOCAL")

# Residential Proxy Credentials
PROXY_HOST = "res.proxy-seller.com"
PROXY_PORT = "10276"
PROXY_USERNAME = "5f1d6a36763c82af"
PROXY_PASSWORD = "1yhfUOBk"

# Account Details
SIGNUP_NAME = "John Smith"
SIGNUP_EMAIL = "some-random-email-12345@example.com"  # Use a real or temporary email
SIGNUP_PASSWORD = "aVeryStrongPassword!123"

class DolphinAPI:
    """A simple wrapper for the Dolphin {anty} API."""

    def __init__(self, api_token):
        self.api_token = api_token
        self.cloud_headers = {"Authorization": f"Bearer {api_token}", "Content-Type": "application/json"}
        self.local_headers = {"Content-Type": "application/json"}

    def login_with_token(self):
        """Authenticates with the API using a token."""
        print("Authenticating with token...")
        try:
            response = requests.post(
                f"{DOLPHIN_API_LOCAL}/v1.0/auth/login-with-token",
                headers=self.local_headers,
                json={"token": self.api_token},
            )
            response.raise_for_status()
            # Assuming the response is JSON and has a "success" key
            if response.json().get("success"):
                print("Successfully authenticated with token.")
                return True
            else:
                print(f"Token authentication failed: {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error during token authentication: {e}")
            if e.response:
                print(f"Response body: {e.response.text}")
            return False
        except ValueError: # Handles JSON decoding errors
            print("Error decoding authentication response JSON.")
            print(f"Response body: {response.text}")
            return False

    def create_profile(self):
        """Creates a new browser profile using the configuration from test.py."""
        print("Creating a new Dolphin {anty} browser profile with specific fingerprint...")
        
        # Payload from test.py, adapted for the automator
        payload = {
            "name": f"Test-Profile-{random.randint(1000, 9999)}",
            "tags": ["Test"],
            "platform": "macos",
            "browserType": "anty",
            "mainWebsite": "",
            "useragent": {
                "mode": "manual",
                "value": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
            "webrtc": {
                "mode": "altered",
                "ipAddress": None
            },
            "canvas": {
                "mode": "real"
            },
            "webgl": {
                "mode": "real"
            },
            "webglInfo": {
                "mode": "manual",
                "vendor": "Google Inc. (Apple)",
                "renderer": "ANGLE (Apple, Apple M1 Max, OpenGL 4.1)",
                "webgl2Maximum": "{\"UNIFORM_BUFFER_OFFSET_ALIGNMENT\":256,\"MAX_TEXTURE_SIZE\":16384,\"MAX_VIEWPORT_DIMS\":[16384,16384],\"MAX_VERTEX_ATTRIBS\":16,\"MAX_VERTEX_UNIFORM_VECTORS\":1024,\"MAX_VARYING_VECTORS\":31,\"MAX_COMBINED_TEXTURE_IMAGE_UNITS\":32,\"MAX_VERTEX_TEXTURE_IMAGE_UNITS\":16,\"MAX_TEXTURE_IMAGE_UNITS\":16,\"MAX_FRAGMENT_UNIFORM_VECTORS\":1024,\"MAX_CUBE_MAP_TEXTURE_SIZE\":16384,\"MAX_RENDERBUFFER_SIZE\":16384,\"MAX_3D_TEXTURE_SIZE\":2048,\"MAX_ELEMENTS_VERTICES\":1048575,\"MAX_ELEMENTS_INDICES\":150000,\"MAX_TEXTURE_LOD_BIAS\":16,\"MAX_DRAW_BUFFERS\":8,\"MAX_FRAGMENT_UNIFORM_COMPONENTS\":4096,\"MAX_VERTEX_UNIFORM_COMPONENTS\":4096,\"MAX_ARRAY_TEXTURE_LAYERS\":2048,\"MIN_PROGRAM_TEXEL_OFFSET\":-8,\"MAX_PROGRAM_TEXEL_OFFSET\":7,\"MAX_VARYING_COMPONENTS\":124,\"MAX_TRANSFORM_FEEDBACK_SEPARATE_COMPONENTS\":4,\"MAX_TRANSFORM_FEEDBACK_INTERLEAVED_COMPONENTS\":64,\"MAX_TRANSFORM_FEEDBACK_SEPARATE_ATTRIBS\":4,\"MAX_COLOR_ATTACHMENTS\":8,\"MAX_SAMPLES\":4,\"MAX_VERTEX_OUTPUT_COMPONENTS\":64,\"MAX_FRAGMENT_INPUT_COMPONENTS\":128,\"MAX_ELEMENT_INDEX\":4294967295}"
            },
            "webgpu": {
                "mode": "manual"
            },
            "clientRect": {
                "mode": "real"
            },
            "notes": {
                "content": None,
                "color": "blue",
                "style": "text",
                "icon": "info"
            },
            "timezone": {
                "mode": "auto",
                "value": None
            },
            "locale": {
                "mode": "auto",
                "value": None
            },
            "statusId": 0,
            "geolocation": {
                "mode": "auto",
                "latitude": None,
                "longitude": None,
                "accuracy": None
            },
            "cpu": {
                "mode": "manual",
                "value": 8
            },
            "memory": {
                "mode": "manual",
                "value": 8
            },
            "screen": {
                "mode": "real",
                "resolution": None
            },
            "audio": {
                "mode": "real"
            },
            "mediaDevices": {
                "mode": "real",
                "audioInputs": None,
                "videoInputs": None,
                "audioOutputs": None
            },
            "ports": {
                "mode": "protect",
                "blacklist": "3389,5900,5800,7070,6568,5938"
            },
            "doNotTrack": False,
            "args": [],
            "platformVersion": "13.4.1",
            "uaFullVersion": "120.0.5845.96",
            "login": "",
            "password": "",
            "appCodeName": "Mozilla",
            "platformName": "MacIntel",
            "connectionDownlink": 2.05,
            "connectionEffectiveType": "4g",
            "connectionRtt": 150,
            "connectionSaveData": 0,
            "cpuArchitecture": "",
            "osVersion": "10.15.7",
            "vendorSub": "",
            "productSub": "20030107",
            "vendor": "Google Inc.",
            "product": "Gecko",
            "proxy": {
                "type": "socks5",
                "host": PROXY_HOST,
                "port": PROXY_PORT,
                "login": PROXY_USERNAME,
                "password": PROXY_PASSWORD,
                "name": f"socks5://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}",
                "changeIpUrl": "",
            },
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
                return full_ws_endpoint
            else:
                print(f"Failed to start profile or get automation endpoint: {data}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error starting Dolphin profile: {e}")
            return None

    def stop_profile(self, profile_id):
        """Stops the browser profile."""
        print(f"Stopping profile {profile_id}...")
        try:
            url = f"{DOLPHIN_API_LOCAL}/v1.0/browser_profiles/{profile_id}/stop"
            response = requests.get(url, headers=self.local_headers)
            response.raise_for_status()
            print("Profile stopped successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error stopping Dolphin profile: {e}")


class GeminiAI:
    """Gemini AI integration for intelligent site analysis"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
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

async def run_ai_driven_signup(playwright: Playwright, ws_endpoint: str):
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
        await page.fill(form_selectors["customer_name_selector"], SIGNUP_NAME)
        await page.fill(form_selectors["email_selector"], SIGNUP_EMAIL)
        await page.fill(form_selectors["password_selector"], SIGNUP_PASSWORD)
        await page.fill(form_selectors["password_check_selector"], SIGNUP_PASSWORD)
        await page.click(form_selectors["submit_button_selector"])
        print("Form submitted.")

    except Exception as e:
        print(f"An error occurred during AI-driven Playwright automation: {e}")
    finally:
        if browser and browser.is_connected():
            print("Closing browser connection...")
            await browser.close()


async def main():
    """Main function to orchestrate the automation process."""
    dolphin = DolphinAPI(DOLPHIN_API_TOKEN)
    profile_id = None

    try:
        # 1. Authenticate with Local API
        if not dolphin.login_with_token():
            return

        # 2. Create Dolphin Profile using Cloud API
        profile_id = dolphin.create_profile()
        if not profile_id:
            return
        
        # Give local client time to sync
        print("Waiting for local client to sync...")
        time.sleep(10)

        # 3. Start Profile and get WebSocket endpoint
        ws_endpoint = dolphin.start_profile_automation(profile_id)
        if not ws_endpoint:
            return

        # 4. Run Playwright automation
        async with async_playwright() as p:
            await run_ai_driven_signup(p, ws_endpoint)

    except Exception as e:
        print(f"An unexpected error occurred in main: {e}")
    finally:
        # 5. Stop the profile
        if profile_id:
            dolphin.stop_profile(profile_id)


if __name__ == "__main__":
    # Check for placeholder credentials
    if "YOUR_DOLPHIN_API_TOKEN" in DOLPHIN_API_TOKEN:
        print("="*60)
        print("!!! CONFIGURATION NEEDED !!!")
        print("Please replace the placeholder values in the CONFIGURATION section.")
        print("="*60)
    else:
        asyncio.run(main())