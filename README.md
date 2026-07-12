# Attendance Engine

A simple offline-friendly face attendance web app built with Flask, OpenCV, and face_recognition.

## Features
- Register students with their face image
- Capture attendance from a photo
- Store attendance sessions and logs locally in SQLite
- Export attendance results to CSV

## Requirements
- Python 3.11
- Windows-compatible virtual environment

## Setup
1. Open PowerShell in the project folder.
2. Create and activate a virtual environment:
   ```powershell
   py -3.11 -m venv attendance-engine\.venv
   .\attendance-engine\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r attendance-engine\requirements.txt
   ```
4. Run the app:
   ```powershell
   python attendance-engine\app.py
   ```

## Access
After starting the app, open:
- http://127.0.0.1:5000
- or the machine's local network IP on port 5000

## Notes
- This app is intended for local/offline use.
- Face recognition depends on the face-recognition model files and may require a compatible Python environment.
- Attendance data is stored locally in the project folder as SQLite database files and CSV exports.
