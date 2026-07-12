import base64

try:
    import numpy as np
except ImportError:  # pragma: no cover - runtime fallback
    np = None

try:
    import cv2
except ImportError:  # pragma: no cover - runtime fallback
    cv2 = None

try:
    import face_recognition
except BaseException:  # pragma: no cover - runtime fallback
    face_recognition = None


def _ensure_dependencies():
    missing = []
    if np is None:
        missing.append('numpy')
    if cv2 is None:
        missing.append('opencv-python')
    if face_recognition is None:
        missing.append('face-recognition')

    if missing:
        raise RuntimeError(
            'Face recognition dependencies are not available. Install them into the project environment with: '
            'C:/Users/91767/OneDrive/Desktop/sa/attendance-engine/.venv/Scripts/python.exe -m pip install -r '
            'C:/Users/91767/OneDrive/Desktop/sa/attendance-engine/requirements.txt'
        )

    return cv2, face_recognition, np


def decode_base64_image(base64_str):
    """Convert a data:image/jpeg;base64,... string into an OpenCV BGR image."""
    cv2, _, np = _ensure_dependencies()
    img_data = base64.b64decode(base64_str.split(',')[1])
    np_arr = np.frombuffer(img_data, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


def get_face_encoding(image):
    """Return the 128-D encoding for the first face found in the image, or None."""
    cv2, face_recognition, _ = _ensure_dependencies()
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_image)
    if len(encodings) == 0:
        return None
    return encodings[0].tolist()


def match_faces(image, known_students, tolerance=0.6):
    """
    Compare every face found in `image` against known_students.
    known_students: list of (student_id, name, encoding_list)
    Returns (present_ids, absent_ids)
    """
    cv2, face_recognition, np = _ensure_dependencies()
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    known_encodings = [np.array(s[2]) for s in known_students]
    known_ids = [s[0] for s in known_students]

    present_ids = set()
    for encoding in face_encodings:
        if len(known_encodings) == 0:
            break
        distances = face_recognition.face_distance(known_encodings, encoding)
        best_match_idx = int(np.argmin(distances))
        if distances[best_match_idx] < tolerance:
            present_ids.add(known_ids[best_match_idx])

    all_ids = set(known_ids)
    absent_ids = all_ids - present_ids
    return list(present_ids), list(absent_ids)
