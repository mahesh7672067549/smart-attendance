import sqlite3
import json
from pathlib import Path

DB_NAME = Path(__file__).resolve().parent / 'attendance.db'


def init_db():
    conn = sqlite3.connect(str(DB_NAME))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Students (
        student_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        face_encoding TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Attendance_Sessions (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_name TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        faculty_id TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Attendance_Logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        student_id TEXT,
        status TEXT CHECK(status IN ('Present','Absent')),
        FOREIGN KEY(session_id) REFERENCES Attendance_Sessions(session_id),
        FOREIGN KEY(student_id) REFERENCES Students(student_id)
    )''')
    conn.commit()
    conn.close()


def save_student(student_id, name, encoding):
    conn = sqlite3.connect(str(DB_NAME))
    c = conn.cursor()
    c.execute(
        "INSERT OR REPLACE INTO Students (student_id, full_name, face_encoding) VALUES (?, ?, ?)",
        (student_id, name, json.dumps(encoding))
    )
    conn.commit()
    conn.close()


def get_all_students():
    conn = sqlite3.connect(str(DB_NAME))
    c = conn.cursor()
    c.execute("SELECT student_id, full_name, face_encoding FROM Students")
    rows = c.fetchall()
    conn.close()
    return [(r[0], r[1], json.loads(r[2])) for r in rows]


def create_session(class_name, faculty_id):
    conn = sqlite3.connect(str(DB_NAME))
    c = conn.cursor()
    c.execute(
        "INSERT INTO Attendance_Sessions (class_name, faculty_id) VALUES (?, ?)",
        (class_name, faculty_id)
    )
    session_id = c.lastrowid
    conn.commit()
    conn.close()
    return session_id


def log_attendance(session_id, student_id, status):
    conn = sqlite3.connect(str(DB_NAME))
    c = conn.cursor()
    c.execute(
        "INSERT INTO Attendance_Logs (session_id, student_id, status) VALUES (?, ?, ?)",
        (session_id, student_id, status)
    )
    conn.commit()
    conn.close()
