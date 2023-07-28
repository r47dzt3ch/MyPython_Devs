# Author: Jerald Jose 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time
import requests
# execute in terminal"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 /prefetch:5 --flag-switches-begin --enable-features=msEdgeDevToolsWdpRemoteDebugging --flag-switches-end
options = Options()
# mobile user agent in edge browser
options.add_argument("user-agent=Mozilla/5.0 (Linux; Android 10; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36 Edg/86.0.622.69")
options.add_experimental_option("debuggerAddress", "localhost:9222")


url = "https://newsinfo.inquirer.net/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
# class="news-card-body card-with-cluster"
trending_topics = soup.find_all("div", id="ncg-info")

driver = webdriver.Edge(options=options)
# window_handles = driver.window_handles
# driver.switch_to.window(window_handles[0]) # 0 is the first tab, 1 is the second tab
print(trending_topics)
for i in trending_topics:
    driver.get("https://www.bing.com/search?q="+i.text)
    time.sleep(5)
    # clear the search bar
    txtb_search = driver.find_element(By.ID, 'sb_form_q')
    txtb_search.clear()

  
    

   







