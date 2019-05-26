# pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib oauth2client httplib2
# python3 add_event.py --noauth_local_webserver

# Reference: https://developers.google.com/calendar/quickstart/python
# Documentation: https://developers.google.com/calendar/overview

# Be sure to enable the Google Calendar API on your Google account by following the reference link above and
# download the credentials.json file and place it in the same directory as this file.

from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools




class createGoogleEvent:


    # If modifying these scopes, delete the file token.json.
    SCOPES = "https://www.googleapis.com/auth/calendar"
    store = file.Storage("token.json")
    creds = store.get()
    service = None


    def __init__(self):
        if(not self.creds or self.creds.invalid):
            flow = client.flow_from_clientsecrets("credentials.json", self.SCOPES)
            self.creds = tools.run_flow(flow, store)
        self.service = build("calendar", "v3", http=self.creds.authorize(Http()))


    def insert(self, username, returnDate, bookName):
        eventDate = returnDate.strftime("%Y-%m-%d")
        time_start = "{}T06:00:00+10:00".format(eventDate)
        time_end = "{}T07:00:00+10:00".format(eventDate)
        eventDetails = {'user': username, 'book': bookName}
        event = {
            "summary": "A book has been borrowed",
            "location": "RMIT Building 14",
            "description": '{user} has borrowed {book}'.format_map(eventDetails),
            "start": {
                "dateTime": time_start,
                "timeZone": "Australia/Melbourne",
            },
            "end": {
                "dateTime": time_end,
                "timeZone": "Australia/Melbourne",
            },
            "attendees": [
                {"email": "{}@gmail.you".format(username)},
            ],

        }

        event = self.service.events().insert(calendarId="primary", body=event).execute()
        print("Event created")

