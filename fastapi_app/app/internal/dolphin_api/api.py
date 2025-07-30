import requests
import time
import random
from app.core.config import settings

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
                f"{settings.DOLPHIN_API_URL}/browser_profiles",
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
                f"{settings.DOLPHIN_API_URL}/browser_profiles",
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
                f"{settings.DOLPHIN_API_URL}/browser_profiles/{profile_id}",
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
            url = f"{settings.DOLPHIN_API_LOCAL}/v1.0/browser_profiles/{profile_id}/start?automation=1"
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

    def stop_profile(self, profile_id):
        """Stops the browser profile."""
        print(f"Stopping profile {profile_id}...")
        try:
            url = f"{settings.DOLPHIN_API_LOCAL}/v1.0/browser_profiles/{profile_id}/stop"
            response = requests.get(url, headers=self.local_headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error stopping Dolphin profile: {e}")
            return None