"""Paired multi-attack CICIoT2023 matched-FAR study (CPU-feasible pilot).

Documents: filename-derived labels; NON-TEMPORAL record order (shuffled stratified
splits). Windows for CNN-LSTM are consecutive rows AFTER the stratified shuffle,
so this evaluates sequence models on non-temporal record sequences, not traffic time order.
Thresholds from validation only. Identical target_ids for RF and CNN-LSTM.
Does not invent scores.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, Dataset

SRC = Path(r"C:\Users\Lenovo\Downloads\17th revision\extracted\17th revision\_experiments\src")
sys.path.insert(0, str(SRC))
from matched_far import evaluate  # noqa: E402


class SeqDS(Dataset):
    def __init__(self, x, y, seq_len):
        self.x = x.astype(np.float32, copy=False)
        self.y = y.astype(np.int64, copy=False)
        self.seq_len = seq_len

    def __len__(self):
        return max(len(self.x) - self.seq_len + 1, 0)

    def __getitem__(self, idx):
        return (
            torch.from_numpy(self.x[idx: idx + self.seq_len]),
            torch.tensor(self.y[idx + self.seq_len - 1], dtype=torch.long),
            idx + self.seq_len - 1,
        )


class CNNLSTM(nn.Module):
    def __init__(self, n_feat, filters=64, hidden=64, dropout=0.3):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(n_feat, filters, 3, padding=1),
            nn.BatchNorm1d(filters),
            nn.ReLU(),
            nn.Dropout(dropout),
        )
        self.lstm = nn.LSTM(filters, hidden, batch_first=True)
        self.head = nn.Sequential(nn.Dropout(dropout), nn.Linear(hidden, 2))

    def forward(self, x):
        h = self.conv(x.transpose(1, 2)).transpose(1, 2)
        out, _ = self.lstm(h)
        return self.head(out[:, -1, :])


def family_from_name(name: str) -> str:
    m = re.match(r"(.+?)(\d*)\.pcap\.csv$", name)
    return m.group(1) if m else Path(name).stem


def load_multi(raw_dir: Path, per_family: int, seed: int):
    files = sorted(raw_dir.rglob("*.csv"))
    rng = np.random.default_rng(seed)
    frames = []
    inventory = []
    for path in files:
        fam = family_from_name(path.name)
        label = 0 if "benign" in fam.lower() else 1
        # Read a generous chunk then subsample
        df = pd.read_csv(path, nrows=max(per_family * 3, per_family))
        if len(df) > per_family:
            idx = rng.choice(len(df), size=per_family, replace=False)
            df = df.iloc[idx]
        df = df.copy()
        df["y_true"] = label
        df["attack_family"] = fam
        df["source_file"] = path.name
        frames.append(df)
        inventory.append({"file": path.name, "family": fam, "label": label, "rows_used": int(len(df))})
    frame = pd.concat(frames, ignore_index=True)
    # Shuffle so sequence windows are NOT chronological traffic order.
    frame = frame.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    feat_cols = [c for c in frame.columns if c not in {"y_true", "attack_family", "source_file"} and pd.api.types.is_numeric_dtype(frame[c])]
    work = frame[feat_cols].replace([np.inf, -np.inf], np.nan).fillna(0).astype(np.float32)
    work["y_true"] = frame["y_true"].astype(np.int8).to_numpy()
    work["attack_family"] = frame["attack_family"].to_numpy()
    y = work["y_true"].to_numpy()
    idx = np.arange(len(work))
    train_idx, temp_idx = train_test_split(idx, test_size=0.30, random_state=seed, stratify=y)
    val_idx, test_idx = train_test_split(temp_idx, test_size=0.50, random_state=seed, stratify=y[temp_idx])
    meta = {
        "source": "hf_baalajimaestro_DDoS-CICIoT2023",
        "labeling": "filename-derived",
        "sequence_semantics": "NON_TEMPORAL_shuffled_record_windows",
        "feature_cols": feat_cols,
        "inventory": inventory,
        "families": sorted(frame["attack_family"].unique().tolist()),
        "rows": int(len(work)),
        "counts": {
            "train": {"n": int(len(train_idx)), "benign": int((y[train_idx] == 0).sum()), "attack": int((y[train_idx] == 1).sum())},
            "val": {"n": int(len(val_idx)), "benign": int((y[val_idx] == 0).sum()), "attack": int((y[val_idx] == 1).sum())},
            "test": {"n": int(len(test_idx)), "benign": int((y[test_idx] == 0).sum()), "attack": int((y[test_idx] == 1).sum())},
        },
    }
    return work.iloc[train_idx].reset_index(drop=True), work.iloc[val_idx].reset_index(drop=True), work.iloc[test_idx].reset_index(drop=True), meta


@torch.no_grad()
def predict(model, loader, device):
    model.eval()
    scores, labels, ids = [], [], []
    for xb, yb, idb in loader:
        prob = torch.softmax(model(xb.to(device)), dim=1)[:, 1].cpu().numpy()
        scores.append(prob)
        labels.append(yb.numpy())
        ids.append(idb.numpy())
    return np.concatenate(scores), np.concatenate(labels), np.concatenate(ids)


def run_seed(train_df, val_df, test_df, seed, seq_len, epochs, batch_size, out_dir: Path, base_meta: dict):
    feat_cols = [c for c in train_df.columns if c not in {"y_true", "attack_family"}]
    x_tr = train_df[feat_cols].to_numpy(np.float32)
    y_tr = train_df["y_true"].to_numpy(np.int8)
    x_va = val_df[feat_cols].to_numpy(np.float32)
    y_va = val_df["y_true"].to_numpy(np.int8)
    x_te = test_df[feat_cols].to_numpy(np.float32)
    y_te = test_df["y_true"].to_numpy(np.int8)

    scaler = MinMaxScaler().fit(x_tr)
    x_tr_s, x_va_s, x_te_s = map(lambda a: scaler.transform(a).astype(np.float32), (x_tr, x_va, x_te))

    rf = RandomForestClassifier(
        n_estimators=100, class_weight="balanced_subsample", n_jobs=-1,
        random_state=seed, max_depth=24, min_samples_leaf=5,
    )
    t0 = time.time()
    rf.fit(x_tr_s, y_tr)
    rf_sec = time.time() - t0
    rf_va = rf.predict_proba(x_va_s)[:, 1]
    rf_te = rf.predict_proba(x_te_s)[:, 1]

    device = torch.device("cpu")
    seq_len = min(seq_len, max(2, len(x_tr_s) // 4))
    tr_loader = DataLoader(SeqDS(x_tr_s, y_tr, seq_len), batch_size=batch_size, shuffle=True)
    va_loader = DataLoader(SeqDS(x_va_s, y_va, seq_len), batch_size=batch_size, shuffle=False)
    te_loader = DataLoader(SeqDS(x_te_s, y_te, seq_len), batch_size=batch_size, shuffle=False)
    model = CNNLSTM(x_tr_s.shape[1]).to(device)
    counts = np.bincount(y_tr, minlength=2).astype(np.float32)
    weights = counts.sum() / (2.0 * np.maximum(counts, 1.0))
    crit = nn.CrossEntropyLoss(weight=torch.tensor(weights, dtype=torch.float32))
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    t1 = time.time()
    for ep in range(epochs):
        model.train()
        total = n = 0
        for xb, yb, _ in tr_loader:
            opt.zero_grad()
            loss = crit(model(xb), yb)
            loss.backward()
            opt.step()
            total += float(loss.item()) * len(yb)
            n += len(yb)
        print(f"seed {seed} epoch {ep+1}/{epochs} loss={total/max(n,1):.4f}", flush=True)
    cnn_sec = time.time() - t1
    cnn_va, cnn_va_y, cnn_va_id = predict(model, va_loader, device)
    cnn_te, cnn_te_y, cnn_te_id = predict(model, te_loader, device)
    assert np.array_equal(y_va[cnn_va_id], cnn_va_y)
    assert np.array_equal(y_te[cnn_te_id], cnn_te_y)

    def pack(split, model_name, ids, y, scores):
        return pd.DataFrame({
            "target_id": [f"{split}_{int(i)}" for i in ids],
            "y_true": y.astype(int),
            "score_attack": scores.astype(float),
            "model": model_name,
            "seed": seed,
        })

    validation = pd.concat([
        pack("val", "RandomForest", cnn_va_id, cnn_va_y, rf_va[cnn_va_id]),
        pack("val", "CNN-LSTM", cnn_va_id, cnn_va_y, cnn_va),
    ], ignore_index=True)
    test = pd.concat([
        pack("test", "RandomForest", cnn_te_id, cnn_te_y, rf_te[cnn_te_id]),
        pack("test", "CNN-LSTM", cnn_te_id, cnn_te_y, cnn_te),
    ], ignore_index=True)
    seed_dir = out_dir / f"seed_{seed}"
    seed_dir.mkdir(parents=True, exist_ok=True)
    validation.to_csv(seed_dir / "predictions_validation.csv", index=False)
    test.to_csv(seed_dir / "predictions_test.csv", index=False)
    result = evaluate(validation, test, [0.01, 0.005, 0.001, 0.0005])
    result.to_csv(seed_dir / "matched_far_results.csv", index=False)
    meta = dict(base_meta)
    meta.update({
        "seed": seed,
        "device": "cpu",
        "torch": torch.__version__,
        "cuda_available": False,
        "seq_len": seq_len,
        "epochs": epochs,
        "rf_seconds": round(rf_sec, 2),
        "cnn_lstm_seconds": round(cnn_sec, 2),
        "n_features": len(feat_cols),
    })
    (seed_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    torch.save({"state_dict": model.state_dict(), "meta": meta}, seed_dir / "cnn_lstm.pt")
    print(result.to_string(index=False), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--per-family", type=int, default=4000)
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 7])
    parser.add_argument("--seq-len", type=int, default=40)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=256)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    all_results = []
    for seed in args.seeds:
        train_df, val_df, test_df, meta = load_multi(args.data, args.per_family, seed)
        print(json.dumps({"seed": seed, "families": meta["families"], "rows": meta["rows"], "counts": meta["counts"]}), flush=True)
        result = run_seed(train_df, val_df, test_df, seed, args.seq_len, args.epochs, args.batch_size, args.out, meta)
        if "seed" not in result.columns:
            result = result.copy()
            result.insert(0, "seed", seed)
        all_results.append(result)
    combined = pd.concat(all_results, ignore_index=True)
    combined.to_csv(args.out / "matched_far_multiattack_all_seeds.csv", index=False)
    summary = {
        "status": "PASS",
        "study": "CICIoT2023 paired multi-attack matched-FAR",
        "seeds": args.seeds,
        "sequence_semantics": "NON_TEMPORAL_shuffled_record_windows",
        "caveat": (
            "Not the original private prepared CICIoT split. Labels from filenames. "
            "CNN-LSTM windows are non-temporal shuffled-record sequences on CPU."
        ),
        "rows_combined_table": int(len(combined)),
    }
    (args.out / "study_status.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
