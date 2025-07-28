"""
Usage examples for the dynamic KoboCollect automation with BeautifulSoup
"""

from kobocollect_automation import DynamicWebDriver, parse_html_with_beautifulsoup, extract_text_from_element
from selenium.webdriver.common.by import By
import time

def example_chrome_usage():
    """Example using Chrome browser"""
    print("=== Chrome Browser Example ===")
    
    # Initialize with Chrome preference
    driver_manager = DynamicWebDriver(
        browser_preference='chrome',
        headless=False,
        debug_port=None  # Don't connect to existing browser
    )
    
    try:
        driver = driver_manager.get_driver()
        
        # Navigate to a test page
        driver.get("https://httpbin.org/html")
        time.sleep(2)
        
        # Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = parse_html_with_beautifulsoup(page_source)
        
        # Extract title using BeautifulSoup
        title = extract_text_from_element(soup, 'title')
        print(f"Page title: {title}")
        
        # Extract heading
        heading = extract_text_from_element(soup, 'h1')
        print(f"Main heading: {heading}")
        
    finally:
        driver_manager.quit()

def example_brave_usage():
    """Example using Brave browser"""
    print("\n=== Brave Browser Example ===")
    
    # Initialize with Brave preference
    driver_manager = DynamicWebDriver(
        browser_preference='brave',
        headless=False,
        debug_port=None
    )
    
    try:
        driver = driver_manager.get_driver()
        
        # Navigate to a test page
        driver.get("https://httpbin.org/json")
        time.sleep(2)
        
        # Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = parse_html_with_beautifulsoup(page_source)
        
        # Extract JSON content
        pre_content = extract_text_from_element(soup, 'pre')
        print(f"JSON content: {pre_content}")
        
    finally:
        driver_manager.quit()

def example_edge_usage():
    """Example using Edge browser"""
    print("\n=== Edge Browser Example ===")
    
    # Initialize with Edge preference
    driver_manager = DynamicWebDriver(
        browser_preference='edge',
        headless=False,
        debug_port=None
    )
    
    try:
        driver = driver_manager.get_driver()
        
        # Navigate to a test page
        driver.get("https://example.com")
        time.sleep(2)
        
        # Get page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = parse_html_with_beautifulsoup(page_source)
        
        # Extract all paragraphs
        paragraphs = soup.find_all('p')
        print("All paragraphs:")
        for i, p in enumerate(paragraphs, 1):
            print(f"  {i}. {p.get_text(strip=True)}")
        
    finally:
        driver_manager.quit()

def example_debug_port_usage():
    """Example connecting to existing browser with debug port"""
    print("\n=== Debug Port Connection Example ===")
    print("Note: Start your browser with --remote-debugging-port=9222 first")
    
    # Initialize with debug port connection
    driver_manager = DynamicWebDriver(
        browser_preference='chrome',
        headless=False,
        debug_port=9222  # Connect to existing browser
    )
    
    try:
        driver = driver_manager.get_driver()
        
        # Get current page source and parse with BeautifulSoup
        page_source = driver.page_source
        soup = parse_html_with_beautifulsoup(page_source)
        
        # Extract current page title
        title = extract_text_from_element(soup, 'title')
        print(f"Current page title: {title}")
        
        # Get current URL
        current_url = driver.current_url
        print(f"Current URL: {current_url}")
        
    except Exception as e:
        print(f"Error connecting to debug port: {e}")
        print("Make sure to start your browser with: --remote-debugging-port=9222")
    finally:
        # Note: Don't quit when using debug port, as it will close the existing browser
        pass

def example_beautifulsoup_parsing():
    """Example of advanced BeautifulSoup parsing"""
    print("\n=== Advanced BeautifulSoup Parsing Example ===")
    
    # Sample HTML content (like what you might get from KoboCollect)
    sample_html = """
    <html>
        <body>
            <div id="kpiapp">
                <div class="data-table">
                    <div class="row" data-sid="12345">
                        <span class="status">Yes</span>
                        <span class="name">John Doe</span>
                        <button data-sid="12345">View</button>
                    </div>
                    <div class="row" data-sid="12346">
                        <span class="status">No</span>
                        <span class="name">Jane Smith</span>
                        <button data-sid="12346">View</button>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """
    
    soup = parse_html_with_beautifulsoup(sample_html)
    
    # Find all rows
    rows = soup.find_all('div', class_='row')
    print(f"Found {len(rows)} rows")
    
    for row in rows:
        data_sid = row.get('data-sid')
        status = extract_text_from_element(row, 'span', class_='status')
        name = extract_text_from_element(row, 'span', class_='name')
        
        print(f"Row {data_sid}: {name} - Status: {status}")
        
        # Only process if status is "Yes"
        if status == "Yes":
            print(f"  -> Would process row {data_sid}")

if __name__ == "__main__":
    print("Dynamic WebDriver Usage Examples")
    print("=" * 50)
    
    # Run BeautifulSoup parsing example first (no browser needed)
    example_beautifulsoup_parsing()
    
    # Uncomment the examples you want to run:
    
    # example_chrome_usage()
    # example_brave_usage()
    # example_edge_usage()
    # example_debug_port_usage()
    
    print("\nTo run browser examples, uncomment the desired functions in the main block.")