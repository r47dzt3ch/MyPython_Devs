# Author: r4dzt3ch

import time
import os
import json
import re
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
import spacy

# load the credentials from the json file
client_secret_path = os.path.join(os.getcwd(), 'Credentials\client_secret.json')
scope = ['https://mail.google.com', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.readonly']

try:
    creds =  Credentials.from_authorized_user_file(client_secret_path, scope)
    service = build('gmail', 'v1', credentials=creds)
except Exception as e:
    print(f"Failed to build service: {e}")

nlp = spacy.load('en_core_web_sm')

def get_email_content():
    try:
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
                    body_data = msg['payload']['body'].get('data')
                    if body_data:
                        body = body_data('utf-8').decode('utf-8')
                    else:
                        # Handle the missing 'data' field
                        body = None
                    print(f_email, body)
                    # Check if the email content is spam using the spacy library
                    if not is_spam(body):
                        yield (f_email, body)
                        print(f_email, body)
    except Exception as e:
        print(f"Failed to get email content: {e}")

def is_spam(text):
    try:
        spam_doc = nlp(text)
        if 'spam' in spam_doc:
            return True
        return False
    except Exception as e:
        print(f"Failed to check for spam: {e}")

def delete_email(domain):
    next_page_token = None
    deleted_emails = 0
    total_emails = 0
    try:
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
    except Exception as e:
        print(f"Failed to delete emails: {e}")

if __name__ == '__main__':
    try:
        get_email_content()
    except Exception as e:
        print(f"Failed to execute main function: {e}")
