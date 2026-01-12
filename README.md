# MLOps ML Pipeline - Iris Classification

A production-ready machine learning pipeline demonstrating MLOps best practices with experiment tracking, model serving, and containerization-ready architecture.

## 🎯 Overview

This project implements an end-to-end ML pipeline for Iris flower classification using:
- **Model**: Random Forest Classifier (98.50% test accuracy)
- **Tracking**: MLFlow for experiment management
- **Serving**: FastAPI with Swagger UI
- **Infrastructure**: Modular, testable Python code with centralized configuration

## 📊 Performance

| Metric | Value |
|--------|-------|
| Test Accuracy | 98.50% |
| Train Accuracy | 99.82% |
| Test Precision | 0.9851 |
| Test Recall | 0.9850 |
| Test F1-Score | 0.9850 |

## 🏗️ Project Structure

```
mlops_m2_lab1/
├── train.py              # Training script with MLFlow integration
├── serve.py              # FastAPI server for model serving
├── src/                  # Core modules
│   ├── __init__.py
│   ├── config.py         # Centralized configuration
│   ├── data_utils.py     # Data loading utilities
│   ├── model_utils.py    # Model training & evaluation
│   └── mlflow_utils.py   # MLFlow helpers
├── data/                 # Training data
│   ├── iris_train.json   # 3,998 training samples
│   └── iris_test.json    # 1,000 test samples
├── mlruns/               # MLFlow experiment store
├── venv/                 # Python virtual environment
├── README.md             # This file
└── SRC_STRUCTURE.md      # Detailed module documentation
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Navigate to project directory
cd mlops_m2_lab1

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if needed)
pip install scikit-learn mlflow fastapi uvicorn pydantic
```

### 2. Train Model

```bash
python train.py
```

**Output:**
```
📚 Loading iris training data...
   ✓ Training samples: 3998
   ✓ Test samples: 1000

🤖 Training Random Forest model...
   ✓ Parameters: {...}

📊 Metrics:
   ✓ Train Accuracy: 0.9982 (99.82%)
   ✓ Test Accuracy:  0.9850 (98.50%)
   ✓ Test Precision: 0.9851
   ✓ Test Recall:    0.9850
   ✓ Test F1:        0.9850

✅ Training complete!
```

### 3. View Experiments

```bash
mlflow ui --backend-store-uri file:./mlruns
```

Visit: http://localhost:5000

### 4. Start API Server

```bash
python serve.py
```

**Available endpoints:**
- 📚 Swagger UI: http://localhost:8000/docs
- 📖 ReDoc: http://localhost:8000/redoc
- 💚 Health: http://localhost:8000/health
- 🔮 Predict: POST http://localhost:8000/predict
- 📊 Metrics: http://localhost:8000/metrics

### 5. Make Predictions

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

**Response:**
```json
{
  "prediction": "setosa",
  "confidence": 0.98
}
```

## 📦 Source Modules

### `config.py`
Centralized configuration for the entire pipeline:
```python
from src.config import (
    MLFLOW_TRACKING_URI,
    MLFLOW_EXPERIMENT_NAME,
    TRAIN_DATA_PATH,
    TEST_DATA_PATH,
    TRAIN_PARAMS,
    API_HOST,
    API_PORT
)
```

### `data_utils.py`
Data loading and preprocessing:
```python
from src.data_utils import prepare_dataset

X_train, y_train = prepare_dataset(TRAIN_DATA_PATH)
```

### `model_utils.py`
Model training and evaluation:
```python
from src.model_utils import create_model, train_model, evaluate_model

model = create_model(TRAIN_PARAMS)
model = train_model(model, X_train, y_train)
metrics = evaluate_model(model, X_test, y_test)
```

### `mlflow_utils.py`
MLFlow integration helpers:
```python
from src.mlflow_utils import setup_mlflow_tracking, get_latest_run

setup_mlflow_tracking(MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME)
latest_run = get_latest_run(MLFLOW_EXPERIMENT_NAME)
```

### `prometheus_metrics.py`
Prometheus monitoring and observability:
```python
from src.prometheus_metrics import record_prediction, request_count

# Automatically tracked by middleware:
# - request_count: API request counters
# - request_duration: Request latency histograms
# - model_loaded: Model loading state
# - api_health: API health status
```

## 📊 Prometheus Monitoring

The API exposes Prometheus metrics for observability:

**Metrics Endpoint**: `GET http://localhost:8000/metrics`

**Available Metrics**:
- `iris_api_requests_total` - Total API requests by method, endpoint, status
- `iris_api_request_duration_seconds` - Request latency distribution
- `iris_predictions_total` - Total predictions by class
- `iris_prediction_confidence` - Confidence score distribution
- `iris_model_loaded` - Model loading state (1=loaded, 0=not)
- `iris_model_load_duration_seconds` - Model loading time
- `iris_api_health` - API health status
- `iris_api_active_requests` - Currently active requests

**Example**: Get all iris metrics
```bash
curl http://localhost:8000/metrics | grep "^iris_"
```

**Prometheus Integration** (optional):
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'iris-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
```

## 📊 MLFlow Dashboard

The MLFlow UI provides:
- ✅ Experiment tracking with automatic metrics logging
- ✅ Run comparison and visualization
- ✅ Parameter management
- ✅ Model versioning and artifacts
- ✅ Performance metrics graphs

**Access at:** http://localhost:5000

## 🔍 Code Statistics

| Metric | Value |
|--------|-------|
| Total Python Files | 7 |
| Total Lines of Code | 455 |
| Source Modules | 4 |
| Test Accuracy | 98.50% |
| Training Time | ~2 seconds |

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| ML Framework | scikit-learn |
| Experiment Tracking | MLFlow |
| API Framework | FastAPI |
| ASGI Server | Uvicorn |
| Monitoring | Prometheus Client |
| Data Validation | Pydantic |
| Python Version | 3.14+ |

## 📈 Model Details

**Algorithm**: Random Forest Classifier
- **Estimators**: 100 trees
- **Max Depth**: 10
- **Min Samples Split**: 2
- **Min Samples Leaf**: 1
- **Random State**: 42 (reproducibility)

**Training Data**:
- Samples: 3,998 (80% of iris dataset)
- Features: 4 (sepal length/width, petal length/width)
- Classes: 3 (setosa, versicolor, virginica)

**Evaluation Data**:
- Samples: 1,000 (20% of iris dataset)
- Balanced class distribution

## 🚢 Deployment

The project is structured for easy containerization:

```bash
# Build Docker image
docker build -t mlops-iris:1.0 .

# Run container
docker run -p 8000:8000 mlops-iris:1.0
```

## 📚 Additional Documentation

- [SRC_STRUCTURE.md](SRC_STRUCTURE.md) - Detailed module documentation
- [README_CLEAN.md](README_CLEAN.md) - Quick reference guide
- [CLEANUP_COMPLETE.md](CLEANUP_COMPLETE.md) - Project cleanup history

## 🔗 Repository

**GitHub**: https://github.com/reyrex-1983/mlops_m2_lab1

## 📝 Git Workflow

```bash
# View commit history
git log --oneline

# Check status
git status

# Make changes and commit
git add .
git commit -m "Your message"
git push origin main
```

## ✅ Checklist

- [x] Data loading utilities
- [x] Model training with metrics
- [x] MLFlow experiment tracking
- [x] FastAPI server with Swagger UI
- [x] Prometheus monitoring
- [x] Modular source code
- [x] Centralized configuration
- [x] Git repository
- [x] Documentation

## 🤝 Contributing

1. Create a new branch: `git checkout -b feature/your-feature`
2. Make changes and test
3. Commit: `git commit -m "feat: description"`
4. Push: `git push origin feature/your-feature`
5. Create a Pull Request

## 📄 License

This project is part of MLOps training.

## 🎓 Learning Outcomes

By working through this project, you'll understand:
- ✅ ML pipeline design and best practices
- ✅ Experiment tracking with MLFlow
- ✅ Model serving with FastAPI
- ✅ Observability with Prometheus metrics
- ✅ Modular Python architecture
- ✅ Git version control for ML projects
- ✅ Production-ready code organization

## 📞 Support

For questions or issues, please refer to the documentation or create an issue in the repository.

---

**Last Updated**: January 12, 2026  
**Status**: Production Ready ✅
