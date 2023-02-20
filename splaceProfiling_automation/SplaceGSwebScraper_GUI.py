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
from config import *
import os
from tkinter import *
from tkinter import ttk
import gspread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

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
all_values = worksheet.get_all_values()
list_areaSupportedZipcodes = worksheet.get_all_values()
 # driver for edge browser
driver = webdriver.Edge()
# function to login to the melissa website
def loginMelissa():
    #open edge browser
    driver.get("https://apps.melissa.com/user/signin.aspx?src=/user/user_account.aspx")
    #find the button and click it
    txtb_email = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Signin1_txtEmail')
    txtb_pass = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Signin1_txtPassword')
    txtb_email.send_keys(melissa_email)
    txtb_pass.send_keys(melissa_password)
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_Signin1_btnLogin")))
    button.click()

# function to filter the data with the verifier name
def filterDataWithVerifierName(verifierName):
    # Get all values from the sheet
    header = all_values[0]
    verifier_name_index = header.index("Verifier")
    phone_index = header.index("Phone Number")
    phone_tblRow = []
    for row in all_values[1:]: # get the list of phone number in phone_index column
        if row[verifier_name_index] == verifierName:
            #output with data frame the phone number
            # df_phoneNum = pd.DataFrame(row[phone_index])
            phone_tblRow.append(row[phone_index])
            # return row[phone_index]
            print("The list of phone number: ",phone_tblRow)
    return phone_tblRow
#this function will send phone number from gs to melissa.com and update the google sheets with the updated data from melissa.com
def sendPhoneNum(phoneN):
    for row in phoneN :
        driver.get("https://www.melissa.com/v2/lookups/personatorsearch/?phoneNumber={0}".format(row))
        time.sleep(2)   
        
        table = driver.find_element(By.ID,'tblPeopleList') #find element using id in table 
        tbl_data= [] 
        for row in table.find_elements(By.XPATH,'//*[@id="tblPeopleList"]/tbody/tr'): # &lt;-- find_elements_by_xpath
            tbl_data = row.find_elements(By.XPATH,'//*[@id="tblPeopleList"]/tbody/tr/td') # &lt;-- find_elements_by_xpath
        print(tbl_data)
        #get the data from the table and update the google sheets with the data

# Main function
if __name__ == '__main__':
    verifier = ''
#create A tkinter gui to input the verifier name
    root = Tk()
    root.title("SplaceGSwebScraper")
    root.geometry("500x500")
    root.configure(bg="white")
    root.resizable(False, False)
    # create a label
    label = Label(root, text="Enter the verifier name", font=("Arial", 20), bg="white")
    label.pack(pady=20)

    #select option from combobox in tkinter
    # create a combobox
    combo = ttk.Combobox(root, font=("Arial", 20), width=20)
    combo.pack(pady=20)
    #comboBox items
    combo['values'] = ('Jose, Jerald P.', 'VERADOR, Jessa P', 'FERNANDEZ, Daryl F.', 'ATANOZA, Rizel Mae L.')
    # get the selected item
    verifier = combo.get()
    Button(root, text='Done', command=root.quit).pack(pady=22)
    root.mainloop()
    loginMelissa()
        # filter the data with the verifier name
    filterDataWithVerifierName(verifier)   
    sendPhoneNum(filterDataWithVerifierName(verifier))



        