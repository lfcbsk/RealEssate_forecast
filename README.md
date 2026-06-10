# RealEstate Forecast API

Machine Learning-powered API for forecasting real estate transactions using recursive multi-step prediction strategy.

## 🚀 Features

- **Recursive Forecasting**: Multi-step ahead predictions month-by-month
- **ONNX Model Inference**: Fast predictions with optimized ONNX runtime
- **Drift Detection**: Monitor data drift for model reliability
- **MLflow Integration**: Track model metrics and versions
- **Swagger Documentation**: Interactive API docs at `/docs`
- **Docker Ready**: Full containerization support

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| POST | `/api/v1/forecast` | Generate n-month forecast |
| POST | `/api/v1/predict` | Single prediction with custom features |
| POST | `/api/v1/upload` | Batch prediction via file upload |
| GET | `/api/v1/sectors` | List all sectors with statistics |
| GET | `/api/v1/metrics` | Model metrics from MLflow |
| GET | `/api/v1/drift` | Drift detection report |

## 🛠️ Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run API server
python -m src.api.main

# Access Swagger UI
open http://localhost:8000/docs
```

### Docker Deployment

```bash
# Build and run with docker-compose
cd docker
docker-compose up --build

# API available at http://localhost:8000
# Dashboard available at http://localhost:8501
```

## 📦 Project Structure

```
├── src/
│   ├── api/
│   │   ├── main.py          # FastAPI application
│   │   ├── routes.py        # API endpoints
│   │   └── schemas.py       # Pydantic models
│   ├── models/
│   │   └── model_registry.py # ONNX model inference
│   ├── pipeline/
│   │   ├── predict.py       # Recursive forecasting
│   │   └── features.py      # Feature engineering
│   └── monitoring/
│       └── detect_drift.py  # Drift detection
├── docker/
│   ├── api.Dockerfile
│   ├── app.Dockerfile
│   └── docker-compose.yml
└── requirements.txt
```

## 🔍 Example Usage

### Get Forecast

```bash
curl -X POST "http://localhost:8000/api/v1/forecast" \
  -H "Content-Type: application/json" \
  -d '{"n_months": 12}'
```

### Single Prediction

```bash
curl -X POST "http://localhost:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "nearby_sectors": 5,
      "pre_owned": 100,
      "lag_1": 500,
      "lag_2": 480
    }
  }'
```

### Upload File for Batch Prediction

```bash
curl -X POST "http://localhost:8000/api/v1/upload" \
  -F "file=@predictions.csv"
```

## 🧪 Testing

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

## 📊 Monitoring

- **Model Metrics**: Track RMSE, MAE, R² via `/api/v1/metrics`
- **Drift Detection**: Monitor data drift via `/api/v1/drift`
- **Health Checks**: Built-in health endpoint for K8s

## 🚢 Kubernetes Deployment

See `k8s/` directory for Kubernetes manifests including:
- Deployment
- Service
- ConfigMap
- CronJob for retraining

## 📝 License

MIT License
