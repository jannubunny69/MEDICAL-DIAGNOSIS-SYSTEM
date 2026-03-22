import torch.nn as nn
import torch
class SnapshotTemporalModel(nn.Module):
    def __init__(self, emb_dim=288, hidden_dim=192, n_classes=3):
        super().__init__()
        self.lstm = nn.LSTM(input_size=emb_dim, hidden_size=hidden_dim, num_layers=1, batch_first=True)
        self.classifier = nn.Sequential(nn.Linear(hidden_dim, 128), nn.ReLU(), nn.Linear(128, n_classes))
    def forward(self, x_seq):
        is_single = False
        if x_seq.dim() == 2:
            x_seq = x_seq.unsqueeze(0); is_single = True
        out, _ = self.lstm(x_seq)
        logits = self.classifier(out)
        return logits.squeeze(0) if is_single else logits