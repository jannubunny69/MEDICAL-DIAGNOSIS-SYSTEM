Project: strong_tgnn_complete

Overview
========
This project is a minimal demonstration of a Temporal Graph Neural Network (TGNN) system for multi-modal medical diagnosis. It includes a static frontend (HTML/JS/CSS), a FastAPI backend that serves APIs and static files, SQLAlchemy models for persistence, and training scripts to generate lightweight synthetic models.

Repository layout
=================
strong_tgnn_complete/
│
├── frontend/                         # HTML/JS/CSS user interface
│   ├── main.html                     # Landing page
│   ├── index.html                    # Disease dashboard
│   ├── alzheimers.html               # Alzheimer's page
│   ├── parkinsons.html               # Parkinson's page
│   ├── brain_tumor.html              # Brain tumor page
│   ├── cancer.html                   # Cancer page
│   ├── styles.css                    # Styling
│   └── app.js                        # API calls → backend
│
├── backend/
│   ├── app.py                        # FastAPI main entry
│   ├── routes/                       # API endpoints
│   │   ├── patients.py               # Create/update patients
│   │   ├── visits.py                 # Upload visits (MRI, notes, genomics)
│   │   └── inference.py              # Run inference using trained model
│   │
│   ├── models/                       # ML/TGNN-related
│   │   ├── tgnn.py                   # Temporal GNN + Fusion definition
│   │   └── checkpoints/              # Trained weights
│   │       ├── alzheimers.pt
│   │       ├── parkinsons.pt
│   │       ├── brain_tumor.pt
│   │       └── cancer.pt
│   │
│   ├── models/database.py           # SQLAlchemy engine + session (current)
│   └── models/*_model.py            # model table definitions (patients, visits, results)
│
└── training/
    └── train_tgnn.py                 # Train TGNN with synthetic/real data

Responsibilities
================
Frontend
- Collects patient intake info (ID, name, age, sex).
- Collects visit data: MRI, CT/PET, DaTscan, notes, genomics, pathology.
- Sends files & metadata → backend API.
- Displays: Inference result (diagnosis prediction) and patient history snapshot.

Backend (FastAPI)
- `patients.py`
  - POST `/patients/create` → create/update patient in DB.
  - GET `/patients/{id}` → fetch patient profile.

- `visits.py`
  - POST `/visits/upload/{disease}` → upload visit files, store on disk, record in DB.

- `inference.py`
  - POST `/inference/{disease}` →
    - Load corresponding model checkpoint from `backend/models/checkpoints/{disease}.pt`.
    - Run TGNN fusion on latest visit data and return prediction (probability, diagnosis).

Models
- `tgnn.py` = architecture (Temporal Graph Neural Network + fusion layers).
- `.pt` files = trained weights for each disease in `backend/models/checkpoints/`.

Training (train_tgnn.py)
- Uses synthetic data generation utilities to train small TGNNs for each disease.
- Saves checkpoints to `backend/models/checkpoints/`.

Database (models/database.py)
- Stores:
  - Patients table (ID, demographics).
  - Visits table (date, uploaded files, metadata).
  - Inference results table.
- `backend/init_db.py` helper creates the database and tables.

How to run
==========
1. Create and activate a Python virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Initialize the database (optional — app will create DB on demand):

```powershell
python backend/init_db.py
```

3. Start the backend server:

```powershell
uvicorn backend.app:app --reload
```

4. Open the UI in a browser:
- Landing page: `http://127.0.0.1:8000/` (redirects to `/main.html`)
- API docs: `http://127.0.0.1:8000/docs`

Notes & Next steps
==================
- The `inference` endpoint currently uses a placeholder random prediction when no real model is available. Replace with TGNN inference by implementing `backend/models/tgnn.py` and loading `.pt` checkpoints.
- Consider adding authentication and request validation for production use.
- Add tests (pytest + httpx) for the API endpoints.

Contact & maintenance
=====================
- Keep model checkpoints out of source control for large models; use an artifact store or cloud bucket and download during deployment.
- Pin package versions in `requirements.txt` and include a `constraints.txt` for reproducibility.

---
Generated: project blueprint inserted into repo.

Fusion workflow (detailed blueprint)
===================================
This section specifies the end-to-end fusion workflow, modality-level intermediate scores, TGNN per-disease structure, the `inference` API contract, and an example output (e.g., "MRI: 65% chance Alzheimer’s"). Use this as the engineering spec to implement the fusion pipeline.

1) Input (from hospital systems)
  - Imaging: MRI (volumetric / series), CT, PET, DaTscan (for Parkinson's), etc.
  - Structured data: demographics, lab values, vitals, pathology tables.
  - Textual data: clinical notes, radiology/pathology reports (free text).
  - Genomics: VCF, gene-expression CSVs, panels.

2) Per-modality feature extraction (examples)
  - MRI / CT / PET / DaTscan: Run a modality-specific CNN or radiomics pipeline to produce an embedding vector and (optionally) a modality-level probability score p_modality(disease).
    - Example: MRI -> CNN encoder -> 256-d embedding -> small classifier -> p_mri = 0.65
  - Reports / Notes: NLP encoder (BioBERT / Clinical BERT) for text embeddings; numeric lab values normalized and concatenated.
  - Genomics: Variant / panel encoding to vector; run a small model to produce genomic embedding / score.
  - Tabular: Standard scaler + MLP to produce an embedding and score.

3) Intermediate predictions (per modality)
  - For interpretability and debugging, compute a per-modality probability score for the disease:
    - p_mri, p_pet, p_ct, p_notes, p_genomics, p_tabular
  - These values are stored alongside visit records and returned in the inference response when requested.

4) Fusion layer design options
  - Stacking / ensemble: Combine modality probabilities with a simple logistic regression or XGBoost on top of modality scores.
  - Neural fusion: Concatenate modality embeddings and pass through a small MLP (fusion net) to produce a fused embedding and probability.
  - Graph + temporal fusion (TGNN):
    - Snapshot-level: build a small Graph Convolution (GCN/GIN) over entities (patient, visit, modalities) to compute a snapshot embedding per visit.
    - Temporal aggregation: feed the sequence of snapshot embeddings into a temporal model (GRU / LSTM / Transformer) to model progression across visits.
    - Prediction head: small MLP or linear layer producing final probability p_final.

5) Per-disease TGNN architecture (blueprint)
  - Alzheimer’s TGNN
    - Modalities: MRI, PET, Clinical notes, Genomics
    - Flow: modality encoders -> snapshot GCN -> GRU over visits -> MLP head -> p_alz
  - Parkinson’s TGNN
    - Modalities: DaTscan, MRI, Clinical notes, Genomics
    - Flow: same as above but configured input encoders
  - Tumor TGNN
    - Modalities: MRI, CT, Reports, Genomics
  - Cancer TGNN
    - Modalities: CT, MRI, PET, Reports, Genomics
  - Notes: each disease model can reuse common encoders and differ in fusion/prediction head.

6) Example fusion output (human readable)
  - Modality-level: MRI: 65% chance Alzheimer’s
  - Full fusion result: {"patient_id":"P-123","disease":"alzheimers","modalities":{"MRI":0.65,"PET":0.78,"Notes":0.55},"fusion":{"method":"TGNN","probability":0.88}}

7) API contract: `/inference/{disease}`
  - Request (JSON)
    - Path: `POST /inference/{disease}`
    - Body (example):
      {
        "patient_id": "P-123",
        "visit_id": "V-2025-09-15",
        "include_modalities": ["MRI","PET","Notes"],    // optional
        "force_reload_model": false                         // optional
      }

  - Response (JSON)
    - Success example:
      {
        "patient_id": "P-123",
        "disease": "alzheimers",
        "modalities": {
          "MRI": 0.65,
          "PET": 0.78,
          "Notes": 0.55
        },
        "fusion": {
          "method": "TGNN",
          "probability": 0.88,
          "explain": {
            "top_modalities": ["PET","MRI"],
            "weights": {"PET":0.6,"MRI":0.3,"Notes":0.1}
          }
        },
        "timestamp": "2025-09-15T12:00:00Z"
      }

  - Error cases:
    - 400: missing `patient_id` or `visit_id`.
    - 404: patient or visit not found.
    - 500: model load or runtime error.

8) Implementation notes
  - Checkpoint storage: keep per-disease checkpoints in `backend/models/checkpoints/{disease}.pt` and load lazily the first time the disease endpoint is called.
  - Model API: create a small wrapper `backend/models/tgnn.py` that exposes `load_model(disease) -> model` and `predict(model, visit_record) -> {modalities, probability}`.
    - We added a `TinyTGNN` stub for integration and testing; replace it with the real TGNN neural architecture.
  - Preprocessing: implement modality-specific preprocessors under `backend/preprocessing/` and standardize feature shapes.
  - Explainability: store modality-level scores and fusion weights for auditability and UI display.

9) Tests and validation
  - Unit tests: verify modality encoders produce expected shapes and deterministic embeddings for fixed inputs.
  - Integration tests: use `scripts/smoke_test.py` pattern to run create -> upload -> inference -> snapshot.
  - Model sanity checks: after training, run a validation set to produce ROC/AUC and store metrics with checkpoint metadata.

10) Deployment considerations
  - GPU: load models with `map_location='cuda'` when available; fallback to CPU for development.
  - Scale: use a model server (TorchServe, Triton, or separate worker processes) for heavy inference loads.
  - Privacy: ensure uploaded files and PHI are stored securely (access control, encryption at rest).

Appendix: example CLI usage
---------------------------------
Run quick local inference (example):
```powershell
# create a patient and upload visit via the UI or API
python -c "from backend.models import tgnn; m=tgnn.load_model('backend/models/checkpoints/alzheimers.pt'); print('loaded', m)"
curl -X POST http://127.0.0.1:8000/inference/alzheimers -H "Content-Type: application/json" -d '{"patient_id":"P-123","visit_id":"V-2025-09-15"}'
```

