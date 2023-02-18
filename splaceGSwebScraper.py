#/usr/bin/python3
#r47dzt3ch
import gspread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
# authenticate with the Google API
from oauth2client.service_account import ServiceAccountCredentials
# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# create the credentials object
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
# create the gspread client

gc = gspread.authorize(credentials)
sh = gc.open('splacegs')
worksheet= sh.worksheet('Sheet1')
#open chrome browser
# driver = webdriver.Chrome()
driver = webdriver.Edge()
#navigate to the website
driver.get("https://apps.melissa.com/user/signin.aspx?src=/user/user_account.aspx")
#find the button and click it
txtb_email = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Signin1_txtEmail')
txtb_pass = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Signin1_txtPassword')
txtb_email.send_keys('jeraldjose16@gmail.com')
txtb_pass.send_keys(':z-YnUmmK-9RH55')
button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_Signin1_btnLogin")))
button.click()
driver.get("https://www.melissa.com/v2/lookups/personatorsearch/")

# Get all values from the sheet
values = worksheet.get_all_values()

# Loop through the list of lists and get the values from the first column
column_values = [row[2] for row in values]  # 2 is the phoneNumber column     
# Convert the list of hashes into a dataframe
# df = pd.DataFrame(column_values)  
for phoneNum in column_values :
    driver.get("https://www.melissa.com/v2/lookups/personatorsearch/?phoneNumber={0}".format(phoneNum))
    time.sleep(5)   
    # Find an element using its XPath
    table = driver.find_element(By.XPATH, '//*[@id="tblPeopleList"]')
    tbl_data= []    
    for row in table.find_element(By.XPATH,".//tr"):
        tbl_data.append([td.text for td in row.find_element(By.XPATH,".//td")])
    print(tbl_data)
    


