'''

From google quickstart

Oh my god.


Need an audio recording software.
will figure that out soon


Open AI Whisper is open source!
Will probably use the smallest model to transcribe

I'm pretty sure the database will be google calendar,
no need to handle database here

Yeah, let's do it

ASK CHAT!


FUTURE GOALS:
    work with differetn calendars, google calendar can overlay diff calendars
    adjust time zones, make it accessible to more


'''

import datetime
import os.path
import json
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google import genai
from geminitoken import TOKEN

client = genai.Client(api_key=TOKEN)


def generate(prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=['I will give you a prompt. Generate a json in this format'
                                            '"summary": "event summary",'
                                            '"location": "location, empty if none specified"'
                                            '"description": "description, empty if none specified"'
                                            '"start": "time"'
                                            '"end": "time"'
                                            ,prompt]
                            )
    return response

'''
Google Calendar Permission Scopes

Useful Scopes
calendar.freebusy - availability
calendar.events   - view/edit events
I think that's all we need
more @ https://developers.google.com/workspace/calendar/api/auth

'''
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # WE DON"T NEED THIS ANYMORE
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()

        with open('ExPrompt.txt', 'r') as f:
            text = f.readline()
        print(text)

        # a = generate(text)
        # print(a)
        # print(type(a))
        # print(a.text)

        # 1. Extract the JSON block using regex
        match = re.search(r'```json\s*(\{.*?\})\s*```', generate(text).text, re.DOTALL)
        if match:
            json_str = match.group(1)
            json_obj = json.loads(json_str)
            
            # 2. Convert the string to a Python dictionary
            
            print("Extracted JSON data:")
            with open("event.json", 'w') as f:
               json.dump(json_obj, f, indent = 2)
        else:
            print("No JSON found.")

        # Open and read the JSON file
        with open('BareEvent.json', 'r') as file:
            data = json.load(file)

        # Print the data
        print(data)
        if not data:
           raise NameError("File not found or file is empty")

        service.events().insert(calendarId='primary', body=data).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")
    except NameError:
        print(f"An error occured {error}")


if __name__ == "__main__":
    main()


