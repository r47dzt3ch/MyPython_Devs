
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from msedge.selenium_tools import  Edge, EdgeOptions 
# # python proxy to change ip address
# import subprocess
# import time
# import requests
# # using the port 9515 to steady connect to new window of Edge
# options = EdgeOptions()
# options.use_chromium = True
# # debugging to open the recent window of Edge browser
# # options.debugger_address = "localhost:34448"
# driver = Edge(options=options, executable_path=r'C:\Users\jeral\Downloads\edgedriver_win64\msedgedriver.exe')
# #in youtube watch using different ip address to watch the video

# # for loop to change the ip address for each watch video
# for i in range(1, 31):
#     driver.get(['./proxychains', 'msedge', 'https://www.youtube.com/watch?v=9XaS93WMRQQ'])
   
#     driver.maximize_window()
#     # wait for 30 seconds to proceed to next ip address
#     time.sleep(30)

from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions
import time


# Configure the HTTP proxy details
proxy_host = 'smartproxy.crawlbase.com'
proxy_port = 8012
proxy_username = 'x7U6TavjC6ICEeeQerlEXQ'
proxies = {"http": f"http://{proxy_username}@{proxy_host}:{proxy_port}/", "https": f"http://{proxy_username}@{proxy_host}:{proxy_port}/"}

# Configure the Selenium WebDriver with the proxy
options = EdgeOptions()
options.use_chromium = True

# Configure proxy settings
options.add_argument(f"--proxy-server={proxies['https']}")
options.add_argument("--ignore-certificate-errors")



# Launch the WebDriver
driver = Edge(options=options, executable_path=r'C:\Users\jeral\Downloads\edgedriver_win64\msedgedriver.exe')

# For loop to change the IP address for each watch video
for i in range(1, 31):
    driver.get('https://www.youtube.com/watch?v=9XaS93WMRQQ')
    driver.maximize_window()
    time.sleep(30)

# Close the WebDriver
driver.quit()








    

   







