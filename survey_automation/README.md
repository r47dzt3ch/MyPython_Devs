# KoboCollect Automation with Dynamic WebDriver

This enhanced KoboCollect automation script supports multiple browsers (Chrome, Edge, Brave, Firefox) and integrates BeautifulSoup for advanced HTML parsing.

## Features

- **Dynamic Browser Support**: Automatically detects and uses available browsers
- **BeautifulSoup Integration**: Advanced HTML parsing capabilities
- **Error Handling**: Robust error handling for automation reliability
- **Debug Port Support**: Connect to existing browser instances
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Supported Browsers

1. **Chrome** - Google Chrome browser
2. **Brave** - Brave browser (uses Chrome driver)
3. **Edge** - Microsoft Edge browser
4. **Firefox** - Mozilla Firefox browser

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. The script will automatically download and manage browser drivers using `webdriver-manager`.

## Usage

### Basic Usage

```python
from kobocollect_automation import DynamicWebDriver

# Initialize with preferred browser
driver_manager = DynamicWebDriver(
    browser_preference='chrome',  # or 'brave', 'edge', 'firefox'
    headless=False,
    debug_port=None
)

driver = driver_manager.get_driver()
# Use driver for automation...
driver_manager.quit()
```

### Connect to Existing Browser

To connect to an existing browser instance (useful for debugging):

1. Start your browser with debug port:
```bash
# Chrome/Brave
chrome.exe --remote-debugging-port=9222

# Edge
msedge.exe --remote-debugging-port=9222
```

2. Connect to the existing browser:
```python
driver_manager = DynamicWebDriver(
    browser_preference='chrome',
    debug_port=9222
)
```

### BeautifulSoup Integration

```python
from kobocollect_automation import parse_html_with_beautifulsoup, extract_text_from_element

# Get page source from Selenium
page_source = driver.page_source

# Parse with BeautifulSoup
soup = parse_html_with_beautifulsoup(page_source)

# Extract specific elements
title = extract_text_from_element(soup, 'title')
paragraphs = soup.find_all('p')
```

## Configuration Options

### DynamicWebDriver Parameters

- `browser_preference`: Preferred browser ('chrome', 'brave', 'edge', 'firefox')
- `headless`: Run browser in headless mode (True/False)
- `debug_port`: Port number to connect to existing browser (e.g., 9222)

### Browser-Specific Paths

The script automatically detects browser installations in common locations:

**Brave Browser Paths:**
- Windows: `C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe`
- macOS: `/Applications/Brave Browser.app/Contents/MacOS/Brave Browser`
- Linux: `/usr/bin/brave-browser`

## Example: KoboCollect Automation

```python
# Initialize driver
dynamic_driver = DynamicWebDriver(browser_preference='chrome')
driver = dynamic_driver.get_driver()

# Navigate to KoboCollect
driver.get("https://kobo.humanitarianresponse.info/accounts/login/")

# Login (replace with your credentials)
username = driver.find_element(By.ID, 'id_login')
username.send_keys("your_username")

password = driver.find_element(By.ID, 'id_password')
password.send_keys("your_password")

driver.find_element(By.NAME, 'Login').click()

# Parse page with BeautifulSoup
page_source = driver.page_source
soup = parse_html_with_beautifulsoup(page_source)

# Extract data and process...
dynamic_driver.quit()
```

## BeautifulSoup Examples

### Basic HTML Parsing

```python
html = "<html><body><p>Hello</p></body></html>"
soup = BeautifulSoup(html, "lxml")
print(soup.p.text)  # Output: Hello
```

### Advanced Parsing

```python
# Find elements by class
elements = soup.find_all('div', class_='data-row')

# Find elements by ID
element = soup.find('div', id='specific-id')

# Extract attributes
data_sid = element.get('data-sid')

# Extract text content
text_content = element.get_text(strip=True)
```

## Error Handling

The script includes comprehensive error handling:

- Browser initialization failures
- Element not found exceptions
- Window handling errors
- Form interaction errors

## Files

- `kobocollect_automation.py` - Main automation script
- `usage_example.py` - Usage examples and demonstrations
- `requirements.txt` - Required Python packages
- `README.md` - This documentation

## Troubleshooting

### Browser Not Found
If a browser fails to initialize, the script will try the next available browser in order of preference.

### Debug Port Connection Issues
Ensure the browser is started with the correct debug port:
```bash
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"
```

### Driver Download Issues
The script uses `webdriver-manager` to automatically download drivers. If you encounter issues:
1. Check your internet connection
2. Clear the driver cache: `~/.wdm/` (Linux/macOS) or `%USERPROFILE%\.wdm\` (Windows)

## Advanced Features

### Custom Browser Options
You can extend the `DynamicWebDriver` class to add custom browser options:

```python
class CustomWebDriver(DynamicWebDriver):
    def _get_chrome_options(self, is_brave=False):
        options = super()._get_chrome_options(is_brave)
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        return options
```

### Multiple Browser Instances
You can run multiple browser instances simultaneously:

```python
chrome_driver = DynamicWebDriver(browser_preference='chrome')
edge_driver = DynamicWebDriver(browser_preference='edge')

chrome = chrome_driver.get_driver()
edge = edge_driver.get_driver()

# Use both browsers...

chrome_driver.quit()
edge_driver.quit()
```

## License

This project is open source and available under the MIT License.