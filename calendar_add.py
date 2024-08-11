from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_1.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def add_event_to_calendar(service, date, summary='Event'):
    event = {
        'summary': summary,
        'start': {
            'dateTime': date.isoformat(),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (date + datetime.timedelta(hours=1)).isoformat(),
            'timeZone': 'UTC',
        },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

def main():
    creds = authenticate_google()
    service = build('calendar', 'v3', credentials=creds)

    # Example date (replace with actual dates you want to add)
    date = datetime.datetime(2023, 8, 15, 9, 0)
    add_event_to_calendar(service, date)

if __name__ == '__main__':
    main()