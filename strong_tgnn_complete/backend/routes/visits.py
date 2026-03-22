from fastapi import APIRouter, UploadFile, Form, Depends, File, HTTPException
from typing import List
from sqlalchemy.orm import Session
import json, os
from ..models.database import get_db
from ..models.visit_model import Visit
from ..models.patient_model import Patient
from ..utils.file_manager import save_uploaded_file
router = APIRouter()
@router.post('/upload/{disease}')
async def upload_visit(disease: str,
                       patient_id: str = Form(...),
                       visit_date: str = Form(...),
                       db: Session = Depends(get_db),
                       files: List[UploadFile] = File(None)):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient: raise HTTPException(status_code=404, detail='Patient not found')
    visit_id = f"V-{visit_date}"
    stored = {}
    if files:
        for file in files:
            path = save_uploaded_file(patient_id, visit_id, file)
            stored[file.filename] = path
    visit = Visit(patient_id=patient_id, disease=disease, visit_date=visit_date, file_paths=json.dumps(stored))
    db.add(visit); db.commit(); db.refresh(visit)
    return {'message': 'Visit uploaded', 'visit': visit.to_dict()}