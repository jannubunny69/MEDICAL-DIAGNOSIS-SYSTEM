"""Simple smoke test script for the strong_tgnn_complete app.

Runs the following sequence against http://127.0.0.1:8000:
- GET /, /main.html, /index.html, /alzheimers.html
- POST /patients/create (JSON)
- POST /visits/upload/alzheimers (multipart/form-data with a small text file)
- POST /inference/alzheimers (JSON)
- GET /snapshots/{patient_id}

Run with: python scripts/smoke_test.py
"""
import requests
from pathlib import Path

BASE = "http://127.0.0.1:8000"

def main():
    pages = ['/', '/main.html', '/index.html', '/alzheimers.html']
    for p in pages:
        r = requests.get(BASE + p)
        print(p, r.status_code)

    pid = 'PYTEST-001'
    # create patient
    r = requests.post(BASE + '/patients/create', json={'patient_id': pid, 'name':'PyTest', 'age':45, 'sex':'M'})
    print('/patients/create', r.status_code, r.json())

    # upload visit
    tmp = Path('scripts/tmp_visit.txt')
    tmp.write_text('this is a test file')
    files = {'files': ('tmp_visit.txt', tmp.read_bytes(), 'text/plain')}
    data = {'patient_id': pid, 'visit_date': '2025-09-15'}
    r = requests.post(BASE + '/visits/upload/alzheimers', files=files, data=data)
    print('/visits/upload/alzheimers', r.status_code, r.json() if r.ok else r.text)

    # inference
    r = requests.post(BASE + '/inference/alzheimers', json={'patient_id': pid})
    print('/inference/alzheimers', r.status_code, r.json())

    # snapshot
    r = requests.get(BASE + f'/snapshots/{pid}')
    print(f'/snapshots/{pid}', r.status_code, r.json())

if __name__ == '__main__':
    main()
