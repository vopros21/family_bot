from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def authorization():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def get_next_event():
    creds = authorization()
    try:
        service = build('calendar', 'v3', credentials=creds)
        now_1hour = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        timepoint = now_1hour.isoformat() + 'Z'
        print('Getting the next event')
        events = service.events().list(calendarId='primary', timeMin=timepoint,
                                       maxResults=1, singleEvents=True).execute()
        next_event = events.get('items', [])

        if not next_event:
            print('No upcoming events found.')
            return
        start = next_event[0]['start'].get('dateTime', next_event[0]['start'].get('date'))
        return start, next_event[0]['summary']
    except HttpError as error:
        print('An error occurred: %s' % error)


def main():
    creds = authorization()

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=15, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    # main()
    print(get_next_event())
