"""
AI QA Automation - Firebase Mode Usage Example
==============================================

This file demonstrates how to run the AI QA Automation system in Firebase mode,
allowing it to be controlled by a remote dashboard or application.
"""

import time
from dotenv import load_dotenv

# Important: Load environment variables before importing the main script
load_dotenv()

from ai_qa_automation import AIQAAutomation

def run_firebase_bot():
    """
    Initializes and runs the QA bot in Firebase listening mode.
    """
    print("🔥 INITIALIZING FIREBASE QA BOT")
    print("="*50)
    print("The bot will connect to Firebase and wait for commands.")
    print("Make sure your .env file is correctly configured.")
    print("Press Ctrl+C to stop the bot.")
    print("="*50)

    automation = None
    try:
        # Initialize in 'firebase' mode. Headless is recommended for server use.
        automation = AIQAAutomation(
            browser_preference='chrome',
            headless=True,
            mode='firebase'
        )
        
        # Start the browser session and the Firebase listener
        automation.start_session()
        automation.run_firebase_session()

    except KeyboardInterrupt:
        print("\n⚠️ Bot shutdown initiated by user.")
    except Exception as e:
        print(f"❌ A critical error occurred: {e}")
    finally:
        if automation:
            print("Cleaning up resources...")
            automation.close_session()
            print("✅ Bot has been shut down.")

if __name__ == "__main__":
    run_firebase_bot()

"""
-------------------------------------------------------------------------------
HOW TO SEND COMMANDS VIA FIREBASE
-------------------------------------------------------------------------------

To control the bot, you need to add data to the 'commands' path in your
Firebase Realtime Database.

Example Command Structure:

/commands/{unique_command_id}:
  {
    "action": "test_url",
    "payload": {
      "url": "https://your-test-site.com",
      "credentials": {
        "username": "your_username",
        "password": "your_password"
      }
    },
    "status": "pending"
  }

The bot will automatically pick up commands with `status: "pending"`.

-------------------------------------------------------------------------------
"""