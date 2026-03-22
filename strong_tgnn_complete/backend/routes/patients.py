from fastapi import APIRouter, Form, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.patient_model import Patient

router = APIRouter()


@router.post('/create')
async def create_or_update_patient(request: Request, patient_id: str = Form(None),
                                   name: str = Form(''),
                                   age: int = Form(None),
                                   sex: str = Form(None),
                                   db: Session = Depends(get_db)):
    """Create or update a patient. Accepts form data or JSON body.

    JSON example: {"patient_id":"P-001","name":"Test","age":30,"sex":"M"}
    """
    # If patient_id not provided via Form, try JSON body
    if not patient_id:
        try:
            body = await request.json()
            if isinstance(body, dict):
                patient_id = body.get('patient_id')
                name = body.get('name', name)
                age = body.get('age', age)
                sex = body.get('sex', sex)
        except Exception:
            # Not JSON or empty body; try form parsing (already covered by Form)
            try:
                form = await request.form()
                patient_id = patient_id or form.get('patient_id')
            except Exception:
                patient_id = patient_id

    if not patient_id:
        raise HTTPException(status_code=400, detail='patient_id is required')

    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if patient:
        patient.name = name; patient.age = age; patient.sex = sex
    else:
        patient = Patient(patient_id=patient_id, name=name, age=age, sex=sex)
        db.add(patient)
    db.commit(); db.refresh(patient)
    return {'message': 'Patient created/updated', 'data': patient.to_dict()}
@router.get('/{patient_id}')
async def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient: raise HTTPException(status_code=404, detail='Patient not found')
    return patient.to_dict()