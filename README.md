# Run this project

## 1. Open a terminal in the project folder

```powershell
cd <project-folder>
```

## 2. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## 4. Run the full automation

```powershell
.\scripts\main.bat
```

This will run both scripts:

- `scripts/test_pyautogui.py` -> extracts Gmail emails into PostgreSQL
- `scripts/quickstart.py` -> creates Google Calendar events from the saved emails

## 5. If you want to run them manually

```powershell
python .\scripts\test_pyautogui.py
python .\scripts\quickstart.py
```

## Note

Before running, make sure:

- PostgreSQL is running
- `.env` values are correct
- Google OAuth credentials are set up in `secrets/credentials.json`
- Chrome is installed and the Gmail profile is available
