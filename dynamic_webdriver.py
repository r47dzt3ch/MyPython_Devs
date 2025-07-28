import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager

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
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
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