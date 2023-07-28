# Author: Jerald Jose 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time
import subprocess
import requests
# execute in terminal"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 /prefetch:5 --flag-switches-begin --enable-features=msEdgeDevToolsWdpRemoteDebugging --flag-switches-end
options = Options()
options.use_chromium = True
# options.add_argument("--remote-debugging-port=9222")
options.add_experimental_option("debuggerAddress", "localhost:9222")
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
window_handles = driver.window_handles
driver.switch_to.window(window_handles[0]) # 0 is the first tab, 1 is the second tab
for i in words:

  
    

   







