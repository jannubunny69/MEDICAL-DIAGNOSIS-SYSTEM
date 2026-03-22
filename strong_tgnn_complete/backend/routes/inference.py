from fastapi import APIRouter, Form, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import json
from ..models.database import get_db
from ..models.patient_model import Patient
from ..models.result_model import InferenceResult
from ..models import tgnn, encoders

router = APIRouter()


@router.post('/{disease}')
async def run_inference(disease: str, request: Request, patient_id: str = Form(None), visit_id: str = Form(None), db: Session = Depends(get_db)):
    """Run inference for `disease` using modality encoders and TGNN fusion.

    Accept `patient_id` via form or JSON body. Optionally `visit_id` to use specific visit metadata.
    """
    # Resolve body/form
    if not patient_id:
        try:
            body = await request.json()
            if isinstance(body, dict):
                patient_id = body.get('patient_id')
                visit_id = visit_id or body.get('visit_id')
        except Exception:
            try:
                form = await request.form()
                patient_id = patient_id or form.get('patient_id')
                visit_id = visit_id or form.get('visit_id')
            except Exception:
                patient_id = patient_id

    if not patient_id:
        raise HTTPException(status_code=400, detail='patient_id is required')

    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail='Patient not found')

    # For the demo, create a visit record-like dict from provided visit_id or defaults
    visit = {'patient_id': patient_id, 'disease': disease, 'visit_date': visit_id or 'latest'}

    # Select encoders based on disease (simple mapping)
    disease_modalities = {
        'alzheimers': ['MRI', 'PET', 'Notes', 'Genomics'],
        'parkinsons': ['DaTscan', 'MRI', 'Notes', 'Genomics'],
        'brain_tumor': ['MRI', 'CT', 'Notes', 'Genomics'],
        'cancer': ['CT', 'MRI', 'PET', 'Notes', 'Genomics']
    }

    modalities = disease_modalities.get(disease.lower(), ['MRI', 'Notes'])
    modality_scores = {}
    embeddings = []

    # Use available encoders; missing ones fall back to a generic encoder (use MRI encoder)
    for mod in modalities:
        enc = encoders.MODALITY_ENCODERS.get(mod, encoders.encode_mri)
        out = enc(visit)
        modality_scores[mod] = out['score']
        embeddings.append(out['embedding'])

    # For fusion, average embeddings into a single vector and run TinyTGNN
    # Stack embeddings (convert to tensor)
    import torch
    stacked = torch.stack(embeddings)
    avg = torch.mean(stacked, dim=0)
    model = tgnn.TinyTGNN()
    prob = round(tgnn.predict_from_features(model, avg), 2)

    # Build timeline from previous inference results for this patient and disease
    previous_results = db.query(InferenceResult).filter(
        InferenceResult.patient_id == patient_id,
        InferenceResult.disease == disease
    ).order_by(InferenceResult.timestamp.asc()).all()
    visits = []
    probabilities = []
    for r in previous_results:
        try:
            r_json = json.loads(r.result_json)
            visit_label = r_json.get('visit_id') or r.timestamp.strftime('%Y-%m-%d')
            visits.append(visit_label)
            fusion = r_json.get('fusion', {})
            probabilities.append(fusion.get('probability', None))
        except Exception:
            continue
    visits.append(visit_id or 'latest')
    probabilities.append(prob)
    result = {
        'patient_id': patient_id,
        'disease': disease,
        'modalities': modality_scores,
        'fusion': {
            'method': 'TGNN',
            'probability': prob,
            'decision': 'High risk' if prob > 0.7 else 'Low risk',
            'explain': {
                'top_modalities': sorted(modality_scores.keys(), key=lambda k: modality_scores[k], reverse=True)[:2],
                'weights': modality_scores
            }
        },
        'timeline': {
            'visits': visits,
            'probabilities': probabilities
        },
        'risk': {
            'groups': ['Low', 'Medium', 'High'],
            'values': [10, 5, 2]
        },
        'explain': {
            'labels': list(modality_scores.keys()),
            'datasets': [{'data': [modality_scores[k] for k in modality_scores]}]
        }
    }

    # Persist result in DB
    rec = InferenceResult(patient_id=patient_id, disease=disease, result_json=json.dumps(result))
    db.add(rec); db.commit(); db.refresh(rec)
    return result