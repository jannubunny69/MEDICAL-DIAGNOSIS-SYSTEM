# Strong TGNN Complete Project

This archive contains a full frontend, backend (FastAPI) with SQLAlchemy DB models, file storage, training scripts for synthetic data, and a small model checkpoint for testing.

Run backend:

```
pip install -r requirements.txt
uvicorn backend.app:app --reload
```

Frontend files are in `frontend/` — either serve with a static server or mount via FastAPI static routes.
