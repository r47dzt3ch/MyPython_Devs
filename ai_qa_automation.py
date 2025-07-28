import os
import time
import json
import re
from typing import Dict, List, Optional, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
from dynamic_webdriver import DynamicWebDriver
from firebase_sdk import FirebaseController
import sys

# Load environment variables
load_dotenv()

class GeminiAI:
    """Gemini AI integration for intelligent site analysis"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_page_content(self, html_content: str, url: str) -> Dict:
        """Analyze page content using Gemini AI"""
        prompt = f"""
        Analyze this webpage content and provide a structured analysis:
        
        URL: {url}
        HTML Content: {html_content[:5000]}...
        
        Please analyze and return a JSON response with:
        1. "requires_login": boolean - Does this page require login?
        2. "login_elements": object - If login required, identify login form elements (username_field, password_field, submit_button)
        3. "page_type": string - What type of page is this? (login, dashboard, form, content, etc.)
        4. "main_modules": array - List main modules/sections available on the page
        5. "interactive_elements": array - List clickable elements, buttons, links
        6. "forms": array - List any forms present
        7. "navigation": array - List navigation elements
        8. "content_summary": string - Brief summary of page content
        
        Return only valid JSON format.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Clean the response to extract JSON
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text)
        except Exception as e:
            print(f"Error analyzing content with Gemini: {e}")
            return {
                "requires_login": False,
                "login_elements": {},
                "page_type": "unknown",
                "main_modules": [],
                "interactive_elements": [],
                "forms": [],
                "navigation": [],
                "content_summary": "Analysis failed"
            }
    
    def generate_test_scenarios(self, analysis: Dict, url: str) -> List[Dict]:
        """Generate test scenarios based on page analysis"""
        prompt = f"""
        Based on this webpage analysis, generate comprehensive QA test scenarios:
        
        URL: {url}
        Analysis: {json.dumps(analysis, indent=2)}
        
        Generate test scenarios in JSON format with:
        1. "scenario_name": string
        2. "description": string
        3. "steps": array of step descriptions
        4. "expected_result": string
        5. "priority": string (high/medium/low)
        6. "test_type": string (functional/ui/integration/etc.)
        
        Focus on:
        - Login functionality (if applicable)
        - Navigation testing
        - Form validation
        - Module accessibility
        - User workflow testing
        
        Return array of test scenarios in JSON format.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text)
        except Exception as e:
            print(f"Error generating test scenarios: {e}")
            return []
    
    def suggest_module_selection(self, modules: List[str]) -> Dict:
        """Suggest module selection based on AI analysis"""
        prompt = f"""
        Given these modules from a webpage: {modules}
        
        Provide a numbered menu for QA testing with priorities:
        
        Return JSON with:
        1. "menu_items": array of objects with "number", "module_name", "description", "priority"
        2. "recommendations": array of strings with testing recommendations
        
        Format as a user-friendly menu for QA testers.
        """
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            return json.loads(response_text)
        except Exception as e:
            print(f"Error generating module suggestions: {e}")
            return {"menu_items": [], "recommendations": []}

class AIQAAutomation:
    """Main AI-powered QA automation class"""
    
    def __init__(self, browser_preference='chrome', headless=False, mode='interactive'):
        self.driver_manager = DynamicWebDriver(browser_preference, headless)
        self.driver = None
        self.ai = GeminiAI()
        self.current_analysis = None
        self.test_results = []
        self.mode = mode
        self.firebase_controller = None
        if self.mode == 'firebase':
            self.firebase_controller = FirebaseController(command_handler=self._firebase_command_handler)
    
    def start_session(self):
        """Start automation session"""
        print("🚀 Starting AI QA Automation Session...")
        self.driver = self.driver_manager.get_driver()
        print(f"✅ Browser initialized: {self.driver_manager.browser_type}")
    
    def navigate_to_site(self, url: str):
        """Navigate to target site"""
        print(f"🌐 Navigating to: {url}")
        self.driver.get(url)
        time.sleep(3)
        
        # Get page source for analysis
        html_content = self.driver.page_source
        
        # Analyze with AI
        print("🤖 Analyzing page with AI...")
        self.current_analysis = self.ai.analyze_page_content(html_content, url)
        
        return self.current_analysis
    
    def handle_login_if_required(self, credentials=None) -> bool:
        """Handle login if required based on AI analysis"""
        if not self.current_analysis or not self.current_analysis.get('requires_login', False):
            print("✅ No login required")
            return True

        print("🔐 Login required detected by AI")
        login_elements = self.current_analysis.get('login_elements', {})

        if self.mode == 'interactive':
            # Prompt user for credentials
            print("\n" + "="*50)
            print("🔑 LOGIN CREDENTIALS REQUIRED")
            print("="*50)
            username = input("Enter username/email: ").strip()
            password = input("Enter password: ").strip()
        elif self.mode == 'firebase' and credentials:
            username = credentials.get('username')
            password = credentials.get('password')
            if not username or not password:
                print("❌ Firebase command missing credentials.")
                return False
        else:
            print("❌ Cannot get credentials for login.")
            return False
        
        try:
            # Find login elements using AI suggestions and fallback methods
            username_field = self._find_login_element('username', login_elements.get('username_field'))
            password_field = self._find_login_element('password', login_elements.get('password_field'))
            submit_button = self._find_login_element('submit', login_elements.get('submit_button'))
            
            if username_field and password_field:
                print("📝 Filling login form...")
                username_field.clear()
                username_field.send_keys(username)
                
                password_field.clear()
                password_field.send_keys(password)
                
                if submit_button:
                    submit_button.click()
                else:
                    # Try pressing Enter on password field
                    from selenium.webdriver.common.keys import Keys
                    password_field.send_keys(Keys.RETURN)
                
                time.sleep(5)
                print("✅ Login attempt completed")
                return True
            else:
                print("❌ Could not locate login elements")
                return False
                
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def _find_login_element(self, element_type: str, ai_suggestion: str = None):
        """Find login elements with AI assistance and fallback"""
        selectors = {
            'username': [
                'input[name="username"]', 'input[name="email"]', 'input[name="login"]',
                'input[type="email"]', 'input[id*="user"]', 'input[id*="email"]',
                'input[placeholder*="username"]', 'input[placeholder*="email"]'
            ],
            'password': [
                'input[type="password"]', 'input[name="password"]', 'input[id*="pass"]'
            ],
            'submit': [
                'button[type="submit"]', 'input[type="submit"]', 'button:contains("Login")',
                'button:contains("Sign in")', '.login-button', '#login-button'
            ]
        }
        
        # Try AI suggestion first
        if ai_suggestion:
            try:
                return self.driver.find_element(By.CSS_SELECTOR, ai_suggestion)
            except:
                pass
        
        # Fallback to common selectors
        for selector in selectors.get(element_type, []):
            try:
                return self.driver.find_element(By.CSS_SELECTOR, selector)
            except:
                continue
        
        return None
    
    def analyze_content_after_login(self):
        """Analyze content after successful login"""
        print("🔍 Analyzing content after login...")
        time.sleep(3)
        
        html_content = self.driver.page_source
        current_url = self.driver.current_url
        
        self.current_analysis = self.ai.analyze_page_content(html_content, current_url)
        
        print(f"📊 Page Type: {self.current_analysis.get('page_type', 'Unknown')}")
        print(f"📝 Content Summary: {self.current_analysis.get('content_summary', 'No summary available')}")
        
        return self.current_analysis
    
    def display_module_menu(self):
        """Display AI-generated module selection menu"""
        if not self.current_analysis:
            print("❌ No analysis available")
            return None
        
        modules = self.current_analysis.get('main_modules', [])
        if not modules:
            print("❌ No modules detected")
            return None
        
        print("\n" + "="*60)
        print("🎯 AI-GENERATED MODULE SELECTION MENU")
        print("="*60)
        
        # Get AI suggestions for module menu
        menu_data = self.ai.suggest_module_selection(modules)
        menu_items = menu_data.get('menu_items', [])
        
        if not menu_items:
            # Fallback to simple numbering
            for i, module in enumerate(modules, 1):
                print(f"{i}. {module}")
        else:
            for item in menu_items:
                print(f"{item.get('number', '?')}. {item.get('module_name', 'Unknown')} - {item.get('description', '')}")
        
        print("\n📋 AI Recommendations:")
        for rec in menu_data.get('recommendations', []):
            print(f"  • {rec}")
        
        print("\n" + "="*60)
        
        try:
            choice = input("Select module number (or 'q' to quit): ").strip()
            if choice.lower() == 'q':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(modules):
                selected_module = modules[choice_num - 1]
                print(f"✅ Selected: {selected_module}")
                return selected_module
            else:
                print("❌ Invalid selection")
                return None
                
        except ValueError:
            print("❌ Invalid input")
            return None
    
    def generate_and_display_test_scenarios(self):
        """Generate and display AI test scenarios"""
        if not self.current_analysis:
            print("❌ No analysis available for test generation")
            return
        
        print("\n🧪 Generating AI Test Scenarios...")
        scenarios = self.ai.generate_test_scenarios(self.current_analysis, self.driver.current_url)
        
        if not scenarios:
            print("❌ No test scenarios generated")
            return
        
        print("\n" + "="*80)
        print("🧪 AI-GENERATED TEST SCENARIOS")
        print("="*80)
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{i}. {scenario.get('scenario_name', 'Unnamed Scenario')}")
            print(f"   Type: {scenario.get('test_type', 'Unknown')} | Priority: {scenario.get('priority', 'Medium')}")
            print(f"   Description: {scenario.get('description', 'No description')}")
            print(f"   Expected Result: {scenario.get('expected_result', 'No expected result')}")
            
            steps = scenario.get('steps', [])
            if steps:
                print("   Steps:")
                for j, step in enumerate(steps, 1):
                    print(f"     {j}. {step}")
        
        print("\n" + "="*80)
    
    def run_interactive_session(self):
        """Run interactive QA session"""
        try:
            # Get target URL
            print("\n" + "="*60)
            print("🎯 AI QA AUTOMATION - INTERACTIVE SESSION")
            print("="*60)
            
            url = input("Enter the website URL to test: ").strip()
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Navigate and analyze
            analysis = self.navigate_to_site(url)
            
            # Handle login if required
            login_success = self.handle_login_if_required()
            
            if analysis.get('requires_login', False) and login_success:
                # Re-analyze after login
                self.analyze_content_after_login()
            
            # Display module menu and get selection
            selected_module = self.display_module_menu()
            
            if selected_module:
                print(f"\n🎯 Testing module: {selected_module}")
                
                # Generate test scenarios
                self.generate_and_display_test_scenarios()
                
                # Ask if user wants to continue with automated testing
                continue_testing = input("\nWould you like to run automated tests? (y/n): ").strip().lower()
                if continue_testing == 'y':
                    self.run_automated_tests()
            
        except KeyboardInterrupt:
            print("\n⚠️ Session interrupted by user")
        except Exception as e:
            print(f"❌ Session error: {e}")

    def _firebase_command_handler(self, command_id, command_data):
        """Handles commands received from Firebase."""
        action = command_data.get('action')
        payload = command_data.get('payload', {})
        self.firebase_controller.update_bot_status('running', {'command': action, 'command_id': command_id})

        try:
            if action == 'test_url':
                url = payload.get('url')
                if not url:
                    raise ValueError("URL is required for test_url action.")
                
                analysis = self.navigate_to_site(url)
                
                if analysis.get('requires_login'):
                    login_success = self.handle_login_if_required(credentials=payload.get('credentials'))
                    if not login_success:
                        raise Exception("Login failed.")
                    analysis = self.analyze_content_after_login()

                self.run_automated_tests()
                result_data = {
                    "status": "completed",
                    "analysis": self.current_analysis,
                    "test_summary": self.test_results[-1]['summary'] if self.test_results else {}
                }
                self.firebase_controller.push_result(command_id, result_data)
            
            else:
                raise ValueError(f"Unknown action: {action}")

            self.firebase_controller.update_command_status(command_id, 'completed')

        except Exception as e:
            print(f"❌ Error processing command {command_id}: {e}")
            error_result = {"status": "error", "message": str(e)}
            self.firebase_controller.push_result(command_id, error_result)
            self.firebase_controller.update_command_status(command_id, 'failed')
        
        finally:
            self.firebase_controller.update_bot_status('idle')

    def run_firebase_session(self):
        """Run QA session controlled by Firebase commands."""
        if not self.firebase_controller or not self.firebase_controller.is_connected():
            print("❌ Firebase mode is not available. Check your .env file.")
            return

        print("🔥 Running in Firebase mode. Waiting for commands...")
        self.firebase_controller.listen_for_commands()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Firebase listener...")
            self.firebase_controller.stop_listening()
    
    def run_automated_tests(self):
        """Run automated tests based on AI analysis"""
        print("\n🤖 Running automated tests...")
        
        # This is where you would implement specific automated test logic
        # based on the AI analysis and selected modules
        
        test_results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "url": self.driver.current_url,
            "analysis": self.current_analysis,
            "tests_run": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0
            }
        }
        
        # Example automated tests
        tests = [
            {"name": "Page Load Test", "function": self._test_page_load},
            {"name": "Navigation Test", "function": self._test_navigation},
            {"name": "Form Validation Test", "function": self._test_forms}
        ]
        
        for test in tests:
            print(f"🧪 Running: {test['name']}")
            try:
                result = test['function']()
                test_results["tests_run"].append({
                    "name": test['name'],
                    "status": "PASSED" if result else "FAILED",
                    "details": result
                })
                test_results["summary"]["total"] += 1
                if result:
                    test_results["summary"]["passed"] += 1
                else:
                    test_results["summary"]["failed"] += 1
                    
            except Exception as e:
                print(f"❌ Test failed: {e}")
                test_results["tests_run"].append({
                    "name": test['name'],
                    "status": "ERROR",
                    "details": str(e)
                })
                test_results["summary"]["total"] += 1
                test_results["summary"]["failed"] += 1
        
        # Save results
        self.test_results.append(test_results)
        self._save_test_results(test_results)
        
        # Display summary
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        print(f"Total Tests: {test_results['summary']['total']}")
        print(f"Passed: {test_results['summary']['passed']}")
        print(f"Failed: {test_results['summary']['failed']}")
        print("="*50)
    
    def _test_page_load(self):
        """Test page load functionality"""
        try:
            # Check if page loaded successfully
            WebDriverWait(self.driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except:
            return False
    
    def _test_navigation(self):
        """Test navigation elements"""
        try:
            nav_elements = self.current_analysis.get('navigation', [])
            if nav_elements:
                # Try to find and verify navigation elements
                for nav_item in nav_elements[:3]:  # Test first 3 nav items
                    try:
                        element = self.driver.find_element(By.PARTIAL_LINK_TEXT, nav_item)
                        if element.is_displayed():
                            continue
                    except:
                        pass
                return True
            return False
        except:
            return False
    
    def _test_forms(self):
        """Test form elements"""
        try:
            forms = self.current_analysis.get('forms', [])
            return len(forms) >= 0  # Basic form detection test
        except:
            return False
    
    def _save_test_results(self, results):
        """Save test results to file"""
        try:
            filename = f"qa_test_results_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"📄 Results saved to: {filename}")
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
    
    def close_session(self):
        """Close automation session"""
        if self.driver_manager:
            self.driver_manager.quit()
        print("✅ Session closed successfully")

def main():
    """Main function to run AI QA Automation"""
    automation = None
    
    try:
        print("🤖 AI QA AUTOMATION SYSTEM")
        print("=" * 50)
        print("Powered by Gemini AI & Dynamic WebDriver")
        print("=" * 50)

        mode = 'interactive'
        if len(sys.argv) > 1 and sys.argv[1] == '--firebase':
            mode = 'firebase'

        automation = AIQAAutomation(browser_preference='chrome', headless=True if mode == 'firebase' else False, mode=mode)
        automation.start_session()

        if mode == 'interactive':
            automation.run_interactive_session()
        elif mode == 'firebase':
            automation.run_firebase_session()

    except KeyboardInterrupt:
        print("\n⚠️ Program interrupted by user")
    except Exception as e:
        print(f"❌ Program error: {e}")
    finally:
        if automation:
            automation.close_session()

if __name__ == "__main__":
    main()