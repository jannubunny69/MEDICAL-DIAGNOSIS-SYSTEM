"""Minimal TGNN stub used for integration and smoke tests.

This file provides:
- A tiny PyTorch model (MLP) that acts as a placeholder for the TGNN.
- `load_model(path)` and `save_model(path)` helpers.
- `predict_from_features(model, features)` which returns a probability.

Replace with a real TGNN implementation when available.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import os
from typing import Dict, Any


class TinyTGNN(nn.Module):
    def __init__(self, in_dim=16, hidden=32):
        super().__init__()
        self.fc1 = nn.Linear(in_dim, hidden)
        self.fc2 = nn.Linear(hidden, 1)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))
        return x.squeeze(-1)


def make_features_from_visit(visit: Dict[str, Any]) -> torch.Tensor:
    """Create a deterministic feature vector from visit metadata.

    This is a placeholder: real preprocessing should encode images/text/genomics.
    """
    # Use simple numeric hashes of strings to create stable features
    vec = torch.zeros(16, dtype=torch.float32)
    s = str(visit.get('patient_id', '')) + '|' + str(visit.get('disease', '')) + '|' + str(visit.get('visit_date', ''))
    h = abs(hash(s))
    for i in range(16):
        vec[i] = ((h >> (i*4)) & 0xF) / 15.0
    return vec


def load_model(path: str) -> TinyTGNN:
    model = TinyTGNN()
    if os.path.isfile(path):
        state = torch.load(path, map_location='cpu')
        model.load_state_dict(state)
    return model


def save_model(model: TinyTGNN, path: str):
    torch.save(model.state_dict(), path)


def predict_from_features(model: TinyTGNN, features: torch.Tensor) -> float:
    model.eval()
    with torch.no_grad():
        if features.dim() == 1:
            features = features.unsqueeze(0)
        out = model(features)
        prob = float(out.item())
    return prob


if __name__ == '__main__':
    # quick smoke run
    m = TinyTGNN()
    f = make_features_from_visit({'patient_id':'P-EX','disease':'alzheimers','visit_date':'2025-09-15'})
    print('prob=', predict_from_features(m, f))
