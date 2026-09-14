import pyautogui
import time
import subprocess
import pyperclip

try:
    time.sleep(1)
    cmd = f'start chrome.exe --user-data-dir="C:\\Users\\sande\\AppData\\Local\\Google\\Chrome\\User Data" --profile-directory="Profile 16" --remote-debugging-port=9222 "https://mail.google.com/mail/u/0/#inbox"'
    subprocess.Popen(cmd,shell=True)
    loaded = False
    while not loaded:
        try:
            gmail_img = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\gmail_logo.png"
            anchor = pyautogui.locateOnScreen(gmail_img,confidence=0.8)
            if anchor:
                print("Loaded gmail")
                loaded = True
            else:
                time.sleep(1)
        except Exception as e:
            print(e)
    time.sleep(2)
    try:
        ai_panel_img = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\ai_panel.png"        
        try:
            aipanel = pyautogui.locateCenterOnScreen(ai_panel_img,confidence=0.75)
        except Exception as e:
            print("AI panel not found. Triggering fallback click.")
            aipanel = None
        gemini_icon = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\gemini_icon.png"
        location_gemini_icon = pyautogui.locateCenterOnScreen(gemini_icon,confidence=0.8)
        if not aipanel:
            pyautogui.click(location_gemini_icon)
            loaded = False
            ai_panel_img = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\ai_panel.png"
            start = time.time()
            while not loaded:
                end = time.time()
                if end-start >=1:
                    pyautogui.click(location_gemini_icon)
                try:
                    anchor = pyautogui.locateOnScreen(ai_panel_img,confidence=0.8)
                    if anchor:
                        print("Loaded ai panel")
                        loaded = True
                    else:
                        time.sleep(1)
                except Exception as e:
                    print(e)
        ai_textbox = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\ai_textbox.png"
        try:
            location_ai_textbox = pyautogui.locateCenterOnScreen(ai_textbox,confidence=0.8)
            region = pyautogui.locateOnScreen(ai_panel_img, confidence=0.8)
            print("Region: ",region)
            pyautogui.click(location_ai_textbox)
            companies = ["Ethos"]
            pyautogui.write("Retrieve today's emails only. For every relevant email, output exactly ONE line in this exact format: SUBJECT: <subject> SENDER: <sender> RECEIVED_DATETIME: <received datetime> ACTIVITY_DATE: <deadline of completion of the task present in the mail's content. or if not present type just NONE> INFORMATION: <information>. Output ONLY the email lines. Do NOT use bullet points, numbering, markdown, headings, code blocks, explanations, or blank lines. Do NOT change, reorder, or rename the five field names. Each email must be exactly one line.")
            pyautogui.press("Enter")
            arrow_img = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\arrow.png"
            loaded = False
            while not loaded:
                try:
                   location_arrow_img = pyautogui.locateCenterOnScreen(arrow_img,confidence=0.9)
                   loaded = True
                except Exception as e:
                    time.sleep(1)
            
            dots = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\dots.png"
            pyautogui.moveTo(region.left + region.width // 2,
                 region.top + region.height // 2)
            # print(region.left,region.width,region.top,region.height)
            # print("mouse:",pyautogui.position())
            loaded = False
            while not loaded:
                region_tuple = (
                    int(region.left),
                    int(region.top),
                    int(region.width),
                    int(region.height)
                )
                loaded = False
                while not loaded:
                    try:
                        location_3_dots = pyautogui.locateCenterOnScreen(dots,confidence=0.9,region=region_tuple)
                        loaded = True
                    except Exception as e:
                        print("Scrolling...")
                        pyautogui.scroll(-500)
                        time.sleep(1)
                print("Executed")
                if location_3_dots:
                    pyautogui.click(location_3_dots)
                    loaded = True
                else:
                    time.sleep(1)
                loaded = False
                while not loaded:
                    copy = r"D:\7th sem\project\Placement_gmails_asst\scripts\images\copy.png"
                    try:
                        location_copy = pyautogui.locateCenterOnScreen(copy,confidence=0.9)
                        pyautogui.click(location_copy)
                        loaded = True
                    except Exception as e:
                        time.sleep(0.01)
                time.sleep(1)
                response = pyperclip.paste()

                import re
                blocks = re.split(r"(?=SUBJECT:)", response.strip())

                subjects = []
                senders = []
                dates = []
                activity_dates = []
                information = []

                for block in blocks:

                    subject = re.search(r"SUBJECT:\s*(.*?)\s+SENDER:", block)
                    sender = re.search(r"SENDER:\s*(.*?)\s+RECEIVED\\_DATETIME:", block)
                    date = re.search(r"RECEIVED\\_DATETIME:\s*(.*?)\s+ACTIVITY\\_DATE:", block)
                    activity_date = re.search(r"ACTIVITY\\_DATE:\s*(.*?)\s+INFORMATION:", block)
                    info = re.search(r"INFORMATION:\s*(.*)", block)

                    if subject and sender and date and activity_date and info:

                        subjects.append(subject.group(1).strip())
                        senders.append(sender.group(1).strip())
                        dates.append(date.group(1).strip())

                        activity = activity_date.group(1).strip()

                        if activity == "NONE":
                            activity = dates[-1]

                        activity_dates.append(activity)

                        information.append(info.group(1).strip())
                print(len(subjects), len(senders), len(dates),len(activity_dates), len(information))
                print(subjects)
                print(senders)
                print(dates)
                print(activity_dates)
                print(information)
                import psycopg

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
                            ON CONFLICT (subject,sender,received_datetime)
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
        except Exception as e:
            print("Fallback: ",repr(e))
        pyautogui.screenshot("scshot.png")
    except Exception as e:
        print(e)
except Exception as e:
    print(e)