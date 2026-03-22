import json, os, random
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np

RNG = np.random.RandomState(42)
def make_random_vector(dim=128):
    return RNG.normal(size=(dim,)).astype(float).tolist()

def generate_patient(patient_id, n_visits=6):
    visits = []
    base_date = datetime(2018,1,1)
    for i in range(n_visits):
        date = (base_date + timedelta(days=90*i)).strftime("%Y-%m-%d")
        img = make_random_vector(128)
        txt = make_random_vector(64)
        labs = make_random_vector(32)
        geno = make_random_vector(64)
        score = RNG.rand() + 0.05*i
        if score > 1.4:
            stage = 2
        elif score > 0.8:
            stage = 1
        else:
            stage = 0
        visits.append({ "visit_id": f'{patient_id}_v{i+1}', "date": date, "image": img, "text": txt, "labs": labs, "genomics": geno, "stage": int(stage) })
    return { "patient_id": patient_id, "visits": visits }

def generate_dataset(out_dir='backend/training/synthetic_dataset', n_patients=200, visits_per_patient=6):
    Path = Path if 'Path' in globals() else __import__('pathlib').Path
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for i in range(n_patients):
        pid = f'P-{1000+i}'
        patient = generate_patient(pid, n_visits=visits_per_patient)
        with open(Path(out_dir)/f'{pid}.json', 'w') as f:
            json.dump(patient, f)
    print('generated')