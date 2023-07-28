# Author: Jerald Jose 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time
import requests
# execute in terminal"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 /prefetch:5 --flag-switches-begin --enable-features=msEdgeDevToolsWdpRemoteDebugging --flag-switches-end
url = "https://newsinfo.inquirer.net/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
trending_topics = soup.find_all("div", id="ncg-info")
options = Options()
driver = webdriver.Edge(options=options)
# options.use_chromium = True
options.add_experimental_option("debuggerAddress", "localhost:9222")
window_handles = driver.window_handles
driver.switch_to.window(window_handles[0]) # 0 is the first tab, 1 is the second tab
print(trending_topics)
for i in trending_topics:
    driver.get("https://www.bing.com/search?q="+i.text)
    time.sleep(5)
    # clear the search bar
    txtb_search = driver.find_element(By.ID, 'sb_form_q')
    txtb_search.clear()

  
    

   







