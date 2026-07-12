import csv
from datetime import datetime
from pathlib import Path

EXPORT_DIR = Path(__file__).resolve().parent / 'exports'
EXPORT_DIR.mkdir(exist_ok=True)


def export_attendance_session(session_id, class_name, faculty_id, present_list, absent_list):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = EXPORT_DIR / f'attendance_{timestamp}_session_{session_id}.csv'

    rows = []
    for entry in present_list:
        rows.append({
            'session_id': session_id,
            'class_name': class_name,
            'faculty_id': faculty_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'student_id': entry['student_id'],
            'name': entry['name'],
            'status': 'Present'
        })

    for entry in absent_list:
        rows.append({
            'session_id': session_id,
            'class_name': class_name,
            'faculty_id': faculty_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'student_id': entry['student_id'],
            'name': entry['name'],
            'status': 'Absent'
        })

    with filename.open('w', newline='', encoding='utf-8') as fh:
        writer = csv.DictWriter(fh, fieldnames=['session_id', 'class_name', 'faculty_id', 'timestamp', 'student_id', 'name', 'status'])
        writer.writeheader()
        writer.writerows(rows)

    return str(filename)
