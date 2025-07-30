from playwright.async_api import Playwright
from app.internal.gemini_ai.api import GeminiAI
from app.schemas.automation import SignupPayload

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