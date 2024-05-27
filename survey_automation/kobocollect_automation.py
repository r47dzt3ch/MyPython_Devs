from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests

options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")
driver = webdriver.Edge(options=options)
# driver.get("https://kobo.humanitarianresponse.info/accounts/login/?next=/kobocat/")
# time.sleep(5)
# username = driver.find_element(By.ID, 'id_login')
# username.send_keys("phatts_de_oro")
# password = driver.find_element(By.ID, 'id_password')
# password.send_keys("phattsJUNE2023$f")
# driver.find_element(By.NAME, 'Login').click()
# time.sleep(5)
# driver.get("https://kobo.humanitarianresponse.info/#/forms/aSuujXtXVGiR8Gg3F3yckM/data/table")
# # Wait for the table to be visible
# time.sleep(20)
# # //*[@id="kpiapp"]/div[2]/div[2]/div[3] thi the table wih header //*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[1]/div[3]/button[1]
# driver.find_element(By.XPATH, '//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[1]/div[3]/button[1]').click()
# time.sleep(5)
# search = driver.find_element(By.XPATH,'//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[5]/input')
# search.send_keys("Vergilia")
# time.sleep(20)
# driver.find_element(By.XPATH, '//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[2]/div/div[1]/div/div[1]/label/input').click() #checkox
# time.sleep(5)
# //*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/div[1]/div/div[1]/div/div/label/input
# //*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/div[1]/div/div[1]/div/button[2]/i  -get the value for each of the data-sid
for i in range(1, 370):
    #  //*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/div[i]/div/div[34]/span = valu is not empty
    value_of_span = driver.find_element(By.XPATH, '//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/div['+str(i)+']/div/div[34]/span')
    value_of_span = value_of_span.text # get the value of the span
    # value_of_17 = driver.find_element(By.XPATH, '//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/div['+str(i)+']/div/div[39]/span')
    # value_of_17 = value_of_17.text
    # value_of_18 = driver.find_element(By.XPATH, '//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/div['+str(i)+']/div/div[40]/span')
    # value_of_18 = value_of_18.text
    # print(value_of_18)
    print(value_of_span)
    if value_of_span != "No":
        data_sid = driver.find_element(By.XPATH, '//*[@id="kpiapp"]/div[2]/div[2]/div[3]/div[2]/div[1]/div[3]/div['+str(i)+']/div/div[1]/div/button[2]')
        print(data_sid.get_attribute("data-sid")," index: ",i)
        data_sid.click() # this will open the data in a new tab 
        time.sleep(10)
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[1]) # 0 is the first tab, 1 is the second tab
        time.sleep(5)
        # scroll down to click radio button /html/body/div[1]/article/form/section[2]/section[2]/section[1]/fieldset[11]/fieldset/div/label[2]/input
        q13 = driver.find_element(By.XPATH, '/html/body/div[1]/article/form/section[2]/section[2]/section[1]/fieldset[11]/fieldset/div/label[2]/input')
        driver.execute_script("arguments[0].scrollIntoView();", q13)
        q13.click()
        # q18 = driver.find_element(By.XPATH, '/html/body/div[1]/article/form/section[2]/section[2]/section[2]/section[2]/label[2]/input')
        # q18.clear()
        # q18.send_keys("")
        # scroll to button 
        submit = driver.find_element(By.XPATH, '//*[@id="submit-form"]')
        submit.click()
        time.sleep(10)
        # close the second tab
        driver.close()
        # switch back to the first tab
        driver.switch_to.window(window_handles[0])
    
    



 














