import asyncio
import random
import requests
from playwright.async_api import async_playwright, Playwright

# --- CONFIGURATION ---
# It's recommended to load these from a .env file or environment variables in a real application.
DOLPHIN_API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiOWExNGM4MzMxM2UyZmVlMTc0NTU2ZGNkN2VlN2E3NTA2ZjU4ZDg3MTQxZTUxNmExZDZkYTdhYTQ5YWY4N2I3MjE0ZTEzMTI5ZWFlYjE3MGIiLCJpYXQiOjE3NTM2ODkzNzMuNTUyOTUzLCJuYmYiOjE3NTM2ODkzNzMuNTUyOTU3LCJleHAiOjE3NTYyODEzNzMuNTQyMjEsInN1YiI6IjQ1NTE4OTUiLCJzY29wZXMiOltdLCJ0ZWFtX2lkIjo0MDM2ODQwLCJ0ZWFtX3BsYW4iOiJlbnRlcnByaXNlIiwidGVhbV9wbGFuX2V4cGlyYXRpb24iOjE3NTYwMDkwNjB9.ZsWd7AK3fNMwBuo8UP6UV1qKBHSg8PwRVtdkNAx4ZSBU3Nlr-zFDXEwmIIjirHtTNnpwGMz2R6a3y9wYHOb0unT0sguApg9nNXXCotlZQ7Mzpv_Z97ly-Tse8HHLhv9FdB-OLaEgX0xxi59NOMh0QPSbdTwTbb4KX_oZ7N1wsVJ7rRd6dTlBGADZ9jT5lh0YxAuQ-PwMnut8tayprcM_hv_hAv3ovNCssr03CagQm21yFJZdrbmSH3XZwXhDsPR3t8Cxiytxh9IFJE1i9WWfi2ljftnOWbm01qNJFA6fImGYG348LGkkfoyS6xw3jG1z4ok0tLNSrDZykYS5x5IRiIUSWQdZKDDFKHhr6PAI8yyNbSur6S62YQ5J1BVnQajrdKxHwnLU3rwxmHyorqhwqHoK44ODlHzT9hJvO1z5_ZPyTPMouGfcNJBKsAsK9oK57wQFRsnFiFAocSj-KmDKoY3o_Pglo49B1W-UXp-WkXKHcRQNdrykxaXIGBQMiQ_hwXN7jzU-HfVOqLRcyvs1EENzVP_pdwwog3rOv6J9e3kop-O3AXMVrdRcRl_VB1tQjut-Qh0RQIEWCYz55e3EicqjQwp41PDi6Z7KLqpVY4v1drnl4ieKMwdiRGPFk2Z9Tb9123JGYCElwO6QVJzIHHXDiud6tlzzfH_e4OF5rj4"  # Replace with your Dolphin {anty} API token
DOLPHIN_API_URL = "http://localhost:3001/v1.0"

# Residential Proxy Credentials
PROXY_HOST = "res.proxy-seller.com"
PROXY_PORT = "10274"
PROXY_USERNAME = "5f1d6a36763c82af"
PROXY_PASSWORD = "1yhfUOBk"

# Account Details
SIGNUP_NAME = "John Smith"
SIGNUP_EMAIL = "some-random-email-12345@example.com"  # Use a real or temporary email
SIGNUP_PASSWORD = "aVeryStrongPassword!123"

class DolphinAPI:
    """A simple wrapper for the Dolphin {anty} Local API."""

    def __init__(self, base_url, api_token):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_token}"}

    def create_profile(self):
        """Creates a new browser profile with specified settings."""
        print("Creating a new Dolphin {anty} browser profile...")
        platforms = ["windows", "macos"]
        
        profile_config = {
            "name": f"Amazon-Signup-{random.randint(1000, 9999)}",
            "platform": random.choice(platforms),
            "browserType": "anty",
            "mainWebsite": "amazon",
            "useragent": {"mode": "random"},
            "webrtc": {"mode": "altered"},
            "fingerprint": {
                "canvas": {"mode": "noise"},
                "webgl": {"mode": "noise"},
                "audio": {"mode": "noise"},
                "fonts": {"mode": "real"},
            },
            "proxy": {
                "type": "socks5",
                "host": PROXY_HOST,
                "port": PROXY_PORT,
                "username": PROXY_USERNAME,
                "password": PROXY_PASSWORD,
            },
        }

        try:
            response = requests.post(
                f"{self.base_url}/browser_profiles",
                headers=self.headers,
                json=profile_config,
            )
            response.raise_for_status()
            profile_data = response.json()
            if profile_data.get("success", False):
                profile_id = profile_data.get("browserProfileId")
                print(f"Successfully created profile. ID: {profile_id}")
                return profile_id
            else:
                print(f"Failed to create profile: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error creating Dolphin profile: {e}")
            return None

    def start_profile_automation(self, profile_id):
        """Starts the browser profile in automation mode."""
        print(f"Starting profile {profile_id} in automation mode...")
        try:
            url = f"{self.base_url}/browser_profiles/{profile_id}/start?automation=1"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            if data.get("success") and "automation" in data:
                ws_endpoint = data["automation"]["wsEndpoint"]
                print(f"Profile started. CDP WebSocket endpoint: {ws_endpoint}")
                return ws_endpoint
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
            url = f"{self.base_url}/browser_profiles/{profile_id}/stop"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            print("Profile stopped successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Error stopping Dolphin profile: {e}")


async def run_amazon_signup(playwright: Playwright, ws_endpoint: str):
    """Connects to the browser and automates Amazon signup."""
    print("Connecting to the browser via Playwright...")
    try:
        browser = await playwright.chromium.connect_over_cdp(ws_endpoint)
        context = browser.contexts[0]  # Use the default context
        page = context.pages[0]       # Use the default page

        print("Navigating to Amazon registration page...")
        await page.goto("https://www.amazon.com/ap/register", timeout=90000)

        # Wait for the main registration form to be visible
        await page.wait_for_selector("#ap_customer_name", timeout=30000)
        print("Registration page loaded. Filling out the form...")

        # Fill in the form
        await page.fill("#ap_customer_name", SIGNUP_NAME)
        await page.fill("#ap_email", SIGNUP_EMAIL)
        await page.fill("#ap_password", SIGNUP_PASSWORD)
        await page.fill("#ap_password_check", SIGNUP_PASSWORD)

        # Click continue
        await page.click("#continue")
        print("Form submitted. Waiting for next page...")

        # --- ERROR AND CAPTCHA HANDLING ---
        # Check for potential outcomes after submission
        try:
            # Look for a CAPTCHA puzzle. This selector is a common pattern.
            captcha_selector = 'iframe[src*="captcha"]'
            email_error_selector = "#auth-email-invalid-claim-alert"
            existing_account_selector = 'h4:has-text("Email address already in use")'
            
            # Wait for one of the possible outcomes
            await page.wait_for_selector(
                f"{captcha_selector}, {email_error_selector}, {existing_account_selector}, #auth-pv-enter-code",
                timeout=15000
            )

            if await page.is_visible(captcha_selector):
                print("WARNING: CAPTCHA detected. Manual intervention may be required.")
                # Here you would add 2Captcha integration if desired
            elif await page.is_visible(email_error_selector):
                print("ERROR: Amazon reported an invalid email address.")
            elif await page.is_visible(existing_account_selector):
                print(f"ERROR: An account with the email '{SIGNUP_EMAIL}' already exists.")
            elif await page.is_visible("#auth-pv-enter-code"):
                print("SUCCESS: Signup form submitted. Now on OTP verification page.")
                # Here you would add IMAP logic to fetch the OTP
            else:
                print("Unknown page state after form submission.")

        except Exception as e:
            print(f"Could not determine page state after submission or timed out. {e}")
            print("Assuming signup was successful if no errors were visible.")

    except Exception as e:
        print(f"An error occurred during Playwright automation: {e}")
    finally:
        if 'browser' in locals() and browser.is_connected():
            print("Closing browser connection...")
            await browser.close()


async def main():
    """Main function to orchestrate the automation process."""
    dolphin = DolphinAPI(DOLPHIN_API_URL, DOLPHIN_API_TOKEN)
    profile_id = None

    try:
        # 1. Create Dolphin Profile
        profile_id = dolphin.create_profile()
        if not profile_id:
            return

        # 2. Start Profile and get WebSocket endpoint
        ws_endpoint = dolphin.start_profile_automation(profile_id)
        if not ws_endpoint:
            return

        # 3. Run Playwright automation
        async with async_playwright() as p:
            await run_amazon_signup(p, ws_endpoint)

    except Exception as e:
        print(f"An unexpected error occurred in main: {e}")
    finally:
        # 4. Stop the profile
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