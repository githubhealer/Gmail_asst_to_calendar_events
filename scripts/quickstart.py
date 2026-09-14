import datetime
import os.path
import psycopg

hostname = "localhost"
database = "placement_mail"
username = "postgres"
pwd = "gmail"
port_id = 5432
conn = None
cur = None

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
    try:
        conn = psycopg.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id
              )
        
        cur = conn.cursor()

        events = []
        select_script = """SELECT * FROM emails"""
        cur.execute(select_script)
        events = cur.fetchall()
        print("Events: ",events)
        created_event = None
        for event in events:
            email_id = event[5]
            subject = event[0]
            event_date = event[3]
            information = event[4]
            cur.execute("""
            SELECT * FROM calendar_events WHERE email_id = %s
            """,(email_id,))
            existing_event = cur.fetchone()
            if existing_event:
              print("Already present: ",subject)
              continue
            calendar_event = {
                "summary": subject,
                "description": information,
                "start": {
                    "date": event_date.date().isoformat()
                },
                "end": {
                    "date": event_date.date().isoformat()
                }
            }
            created_event = service.events().insert(
                calendarId='primary',
                body=calendar_event
            ).execute()
            insert_script = """
                            INSERT INTO calendar_events (email_id, calendar_event_id)
                            VALUES (%s,%s)
                            """
            calendar_event_id = created_event['id']
            cur.execute(insert_script,(email_id,calendar_event_id))
            conn.commit()
        if created_event:
          print('Event created:', created_event.get('htmlLink'))
    except Exception as e:
      print(e)
    finally:
      cur.close()
      conn.close()
  except HttpError as error:
    print(f"An error occurred: {error}")


if __name__ == "__main__":
  main()