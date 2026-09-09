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
            pyautogui.write("Return the 5 most recent emails. I will check it myself For each email use exactly this format: SUBJECT: SENDER: DATE: INFORMATION: Do not add any other text.Also dont include any escape sequence or escape character")
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
                print("Hello")
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

                subject_pattern = r"SUBJECT:\s*(.*)"
                sender_pattern = r"SENDER:\s*(.*)"
                date_pattern = r"DATE:\s*(.*)"
                information_pattern = r"INFORMATION:\s*(.*)"

                subjects = [x.replace("\\!","!").strip() for x in re.findall(subject_pattern, response)]
                senders = [x.strip() for x in re.findall(sender_pattern, response)]
                dates = [x.strip() for x in re.findall(date_pattern, response)]
                information = [x.strip() for x in re.findall(information_pattern, response)]

                print(subjects)
                print(senders)
                print(dates)
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
                                email_body,
                                received_datetime
                            )
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (subject,sender,received_datetime)
                            DO NOTHING
                        """, (
                            subjects[i],
                            senders[i],
                            information[i],
                            dates[i]
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