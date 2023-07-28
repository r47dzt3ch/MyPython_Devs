# Author: Jerald Jose 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time
import subprocess
import requests
# from msedge.selenium_tools import  Edge, EdgeOptions 
# "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 /prefetch:5 --flag-switches-begin --enable-features=msEdgeDevToolsWdpRemoteDebugging --flag-switches-end
# using the port 9515 to steady connect to new window of Edge
options = Options()
options.use_chromium = True
options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option("debuggerAddress", "localhost:9222")

# Configure the HTTP proxy details
proxy_host = 'smartproxy.crawlbase.com'
proxy_port = 8012
proxy_username = 'x7U6TavjC6ICEeeQerlEXQ'
# options proxy
options.add_argument(f"--proxy-server={proxy_username}@{proxy_host}:{proxy_port}")
# proxy_url = "http://x7U6TavjC6ICEeeQerlEXQ:@smartproxy.crawlbase.com:8012"
# proxies = {"http": proxy_url, "https": proxy_url}
seleniumwire_options = {
    'proxy': {
        'http': f'http://{proxy_username}@{proxy_host}:{proxy_port}',
        'https': f'http://{proxy_username}@{proxy_host}:{proxy_port}',
        'verify_ssl': False

    }
}



words = [
    "earn money",
    "online surveys",
    "work from home",
    "passive income",
    "freelancing",
    "affiliate marketing",
    "investment opportunities",
    "money-saving tips",
    "side hustles",
    "cashback rewards",
    "financial independence",
    "make money online",
    "money management",
    "money mindset",
    "money-making ideas",
    "entrepreneurship",
    "financial freedom",
    "saving strategies",
    "money goals",
    "budgeting tips"
]
driver = webdriver.Edge(options=options)
# Get the window handles
window_handles = driver.window_handles
# Switch to the second tab
driver.switch_to.window(window_handles[0]) # 0 is the first tab, 1 is the second tab
# driver.get('https://search.swagbucks.com/')
# use for loop to loop the words
for i in range(1, 2000):
    driver.get('https://www.youtube.com/watch?v=6CsOyesR2q4')
    # wait until the video is played
    driver.maximize_window()
    driver.implicitly_wait(10) # seconds


        # debugging to open the recent window of Edge browser
    # options.debugger_address = "localhost:34448"

    # the words or sentence is related to earn money
    # search the word in bing
    # search element by name
    # search = driver.find_element(By.NAME, 'q')
    # search.send_keys(word)
    # search.submit()
    # # scroll down to the bottom of the page
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # # wait for 20 seconds
    # time.sleep(20)
    # # go back to bing
    # driver.back()
    # # clear the search box
    # search = driver.find_element(By.NAME, 'q')
    # search.clear()
    # print the ip address to request 
    # response = requests.get(url="https://api.ipify.org?format=json")
    # print(response.json())

  
    

   







