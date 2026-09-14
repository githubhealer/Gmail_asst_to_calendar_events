import pyautogui
import pyperclip
import subprocess
import time
import re
import psycopg

# Open Chrome with your Gmail profile
cmd = 'start chrome.exe --user-data-dir="C:\\Users\\sande\\AppData\\Local\\Google\\Chrome\\User Data" --profile-directory="Profile 16" --remote-debugging-port=9222 "https://mail.google.com/mail/u/0/#inbox"'
subprocess.Popen(cmd, shell=True)

try:

    # Wait for Gmail to load
    gmail_img = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\gmail_logo.png"

    anchor = None

    for _ in range(30):
        anchor = pyautogui.locateOnScreen(
            gmail_img,
            confidence=0.8
        )

        if anchor:
            print("Gmail loaded")
            break

        time.sleep(1)

    if not anchor:
        print("Gmail not detected")
        raise Exception("Gmail did not load")

    # Find Gemini panel
    ai_panel_img = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\ai_panel.png"

    region = None

    for _ in range(30):
        region = pyautogui.locateOnScreen(
            ai_panel_img,
            confidence=0.8
        )

        if region:
            print("AI panel found:", region)
            break

        time.sleep(1)

    if not region:
        print("AI panel not found")
        raise Exception("AI panel not found")

    region_tuple = (
        int(region.left),
        int(region.top),
        int(region.width),
        int(region.height)
    )

    # Companies you have applied to
    companies = ["Ethos"]

    prompt = (
        f"I have applied to these companies: {companies}. "
        "Retrieve today's placement-related emails only. "
        "For every relevant email, output exactly ONE line in this exact format: "
        "SUBJECT: <subject> SENDER: <sender> RECEIVED_DATETIME: <received datetime> "
        "ACTIVITY_DATE: <activity date or NONE> INFORMATION: <information>. "
        "Output ONLY the email lines. "
        "Do NOT use bullet points, numbering, markdown, headings, code blocks, "
        "explanations, or blank lines. "
        "Do NOT change, reorder, or rename the five field names. "
        "Each email must be exactly one line."
    )

    # Click Gemini input area
    pyautogui.click(
        region.left + region.width // 2,
        region.top + region.height - 80
    )

    pyautogui.write(
        prompt,
        interval=0.001
    )

    pyautogui.press("enter")

    # Wait for Gemini response
    time.sleep(15)

    # Scroll Gemini panel to bottom
    pyautogui.moveTo(
        region.left + region.width // 2,
        region.top + region.height // 2
    )

    pyautogui.scroll(-500)

    time.sleep(2)

    # Find three dots
    dots = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\three_dots.png"

    location_3_dots = pyautogui.locateCenterOnScreen(
        dots,
        confidence=0.9,
        region=region_tuple
    )

    if location_3_dots:
        pyautogui.click(location_3_dots)
        time.sleep(1)

        # Click copy option
        copy_img = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\copy.png"

        copy_location = pyautogui.locateCenterOnScreen(
            copy_img,
            confidence=0.9
        )

        if copy_location:
            pyautogui.click(copy_location)

            time.sleep(1)

            response = pyperclip.paste()

            print(response)

            # -------------------------
            # PARSING
            # -------------------------

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
                    r"SENDER:\s*(.*?)\s+RECEIVED\\_DATETIME:",
                    block
                )

                date = re.search(
                    r"RECEIVED\\_DATETIME:\s*(.*?)\s+ACTIVITY\\_DATE:",
                    block
                )

                activity_date = re.search(
                    r"ACTIVITY\\_DATE:\s*(.*?)\s+INFORMATION:",
                    block
                )

                info = re.search(
                    r"INFORMATION:\s*(.*)",
                    block
                )

                if subject and sender and date and activity_date and info:

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

            print(subjects)
            print(senders)
            print(dates)
            print(activity_dates)
            print(information)

            # -------------------------
            # POSTGRESQL
            # -------------------------

            hostname = "localhost"
            database = "placement_mail"
            username = "postgres"
            pwd = "gmail"
            port_id = 5432

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

                for i in range(len(subjects)):

                    cur.execute("""
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
                    """, (
                        subjects[i],
                        senders[i],
                        dates[i],
                        activity_dates[i],
                        information[i],
                    ))

                conn.commit()

            except Exception as e:
                print(e)

            finally:

                if cur:
                    cur.close()

                if conn:
                    conn.close()

    else:
        print("Three dots not found")

except Exception as e:
    print("Fallback:", repr(e))
