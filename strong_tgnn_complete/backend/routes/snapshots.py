from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.patient_model import Patient
from ..models.visit_model import Visit
from ..models.result_model import InferenceResult
import json
router = APIRouter()
@router.get('/{patient_id}')
async def get_snapshot(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient: raise HTTPException(status_code=404, detail='Patient not found')
    visits = db.query(Visit).filter(Visit.patient_id == patient_id).all()
    results = db.query(InferenceResult).filter(InferenceResult.patient_id == patient_id).all()
    return {
        'patient': patient.to_dict(),
        'visits': [v.to_dict() for v in visits],
        'inference_results': [r.to_dict() for r in results]
    }