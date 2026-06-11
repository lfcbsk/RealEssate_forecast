RealEssate_forecast/
├── README.md                          # Tài liệu dự án
├── .gitignore                         
├── .env.example                       # MỚI: Mẫu biến môi trường (API keys cloud, v.v.)
├── Makefile                           # Lệnh shortcut (make up, make test, make train)
├── pyproject.toml                     # Quản lý dependencies (Poetry/pip)
├── .github/                           
│   └── workflows/                     
│       ├── pr-checks.yml              # Chạy pytest, lint khi có PR
│       └── build-and-push.yml         # Build docker image và push lên Docker Hub
├── configs/
│   └── config.yaml                    # Cấu hình: đường dẫn cloud storage, threshold drift, v.v.
├── data/
│   ├── data_source.md                 
│   └── raw/                           # Dữ liệu thô (được .gitignore)
├── docker/                            # TRUNG TÂM: Orchestrate mọi thứ bằng Docker Compose
│   ├── api.Dockerfile                 # Image cho FastAPI
│   ├── app.Dockerfile                 # Image cho Streamlit
│   ├── airflow/                       # MỚI: Cấu hình Airflow
│   │   ├── Dockerfile                 # Custom Airflow image (cài thêm src/ của bạn)
│   │   ├── dags/                      # Thư mục chứa DAGs
│   │   │   ├── train_pipeline.py      # DAG: Ingest -> Preprocess -> Train -> Push Cloud
│   │   │   └── monitor_drift.py       # DAG: Chạy hàng tuần, check drift, gửi alert
│   │   └── requirements.txt           # Deps riêng cho Airflow workers
│   ├── prometheus/                    # MỚI: Cấu hình Prometheus
│   │   └── prometheus.yml             # Khai báo targets (API metrics, Node exporter)
│   ├── grafana/                       # MỚI: Cấu hình Grafana
│   │   ├── provisioning/
│   │   │   ├── datasources/
│   │   │   │   └── prometheus.yml     # Tự động kết nối Prometheus khi khởi động
│   │   │   └── dashboards/
│   │   │       └── mlops-dashboard.json # Dashboard theo dõi MAE, Drift Score, API latency
│   └── docker-compose.yml             # File duy nhất để chạy toàn bộ hệ thống
├── notebooks/                         
│   ├── eda.ipynb                      
│   └── main_nb.ipynb                  
├── scripts/                           # MỚI: Script tiện ích
│   ├── upload_artifacts.py            # Script đẩy model.pkl, features.pkl lên Cloud
│   └── download_artifacts.py          # Script tải artifacts từ Cloud về khi API khởi động
├── src/                               
│   ├── api/                           # FastAPI service
│   ├── app/                           # Streamlit dashboard
│   ├── models/                        # Model registry (logic load/save từ Cloud)
│   ├── monitoring/                    # Drift detection, logging
│   └── pipeline/                      # Ingest, features, training, evaluation
└── tests/                             
    ├── conftest.py
    ├── test_evaluate.py
    ├── test_features.py
    ├── test_ingest.py
    └── test_drift.py