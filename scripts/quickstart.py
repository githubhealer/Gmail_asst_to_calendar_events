import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "secrets/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    events = [
        {
            'summary': 'Capgemini Placement Drive',
            'location': 'VIT Chennai Campus',
            'description': 'Attend the Capgemini Super Dream placement drive.',
            'start': {
                'dateTime': '2026-09-10T09:00:00+05:30',
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': '2026-09-10T17:00:00+05:30',
                'timeZone': 'Asia/Kolkata',
            },
        },
        {
            'summary': 'E-Con Systems Selection Process',
            'location': 'VIT Chennai Campus',
            'description': 'Attend the next round of the E-Con Systems selection process.',
            'start': {
                'dateTime': '2026-09-11T08:30:00+05:30',
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': '2026-09-11T13:00:00+05:30',
                'timeZone': 'Asia/Kolkata',
            },
        },
        {
            'summary': 'American Express Placement Activity',
            'location': 'VIT Chennai Campus',
            'description': 'American Express Super Dream internship/placement activity.',
            'start': {
                'dateTime': '2026-09-12T10:00:00+05:30',
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': '2026-09-12T12:00:00+05:30',
                'timeZone': 'Asia/Kolkata',
            },
        }
    ]

    for event in events:
      created_event = service.events().insert(
          calendarId='primary',
          body=event
      ).execute()

    print('Event created:', created_event.get('htmlLink'))

  #   print("Getting the upcoming 10 events")
  #   events_result = (
  #       service.events()
  #       .list(
  #           calendarId="primary",
  #           timeMin=now,
  #           maxResults=10,
  #           singleEvents=True,
  #           orderBy="startTime",
  #       )
  #       .execute()
  #   )
  #   events = events_result.get("items", [])

  #   if not events:
  #     print("No upcoming events found.")
  #     return

  #   # Prints the start and name of the next 10 events
  #   for event in events:
  #     start = event["start"].get("dateTime", event["start"].get("date"))
  #     print(start, event["summary"])

  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()