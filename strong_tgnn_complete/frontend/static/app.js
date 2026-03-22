// frontend app.js - handles API calls
// NOTE: backend routes are mounted at the root (e.g. /inference, /patients)
// so use an empty API_BASE. Change to '/api' only if you mount APIs under /api.
const API_BASE = '';

function showResult(targetId, data) {
  const el = document.getElementById(targetId) || document.getElementById('result');
  if (!el) return;
  el.textContent = JSON.stringify(data, null, 2);
}

async function createOrUpdatePatient(formEl) {
  const formData = new FormData(formEl);
  const body = {};
  for (const pair of formData.entries()) body[pair[0]] = pair[1];
  const res = await fetch(`${API_BASE}/patients/create`, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body)});
  const data = await res.json();
  alert(data.message || 'Saved');
}

async function uploadVisit(formEl, disease) {
  const fd = new FormData(formEl);
  const res = await fetch(`${API_BASE}/visits/upload/${disease}`, { method: 'POST', body: fd });
  const data = await res.json();
  alert(data.message || 'Uploaded');
}

async function runInference(disease, formEl) {
  const form = new FormData(formEl);
  const pid = form.get('patient_id');
  if (!pid) return alert('Provide patient_id');
  const res = await fetch(`${API_BASE}/inference/${disease}`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({patient_id: pid}) });
  const data = await res.json();
  showResult('result', data);
}

async function loadSnapshot(pid) {
  if (!pid) return alert('Provide patient id');
  const res = await fetch(`${API_BASE}/snapshots/${encodeURIComponent(pid)}`);
  const data = await res.json();
  const el = document.getElementById('snapshot');
  if (el) el.textContent = JSON.stringify(data, null, 2);
}

window.createOrUpdatePatient = createOrUpdatePatient;
window.uploadVisit = uploadVisit;
window.runInference = runInference;
window.loadSnapshot = loadSnapshot;