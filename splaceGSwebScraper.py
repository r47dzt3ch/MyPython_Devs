#/usr/bin/python3
#r47dzt3ch
from config import *
import sys
import gspread
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from itertools import chain
# authenticate with the Google API
from oauth2client.service_account import ServiceAccountCredentials
options = webdriver.EdgeOptions() 
options.add_argument("start-maximized")
# to supress the error messages/logs
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# driver for edge browser
driver = webdriver.Edge(options=options)
#hide the browser window
# driver.minimize_window()
# define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
# create the credentials object
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
# create the gspread client
gc = gspread.authorize(credentials)
sh1 = gc.open('splacegs')
worksheet= sh1.worksheet('Sheet1')
#open zipcodes sheet
sh2 = gc.open('zipcodes')
worksheet2= sh2.worksheet('VIVO Solar')
# Get all values from the sheet
all_values = worksheet.get_all_values()
list_areaSupportedZipcodes = worksheet2.get_all_values()
# # Loop through the list of lists and get the values from the first column
list_asptZipcodes = [row[0] for row in list_areaSupportedZipcodes]
# phoneNum_values = [row[2] for row in values]  # 2 is the phoneNumber column   
# zipcode_values = [row[7] for row in values]  # 7 is the zipcode column  
# df_list_asptZipcodes = pd.DataFrame(list_asptZipcodes)
# df_zipcode = pd.DataFrame(zipcode_values) 
# phone_rows = worksheet.col_values(3)


#function to login to melissa.com
def loginMelissa():
    try:
        #open edge browser
        driver.get("https://apps.melissa.com/user/signin.aspx?src=/user/user_account.aspx") #open the melissa website sign in page
        #find the button and click it
        txtb_email = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Signin1_txtEmail') # 1st argument is the locator type, 2nd argument is the locator value
        txtb_pass = driver.find_element(By.ID, 'ctl00_ContentPlaceHolder1_Signin1_txtPassword') 
        txtb_email.send_keys(melissa_email)
        txtb_pass.send_keys(melissa_password)
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ctl00_ContentPlaceHolder1_Signin1_btnLogin")))
        button.click()
        time.sleep(4)
    except Exception as e:
        print('Error 101: Sign In to melissa: ',e)
        pass


#this function to filter the data from google sheets with the verifier name column  and get all the phone number
def filterDataWithVerifierName(verifierName):
    # Get all values from the sheet
    header = all_values[0]
    verifier_name_index = header.index("Verifier")
    phone_index = header.index("Phone Number")
    phone_tblRow = []
    df_phoneNum = pd.DataFrame()
    try:
        for row in all_values[1:]: # get the list of phone number in phone_index column
            if row[verifier_name_index] == verifierName:
                # if row is empty then catch the error and pass
                if row[phone_index] == '':
                    print('empty row')
                    pass
                #appending to phone_tblRow list

                phone_tblRow.append(row[phone_index])
        return phone_tblRow
        #convert the list to dataframe

    except Exception as e:
        print("Error 102: with filtering verifier name: ",e)
        pass

#this function will send phone number from gs to melissa.com and update the google sheets with the updated data from melissa.com
def sendPhoneNum(phoneN):
    try:
        tbl_data = []
        #loop through the phone number list  
        for row in phoneN :
            phoneN = row
            #open the melissa.com phone look up page
            driver.get("https://www.melissa.com/v2/lookups/personatorsearch/?phoneNumber={0}".format(row))
            time.sleep(2)

            # check if the table ID is present in the page
            try:  # try and except block to catch the error if the table is not found and continue the loop
                table = driver.find_element(By.ID,'tblPeopleList') #find element using id in table 
                tbl_header = table.find_elements(By.TAG_NAME,"thead") # find the header of the table
                tbl_header_cols = tbl_header[0].find_elements(By.TAG_NAME,"th") # find the columns of the table
                tbl_rows = table.find_elements(By.TAG_NAME,"tr") #get all of the rows in the table
                zipcode_index = tbl_header_cols.index("ZIP") #get the index of zipcode column
                print(zipcode_index)
                time.sleep(2)
                # Get all rows from the table
                for tbl_tr in tbl_rows:
                    # Get all columns
                    tbl_cols = tbl_tr.find_elements(By.TAG_NAME,"td") #note: index start from 0, 1 is col 2
                    # Get the text from columns in for loop
                    for col_text in tbl_cols:
                        #condition to filter the appended data with zipcode column that supported in zipcode sheet
                        #codition for two arrays in if statement in python
                        try :
                            if col_text[zipcode_index] == list_asptZipcodes[1:]:
                                #append the data to tbl_data list
                                tbl_data = col_text.append(col_text.text)
                                print('Phone Number: {0} = {1}'.format(phoneN,tbl_data))
                        except Exception as e:
                            print("Error 103.1: with filtering zipcode: ",e)
                            pass
                    
            except:
                print("No Results Found for {0}".format(row))
                continue
       
            # if driver.find_element(By.XPATH,'//*[@id="tblPeopleList"]/tbody') is None:
            #     print("Failed to find table")  
            # else:        
            #     table = driver.find_element(By.ID,'tblPeopleList') #find element using id in table 
            #     time.sleep(2)
            #     print(table)
            # Get all rows
    except Exception as e:
        print("Error 103: Sending Phone Numbers to melissa phone lookUp: ",e)
        pass

#Function for getting zipcodes from google sheets
def getZipcodes():
    try:
        # Get all values from the sheet
        all_values = worksheet2.get_all_values()
        # Loop through the list of lists and get the values from the first column
        list_asptZipcodes = [row[0] for row in all_values]
        df_list_asptZipcodes = pd.DataFrame(list_asptZipcodes)
        return df_list_asptZipcodes
    except Exception as e:
        print("Error 104: Getting zipcodes from google sheets: ",e)
        pass

#main function
if __name__ == '__main__':
     # login to melissa.com
    phoneN_rows = []
    loginMelissa()
    # filter the data from google sheets with the verifier name
    name_verifier = "Jose, Jerald P"
    phoneN_rows=filterDataWithVerifierName(name_verifier)
    #limit the range of the phone number to 10
    # phoneN_rows = phoneN_rows[0:10]

    # send the phone number to melissa.com and update the google sheets
    sendPhoneNum(phoneN_rows)
    

