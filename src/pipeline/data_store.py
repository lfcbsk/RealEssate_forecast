"""Raw CSV storage, merge, and prediction pipeline (shared by API & Streamlit)."""

from __future__ import annotations

import io
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd

from src.models.model_config import ModelConfig
from src.models.model_registry import ModelRegistry
from src.pipeline.features import (
    apply_zero_sector_rule,
    build_sector_profile,
    compute_sector_stats,
    create_training_features,
)
from src.pipeline.ingest_preprocess import load_and_merge
from src.utils.config import load_config

cfg = load_config()
TARGET = cfg["target"]["column"]
TARGET_TRANSFORM = cfg["target"]["transform"]
TARGET_LOG = f"log_{TARGET}" if TARGET_TRANSFORM == "log1p" else TARGET

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FILE_SPECS = {
    "main": {
        "label": "New house transactions",
        "filename": "new_house_transactions.csv",
    },
    "nearby": {
        "label": "New house transactions (nearby sectors)",
        "filename": "new_house_transactions_nearby_sectors.csv",
    },
    "pre": {
        "label": "Pre-owned house transactions",
        "filename": "pre_owned_house_transactions.csv",
    },
}


def get_train_dir() -> Path:
    candidates = [
        PROJECT_ROOT / "data" / "train",
        (PROJECT_ROOT / cfg["data"]["train_dir"]).resolve(),
    ]
    for path in candidates:
        if path.exists():
            return path
    path = PROJECT_ROOT / "data" / "train"
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_upload_bytes(content: bytes, filename: str) -> pd.DataFrame:
    name = filename.lower()
    if name.endswith(".csv"):
        return pd.read_csv(io.BytesIO(content))
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(io.BytesIO(content))
    raise ValueError(f"Unsupported file type: {filename}")


def read_uploaded_csv(uploaded_file) -> pd.DataFrame:
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)
    raise ValueError(f"Unsupported file type: {uploaded_file.name}")


def _normalise_upload(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "month" not in df.columns:
        raise ValueError("File must contain a 'month' column")
    if "sector" not in df.columns:
        raise ValueError("File must contain a 'sector' column")

    df["month"] = pd.to_datetime(df["month"])
    if df["sector"].dtype == object:
        df["sector"] = df["sector"].astype(str).str.split().str[-1].astype(int)
    else:
        df["sector"] = df["sector"].astype(int)
    return df


def append_raw_to_csv(new_df: pd.DataFrame, csv_path: Path) -> Tuple[pd.DataFrame, int, int]:
    new_df = _normalise_upload(new_df)
    before_rows = 0

    if csv_path.exists():
        existing = pd.read_csv(csv_path)
        if "month" in existing.columns:
            existing["month"] = pd.to_datetime(existing["month"])
        before_rows = len(existing)
        combined = pd.concat([existing, new_df], ignore_index=True)
    else:
        combined = new_df

    combined = combined.drop_duplicates(subset=["month", "sector"], keep="last")
    combined = combined.sort_values(["month", "sector"]).reset_index(drop=True)
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(csv_path, index=False)

    added = len(combined) - before_rows if before_rows else len(combined)
    updated = len(new_df) - added if before_rows else 0
    return combined, added, max(updated, 0)


def save_uploaded_raw_files(
    main_df: pd.DataFrame,
    nearby_df: pd.DataFrame,
    pre_df: pd.DataFrame,
    train_dir: Optional[Path] = None,
) -> Dict[str, Dict[str, int]]:
    train_dir = train_dir or get_train_dir()
    stats: Dict[str, Dict[str, int]] = {}

    for key, df in [("main", main_df), ("nearby", nearby_df), ("pre", pre_df)]:
        path = train_dir / RAW_FILE_SPECS[key]["filename"]
        _, added, updated = append_raw_to_csv(df, path)
        stats[key] = {
            "filename": RAW_FILE_SPECS[key]["filename"],
            "total_rows": len(pd.read_csv(path)),
            "added": added,
            "updated": updated,
        }
    return stats


def get_raw_csv_paths(train_dir: Optional[Path] = None) -> Dict[str, Path]:
    train_dir = train_dir or get_train_dir()
    return {key: train_dir / spec["filename"] for key, spec in RAW_FILE_SPECS.items()}


def load_production_model() -> ModelRegistry:
    if not ModelConfig.MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Production model not found at {ModelConfig.MODEL_PATH}. "
            "Run training first: uv run python -m src.pipeline.training"
        )
    return ModelRegistry()


def load_merged_training_data(train_dir: Optional[Path] = None) -> pd.DataFrame:
    paths = get_raw_csv_paths(train_dir)
    for key, path in paths.items():
        if not path.exists():
            raise FileNotFoundError(f"Missing {RAW_FILE_SPECS[key]['filename']}")

    return load_and_merge(
        path_main=str(paths["main"]),
        path_nearby=str(paths["nearby"]),
        path_pre=str(paths["pre"]),
        build_grid=True,
        verbose=False,
    )


def predict_on_uploaded_months(
    upload_months: pd.Series,
    train_dir: Optional[Path] = None,
) -> pd.DataFrame:
    df = load_merged_training_data(train_dir)
    registry = load_production_model()
    zero_sectors = registry.zero_sectors

    sector_stats = compute_sector_stats(df, TARGET_LOG)
    sector_profile = build_sector_profile(df)
    featured = create_training_features(
        df,
        target_col=TARGET_LOG,
        sector_stats=sector_stats,
        sector_profile=sector_profile,
        keep_nan=False,
    )

    upload_dates = pd.to_datetime(upload_months).normalize().unique()
    predict_df = featured[featured["date"].isin(upload_dates)].copy()
    if predict_df.empty:
        raise ValueError("No rows matched the uploaded month(s) after preprocessing.")

    pred_log = np.clip(registry.predict(predict_df), 0, None).reshape(-1)
    pred_amount = np.expm1(pred_log)
    pred_amount = apply_zero_sector_rule(pred_amount, predict_df["sector"], zero_sectors)
    pred_amount = np.round(pred_amount).astype(int)

    result = predict_df[["date", "sector"]].copy()
    result["predicted_log"] = pred_log
    result["predicted_amount"] = pred_amount
    if TARGET in predict_df.columns:
        result["actual_amount"] = np.expm1(predict_df[TARGET_LOG].clip(lower=0)).astype(int)

    return result.sort_values(["date", "sector"]).reset_index(drop=True)


def process_raw_upload(
    main_df: pd.DataFrame,
    nearby_df: pd.DataFrame,
    pre_df: pd.DataFrame,
) -> Tuple[Dict[str, Dict[str, int]], pd.DataFrame]:
    """Merge 3 raw files into data/train CSVs, then run the prediction pipeline."""
    stats = save_uploaded_raw_files(main_df, nearby_df, pre_df)
    predictions = predict_on_uploaded_months(main_df["month"])
    return stats, predictions
