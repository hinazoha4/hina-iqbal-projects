"""CICDDoS2019 RF + CNN-LSTM controlled feature ablations on identical targets.

Uses the four-file all-data.csv. Training-only imputation. Non-temporal sequences
for CNN-LSTM (shuffled stratified rows). Validation thresholds not used here for
the table-11 style 0.5-threshold comparison; matched-FAR also exported.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import confusion_matrix, matthews_corrcoef
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from torch.utils.data import DataLoader, Dataset

SRC = Path(r"C:\Users\Lenovo\Downloads\17th revision\extracted\17th revision\_experiments\src")
sys.path.insert(0, str(SRC))
from matched_far import evaluate  # noqa: E402


def find_col(columns, name):
    t = name.strip().lower()
    for c in columns:
        if str(c).strip().lower() == t:
            return c
    return None


def rates(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
        "far": float(fp / (fp + tn)) if (fp + tn) else None,
        "fnr": float(fn / (fn + tp)) if (fn + tp) else None,
        "mcc": float(matthews_corrcoef(y_true, y_pred)) if len(np.unique(y_true)) > 1 else None,
    }


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
    def __init__(self, n_feat, filters=32, hidden=32, dropout=0.3):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(n_feat, filters, 3, padding=1), nn.ReLU(), nn.Dropout(dropout)
        )
        self.lstm = nn.LSTM(filters, hidden, batch_first=True)
        self.head = nn.Linear(hidden, 2)

    def forward(self, x):
        h = self.conv(x.transpose(1, 2)).transpose(1, 2)
        out, _ = self.lstm(h)
        return self.head(out[:, -1, :])


@torch.no_grad()
def cnn_scores(model, x, y, seq_len, batch_size=256):
    loader = DataLoader(SeqDS(x, y, seq_len), batch_size=batch_size, shuffle=False)
    model.eval()
    scores, labels, ids = [], [], []
    for xb, yb, idb in loader:
        prob = torch.softmax(model(xb), dim=1)[:, 1].cpu().numpy()
        scores.append(prob)
        labels.append(yb.numpy())
        ids.append(idb.numpy())
    return np.concatenate(scores), np.concatenate(labels), np.concatenate(ids)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--seq-len", type=int, default=30)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    head = args.data.read_bytes()[:40]
    if head.lstrip().startswith(b"<"):
        raise SystemExit("Refused HTML")

    df = pd.read_csv(args.data, low_memory=False)
    # Shuffle for non-temporal sequences
    df = df.sample(frac=1.0, random_state=args.seed).reset_index(drop=True)
    label_col = find_col(df.columns, "Label")
    y = (df[label_col].astype(str).str.strip().str.upper() != "BENIGN").astype(np.int8).to_numpy()
    flow_id = find_col(df.columns, "Flow ID")
    src_ip = find_col(df.columns, "Source IP")
    dst_ip = find_col(df.columns, "Destination IP")
    ts_col = find_col(df.columns, "Timestamp")
    inbound = find_col(df.columns, "Inbound")
    sport = find_col(df.columns, "Source Port")
    dport = find_col(df.columns, "Destination Port")

    drop_always = {c for c in [label_col, src_ip, dst_ip, flow_id, find_col(df.columns, "SimillarHTTP"), find_col(df.columns, "Unnamed: 0")] if c}
    numeric = [c for c in df.columns if c not in drop_always and pd.api.types.is_numeric_dtype(df[c])]
    configs = {
        "full_numeric": numeric,
        "no_timestamp": [c for c in numeric if c != ts_col and "timestamp" not in str(c).strip().lower()],
        "no_timestamp_inbound": [c for c in numeric if c not in {ts_col, inbound} and "timestamp" not in str(c).strip().lower()],
        "no_timestamp_inbound_ports": [c for c in numeric if c not in {ts_col, inbound, sport, dport} and "timestamp" not in str(c).strip().lower()],
    }

    idx = np.arange(len(df))
    train_idx, temp_idx = train_test_split(idx, test_size=0.30, random_state=args.seed, stratify=y)
    val_idx, test_idx = train_test_split(temp_idx, test_size=0.50, random_state=args.seed, stratify=y[temp_idx])

    overlap = {"exact_duplicate_rows": int(df.duplicated(keep=False).sum())}
    if flow_id:
        tr = set(df.iloc[train_idx][flow_id].astype(str))
        te = set(df.iloc[test_idx][flow_id].astype(str))
        overlap["flow_id_train_test_overlap"] = int(len(tr & te))

    report = {
        "seed": args.seed,
        "rows": int(len(df)),
        "sequence_semantics": "NON_TEMPORAL_shuffled_record_windows",
        "overlap": overlap,
        "configs": {},
    }
    score_rows = []
    for name, cols in configs.items():
        frame = df[cols].replace([np.inf, -np.inf], np.nan)
        imputer = SimpleImputer(strategy="median")
        x_tr = imputer.fit_transform(frame.iloc[train_idx])
        x_va = imputer.transform(frame.iloc[val_idx])
        x_te = imputer.transform(frame.iloc[test_idx])
        scaler = MinMaxScaler().fit(x_tr)
        x_tr_s = scaler.transform(x_tr).astype(np.float32)
        x_va_s = scaler.transform(x_va).astype(np.float32)
        x_te_s = scaler.transform(x_te).astype(np.float32)

        rf = RandomForestClassifier(
            n_estimators=80, max_depth=24, min_samples_leaf=5,
            class_weight="balanced_subsample", n_jobs=-1, random_state=args.seed,
        )
        rf.fit(x_tr_s, y[train_idx])
        rf_va = rf.predict_proba(x_va_s)[:, 1]
        rf_te = rf.predict_proba(x_te_s)[:, 1]
        rf_pred = (rf_te >= 0.5).astype(int)

        # CNN-LSTM
        seq_len = min(args.seq_len, max(2, len(x_tr_s) // 5))
        model = CNNLSTM(x_tr_s.shape[1])
        counts = np.bincount(y[train_idx], minlength=2).astype(np.float32)
        w = counts.sum() / (2 * np.maximum(counts, 1))
        crit = nn.CrossEntropyLoss(weight=torch.tensor(w, dtype=torch.float32))
        opt = torch.optim.Adam(model.parameters(), lr=1e-3)
        loader = DataLoader(SeqDS(x_tr_s, y[train_idx], seq_len), batch_size=256, shuffle=True)
        for _ in range(args.epochs):
            model.train()
            for xb, yb, _id in loader:
                opt.zero_grad()
                crit(model(xb), yb).backward()
                opt.step()
        cnn_va, cnn_va_y, cnn_va_id = cnn_scores(model, x_va_s, y[val_idx], seq_len)
        cnn_te, cnn_te_y, cnn_te_id = cnn_scores(model, x_te_s, y[test_idx], seq_len)
        cnn_pred = (cnn_te >= 0.5).astype(int)

        cfg = {
            "n_features": len(cols),
            "RF_threshold_0.5": rates(y[test_idx], rf_pred),
            "CNN_LSTM_threshold_0.5": rates(y[test_idx][cnn_te_id], cnn_pred),
        }
        # matched FAR on aligned IDs
        validation = pd.concat([
            pd.DataFrame({"target_id": [f"val_{int(i)}" for i in cnn_va_id], "y_true": cnn_va_y.astype(int),
                          "score_attack": rf_va[cnn_va_id].astype(float), "model": "RandomForest", "seed": args.seed}),
            pd.DataFrame({"target_id": [f"val_{int(i)}" for i in cnn_va_id], "y_true": cnn_va_y.astype(int),
                          "score_attack": cnn_va.astype(float), "model": "CNN-LSTM", "seed": args.seed}),
        ], ignore_index=True)
        test = pd.concat([
            pd.DataFrame({"target_id": [f"test_{int(i)}" for i in cnn_te_id], "y_true": cnn_te_y.astype(int),
                          "score_attack": rf_te[cnn_te_id].astype(float), "model": "RandomForest", "seed": args.seed}),
            pd.DataFrame({"target_id": [f"test_{int(i)}" for i in cnn_te_id], "y_true": cnn_te_y.astype(int),
                          "score_attack": cnn_te.astype(float), "model": "CNN-LSTM", "seed": args.seed}),
        ], ignore_index=True)
        mfar = evaluate(validation, test, [0.01, 0.005, 0.001])
        mfar.to_csv(args.out / f"matched_far_{name}.csv", index=False)
        cfg["matched_far_rows"] = int(len(mfar))
        report["configs"][name] = cfg
        print(name, cfg["RF_threshold_0.5"], cfg["CNN_LSTM_threshold_0.5"], flush=True)
        for split, scores, labels, indices, model_name in (
            ("val", rf_va[cnn_va_id], cnn_va_y, cnn_va_id, "RF"),
            ("test", rf_te[cnn_te_id], cnn_te_y, cnn_te_id, "RF"),
            ("val", cnn_va, cnn_va_y, cnn_va_id, "CNN-LSTM"),
            ("test", cnn_te, cnn_te_y, cnn_te_id, "CNN-LSTM"),
        ):
            for i, s, lab in zip(indices, scores, labels):
                score_rows.append({
                    "config": name, "split": split, "model": model_name,
                    "target_id": f"{split}_{int(i)}", "y_true": int(lab),
                    "score_attack": float(s), "seed": args.seed,
                })

    pd.DataFrame(score_rows).to_csv(args.out / "predictions_rf_cnn.csv", index=False)
    (args.out / "cicddos_rf_cnn_ablation_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"status": "PASS", "configs": list(report["configs"])}), flush=True)


if __name__ == "__main__":
    main()
