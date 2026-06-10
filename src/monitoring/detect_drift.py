"""Drift detection module for monitoring data quality."""

import logging
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def detect_data_drift(
    reference_data: pd.DataFrame,
    current_data: Optional[pd.DataFrame] = None,
    threshold: float = 0.1,
) -> Dict[str, Any]:
    """
    Detect data drift between reference and current data.
    
    If current_data is not provided, uses recent data from reference_data.
    
    Parameters
    ----------
    reference_data : pd.DataFrame
        Historical reference data
    current_data : pd.DataFrame, optional
        Current data to compare against reference
    threshold : float
        Drift threshold (default 0.1)
    
    Returns
    -------
    Dict containing:
        - drift_detected: bool
        - drift_score: float
        - affected_features: List[str]
        - severity: str
        - recommendation: str
    """
    try:
        if current_data is None:
            # Split reference data into two periods
            reference_data = reference_data.sort_values("date")
            split_point = int(len(reference_data) * 0.7)
            reference_data = reference_data.iloc[:split_point]
            current_data = reference_data.iloc[split_point:].copy()
        
        # Get numeric features for comparison
        numeric_cols = reference_data.select_dtypes(include=[np.number]).columns.tolist()
        exclude_cols = {"date", "sector", "amount_new_house_transactions", "log_amount_new_house_transactions"}
        feature_cols = [c for c in numeric_cols if c not in exclude_cols]
        
        if not feature_cols:
            return {
                "drift_detected": False,
                "drift_score": 0.0,
                "affected_features": [],
                "severity": "low",
                "recommendation": "No features available for drift detection",
            }
        
        # Compute PSI (Population Stability Index) for each feature
        drift_scores = {}
        affected_features = []
        
        for col in feature_cols:
            psi = compute_psi(
                reference_data[col].dropna(),
                current_data[col].dropna(),
                buckets=10
            )
            drift_scores[col] = psi
            
            if psi > threshold:
                affected_features.append(col)
        
        # Overall drift score (mean of all feature drifts)
        overall_drift = np.mean(list(drift_scores.values())) if drift_scores else 0.0
        
        # Determine severity
        if overall_drift > 0.25:
            severity = "high"
            recommendation = "Immediate action required: retrain model with recent data"
        elif overall_drift > 0.1:
            severity = "medium"
            recommendation = "Monitor closely and consider retraining soon"
        else:
            severity = "low"
            recommendation = "Continue monitoring, no immediate action needed"
        
        drift_detected = len(affected_features) > 0
        
        logger.info(f"Drift detection completed: {drift_detected}, score={overall_drift:.4f}")
        
        return {
            "drift_detected": drift_detected,
            "drift_score": float(overall_drift),
            "affected_features": affected_features,
            "severity": severity,
            "recommendation": recommendation,
            "feature_scores": drift_scores,
        }
    
    except Exception as e:
        logger.error(f"Drift detection failed: {str(e)}")
        return {
            "drift_detected": False,
            "drift_score": 0.0,
            "affected_features": [],
            "severity": "low",
            "recommendation": f"Error computing drift: {str(e)}",
        }


def compute_psi(
    expected: pd.Series,
    actual: pd.Series,
    buckets: int = 10,
) -> float:
    """
    Compute Population Stability Index (PSI) between two distributions.
    
    PSI < 0.1: No significant change
    0.1 <= PSI < 0.2: Moderate change
    PSI >= 0.2: Significant change
    
    Parameters
    ----------
    expected : pd.Series
        Reference distribution
    actual : pd.Series
        Current distribution
    buckets : int
        Number of bins for discretization
    
    Returns
    -------
    float : PSI value
    """
    if len(expected) == 0 or len(actual) == 0:
        return 0.0
    
    # Create breakpoints based on expected distribution
    breakpoints = np.percentile(expected, np.linspace(0, 100, buckets + 1))
    breakpoints = np.unique(breakpoints)
    
    if len(breakpoints) < 2:
        return 0.0
    
    # Bin both distributions
    expected_counts = np.histogram(expected, bins=breakpoints)[0]
    actual_counts = np.histogram(actual, bins=breakpoints)[0]
    
    # Convert to percentages (add small epsilon to avoid division by zero)
    epsilon = 1e-5
    expected_percents = (expected_counts + epsilon) / (len(expected) + epsilon * buckets)
    actual_percents = (actual_counts + epsilon) / (len(actual) + epsilon * buckets)
    
    # Compute PSI
    psi = np.sum((actual_percents - expected_percents) * np.log(actual_percents / expected_percents))
    
    return float(psi)


def get_drift_report(
    train_data: pd.DataFrame,
    output_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate comprehensive drift report.
    
    Parameters
    ----------
    train_data : pd.DataFrame
        Training data
    output_path : str, optional
        Path to save report (if provided)
    
    Returns
    -------
    Dict containing full drift analysis
    """
    result = detect_data_drift(train_data)
    
    report = {
        "summary": {
            "drift_detected": result["drift_detected"],
            "overall_score": result["drift_score"],
            "severity": result["severity"],
        },
        "details": {
            "affected_features": result["affected_features"],
            "feature_scores": result.get("feature_scores", {}),
        },
        "recommendations": result["recommendation"],
    }
    
    if output_path:
        import json
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2, default=str)
        logger.info(f"Drift report saved to {output_path}")
    
    return report


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create sample data for testing
    np.random.seed(42)
    n_samples = 1000
    
    df = pd.DataFrame({
        "date": pd.date_range("2023-01-01", periods=n_samples, freq="D"),
        "sector": np.random.choice(["District 1", "District 2", "District 3"], n_samples),
        "feature_1": np.random.normal(100, 20, n_samples),
        "feature_2": np.random.normal(50, 10, n_samples),
        "lag_1": np.random.normal(80, 15, n_samples),
    })
    
    result = detect_data_drift(df)
    print(f"Drift detected: {result['drift_detected']}")
    print(f"Drift score: {result['drift_score']:.4f}")
    print(f"Severity: {result['severity']}")
    print(f"Recommendation: {result['recommendation']}")
