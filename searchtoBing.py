import config
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random

driver=webdriver.Edge()
driver.get("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&id=264960&wreply=https%3a%2f%2fwww.bing.com%2fsecure%2fPassport.aspx%3frequrl%3dhttps%253a%252f%252fwww.bing.com%252f%253fstep%253dsignin%2526wlsso%253d1%2526wlexpsignin%253d1%26sig%3d357812B588BE64C83B36000E89AA65ED&wp=MBI_SSL&lc=1033&CSRFToken=362a0359-2493-4281-a580-7cabdf8c07c9&aadredir=1")
txtb_email = driver.find_element(By.ID, 'i0116')
txtb_email.send_keys(config.email)
time.sleep(2)
signOption = driver.find_element(By.ID, 'idA_PWD_SwitchToCredPicker')
signOption.click()
time.sleep(2)
useApassword = driver.find_element(By.ID, 'credType')
useApassword.click()
time.sleep(2)
nextButton = driver.find_element(By.ID, 'idSIButton9')
nextButton.click()
time.sleep(2)
txtb_pass = driver.find_element(By.ID, 'i0118')
txtb_pass.send_keys(config.password)
time.sleep(2)
nextButton = driver.find_element(By.ID, 'idSIButton9')
nextButton.click()
time.sleep(2)




