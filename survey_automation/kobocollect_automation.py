from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import time
import requests
import os
import sys
from pathlib import Path

class DynamicWebDriver:
    """Dynamic WebDriver class that supports Chrome, Edge, Brave, and Firefox"""
    
    def __init__(self, browser_preference=None, headless=False, debug_port=None):
        self.browser_preference = browser_preference
        self.headless = headless
        self.debug_port = debug_port
        self.driver = None
        self.browser_type = None
        
    def _get_chrome_options(self, is_brave=False):
        """Configure Chrome/Brave options"""
        options = ChromeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        # Common Chrome/Brave arguments
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        # If debug port is specified, connect to existing browser
        if self.debug_port:
            options.add_experimental_option("debuggerAddress", f"localhost:{self.debug_port}")
        
        # Brave-specific executable path
        if is_brave:
            brave_paths = [
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Users\{}\AppData\Local\BraveSoftware\Brave-Browser\Application\brave.exe".format(os.getenv('USERNAME')),
                "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",  # macOS
                "/usr/bin/brave-browser",  # Linux
                "/snap/bin/brave"  # Linux snap
            ]
            
            for path in brave_paths:
                if os.path.exists(path):
                    options.binary_location = path
                    break
        
        return options
    
    def _get_edge_options(self):
        """Configure Edge options"""
        options = EdgeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        if self.debug_port:
            options.add_experimental_option("debuggerAddress", f"localhost:{self.debug_port}")
        
        return options
    
    def _get_firefox_options(self):
        """Configure Firefox options"""
        options = FirefoxOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        return options
    
    def _try_chrome(self):
        """Try to initialize Chrome driver"""
        try:
            options = self._get_chrome_options()
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.browser_type = "Chrome"
            return True
        except Exception as e:
            print(f"Chrome initialization failed: {e}")
            return False
    
    def _try_brave(self):
        """Try to initialize Brave driver"""
        try:
            options = self._get_chrome_options(is_brave=True)
            service = ChromeService(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.browser_type = "Brave"
            return True
        except Exception as e:
            print(f"Brave initialization failed: {e}")
            return False
    
    def _try_edge(self):
        """Try to initialize Edge driver"""
        try:
            options = self._get_edge_options()
            service = EdgeService(EdgeChromiumDriverManager().install())
            self.driver = webdriver.Edge(service=service, options=options)
            self.browser_type = "Edge"
            return True
        except Exception as e:
            print(f"Edge initialization failed: {e}")
            return False
    
    def _try_firefox(self):
        """Try to initialize Firefox driver"""
        try:
            options = self._get_firefox_options()
            service = FirefoxService(GeckoDriverManager().install())
            self.driver = webdriver.Firefox(service=service, options=options)
            self.browser_type = "Firefox"
            return True
        except Exception as e:
            print(f"Firefox initialization failed: {e}")
            return False
    
    def initialize_driver(self):
        """Initialize the best available driver"""
        browsers_to_try = []
        
        # If user specified a preference, try that first
        if self.browser_preference:
            browsers_to_try.append(self.browser_preference.lower())
        
        # Add remaining browsers in order of preference
        default_order = ['chrome', 'brave', 'edge', 'firefox']
        for browser in default_order:
            if browser not in browsers_to_try:
                browsers_to_try.append(browser)
        
        for browser in browsers_to_try:
            print(f"Trying to initialize {browser.title()} driver...")
            
            if browser == 'chrome' and self._try_chrome():
                break
            elif browser == 'brave' and self._try_brave():
                break
            elif browser == 'edge' and self._try_edge():
                break
            elif browser == 'firefox' and self._try_firefox():
                break
        
        if not self.driver:
            raise Exception("Failed to initialize any browser driver")
        
        print(f"Successfully initialized {self.browser_type} driver")
        return self.driver
    
    def get_driver(self):
        """Get the initialized driver"""
        if not self.driver:
            self.initialize_driver()
        return self.driver
    
    def quit(self):
        """Quit the driver"""
        if self.driver:
            self.driver.quit()
            self.driver = None

def parse_html_with_beautifulsoup(html_content):
    """Parse HTML content using BeautifulSoup"""
    soup = BeautifulSoup(html_content, "lxml")
    return soup

def extract_text_from_element(soup, tag, **kwargs):
    """Extract text from HTML element using BeautifulSoup"""
    element = soup.find(tag, **kwargs)
    if element:
        return element.get_text(strip=True)
    return None

# Initialize dynamic driver
# You can specify browser preference: 'chrome', 'brave', 'edge', 'firefox'
# You can also specify debug_port if you want to connect to existing browser
dynamic_driver = DynamicWebDriver(
    browser_preference='chrome',  # Change this to your preferred browser
    headless=False,  # Set to True for headless mode
    debug_port=None  # Set to None if you don't want to connect to existing browser 9222
)

# Get the driver
driver = dynamic_driver.get_driver()
# driver.get("https://kobo.humanitarianresponse.info/accounts/login/?next=/kobocat/")
# time.sleep(5)
# username = driver.find_element(By.ID, 'id_login')
# username.send_keys("phatts_de_oro")
# password = driver.find_element(By.ID, 'id_password')
# password.send_keys("phattsJUNE2023$f")
# driver.find_element(By.NAME, 'Login').click()
# time.sleep(5)
# driver.get("https://kobo.humanitarianresponse.info/#/forms/aSuujXtXVGiR8Gg3F3yckM/data/table")
# # Wait for the table to be visible
# time.sleep(20)
# # //*[@id="kpiapp"]/div[2]/div[2]/div[3] thi the table wih header //*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[1]/div[3]/button[1]
# driver.find_element(By.XPATH, '//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[1]/div[3]/button[1]').click()
# time.sleep(5)
# search = driver.find_element(By.XPATH,'//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[5]/input')
# search.send_keys("Vergilia")
# time.sleep(20)
# driver.find_element(By.XPATH, '//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/label/input').click() #checkox
# time.sleep(5)
# //*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/div[1]/div/div[1]/div/div/label/input
# //*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/div[1]/div/div[1]/div/button[2]/i  -get the value for each of the data-sid
def kobo_automation_with_beautifulsoup():
    """Main automation function with BeautifulSoup integration"""
    try:
        # Example: Login to KoboCollect (uncomment and modify as needed)
        # driver.get("https://kobo.humanitarianresponse.info/accounts/login/?next=/kobocat/")
        # time.sleep(5)
        # username = driver.find_element(By.ID, 'id_login')
        # username.send_keys("your_username")
        # password = driver.find_element(By.ID, 'id_password')
        # password.send_keys("your_password")
        # driver.find_element(By.NAME, 'Login').click()
        # time.sleep(5)
        
        # Navigate to forms data table
        # driver.get("https://kobo.humanitarianresponse.info/#/forms/aSuujXtXVGiR8Gg3F3yckM/data/table")
        # time.sleep(20)
        
        # Click on table header button
        # driver.find_element(By.XPATH, '//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[1]/div[3]/button[1]').click()
        # time.sleep(5)
        
        # Search functionality
        # search = driver.find_element(By.XPATH,'//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[5]/input')
        # search.send_keys("Vergilia")
        # time.sleep(20)
        
        # Process survey data with enhanced error handling
        for i in range(1, 370):
            try:
                # Get page source and parse with BeautifulSoup
                page_source = driver.page_source
                soup = parse_html_with_beautifulsoup(page_source)
                
                # Extract span value using Selenium
                span_xpath = f'//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/div[{i}]/div/div[34]/span'
                
                try:
                    value_element = driver.find_element(By.XPATH, span_xpath)
                    value_of_span = value_element.text
                except Exception as e:
                    print(f"Could not find span element for row {i}: {e}")
                    continue
                
                # Alternative: Extract using BeautifulSoup (if you have specific selectors)
                # You can also use BeautifulSoup to parse specific elements
                # span_elements = soup.find_all('span', class_='your-class-name')
                
                print(f"Row {i}: {value_of_span}")
                
                # Process only if value is not "No"
                if value_of_span != "No":
                    try:
                        # Get data-sid attribute
                        data_sid_element = driver.find_element(
                            By.XPATH,
                            f'//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/div[{i}]/div/div[1]/div/button[2]'
                        )
                        data_sid = data_sid_element.get_attribute("data-sid")
                        print(f"Data SID: {data_sid}, Index: {i}")
                        
                        # Click to open in new tab
                        data_sid_element.click()
                        time.sleep(10)
                        
                        # Handle multiple windows
                        window_handles = driver.window_handles
                        if len(window_handles) > 1:
                            driver.switch_to.window(window_handles[1])
                            time.sleep(5)
                            
                            # Parse the new page with BeautifulSoup
                            form_page_source = driver.page_source
                            form_soup = parse_html_with_beautifulsoup(form_page_source)
                            
                            # Example: Extract form data using BeautifulSoup
                            # form_title = extract_text_from_element(form_soup, 'title')
                            # print(f"Form title: {form_title}")
                            
                            # Interact with form elements
                            try:
                                q13_xpath = '/html/body/div[1]/article/form/section[2]/section[2]/section[1]/fieldset[11]/fieldset/div/label[2]/input'
                                q13 = driver.find_element(By.XPATH, q13_xpath)
                                driver.execute_script("arguments[0].scrollIntoView();", q13)
                                q13.click()
                                
                                # Submit form
                                submit_button = driver.find_element(By.XPATH, '//*[@id="submit-form"]')
                                submit_button.click()
                                time.sleep(10)
                                
                            except Exception as form_error:
                                print(f"Error interacting with form: {form_error}")
                            
                            # Close the second tab and switch back
                            driver.close()
                            driver.switch_to.window(window_handles[0])
                            time.sleep(2)
                        
                    except Exception as processing_error:
                        print(f"Error processing row {i}: {processing_error}")
                        continue
                        
            except Exception as row_error:
                print(f"Error in row {i}: {row_error}")
                continue
                
    except Exception as main_error:
        print(f"Main automation error: {main_error}")
    finally:
        # Clean up
        print("Automation completed")

def demonstrate_beautifulsoup():
    """Demonstrate BeautifulSoup usage as requested"""
    html = "<html><body><p>Hello</p></body></html>"
    soup = BeautifulSoup(html, "lxml")
    print("BeautifulSoup demo:")
    print(f"Paragraph text: {soup.p.text}")
    
    # More advanced BeautifulSoup examples
    complex_html = """
    <html>
        <body>
            <div class="container">
                <p id="greeting">Hello World</p>
                <p class="info">This is information</p>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
            </div>
        </body>
    </html>
    """
    
    complex_soup = BeautifulSoup(complex_html, "lxml")
    print(f"Greeting by ID: {complex_soup.find('p', id='greeting').text}")
    print(f"Info by class: {complex_soup.find('p', class_='info').text}")
    
    # Extract all list items
    list_items = complex_soup.find_all('li')
    print("List items:")
    for item in list_items:
        print(f"  - {item.text}")

if __name__ == "__main__":
    try:
        # Demonstrate BeautifulSoup functionality
        demonstrate_beautifulsoup()
        
        # Run the main automation
        print("\nStarting KoboCollect automation...")
        kobo_automation_with_beautifulsoup()
        
    except KeyboardInterrupt:
        print("\nAutomation interrupted by user")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Always clean up the driver
        dynamic_driver.quit()
        print("Driver closed successfully")



 














