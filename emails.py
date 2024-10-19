from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_gmail(cred_file, token_file):
    creds = None
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # save credentials
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)
    print(f"Authorized scopes: {creds.scopes}")
    return build('gmail', 'v1', credentials=creds)

def delete_old_unread_emails(service, days=90):
    date_cutoff = datetime.now() - timedelta(days=90)
    query = f"before:{date_cutoff.strftime('%Y/%m/%d')} is:unread"
    
    deleted_count = 0
    next_page_token = None
    
    while True:
        results = service.users().messages().list(userId='me', q=query, pageToken=next_page_token).execute()
        messages = results.get('messages', [])

        if not messages:
            break

        for msg in messages:
            service.users().messages().trash(userId='me', id=msg['id']).execute() # move email to trash
            print(f'Deleted message with ID: {msg["id"]}')
            deleted_count += 1

        next_page_token = results.get('nextPageToken')
        if not next_page_token:
            break

    print(f"Total unread emails older than 90 days moved to trash: {deleted_count}")
    return deleted_count


def delete_old_promotions_or_social(service, category, days=30):
    date_cutoff = datetime.now() - timedelta(days=30)
    query = f"before:{date_cutoff.strftime('%Y/%m/%d')} is:unread category:{category}"
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    deleted_count = 0
    if not messages:
        print(f'No old unread {category} emails found.')
    else:
        for msg in messages:
            service.users().messages().trash(userId='me', id=msg['id']).execute()
            print(f'Deleted {category} email with ID: {msg["id"]}')
            deleted_count += 1

    print(f"Total unread {category} emails older than {days} days moved to trash: {deleted_count}")
    return deleted_count

def delete_spam_emails(service):
    # find all emails in the Spam folder
    query = 'in:spam'
    
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])

    deleted_count = 0
    if not messages:
        print('No spam emails found.')
    else:
        for msg in messages:
            service.users().messages().trash(userId='me', id=msg['id']).execute()
            print(f'Deleted spam email with ID: {msg["id"]}')
            deleted_count += 1

    print(f"Total spam emails moved to trash: {deleted_count}")
    return deleted_count

if __name__ == '__main__':
    accounts = [
        {
            'cred_file': 'credentials_kearatlopez210.json',
            'token_file': 'token_kearatlopez210.pickle',
            'email': 'kearatlopez210@gmail.com'
        },
        {
            'cred_file': 'credentials_kearataylorlopez.json',
            'token_file': 'token_kearataylorlopez.pickle',
            'email': 'kearataylorlopez@gmail.com'
        }
    ]
    
    for account in accounts:
        print(f"Processing for {account['email']}...")
        service = authenticate_gmail(account['cred_file'], account['token_file'])
        
        # delete unread emails older > 90 days
        unread_deleted_count = delete_old_unread_emails(service, days=90)
        
        # delete unread promotions older > 30 days
        promotions_deleted_count = delete_old_promotions_or_social(service, category="promotions", days=30)
        
        # delete unread social emails older > 30 days
        social_deleted_count = delete_old_promotions_or_social(service, category="social", days=30)
        
        # delete all emails in the spam folder
        spam_deleted_count = delete_spam_emails(service)
        
        # print total number of emails moved to trash
        total_deleted = unread_deleted_count + promotions_deleted_count + social_deleted_count + spam_deleted_count
        print(f"Total emails moved to trash for {account['email']}: {total_deleted}")
