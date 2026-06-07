import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, explained_variance_score, mean_absolute_percentage_error, median_absolute_error
def competition_score(y_true, y_pred, eps=1e-12):

    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)

    ape = np.abs(
        y_pred - y_true
    ) / np.maximum(y_true, eps)

    # Stage 1
    bad_rate = (ape > 1.0).mean()
    if bad_rate > 0.30:
        return 0.0
    
    # Stage 2
    good_mask = ape <= 1.0
    D = ape[good_mask]
    if len(D) == 0:
        return 0.0
    mape_D = D.mean()
    good_rate = good_mask.mean()
    score = 1.0 - (mape_D / good_rate)

    return score

def evaluate_regression(y_true, y_pred, verbose=True):
    """
    Regression metrics dashboard
    """

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)

    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    medae = median_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    evs = explained_variance_score(y_true, y_pred)

    # tránh chia cho 0
    mask = y_true > 0
    if mask.sum() > 0:
        mape = np.mean(
            np.abs(y_true[mask] - y_pred[mask])
            / y_true[mask]
        ) * 100
    else:
        mape = np.nan
    bias = np.mean(y_pred - y_true)

    metrics = {
        "rmse": rmse,
        "mae": mae,
        "mse": mse,
        "medae": medae,
        "mape": mape,
        "r2": r2,
        "Explained Variance": evs,
        "Bias": bias,
    }

    return metrics