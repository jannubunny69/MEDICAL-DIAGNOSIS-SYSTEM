from fastapi import APIRouter, Request, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.patient_model import Patient
from ..models.result_model import InferenceResult
from ..models import tgnn, encoders
import json

router = APIRouter()

@router.post('/multi')
async def run_multidisease_inference(request: Request, patient_id: str = Form(None), db: Session = Depends(get_db)):
    """Run predictions for all supported diseases in one call."""
    if not patient_id:
        try:
            body = await request.json()
            if isinstance(body, dict):
                patient_id = body.get('patient_id')
        except Exception:
            try:
                form = await request.form()
                patient_id = patient_id or form.get('patient_id')
            except Exception:
                patient_id = patient_id
    if not patient_id:
        raise HTTPException(status_code=400, detail='patient_id is required')
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail='Patient not found')
    diseases = ['alzheimers', 'parkinsons', 'brain_tumor', 'cancer']
    results = {}
    for disease in diseases:
        # Simulate inference for each disease
        result = {'probability': 0.5, 'decision': 'Low risk'}
        results[disease] = result
    rec = InferenceResult(patient_id=patient_id, disease='multi', result_json=json.dumps(results))
    db.add(rec); db.commit(); db.refresh(rec)
    return results
