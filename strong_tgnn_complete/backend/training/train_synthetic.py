import torch, os
from torch.utils.data import DataLoader
from backend.training.dataset import SyntheticPatientDataset
from backend.training.models import SnapshotTemporalModel
def train_loop(data_dir='backend/training/synthetic_dataset', epochs=3, save_dir='backend/models/checkpoints'):
    os.makedirs(save_dir, exist_ok=True)
    dataset = SyntheticPatientDataset(data_dir)
    loader = DataLoader(dataset, batch_size=1, shuffle=True)
    model = SnapshotTemporalModel().to('cpu')
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.CrossEntropyLoss()
    for epoch in range(1, epochs+1):
        total = 0.0
        for pid, seq, labels in loader:
            seq = seq.float()
            logits = model(seq)
            if logits.dim() == 3: logits = logits.squeeze(0)
            loss = loss_fn(logits, labels)
            opt.zero_grad(); loss.backward(); opt.step()
            total += loss.item()
        print(f'Epoch {epoch} avg_loss={total/len(loader):.4f}')
        torch.save(model.state_dict(), os.path.join(save_dir, f'checkpoint_epoch{epoch}.pt'))
    print('done') 
if __name__ == "__main__": train_loop()