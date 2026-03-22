"""Simple modality encoders (stubs) that return deterministic scores and embeddings.

These are placeholders to demo fusion; replace with real CNN/NLP/Genomics encoders.
"""
from typing import Dict, Any
import torch
from .tgnn import make_features_from_visit


def encode_mri(visit: Dict[str, Any]):
    vec = make_features_from_visit(visit)
    score = float((vec.sum() % 100) / 100.0)
    return {'embedding': vec, 'score': round(score, 2)}


def encode_pet(visit: Dict[str, Any]):
    vec = make_features_from_visit(visit)
    score = float(((vec.sum() + 3) % 100) / 100.0)
    return {'embedding': vec, 'score': round(score, 2)}


def encode_notes(visit: Dict[str, Any]):
    vec = make_features_from_visit(visit)
    score = float(((vec.sum() + 5) % 100) / 100.0)
    return {'embedding': vec, 'score': round(score, 2)}


def encode_genomics(visit: Dict[str, Any]):
    vec = make_features_from_visit(visit)
    score = float(((vec.sum() + 7) % 100) / 100.0)
    return {'embedding': vec, 'score': round(score, 2)}


MODALITY_ENCODERS = {
    'MRI': encode_mri,
    'PET': encode_pet,
    'Notes': encode_notes,
    'Genomics': encode_genomics,
}
