from scipy.stats import ks_2samp

import numpy as np
import pandas as pd


def ks_test_feature(
    reference: pd.Series,
    current: pd.Series,
    alpha: float = 0.05
):

    reference = reference.dropna()
    current = current.dropna()

    statistic, pvalue = ks_2samp(
        reference,
        current
    )

    return {
        "statistic": statistic,
        "pvalue": pvalue,
        "drift": pvalue < alpha
    }


def detect_feature_drift(
    reference_df: pd.DataFrame,
    current_df: pd.DataFrame,
    alpha: float = 0.05
):

    report = {}

    numeric_cols = (
        reference_df
        .select_dtypes(
            include=np.number
        )
        .columns
    )

    for col in numeric_cols:

        result = ks_test_feature(
            reference_df[col],
            current_df[col],
            alpha
        )

        report[col] = result

    drifted = sum(
        v["drift"]
        for v in report.values()
    )

    drift_ratio = (
        drifted / len(report)
        if report else 0
    )

    return {
        "feature_report": report,
        "drift_ratio": drift_ratio,
        "drift_detected": drift_ratio > 0.3
    }


def detect_concept_drift(
    baseline_mae: float,
    current_mae: float,
    threshold: float = 0.2
):

    degradation = (
        current_mae - baseline_mae
    ) / baseline_mae

    return {
        "baseline_mae": baseline_mae,
        "current_mae": current_mae,
        "performance_drop": degradation,
        "concept_drift": degradation > threshold
    }