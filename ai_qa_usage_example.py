"""
AI QA Automation - Usage Examples
=================================

This file demonstrates various ways to use the AI QA Automation system.
"""

from ai_qa_automation import AIQAAutomation, GeminiAI
from dynamic_webdriver import DynamicWebDriver
import time

def example_basic_usage():
    """Basic usage example - Interactive session"""
    print("🔥 EXAMPLE 1: Basic Interactive Usage")
    print("="*50)
    
    # Initialize the automation system
    automation = AIQAAutomation(browser_preference='chrome', headless=False)
    
    try:
        # Start session
        automation.start_session()
        
        # Run interactive session (user will be prompted for URL and credentials)
        automation.run_interactive_session()
        
    finally:
        automation.close_session()

def example_programmatic_usage():
    """Programmatic usage example - No user interaction"""
    print("🔥 EXAMPLE 2: Programmatic Usage")
    print("="*50)
    
    automation = AIQAAutomation(browser_preference='chrome', headless=False)
    
    try:
        automation.start_session()
        
        # Navigate to a specific site
        url = "https://example.com"  # Replace with your target URL
        analysis = automation.navigate_to_site(url)
        
        print(f"📊 Analysis Results:")
        print(f"  - Requires Login: {analysis.get('requires_login', False)}")
        print(f"  - Page Type: {analysis.get('page_type', 'Unknown')}")
        print(f"  - Modules Found: {len(analysis.get('main_modules', []))}")
        
        # If login is required, you would handle it here
        if analysis.get('requires_login', False):
            print("🔐 Login required - implement credential handling")
            # automation.handle_login_if_required()  # This prompts for credentials
        
        # Generate test scenarios
        automation.generate_and_display_test_scenarios()
        
        # Run automated tests
        automation.run_automated_tests()
        
    finally:
        automation.close_session()

def example_custom_ai_analysis():
    """Example of using AI analysis independently"""
    print("🔥 EXAMPLE 3: Custom AI Analysis")
    print("="*50)
    
    # Initialize just the AI component
    ai = GeminiAI()
    
    # Example HTML content (you would get this from selenium)
    sample_html = """
    <html>
        <head><title>Sample App</title></head>
        <body>
            <nav>
                <a href="/dashboard">Dashboard</a>
                <a href="/users">Users</a>
                <a href="/reports">Reports</a>
            </nav>
            <form id="loginForm">
                <input type="email" name="email" placeholder="Email">
                <input type="password" name="password" placeholder="Password">
                <button type="submit">Login</button>
            </form>
            <div class="content">
                <h1>Welcome to Sample App</h1>
                <p>Please login to continue</p>
            </div>
        </body>
    </html>
    """
    
    # Analyze the content
    analysis = ai.analyze_page_content(sample_html, "https://example.com")
    
    print("🤖 AI Analysis Results:")
    print(f"  - Requires Login: {analysis.get('requires_login', False)}")
    print(f"  - Page Type: {analysis.get('page_type', 'Unknown')}")
    print(f"  - Main Modules: {analysis.get('main_modules', [])}")
    print(f"  - Content Summary: {analysis.get('content_summary', 'No summary')}")
    
    # Generate test scenarios
    scenarios = ai.generate_test_scenarios(analysis, "https://example.com")
    
    print(f"\n🧪 Generated {len(scenarios)} test scenarios:")
    for i, scenario in enumerate(scenarios[:3], 1):  # Show first 3
        print(f"  {i}. {scenario.get('scenario_name', 'Unnamed')}")
        print(f"     Priority: {scenario.get('priority', 'Medium')}")

def example_dynamic_webdriver():
    """Example of using the dynamic webdriver independently"""
    print("🔥 EXAMPLE 4: Dynamic WebDriver Usage")
    print("="*50)
    
    # Initialize with different browser preferences
    browsers_to_try = ['chrome', 'edge', 'firefox']
    
    for browser in browsers_to_try:
        print(f"\n🌐 Trying {browser.title()} browser...")
        
        driver_manager = DynamicWebDriver(
            browser_preference=browser,
            headless=False  # Set to True for headless mode
        )
        
        try:
            driver = driver_manager.get_driver()
            print(f"✅ Successfully initialized {driver_manager.browser_type}")
            
            # Example usage
            driver.get("https://httpbin.org/html")
            time.sleep(2)
            
            title = driver.title
            print(f"📄 Page title: {title}")
            
            # Clean up
            driver_manager.quit()
            break
            
        except Exception as e:
            print(f"❌ Failed to initialize {browser}: {e}")
            continue

def example_batch_testing():
    """Example of batch testing multiple URLs"""
    print("🔥 EXAMPLE 5: Batch Testing Multiple Sites")
    print("="*50)
    
    # List of URLs to test
    test_urls = [
        "https://httpbin.org/html",
        "https://example.com",
        # Add more URLs as needed
    ]
    
    automation = AIQAAutomation(browser_preference='chrome', headless=True)  # Headless for batch
    
    try:
        automation.start_session()
        
        results = []
        
        for url in test_urls:
            print(f"\n🌐 Testing: {url}")
            
            try:
                # Navigate and analyze
                analysis = automation.navigate_to_site(url)
                
                # Store results
                results.append({
                    'url': url,
                    'analysis': analysis,
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                })
                
                print(f"✅ Analysis completed for {url}")
                
            except Exception as e:
                print(f"❌ Failed to analyze {url}: {e}")
                results.append({
                    'url': url,
                    'error': str(e),
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        # Summary
        print(f"\n📊 Batch Testing Summary:")
        print(f"  - Total URLs: {len(test_urls)}")
        print(f"  - Successful: {len([r for r in results if 'analysis' in r])}")
        print(f"  - Failed: {len([r for r in results if 'error' in r])}")
        
    finally:
        automation.close_session()

def example_custom_test_scenarios():
    """Example of implementing custom test scenarios"""
    print("🔥 EXAMPLE 6: Custom Test Scenarios")
    print("="*50)
    
    automation = AIQAAutomation()
    
    try:
        automation.start_session()
        
        # Navigate to site
        url = "https://httpbin.org/forms/post"
        analysis = automation.navigate_to_site(url)
        
        # Custom test: Form validation
        def test_form_submission():
            """Custom test for form submission"""
            try:
                # Find form elements
                driver = automation.driver
                
                # Fill form
                name_field = driver.find_element("name", "custname")
                name_field.send_keys("Test User")
                
                email_field = driver.find_element("name", "custemail")
                email_field.send_keys("test@example.com")
                
                # Submit
                submit_btn = driver.find_element("css selector", "input[type='submit']")
                submit_btn.click()
                
                time.sleep(2)
                return True
                
            except Exception as e:
                print(f"Form test failed: {e}")
                return False
        
        # Run custom test
        print("🧪 Running custom form test...")
        result = test_form_submission()
        print(f"✅ Form test: {'PASSED' if result else 'FAILED'}")
        
    finally:
        automation.close_session()

if __name__ == "__main__":
    print("🤖 AI QA AUTOMATION - USAGE EXAMPLES")
    print("="*60)
    
    examples = [
        ("Basic Interactive Usage", example_basic_usage),
        ("Programmatic Usage", example_programmatic_usage),
        ("Custom AI Analysis", example_custom_ai_analysis),
        ("Dynamic WebDriver", example_dynamic_webdriver),
        ("Batch Testing", example_batch_testing),
        ("Custom Test Scenarios", example_custom_test_scenarios)
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = input("\nSelect example to run (1-6, or 'all' for all): ").strip()
        
        if choice.lower() == 'all':
            for name, func in examples:
                print(f"\n{'='*60}")
                print(f"Running: {name}")
                print('='*60)
                try:
                    func()
                except Exception as e:
                    print(f"❌ Example failed: {e}")
                print("\n" + "="*60)
                input("Press Enter to continue to next example...")
        else:
            choice_num = int(choice)
            if 1 <= choice_num <= len(examples):
                name, func = examples[choice_num - 1]
                print(f"\n{'='*60}")
                print(f"Running: {name}")
                print('='*60)
                func()
            else:
                print("❌ Invalid choice")
                
    except (ValueError, KeyboardInterrupt):
        print("\n⚠️ Example selection cancelled")
    except Exception as e:
        print(f"❌ Error running example: {e}")