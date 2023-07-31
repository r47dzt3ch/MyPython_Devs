# Author: r4dzt3ch

import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
import re


# load the credentials from the json file
client_secret_path = os.path.join(os.getcwd(), 'Credentials\client_secret.json')
scope = ['https://mail.google.com', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.readonly']
creds =  Credentials.from_authorized_user_file(client_secret_path, scope)
service = build('gmail', 'v1', credentials=creds)



def get_email_content(): # if content is bad then delete the email
    # Call the Gmail API to get a list of messages
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    print(len(results['messages']))
    messages = results.get('messages', [])
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        # extract the email address from the message
        headers = msg['payload']['headers']
        for header in headers:
            print(header['name']) 
            if header['name'].lower() == 'from':
                f_email = header['value']  
                    
                # print(f_email)

def delete_email(domain):
    next_page_token = None
    deleted_emails = 0
    total_emails = 0
    while True:
        # Call the Gmail API to get a list of messages
        results = service.users().messages().list(userId='me', labelIds=['INBOX'],pageToken=next_page_token).execute()
        # get the email, subject, and body
        messages = results.get('messages', [])
        total_emails += len(messages)
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            # extract the email address from the message
            headers = msg['payload']['headers']
            for header in headers:
                if header['name'].lower() == 'from':
                    f_email = header['value']        
                    email = re.findall(r'@[\w\.-]+', f_email)     
                    break
            else:
                # If no 'From' header is found, skip this message
                continue

            # if the email address matches the domain, delete the message
            if email[0].lower() == '@' + domain.lower():
                service.users().messages().delete(userId='me', id=message['id']).execute()
                print('From Email: {} is deleted successfully'.format(f_email))
                deleted_emails += 1
            
        # Check if there are more messages on the next page
        next_page_token = results.get('nextPageToken')
        print('Total emails in INBOX:', total_emails)
        print('Total emails deleted:', deleted_emails)
        print('Total emails remaining in INBOX:', total_emails - deleted_emails)



if __name__ == '__main__':
    # get_email_content()
    # get_email()
    delete_email('linkedin.com')



        
    




