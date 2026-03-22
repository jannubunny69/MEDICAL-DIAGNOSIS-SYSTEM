import os
from fastapi import UploadFile
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'uploads')
def save_uploaded_file(patient_id: str, visit_id: str, file: UploadFile) -> str:
    patient_dir = os.path.join(UPLOAD_DIR, patient_id, visit_id)
    os.makedirs(patient_dir, exist_ok=True)
    file_path = os.path.join(patient_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return file_path