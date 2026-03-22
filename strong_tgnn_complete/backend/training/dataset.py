import json
from torch.utils.data import Dataset
import torch
from pathlib import Path
class SyntheticPatientDataset(Dataset):
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)
        self.files = list(self.data_dir.glob('P-*.json'))
    def __len__(self): return len(self.files)
    def _fuse_visit(self, visit):
        img = torch.tensor(visit['image'], dtype=torch.float32)
        txt = torch.tensor(visit['text'], dtype=torch.float32)
        labs = torch.tensor(visit['labs'], dtype=torch.float32)
        geno = torch.tensor(visit['genomics'], dtype=torch.float32)
        return torch.cat([img, txt, labs, geno], dim=0)
    def __getitem__(self, idx):
        path = self.files[idx]; data = json.loads(path.read_text())
        visits = sorted(data['visits'], key=lambda v: v['date'])
        fused = [self._fuse_visit(v) for v in visits]
        stages = [v['stage'] for v in visits]
        return data['patient_id'], torch.stack(fused), torch.tensor(stages, dtype=torch.long)