from pathlib import Path
import json

import pandas as pd

from src.models.model_config import ModelConfig


def save_reference_dataset(
    df: pd.DataFrame
):
    """
    Save reference dataset used for drift detection.
    """

    path = ModelConfig.REFERENCE_DATA_PATH

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_parquet(
        path,
        index=False
    )

    print(
        f"✓ Saved reference dataset -> {path}"
    )


def load_reference_dataset():

    return pd.read_parquet(
        ModelConfig.REFERENCE_DATA_PATH
    )


def save_reference_statistics(
    df: pd.DataFrame
):

    stats = {}

    for col in df.columns:

        if pd.api.types.is_numeric_dtype(df[col]):

            stats[col] = {
                "mean": float(df[col].mean()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "max": float(df[col].max())
            }

    path = (
        ModelConfig.ARTIFACT_DIR
        / "reference_stats.json"
    )

    with open(path, "w") as f:

        json.dump(
            stats,
            f,
            indent=4
        )

    print(
        f"✓ Saved statistics -> {path}"
    )