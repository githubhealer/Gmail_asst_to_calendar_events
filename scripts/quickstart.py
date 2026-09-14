import os

import psycopg
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Load environment variables from .env
load_dotenv()


# PostgreSQL configuration
hostname = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
pwd = os.getenv("DB_PASSWORD")
port_id = int(os.getenv("DB_PORT"))


# Google configuration
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")
GOOGLE_TOKEN_FILE = os.getenv("GOOGLE_TOKEN_FILE")


# Google Calendar API scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    """Create Google Calendar events from emails stored in PostgreSQL."""

    creds = None

    # token.json stores the user's access and refresh tokens.
    if os.path.exists(GOOGLE_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            GOOGLE_TOKEN_FILE,
            SCOPES
        )

    # If there are no valid credentials, authorize the user.
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_CREDENTIALS_FILE,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save the credentials for future runs.
        with open(GOOGLE_TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    try:
        service = build(
            "calendar",
            "v3",
            credentials=creds
        )

        conn = None
        cur = None

        try:
            # Connect to PostgreSQL
            conn = psycopg.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id
            )

            cur = conn.cursor()

            # Get all emails from the database
            select_script = "SELECT * FROM emails"

            cur.execute(select_script)

            events = cur.fetchall()

            print("Events:", events)

            created_event = None

            # Process each email
            for event in events:

                email_id = event[5]
                subject = event[0]
                event_date = event[3]
                information = event[4]

                # Check whether this email already has a calendar event
                cur.execute(
                    """
                    SELECT *
                    FROM calendar_events
                    WHERE email_id = %s
                    """,
                    (email_id,)
                )

                existing_event = cur.fetchone()

                if existing_event:
                    print("Already present:", subject)
                    continue

                # Create Google Calendar event
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
                    calendarId="primary",
                    body=calendar_event
                ).execute()

                # Store Google Calendar event ID in database
                insert_script = """
                    INSERT INTO calendar_events (
                        email_id,
                        calendar_event_id
                    )
                    VALUES (%s, %s)
                """

                calendar_event_id = created_event["id"]

                cur.execute(
                    insert_script,
                    (email_id, calendar_event_id)
                )

                conn.commit()

            if created_event:
                print(
                    "Event created:",
                    created_event.get("htmlLink")
                )

        except Exception as e:
            print("Database error:", e)

        finally:
            if cur:
                cur.close()

            if conn:
                conn.close()

    except HttpError as error:
        print(f"Google Calendar API error: {error}")


if __name__ == "__main__":
    main()