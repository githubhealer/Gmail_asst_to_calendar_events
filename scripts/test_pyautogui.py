import os
import time
import subprocess
import re

import pyautogui
import pyperclip
import psycopg
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# PostgreSQL configuration
hostname = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
pwd = os.getenv("DB_PASSWORD")
port_id = int(os.getenv("DB_PORT"))


# Chrome configuration
chrome_user_data_dir = os.getenv("CHROME_USER_DATA_DIR")
chrome_profile_directory = os.getenv("CHROME_PROFILE_DIRECTORY")
remote_debugging_port = os.getenv("CHROME_REMOTE_DEBUGGING_PORT")
gmail_url = os.getenv("GMAIL_URL")


# Image paths
gmail_img = os.getenv("GMAIL_LOGO_IMAGE")
ai_panel_img = os.getenv("AI_PANEL_IMAGE")
gemini_icon = os.getenv("GEMINI_ICON_IMAGE")
ai_textbox = os.getenv("AI_TEXTBOX_IMAGE")
arrow_img = os.getenv("ARROW_IMAGE")
dots = os.getenv("DOTS_IMAGE")
copy_img = os.getenv("COPY_IMAGE")
screenshot_file = os.getenv("SCREENSHOT_FILE")


try:
    time.sleep(1)

    # Start Chrome with the required profile
    cmd = (
        f'start chrome.exe '
        f'--user-data-dir="{chrome_user_data_dir}" '
        f'--profile-directory="{chrome_profile_directory}" '
        f'--remote-debugging-port={remote_debugging_port} '
        f'"{gmail_url}"'
    )

    subprocess.Popen(cmd, shell=True)

    # Wait for Gmail to load
    loaded = False

    while not loaded:
        try:
            anchor = pyautogui.locateOnScreen(
                gmail_img,
                confidence=0.8
            )

            if anchor:
                print("Loaded Gmail")
                loaded = True
            else:
                time.sleep(1)

        except Exception as e:
            print(e)

    time.sleep(2)

    try:
        # Try to find the AI panel
        try:
            aipanel = pyautogui.locateCenterOnScreen(
                ai_panel_img,
                confidence=0.75
            )

        except Exception:
            print("AI panel not found. Triggering fallback click.")
            aipanel = None

        # Locate Gemini icon
        location_gemini_icon = pyautogui.locateCenterOnScreen(
            gemini_icon,
            confidence=0.8
        )

        # Open AI panel if necessary
        if not aipanel:

            pyautogui.click(location_gemini_icon)

            loaded = False
            start = time.time()

            while not loaded:

                end = time.time()

                if end - start >= 1:
                    pyautogui.click(location_gemini_icon)
                    start = time.time()

                try:
                    anchor = pyautogui.locateOnScreen(
                        ai_panel_img,
                        confidence=0.8
                    )

                    if anchor:
                        print("Loaded AI panel")
                        loaded = True
                    else:
                        time.sleep(1)

                except Exception as e:
                    print(e)

        # Locate AI textbox
        try:
            location_ai_textbox = pyautogui.locateCenterOnScreen(
                ai_textbox,
                confidence=0.8
            )

            region = pyautogui.locateOnScreen(
                ai_panel_img,
                confidence=0.8
            )

            print("Region:", region)

            pyautogui.click(location_ai_textbox)

            prompt = (
                "Retrieve today's emails only. "
                "For every relevant email, output exactly ONE line "
                "in this exact format: "
                "SUBJECT: <subject> "
                "SENDER: <sender> "
                "RECEIVED_DATETIME: <received datetime> "
                "ACTIVITY_DATE: <deadline of completion of the task "
                "present in the mail's content. or if not present "
                "type just NONE> "
                "INFORMATION: <information>. "
                "Output ONLY the email lines. "
                "Do NOT use bullet points, numbering, markdown, headings, "
                "code blocks, explanations, or blank lines. "
                "Do NOT change, reorder, or rename the five field names. "
                "Each email must be exactly one line."
            )

            pyautogui.write(prompt)
            pyautogui.press("Enter")

            # Wait for Gemini response
            loaded = False

            while not loaded:
                try:
                    location_arrow_img = pyautogui.locateCenterOnScreen(
                        arrow_img,
                        confidence=0.9
                    )

                    loaded = True

                except Exception:
                    time.sleep(1)

            # Move inside AI panel
            pyautogui.moveTo(
                region.left + region.width // 2,
                region.top + region.height // 2
            )

            # Find three-dot menu
            loaded = False

            while not loaded:

                region_tuple = (
                    int(region.left),
                    int(region.top),
                    int(region.width),
                    int(region.height)
                )

                try:
                    location_3_dots = (
                        pyautogui.locateCenterOnScreen(
                            dots,
                            confidence=0.9,
                            region=region_tuple
                        )
                    )

                    loaded = True

                except Exception:
                    print("Scrolling...")
                    pyautogui.scroll(-500)
                    time.sleep(1)

            print("Executed")

            if location_3_dots:
                pyautogui.click(location_3_dots)
            else:
                time.sleep(1)

            # Find and click Copy
            loaded = False

            while not loaded:

                try:
                    location_copy = (
                        pyautogui.locateCenterOnScreen(
                            copy_img,
                            confidence=0.9
                        )
                    )

                    pyautogui.click(location_copy)

                    loaded = True

                except Exception:
                    time.sleep(0.01)

            time.sleep(1)

            # Get copied Gemini response
            response = pyperclip.paste()

            print("\nGemini Response:")
            print(response)

            # Parse Gemini response
            blocks = re.split(
                r"(?=SUBJECT:)",
                response.strip()
            )

            subjects = []
            senders = []
            dates = []
            activity_dates = []
            information = []

            for block in blocks:

                subject = re.search(
                    r"SUBJECT:\s*(.*?)\s+SENDER:",
                    block
                )

                sender = re.search(
                    r"SENDER:\s*(.*?)\s+RECEIVED_DATETIME:",
                    block
                )

                date = re.search(
                    r"RECEIVED_DATETIME:\s*(.*?)\s+ACTIVITY_DATE:",
                    block
                )

                activity_date = re.search(
                    r"ACTIVITY_DATE:\s*(.*?)\s+INFORMATION:",
                    block
                )

                info = re.search(
                    r"INFORMATION:\s*(.*)",
                    block
                )

                if (
                    subject
                    and sender
                    and date
                    and activity_date
                    and info
                ):

                    subjects.append(
                        subject.group(1).strip()
                    )

                    senders.append(
                        sender.group(1).strip()
                    )

                    dates.append(
                        date.group(1).strip()
                    )

                    activity = activity_date.group(1).strip()

                    if activity == "NONE":
                        activity = dates[-1]

                    activity_dates.append(activity)

                    information.append(
                        info.group(1).strip()
                    )

            # Display parsed results
            print("\nParsed Results:")
            print("Subjects:", subjects)
            print("Senders:", senders)
            print("Dates:", dates)
            print("Activity Dates:", activity_dates)
            print("Information:", information)

            print(
                "\nNumber of emails:",
                len(subjects)
            )

            # Connect to PostgreSQL
            conn = None
            cur = None

            try:
                conn = psycopg.connect(
                    host=hostname,
                    dbname=database,
                    user=username,
                    password=pwd,
                    port=port_id
                )

                cur = conn.cursor()

                # Insert emails into database
                for i in range(len(subjects)):

                    cur.execute(
                        """
                        INSERT INTO emails (
                            subject,
                            sender,
                            received_datetime,
                            activity_date,
                            information
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (
                            subject,
                            sender,
                            received_datetime
                        )
                        DO NOTHING
                        """,
                        (
                            subjects[i],
                            senders[i],
                            dates[i],
                            activity_dates[i],
                            information[i]
                        )
                    )

                conn.commit()

                print("Emails inserted into database.")

            except Exception as e:
                print("Database error:", e)

            finally:
                if cur:
                    cur.close()

                if conn:
                    conn.close()

        except Exception as e:
            print("Fallback:", repr(e))

        # Take screenshot
        pyautogui.screenshot(screenshot_file)

    except Exception as e:
        print(e)

except Exception as e:
    print(e)