#google service account
from google.oauth2 import service_account
import pandas as pd
import gspread
import time
import re
import random
import string
import requests

# webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


#google service account
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'gspread_creds.json'
creds = None
creds = service_account.Credentials.from_service_account_file( SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

#read spreadsheet
sheet = client.open('WichitaKS').sheet1
zipcode = client.open('ZipCode').sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)
zipdata = zipcode.get_all_records()
zipdf = pd.DataFrame(zipdata)

Options = Options()
Options.add_argument("--disable-infobars")
Options.add_argument("--disable-extensions")
Options.add_argument("--disable-gpu")
Options.add_argument("--headless")

# Options.add_experimental_option("debuggerAddress", "localhost:9222")
driver = webdriver.Chrome(options=Options)
driver.get("https://apps.melissa.com/user/signin.aspx")
time.sleep(5)               
driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_Signin1_txtEmail").send_keys("jeraldjose16@gmail.com")
driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_Signin1_txtPassword").send_keys(":z-YnUmmK-9RH55")
driver.find_element(By.ID,"ctl00_ContentPlaceHolder1_Signin1_btnLogin").click()
driver.get("https://lookups.melissa.com/home/personatorsearch")
for i in range(len(df)):
    phone = df['phone_number'][i]
    status = df['Status'][i]
    if status == "": 
        driver.get("https://lookups.melissa.com/home/personatorsearch/?name=&city=&state=&postalCode=&melissaAddressKey=&phoneNumber={}&emailAddress=&freeForm=".format(phone))
        time.sleep(5)
        try:
            card = driver.find_element(By.XPATH,'//*[@id="tblPeopleList"]')
            thead = card.find_element(By.TAG_NAME,"thead")
            tbody = card.find_element(By.TAG_NAME,"tbody")
            tr = tbody.find_elements(By.TAG_NAME,"tr")
            tr_count = 0
            for j in range(len(tr)):  
                td = tr[j].find_elements(By.TAG_NAME,"td")
                zip = td[4].text
                for k in range(len(zipdf)):
                    spt_zip = zipdf['Wichita KS'][k]
                    spt_zip = int(spt_zip)
                    zip = int(zip)

                    if spt_zip == zip:
                        
                        if tr_count  == 0:

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
                            disposition = "Done"
                            zip1 = zip
                            
                            

                            

                            print("first_name: ",first_name,"last_name: ",last_name,"address: ",address,"city: ",city,"state: ",state,"zip: ",zip)
                            try:

                                sheet.update_cell(i+2, 2, first_name)
                                sheet.update_cell(i+2, 3, last_name)
                                sheet.update_cell(i+2, 4, address)
                                sheet.update_cell(i+2, 5, city)
                                sheet.update_cell(i+2, 6, state)
                                sheet.update_cell(i+2, 7, zip)
                                sheet.update_cell(i+2, 8, disposition)

                                
                            except Exception as e:
                                print(e)
                            tr_count += 1
                        
                        elif tr_count == 1 and zip1 == zip:
                            name = td[0].text
                            sheet.update_cell(i+2, 9, name)
                            print("additional name1: ",name)
                            tr_count += 1
                            continue

                        elif tr_count == 2 and zip1 == zip:
                            name = td[0].text
                            sheet.update_cell(i+2, 10, name)
                            print("additional name:2 ",name)
                            tr_count += 1
                            continue
                        elif tr_count == 3 and zip1 == zip:
                            name = td[0].text
                            sheet.update_cell(i+2, 11, name)
                            print("additional name3: ",name)
                            continue

                        else:
                            continue                
                    else:
                        continue  
        except:
            print("No MATCH FOUND for {}".format(phone))
            disposition = "No Result"
            sheet.update_cell(i+2, 8, disposition)
            continue 
    else:
        continue
