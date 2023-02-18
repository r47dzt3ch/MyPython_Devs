from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver=webdriver.Edge()
driver.get("youtube.com")
txtb_search = driver.find_element(By.ID, 'search')
txtb_search.send_keys('r47dzt3ch')
time.sleep(2)
searchButton = driver.find_element(By.ID, 'search-icon-legacy')
searchButton.click()
time.sleep(2)
# //*[@id="video-title"]

