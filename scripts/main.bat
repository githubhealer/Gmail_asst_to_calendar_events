@echo off
:: Step 1: Run the PyAutoGUI test script using explicit backslashes
echo Running test_pyautogui.py...
"venv\Scripts\python.exe" "scripts\test_pyautogui.py"

echo.

:: Step 2: Run the quickstart script
echo Running quickstart.py...
"venv\Scripts\python.exe" "scripts\quickstart.py"
