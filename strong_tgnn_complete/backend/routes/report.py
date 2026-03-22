from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.patient_model import Patient
from ..models.result_model import InferenceResult
import json
import io
from fastapi.responses import StreamingResponse
from reportlab.pdfgen import canvas
router = APIRouter()

@router.get('/pdf/{patient_id}')
async def generate_report(patient_id: str, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail='Patient not found')
    results = db.query(InferenceResult).filter(InferenceResult.patient_id == patient_id).all()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Patient Report: {patient_id}")
    y = 780
    for r in results:
        p.drawString(100, y, str(r.result_json))
        y -= 20
    p.showPage()
    p.save()
    buffer.seek(0)
    return StreamingResponse(buffer, media_type='application/pdf', headers={"Content-Disposition": f"attachment;filename=report_{patient_id}.pdf"})
