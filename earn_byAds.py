# Description: This script is used to earn by watching ads on youtube
from seleniumwire  import webdriver
from selenium.webdriver.common.by import By
import time
import subprocess
# Configure the HTTP proxy details
proxy_host = 'smartproxy.crawlbase.com'
proxy_port = 8012
proxy_username = 'x7U6TavjC6ICEeeQerlEXQ'
seleniumwire_options = {
    'proxy': {
        'http': f'http://{proxy_username}@{proxy_host}:{proxy_port}'
        # 'verify_ssl': False
    }
}
# Configure the Selenium WebDriver with the proxy
driver = webdriver.Edge(seleniumwire_options=seleniumwire_options)


for i in range(1, 100):
    
    driver.get('https://www.youtube.com/watch?v=6CsOyesR2q4')
    # wait until the video is played
    driver.maximize_window()
    driver.implicitly_wait(10) # seconds


    
    

