from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PROJECT_DIR = ROOT / 'attendance-engine'
VENV_PYTHON = PROJECT_DIR / '.venv' / 'Scripts' / 'python.exe'
APP_ENTRY = PROJECT_DIR / 'app.py'


def _python_has_dependencies(python_exe):
    command = [str(python_exe), '-c', 'import flask, cv2, numpy, face_recognition']
    result = subprocess.run(command, cwd=str(PROJECT_DIR), capture_output=True, text=True)
    return result.returncode == 0


if __name__ == '__main__':
    candidates = []
    if sys.executable:
        candidates.append(Path(sys.executable))
    if VENV_PYTHON.exists():
        candidates.append(VENV_PYTHON)

    python_exe = None
    for candidate in candidates:
        if candidate and _python_has_dependencies(candidate):
            python_exe = candidate
            break

    if python_exe is None:
        if VENV_PYTHON.exists():
            python_exe = VENV_PYTHON
        else:
            print(f'Project virtual environment not found at: {VENV_PYTHON}')
            sys.exit(1)

    subprocess.run([str(python_exe), str(APP_ENTRY)], cwd=str(PROJECT_DIR), check=False)
