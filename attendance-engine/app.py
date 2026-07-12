import os
from pathlib import Path

from flask import Flask, render_template, request, jsonify

try:
    from .database import (
        init_db, save_student, get_all_students,
        create_session, log_attendance
    )
    from .face_engine import decode_base64_image, get_face_encoding, match_faces
    from .attendance_export import export_attendance_session
except ImportError:  # pragma: no cover - supports running the module directly
    from database import (
        init_db, save_student, get_all_students,
        create_session, log_attendance
    )
    from face_engine import decode_base64_image, get_face_encoding, match_faces
    from attendance_export import export_attendance_session

BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__, template_folder=str(BASE_DIR / 'templates'), static_folder=str(BASE_DIR / 'static'))
init_db()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register')
def register_page():
    return render_template('register.html')


@app.route('/attendance')
def attendance_page():
    return render_template('attendance.html')


@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    student_id = data.get('student_id')
    name = data.get('name')
    image_b64 = data.get('image')

    if not student_id or not name or not image_b64:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400

    try:
        image = decode_base64_image(image_b64)
        encoding = get_face_encoding(image)
    except RuntimeError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 503

    if encoding is None:
        return jsonify({'success': False, 'message': 'No face detected. Try better lighting.'})

    save_student(student_id, name, encoding)
    return jsonify({'success': True, 'message': f'{name} registered successfully.'})


@app.route('/api/process_attendance', methods=['POST'])
def api_process_attendance():
    data = request.json
    image_b64 = data.get('image')
    class_name = data.get('class_name', 'Unnamed Class')
    faculty_id = data.get('faculty_id', 'unknown')
    tolerance = float(data.get('tolerance', 0.6))

    if not image_b64:
        return jsonify({'success': False, 'message': 'No image provided'}), 400

    try:
        image = decode_base64_image(image_b64)
        students = get_all_students()

        if len(students) == 0:
            return jsonify({'success': False, 'message': 'No students registered yet.'})

        present_ids, absent_ids = match_faces(image, students, tolerance=tolerance)
    except RuntimeError as exc:
        return jsonify({'success': False, 'message': str(exc)}), 503

    id_to_name = {s[0]: s[1] for s in students}
    present_list = [{'student_id': sid, 'name': id_to_name[sid]} for sid in present_ids]
    absent_list = [{'student_id': sid, 'name': id_to_name[sid]} for sid in absent_ids]

    session_id = create_session(class_name, faculty_id)
    for sid in present_ids:
        log_attendance(session_id, sid, 'Present')
    for sid in absent_ids:
        log_attendance(session_id, sid, 'Absent')

    csv_path = export_attendance_session(session_id, class_name, faculty_id, present_list, absent_list)

    return jsonify({
        'success': True,
        'session_id': session_id,
        'present': present_list,
        'absent': absent_list,
        'csv_path': csv_path
    })


if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '5000'))
    app.run(debug=False, host=host, port=port)
