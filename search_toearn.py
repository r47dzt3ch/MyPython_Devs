

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import os

# Set up the Selenium WebDriver with Microsoft Edge
options = webdriver.EdgeOptions() 
options.add_experimental_option("debuggerAddress", "localhost:9222")
driver = webdriver.Edge(options=options)
window_handles = driver.window_handles
driver.switch_to.window(window_handles[1]) # 0 is the first tab, 1 is the second tab

# Navigate to the webpage
url = "https://www.msn.com/en-ph/feed"
driver.get(url)
time.sleep(5)  # wait for 5 seconds

# Use the full XPath to find the element and extract its text
full_xpath = '/html/body/div/msn-windows-page/fluent-design-system-provider/div/div[2]/grid-view-feed//div/div[1]/cs-super-container//cs-personalized-feed//cs-feed-layout//cs-responsive-card[1]//div/div[2]/div[1]/a'  # wait for 5 seconds before finding the element
# news_feeds = driver.find_element(By.XPATH, '//*[@id="root"]/msn-windows-page/fluent-design-system-provider/div/div[2]/grid-view-feed//div/div[1]')
# text = news_feeds.text  # div > div.body > div.text

# print(text)  # Print the text content

# Remember to clear the search bar if needed '//*[@id="srchfrm"]'
search_bar = driver.find_element(By.ID,'q' )
search_bar.click()
search_bar.send_keys('arduino')
# search_bar.clear()

# Add any additional code you need here

# Close the browser when done
driver.quit()
