# Author: r4dzt3ch
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
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

def delete_email(domain):
    # Call the Gmail API to get a list of messages
    results = service.users().messages().list(userId='me', maxResults=500).execute()
    # get the email, subject, and body
    messages = results.get('messages', [])
    
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        # extract the email address from the message
        headers = msg['payload']['headers']
        for header in headers:
            if header['name'].lower() == 'from':
                email = header['value']
            # using regex to extract the email address only domain
                email = re.findall(r'@[\w\.-]+', email)     
                break
        else:
            # If no 'From' header is found, skip this message
            continue

        # if the email address matches the domain, delete the message
        if email[0].lower() == '@' + domain.lower():
            service.users().messages().delete(userId='me', id=message['id']).execute()
            print('Message with id: {} deleted successfully.'.format(message['id']))
    else:
        print('No emails found with the domain', domain)
delete_email('linkedin.com')


        
    




