"""CICIoT2023 paired matched-FAR one-seed pilot.

Uses identical target_ids for Random Forest (tabular) and CNN–LSTM (sequences).
Thresholds are selected on validation scores only. Does not invent predictions.
"""
from __future__ import annotations

import argparse
import json
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

from matched_far import evaluate


class StreamingSequenceDataset(Dataset):
    def __init__(self, x: np.ndarray, y: np.ndarray, seq_len: int):
        self.x = x.astype(np.float32, copy=False)
        self.y = y.astype(np.int64, copy=False)
        self.seq_len = seq_len

    def __len__(self) -> int:
        return max(len(self.x) - self.seq_len + 1, 0)

    def __getitem__(self, idx: int):
        return (
            torch.from_numpy(self.x[idx: idx + self.seq_len]),
            torch.tensor(self.y[idx + self.seq_len - 1], dtype=torch.long),
            idx + self.seq_len - 1,
        )


class CNNLSTM(nn.Module):
    """Architecture aligned with the thesis CNN–LSTM hybrid (fixed pilot hyperparameters)."""

    def __init__(self, num_features: int, cnn_filters: int = 64, lstm_hidden: int = 64, dropout: float = 0.3):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv1d(num_features, cnn_filters, kernel_size=3, padding=1),
            nn.BatchNorm1d(cnn_filters),
            nn.ReLU(),
            nn.Dropout(dropout),
        )
        self.lstm = nn.LSTM(cnn_filters, lstm_hidden, batch_first=True)
        self.head = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(lstm_hidden, 2),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: [B, T, F] -> conv wants [B, F, T]
        h = self.conv(x.transpose(1, 2)).transpose(1, 2)
        out, _ = self.lstm(h)
        return self.head(out[:, -1, :])


def _load_prepared(data_dir: Path, max_rows: int | None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    train = pd.read_csv(data_dir / "train" / "train.csv", nrows=max_rows)
    val = pd.read_csv(data_dir / "validation" / "validation.csv", nrows=max_rows)
    test = pd.read_csv(data_dir / "test" / "test.csv", nrows=max_rows)
    return train, val, test


def _label_from_ciciot_filename(name: str) -> int:
    lower = name.lower()
    if "benign" in lower:
        return 0
    return 1


def _load_raw_and_split(raw_dir: Path, seed: int, max_rows: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    files = sorted(raw_dir.rglob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSVs in {raw_dir}")
    # Balance benign and attack file quotas for a usable FAR pilot.
    benign_files = [p for p in files if "benign" in p.name.lower()]
    attack_files = [p for p in files if "benign" not in p.name.lower()]
    per_class = max(max_rows // 2, 1000)
    frames = []
    for group, quota in ((benign_files, per_class), (attack_files, per_class)):
        remaining = quota
        for path in group:
            if remaining <= 0:
                break
            chunk = pd.read_csv(path, nrows=remaining)
            chunk["y_true"] = _label_from_ciciot_filename(path.name)
            frames.append(chunk)
            remaining -= len(chunk)
    if not frames:
        raise FileNotFoundError(f"No readable CICIoT CSVs in {raw_dir}")
    frame = pd.concat(frames, ignore_index=True)
    label_col = None
    for candidate in ("label", "Label", "y_true"):
        if candidate in frame.columns and candidate != "y_true":
            label_col = candidate
            break
    if label_col is not None:
        y = (frame[label_col].astype(str).str.lower() != "benign").astype(np.int8)
        frame["y_true"] = y
    y = frame["y_true"].astype(np.int8)
    feature_cols = [
        c for c in frame.columns
        if c not in {"y_true", label_col} and pd.api.types.is_numeric_dtype(frame[c])
    ]
    if not feature_cols:
        raise ValueError(f"No numeric feature columns; columns={list(frame.columns)[:20]}")
    work = frame[feature_cols].replace([np.inf, -np.inf], np.nan).fillna(0).astype(np.float32)
    work["y_true"] = y.to_numpy()
    idx = np.arange(len(work))
    train_idx, temp_idx = train_test_split(idx, test_size=0.30, random_state=seed, stratify=y)
    val_idx, test_idx = train_test_split(temp_idx, test_size=0.50, random_state=seed, stratify=y[temp_idx])
    meta = {
        "source": "raw_hf_filename_labels",
        "feature_cols": feature_cols,
        "label_col": label_col or "filename",
        "rows": int(len(work)),
        "files": [p.name for p in files],
    }
    return (
        work.iloc[train_idx].reset_index(drop=True),
        work.iloc[val_idx].reset_index(drop=True),
        work.iloc[test_idx].reset_index(drop=True),
        meta,
    )


def _binary_from_label(series: pd.Series) -> np.ndarray:
    if pd.api.types.is_numeric_dtype(series):
        return series.astype(np.int8).to_numpy()
    return (series.astype(str).str.lower() != "benign").astype(np.int8).to_numpy()


def _feature_matrix(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray, list[str]]:
    if "y_true" in df.columns:
        y = df["y_true"].to_numpy(dtype=np.int8)
        cols = [c for c in df.columns if c != "y_true"]
    else:
        label_col = "label" if "label" in df.columns else "Label"
        y = _binary_from_label(df[label_col])
        cols = [c for c in df.columns if c != label_col and pd.api.types.is_numeric_dtype(df[c])]
    x = df[cols].replace([np.inf, -np.inf], np.nan).fillna(0).to_numpy(dtype=np.float32)
    return x, y, cols


@torch.no_grad()
def _predict_scores(model: nn.Module, loader: DataLoader, device: torch.device) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    model.eval()
    scores, labels, ids = [], [], []
    for xb, yb, idb in loader:
        logits = model(xb.to(device))
        prob = torch.softmax(logits, dim=1)[:, 1].cpu().numpy()
        scores.append(prob)
        labels.append(yb.numpy())
        ids.append(idb.numpy())
    return np.concatenate(scores), np.concatenate(labels), np.concatenate(ids)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-rows", type=int, default=80_000)
    parser.add_argument("--seq-len", type=int, default=50)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch-size", type=int, default=256)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    prepared = (args.data / "train" / "train.csv").is_file()
    meta = {"seed": args.seed, "prepared_split": prepared, "device": "cpu"}
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    meta["device"] = str(device)
    meta["torch"] = torch.__version__
    meta["cuda_available"] = bool(torch.cuda.is_available())

    if prepared:
        train_df, val_df, test_df = _load_prepared(args.data, args.max_rows)
        meta["source"] = "prepared_train_val_test"
    else:
        raw_dir = args.data / "raw" if (args.data / "raw").exists() else args.data
        train_df, val_df, test_df, raw_meta = _load_raw_and_split(raw_dir, args.seed, args.max_rows)
        meta.update(raw_meta)

    x_train, y_train, cols = _feature_matrix(train_df)
    x_val, y_val, _ = _feature_matrix(val_df)
    x_test, y_test, _ = _feature_matrix(test_df)
    meta["n_features"] = len(cols)
    meta["counts"] = {
        "train": {"n": int(len(y_train)), "benign": int((y_train == 0).sum()), "attack": int((y_train == 1).sum())},
        "val": {"n": int(len(y_val)), "benign": int((y_val == 0).sum()), "attack": int((y_val == 1).sum())},
        "test": {"n": int(len(y_test)), "benign": int((y_test == 0).sum()), "attack": int((y_test == 1).sum())},
    }

    scaler = MinMaxScaler()
    scaler.fit(x_train)
    x_train_s = scaler.transform(x_train).astype(np.float32)
    x_val_s = scaler.transform(x_val).astype(np.float32)
    x_test_s = scaler.transform(x_test).astype(np.float32)

    # Random Forest on identical rows (target_id = row index within split).
    t0 = time.time()
    rf = RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced_subsample",
        n_jobs=-1,
        random_state=args.seed,
        max_depth=24,
        min_samples_leaf=5,
    )
    rf.fit(x_train_s, y_train)
    rf_val = rf.predict_proba(x_val_s)[:, 1]
    rf_test = rf.predict_proba(x_test_s)[:, 1]
    meta["rf_seconds"] = round(time.time() - t0, 2)

    # CNN–LSTM sequences; target_id aligns to the terminal row of each window.
    seq_len = min(args.seq_len, max(2, len(x_train_s) // 4))
    train_ds = StreamingSequenceDataset(x_train_s, y_train, seq_len)
    val_ds = StreamingSequenceDataset(x_val_s, y_val, seq_len)
    test_ds = StreamingSequenceDataset(x_test_s, y_test, seq_len)
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False)
    test_loader = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False)

    model = CNNLSTM(num_features=x_train_s.shape[1]).to(device)
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    # Class weights from training labels only.
    counts = np.bincount(y_train, minlength=2).astype(np.float32)
    weights = counts.sum() / (2.0 * np.maximum(counts, 1.0))
    criterion = nn.CrossEntropyLoss(weight=torch.tensor(weights, dtype=torch.float32, device=device))

    t1 = time.time()
    model.train()
    for epoch in range(args.epochs):
        total = 0.0
        n = 0
        for xb, yb, _ in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            opt.zero_grad()
            loss = criterion(model(xb), yb)
            loss.backward()
            opt.step()
            total += float(loss.item()) * len(yb)
            n += len(yb)
        print(f"epoch {epoch+1}/{args.epochs} loss={total/max(n,1):.4f}", flush=True)
    meta["cnn_lstm_seconds"] = round(time.time() - t1, 2)

    cnn_val, cnn_val_y, cnn_val_id = _predict_scores(model, val_loader, device)
    cnn_test, cnn_test_y, cnn_test_id = _predict_scores(model, test_loader, device)

    # Restrict RF to the same terminal target_ids used by sequence models.
    rf_val_aligned = rf_val[cnn_val_id]
    rf_test_aligned = rf_test[cnn_test_id]
    assert np.array_equal(y_val[cnn_val_id], cnn_val_y)
    assert np.array_equal(y_test[cnn_test_id], cnn_test_y)

    def pack(split: str, model_name: str, target_ids, y, scores) -> pd.DataFrame:
        return pd.DataFrame({
            "target_id": [f"{split}_{int(i)}" for i in target_ids],
            "y_true": y.astype(int),
            "score_attack": scores.astype(float),
            "model": model_name,
            "seed": args.seed,
        })

    validation = pd.concat([
        pack("val", "RandomForest", cnn_val_id, cnn_val_y, rf_val_aligned),
        pack("val", "CNN-LSTM", cnn_val_id, cnn_val_y, cnn_val),
    ], ignore_index=True)
    test = pd.concat([
        pack("test", "RandomForest", cnn_test_id, cnn_test_y, rf_test_aligned),
        pack("test", "CNN-LSTM", cnn_test_id, cnn_test_y, cnn_test),
    ], ignore_index=True)
    validation.to_csv(args.out / "predictions_validation.csv", index=False)
    test.to_csv(args.out / "predictions_test.csv", index=False)

    budgets = [0.01, 0.005, 0.001, 0.0005]
    result = evaluate(validation, test, budgets)
    result.to_csv(args.out / "matched_far_results.csv", index=False)
    (args.out / "pilot_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    torch.save({"state_dict": model.state_dict(), "meta": meta, "cols": cols}, args.out / "cnn_lstm_pilot.pt")
    print(result.to_string(index=False))
    print(json.dumps({"status": "PASS", "rows": int(len(result)), "out": str(args.out)}))


if __name__ == "__main__":
    main()
