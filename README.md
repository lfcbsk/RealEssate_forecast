# RealEssate Forecast

MLOps pipeline for **China Real Estate Demand Prediction** — forecast monthly new-house transaction volumes across 96 sectors using CatBoost, served via FastAPI (ONNX) and a Streamlit dashboard, with MLflow tracking and drift-based retraining.

**Data:** [Kaggle — China Real Estate Demand Prediction](https://www.kaggle.com/competitions/china-real-estate-demand-prediction/data)

---

## Prerequisites

- Python **3.10+**
- Git
- (Optional) Docker & Docker Compose
- Kaggle account to download competition CSVs

---

## Project structure

```
RealEssate_forecast/
├── README.md
├── pyproject.toml                 # Dependencies & pytest config
├── configs/
│   └── config.yaml                # Data paths, CV, Optuna, orchestration gates
├── data/
│   ├── data_source.md             # Dataset notes
│   └── train/                     # Competition CSVs (gitignored — you add these)
│       ├── new_house_transactions.csv
│       ├── new_house_transactions_nearby_sectors.csv
│       └── pre_owned_house_transactions.csv
├── docker/
│   ├── api.Dockerfile             # FastAPI image
│   ├── app.Dockerfile             # Streamlit image
│   └── docker-compose.yml         # API + dashboard services
├── notebooks/
│   ├── eda.ipynb
│   ├── main_nb.ipynb
│   └── variable_dictionary.md
├── src/
│   ├── api/                       # FastAPI REST service
│   │   ├── main.py
│   │   ├── routes.py              # /health, /forecast, /predict, /drift, …
│   │   └── schemas.py
│   ├── app/
│   │   └── streamlit_app.py       # Interactive dashboard
│   ├── models/
│   │   ├── model_config.py        # Artifact paths (artifacts/)
│   │   ├── model_registry.py      # ONNX Runtime inference
│   │   └── retrain.py             # Final fit + save ONNX/pickles
│   ├── monitoring/
│   │   ├── detect_drift.py        # PSI, KS, concept drift
│   │   ├── reference.py           # Reference parquet for drift baseline
│   │   └── log_report.py          # Drift report JSON export
│   ├── pipeline/
│   │   ├── ingest_preprocess.py   # Load/merge CSVs, impute, train/test split
│   │   ├── features.py            # Lag, rolling, regime, sector features
│   │   ├── training.py            # Optuna + TimeSeriesSplit CV + MLflow
│   │   ├── evaluation.py          # Competition score & holdout metrics
│   │   ├── predict.py             # Recursive multi-month forecast
│   │   └── orchestrator.py        # Drift → retrain → registry workflow
│   └── utils/
│       └── config.py
├── tests/                         # pytest suite (unit + integration)
├── artifacts/                     # Model outputs (gitignored — created by training)
│   ├── model.onnx
│   ├── feature_list.pkl
│   ├── sector_stats.pkl
│   ├── sector_profile.pkl
│   ├── zero_sectors.pkl
│   └── reference.parquet
├── reports/                       # Drift monitoring JSON reports
├── mlruns/                        # MLflow experiment tracking
└── .github/workflows/
    ├── pr-checks.yml              # Tests, lint, Docker build on PR
    ├── build-and-push.yml         # Build & push images to GHCR on main
    └── orchestration.yml          # Scheduled drift check + optional retrain
```

---

## End-to-end workflow

### 1. Clone and install

```bash
git clone https://github.com/lfcbsk/RealEssate_forecast.git
cd RealEssate_forecast

pip install -e ".[dev]"
```

### 2. Download data

Place the three Kaggle CSVs under `data/train/`:

```bash
# Requires Kaggle API credentials (~/.kaggle/kaggle.json)
kaggle competitions download -c china-real-estate-demand-prediction -p data/train/
cd data/train && unzip china-real-estate-demand-prediction.zip
```

Expected files (see `configs/config.yaml` → `data.train_dir`):

| File | Description |
|------|-------------|
| `new_house_transactions.csv` | Main target sector transactions |
| `new_house_transactions_nearby_sectors.csv` | Nearby sector features |
| `pre_owned_house_transactions.csv` | Pre-owned market features |

### 3. Train the model

Full pipeline: ingest → feature engineering → Optuna tuning → 5-fold time-series CV → holdout eval → production model → save artifacts.

```bash
python -m src.pipeline.training
```

This will:

1. Load and preprocess data from `data/train/`
2. Tune CatBoost hyperparameters (50 Optuna trials by default)
3. Run leakage-safe TimeSeriesSplit cross-validation
4. Evaluate on temporal holdout
5. Retrain on full data and write artifacts to `artifacts/`:
   - `model.onnx` — production ONNX model
   - `feature_list.pkl`, `sector_stats.pkl`, `sector_profile.pkl`, `zero_sectors.pkl`
6. Log experiments to MLflow (`mlruns/`, experiment: `catboost_timeseries`)

**Tune settings** in `configs/config.yaml`:

```yaml
optimization:
  n_trials: 50      # reduce for faster runs, e.g. 5
cv:
  n_splits: 5
```

**Programmatic training** (from Python):

```python
from src.pipeline.training import run_pipeline

results = run_pipeline(tune=True, n_trials=10)
print(results["test_results"])
```

### 4. Save reference baseline (for drift monitoring)

After the first successful train, save the reference dataset used for drift checks:

```python
from src.pipeline.ingest_preprocess import run as ingest_run
from src.monitoring.reference import save_reference_dataset, save_reference_statistics

df_train, _ = ingest_run(test_ratio=0.2, save_outputs=False)
save_reference_dataset(df_train)
save_reference_statistics(df_train)
```

This writes `artifacts/reference.parquet` and `artifacts/reference_stats.json`.

### 5. Run drift → retrain → registry orchestration

When new data arrives, the orchestrator compares current data against the reference baseline, decides whether to retrain, evaluates holdout metrics, and promotes the model only if registry gates pass.

```bash
# Fast retrain (no Optuna) — recommended for routine checks
python -m src.pipeline.orchestrator --tune false --promote true

# Full retrain with Optuna tuning
python -m src.pipeline.orchestrator --tune true --promote true --n-trials 10
```

**Registry gates** (`configs/config.yaml` → `orchestration.registry`):

| Gate | Default | Meaning |
|------|---------|---------|
| `min_competition_score` | 0.55 | Minimum holdout competition score |
| `min_r2` | 0.0 | Minimum R² |
| `max_mape` | 100.0 | Maximum MAPE (%) |
| `require_improvement_over_current` | false | New model must beat current score |

Drift reports are saved under `reports/`.

**Flow:**

```
New data → drift vs reference → retrain? → holdout eval → gates pass? → promote to artifacts/
```

### 6. Start the API

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Health check |
| `/api/v1/forecast` | POST | Multi-month forecast (`{"n_months": 12}`) |
| `/api/v1/predict` | POST | Single-row prediction from features |
| `/api/v1/sectors` | GET | Sector list and zero-sector info |
| `/api/v1/metrics` | GET | MLflow run metrics |
| `/api/v1/drift` | GET | Drift report |
| `/api/v1/upload` | POST | Upload new CSV data |
| `/docs` | GET | Swagger UI |

**Example forecast:**

```bash
curl -X POST http://localhost:8000/api/v1/forecast \
  -H "Content-Type: application/json" \
  -d '{"n_months": 12}'
```

### 7. Start the Streamlit dashboard

```bash
streamlit run src/app/streamlit_app.py
```

Open [http://localhost:8501](http://localhost:8501) for forecasts, uploads, and drift views.

### 8. Run with Docker (optional)

```bash
cd docker
docker compose up --build
```

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| Dashboard | http://localhost:8501 |

> **Note:** Training writes to `artifacts/`. Mount or copy `artifacts/` into containers before serving. Docker Compose currently mounts `models/` — symlink or copy `artifacts/` → `models/` if needed.

---

## Tests and CI

```bash
# Run all tests
pytest tests/ -v -m "not e2e"

# With coverage (CI gate: 50%)
pytest tests/ --cov=src --cov-fail-under=50
```

**GitHub Actions workflows:**

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `pr-checks.yml` | PR / push to `main`, `develop` | pytest, lint, Docker build |
| `build-and-push.yml` | push to `main`, tags `v*` | Build & push API/app images to GHCR |
| `orchestration.yml` | Weekly + manual dispatch | Drift check and optional retrain |

---

## Configuration reference

`configs/config.yaml`:

```yaml
data:
  train_dir: "../data/train/"

target:
  column: amount_new_house_transactions
  transform: log1p

cv:
  n_splits: 5

optimization:
  n_trials: 50

orchestration:
  drift:
    feature_drift_ratio_threshold: 0.2
    severity_for_retrain: ["medium", "high"]
  registry:
    min_competition_score: 0.55
    min_r2: 0.0
    max_mape: 100.0
```

---

## Typical first-time checklist

1. `pip install -e ".[dev]"`
2. Download CSVs → `data/train/`
3. `python -m src.pipeline.training`
4. Save reference baseline (step 4 above)
5. `uvicorn src.api.main:app --reload`
6. `streamlit run src/app/streamlit_app.py`
7. `pytest tests/ -v` to verify everything works

---

## License

See repository for license details.
