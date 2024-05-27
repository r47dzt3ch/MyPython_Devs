
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
#google service account
from google.oauth2 import service_account
import pandas as pd
import gspread
import time
import random
import string
import requests
import json
# stem for changing ip
from stem import Signal
from stem.control import Controller
import  os      

#change ip
def change_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)   
        controller.close()
Options = Options()
Options.add_argument("--remote-debugging-port=9222")
Options.add_argument("--disable-notifications")
Options.add_argument("--detach") # to keep chrome open after script finishes
Options.add_argument('--proxy-server=socks5://localhost:9050') # Tor proxy
# Options.add_experimental_option("debuggerAddress", "localhost:9222")
Options.add_argument("--headless")
Options.add_argument("--disable-gpu")
Options.add_argument("--disable-dev-shm-usage")
Options.add_argument("--no-cache")
Options.add_argument("--incognito")
Options.add_argument("--disable-extensions")
Options.add_argument("--disable-infobars")
Options.add_argument("--disable-features=VizDisplayCompositor")
Options.add_argument("--use-fake-ui-for-media-stream")
Options.add_argument("--disable-blink-features=AutomationControlled")
Options.add_argument("--disable-user-media-security=true")
Options.add_argument("--disable-web-security=true")
Options.add_argument("--allow-running-insecure-content=true")
Options.add_argument("--ignore-certificate-errors")
Options.add_argument("--disable-popup-blocking")
Options.add_argument("--disable-logging")
Options.add_argument("--log-level=3")
Options.add_argument("--disable-session-crashed-bubble")
Options.add_argument("--disable-ipv6")
Options.add_argument("--disable-sync")
Options.add_argument("--disable-background-networking")






#google service account
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'gspread_creds.json'
creds = None
creds = service_account.Credentials.from_service_account_file( SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

#open google sheet
sheet = client.open('ddo_SCdata').sheet1
data = sheet.get_all_records()
# extract to pandas dataframe
df = pd.DataFrame(data)

for i in range(len(df)):
    if df['Email Address'][i] == '':
        change_ip()
        # clear cookies and cache argument for chrome 
     
        driver = webdriver.Chrome(options=Options)
        ip_a= driver.get('https://api64.ipify.org')
        s= driver.find_element(By.XPATH,'/html/body/pre').text
        print(s)
        first_name = df['First Name'][i]
        last_name = df['Last Name'][i]
        split_yearofbirth = df['Birth Date'][i].split('-')
        yearofbirth = split_yearofbirth[2]
        #open website
        # clear cookies and cache
        driver.delete_all_cookies()
        

        driver.get('https://accounts.google.com/')
        # wait for page to load
        time.sleep(3)
        # click on create account
        driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div/button').click()
        # click list for my personal use
        driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div/ul/li[1]').click()
        fname = driver.find_element(By.NAME,"firstName")
        fname.send_keys(first_name)
        lname = driver.find_element(By.NAME,"lastName")
        lname.send_keys(last_name)
        driver.find_element(By.ID,"collectNameNext").click()
        time.sleep(10)
    
        driver.find_element(By.NAME,"day").send_keys(split_yearofbirth[1])
        
        driver.find_element(By.NAME,"year").send_keys(yearofbirth)
        # select month
        select = driver.find_element(By.ID,"month")
        options = select.find_elements(By.TAG_NAME,"option")
        for option in options:
            # get the value of the option in the dropdown
            value = option.get_attribute("value")
           

            if split_yearofbirth[0] != "10":# not remove the 0
                remove_zero = split_yearofbirth[0].lstrip("0")
            else:
                remove_zero = split_yearofbirth[0]
            
            if value == remove_zero:
                option.click()
                break
        
        gender = driver.find_element(By.ID,"gender")
        gender_select = gender.find_elements(By.TAG_NAME,"option")
        for g_value in gender_select:
            if g_value.text == "Rather not say":
                g_value.click()
                break
        
        # click next
        driver.find_element(By.ID,"birthdaygenderNext").click()
        time.sleep(10)

        driver.find_element(By.ID,"selectionc1").click()
        # get the email
        


        driver.find_element(By.ID,"next").click()
        time.sleep(10)
        # randomize password from the last name and add random string
        email_pass = last_name + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
        driver.find_element(By.NAME,"Passwd").send_keys(email_pass)
        confirm_pass = driver.find_element(By.NAME,"PasswdAgain")
        confirm_pass.send_keys(email_pass)
        # click next
        driver.find_element(By.ID,"createpasswordNext").click()
        time.sleep(3)
        # print("email: " + email)
        print("password: " + email_pass)
        # write to google sheet         
        sheet.update_cell(i+2, 7, email_pass) #2 is the column number i+2 is the row number 
                              
        driver.find_element(By.XPATH,'//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div/div/div/button')
        
        # # click next
        # driver.find_element(By.ID,"identifierNext").click()

        


            






        


