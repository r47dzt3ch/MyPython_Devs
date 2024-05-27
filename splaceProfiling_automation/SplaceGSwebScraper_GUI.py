''' 
Client: Splace Corporation
Developer: RaldzInfoTechPH
Contact Info: 
    - Mobile: 09306619472
    - Email: jeraldjose16@gmail.com
Social Media:
    - Facebook: https://www.facebook.com/raldzinfotechph
    - Instagram: https://www.instagram.com/raldzinfotechph
    - Twitter: https://twitter.com/raldzinfotechph
    - Youtube: https://www.youtube.com/channel/UCZ8Y4Z5ZQ5ZQ5ZQ5ZQ5ZQ5Q
If you support this project, please donate to:
    - GCash: 09306619472
    - Paymaya: 09306619472
    - Paypal: https://www.paypal.me/raldzinfotechph
    - Buy me a coffee: https://www.buymeacoffee.com/raldzinfotechph
    - Coin PH: https://www.coin.ph/link/raldzinfotechph
############################################################################################
Purpose:
This code is for Splace Corporation's  to be able to scrape data from the web and update
the google sheets with the data from the web.

requirements:
    - selenium
    - google sheets api
    - google chrome or edge driver
    - python 3.8
    - tkinter
Setup:
    - install selenium and google sheets api
    - download google chrome or edge driver
    - create a google sheets
    - create a google cloud platform account
    - create a service account key
    - create a google cloud platform project
    - create a google cloud platform service account
    - create a google cloud platform service account key
'''

############################################################################################
import os
from tkinter import *
from tkinter import ttk

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# edge options
from selenium.webdriver.edge.options import Options
import time

options = Options()
options.use_chromium = True
# prevent close browser module
options.add_experimental_option("debuggerAddress", "localhost:9222")
 # driver for edge browser
driver = webdriver.Edge(options=options)
# driver.get("https://apps.melissa.com/user/signin.aspx")
# time.sleep(5)               
# driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_Signin1_txtEmail").send_keys("jeraldjose16@gmail.com")
# driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_Signin1_txtPassword").send_keys(":z-YnUmmK-9RH55")
# driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_Signin1_btnLogin").click()
# driver.get("https://lookups.melissa.com/home/personatorsearch")



# switch to the new window which is second in window_handles array

# driver.get("http://134.209.108.40/login")
# user_name = driver.find_element(By.ID,"username_login")
# user_name.send_keys("profiler2")
# password = driver.find_element(By.ID,"pwd_login")
# password.send_keys("qwerty16!@#")
# form submit by name
# driver.find_element(By.NAME,"login").click()
# time.sleep(5)
# driver.get('http://134.209.108.40/profiler/verify-leads')
while True:
    driver.switch_to.window(driver.window_handles[1])
    # driver.find_element(By.ID,"verify-btn").click() #this will open modal
    # copy the #phone number from the modal
    # wait for the modal to load using WebDriverWait
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "phone")))
    phone_number = driver.find_element(By.ID,"phone")
    phone_number = phone_number.get_attribute("value")
    print(phone_number)
    driver.switch_to.window(driver.window_handles[0])
    # paste the #phone number to the search box
    driver.get("https://lookups.melissa.com/home/personatorsearch/?name=&city=&state=&postalCode=&melissaAddressKey=&phoneNumber={}&emailAddress=&freeForm=".format(phone_number))
    try:
        card = driver.find_element(By.XPATH,'//*[@id="tblPeopleList"]')
        thead = card.find_element(By.TAG_NAME,"thead")
        tbody = card.find_element(By.TAG_NAME,"tbody")
        tr = tbody.find_elements(By.TAG_NAME,"tr")
        tr_count = 0
        # if len(tr) < 0:
        #     driver.switch_to.window(driver.window_handles[1])
        #     disposition = driver.find_element(By.ID,'dispo')
        #     # change value of disposition to 4
        #     disposition.send_keys("4")
        #     # submit the form
        #     driver.find_element(By.XPATH,'//*[@id="data_submitForm"]/div/div[3]/button').click()
        #     time.sleep(5)
        #     driver.switch_to.window(driver.window_handles[0])
        # else:
        for j in range(len(tr)):
            td = tr[j].find_elements(By.TAG_NAME,"td")
            zipcode = td[4].text
            # back to the second tab
            driver.switch_to.window(driver.window_handles[1])
            # paste the #zipcode to the search box
            # clear the zipcode field

            driver.find_element(By.ID,"zcode").clear()
            driver.find_element(By.ID,"zcode").send_keys(zipcode)
            # get status if the zipcode is valid or not from id of zipcode_status = 'Zipcode is supported'
            zipcode_status = driver.find_element(By.ID,"zipcode_status").text
            print(zipcode_status)
            if zipcode_status == 'Zipcode is supported':
                if tr_count == 0:
                    tr_count += 1
                    driver.switch_to.window(driver.window_handles[0])
                    # get the name, address, city, state, zipcode
                    name = td[0].text
                    split_name = name.split(" ")
                    if len(split_name) == 2:
                        first_name = split_name[0]
                        last_name = split_name[1]
                    elif len(split_name) == 3:
                        first_name = split_name[0] + " " + split_name[1]
                        last_name = split_name[2]
                    else:
                        first_name = split_name[0]
                        last_name = split_name[1]
                    address = td[1].text
                    city = td[2].text
                    state = td[3].text
                    age = td[5].text
                    if age == '?':
                        age = ""
                    
                    disposition = "Done"
                    zip1 = zipcode
                    print("first_name: ",first_name,"last_name: ",last_name,"address: ",address,"city: ",city,"state: ",state,"zip: ",zip1)
                    # switch to the second tab

                    driver.switch_to.window(driver.window_handles[1])
                    # clear data_submitForm
                    driver.find_element(By.ID,"fname").clear()
                    driver.find_element(By.ID,"lname").clear()
                    driver.find_element(By.ID,"address").clear()
                    driver.find_element(By.ID,"city").clear()
                    driver.find_element(By.ID,"state").clear()
                    driver.find_element(By.ID,"zcode").clear()
                    driver.find_element(By.ID,"age").clear()

                    # paste the #first_name to the search box
                    driver.find_element(By.ID,"fname").send_keys(first_name)
                    # paste the #last_name to the search box
                    driver.find_element(By.ID,"lname").send_keys(last_name)
                    # paste the #address to the search box
                    driver.find_element(By.ID,"address").send_keys(address)
                    # paste the #city to the search box
                    driver.find_element(By.ID,"city").send_keys(city)
                    # paste the #state to the search box
                    driver.find_element(By.ID,"state").send_keys(state)
                    # paste the #zipcode to the search box
                    driver.find_element(By.ID,"zcode").send_keys(zip1)
                    driver.find_element(By.ID,"age").send_keys(age)
                    driver.switch_to.window(driver.window_handles[0])
                elif tr_count == 1 and zip1 == zipcode:
                    driver.switch_to.window(driver.window_handles[0])
                    age = td[5].text
                    if  age == '?' or age == '??':
                        age = ""
                    co_owner = td[0].text + " " + age
                    driver.switch_to.window(driver.window_handles[1])
                    driver.find_element(By.ID,"add-co-owner").click()
                    # co-owners-section array 0 is the first co-owner
                    co_section = driver.find_element(By.ID,"co-owners-section" ).find_elements(By.TAG_NAME,"input")[0].send_keys(co_owner)
                    tr_count += 1
                    driver.switch_to.window(driver.window_handles[0])
                    print("additional name1: ",co_owner)
                elif tr_count == 2 and zip1 == zipcode:
                    driver.switch_to.window(driver.window_handles[0])
                    age = td[5].text
                    if age == '?' or age == '??':
                        age = ""
                    co_owner = td[0].text + " " + age
                    driver.switch_to.window(driver.window_handles[1])
                    driver.find_element(By.ID,"add-co-owner").click()
                    # co-owners-section array 1 is the second co-owner
                    driver.find_element(By.ID,"co-owners-section").find_elements(By.TAG_NAME,"input")[1].send_keys(co_owner)
                    print("additional name2: ",co_owner)
                    tr_count += 1
                    driver.switch_to.window(driver.window_handles[0])
                elif tr_count == 3 and zip1 == zipcode:
                    driver.switch_to.window(driver.window_handles[0])
                    age = td[5].text
                    if age == '?' or age == '??':
                        age = ""
                    co_owner = td[0].text + " " + age
                    driver.switch_to.window(driver.window_handles[1])
                    driver.find_element(By.ID,"add-co-owner").click()
                    # co-owners-section array 2 is the third co-owner
                    driver.find_element(By.ID,"co-owners-section").find_elements(By.TAG_NAME,"input")[2].send_keys(co_owner)  
                    print("additional name3: ",co_owner)
                    driver.switch_to.window(driver.window_handles[0])    
                    tr_count += 1
                else:
                    continue  
            else:
                continue            
        #submit the form
        driver.switch_to.window(driver.window_handles[1])
        driver.find_element(By.XPATH,'//*[@id="data_submitForm"]/div/div[3]/button').click() 
        time.sleep(2) 
        driver.switch_to.window(driver.window_handles[0]) 
    except Exception as e:
        driver.switch_to.window(driver.window_handles[1])
        disposition = driver.find_element(By.ID,'dispo')
        # change value of disposition to 4
        disposition.send_keys("4")
        # submit the form
        driver.find_element(By.XPATH,'//*[@id="data_submitForm"]/div/div[3]/button').click()
        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        print(e)


       






        