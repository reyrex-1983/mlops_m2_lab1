# MLOps Source Code Organization

## Project Structure

```
mlops_m2_lab1/
├── train.py              # Training entry point (refactored to use src/ modules)
├── serve.py              # API server entry point (refactored to use src/ modules)
├── src/                  # Source code modules
│   ├── __init__.py       # Package initialization
│   ├── config.py         # Centralized configuration & paths
│   ├── data_utils.py     # Data loading & preprocessing utilities
│   ├── model_utils.py    # Model training & prediction utilities
│   └── mlflow_utils.py   # MLFlow integration helpers
├── data/                 # Training & test datasets
│   ├── iris_train.json   # 3,998 training samples
│   ├── iris_test.json    # 1,000 test samples
│   ├── iris_data.json
│   └── iris_metadata.json
├── mlruns/               # MLFlow experiment storage
├── venv/                 # Python virtual environment
├── README_CLEAN.md       # Quick start guide
└── CLEANUP_COMPLETE.md   # Cleanup documentation
```

## Source Modules Overview

### `src/config.py`
Centralized configuration for the entire pipeline:
- **Paths**: PROJECT_ROOT, DATA_DIR, MODELS_DIR, MLRUNS_DIR
- **MLFlow Settings**: MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME
- **Data Paths**: TRAIN_DATA_PATH, TEST_DATA_PATH
- **Training Parameters**: TRAIN_PARAMS with hyperparameters
- **API Config**: API_HOST, API_PORT
- **Feature Mappings**: FEATURE_NAMES, CLASS_NAMES

### `src/data_utils.py`
Data loading and preprocessing:
- `load_json_data()` - Load JSON data from file
- `extract_features_and_labels()` - Convert raw data to X, y arrays
- `prepare_dataset()` - One-step data preparation

### `src/model_utils.py`
Model training and evaluation:
- `create_model()` - Create Random Forest with configured params
- `train_model()` - Train the model on data
- `evaluate_model()` - Compute metrics (accuracy, precision, recall, F1)
- `make_prediction()` - Make predictions with confidence scores

### `src/mlflow_utils.py`
MLFlow integration helpers:
- `setup_mlflow_tracking()` - Configure MLFlow tracking URI and experiment
- `get_or_create_experiment()` - Get or create an experiment
- `get_latest_run()` - Retrieve the latest run from an experiment
- `log_params_and_metrics()` - Log parameters and metrics to MLFlow

## Key Improvements

### 1. **Separation of Concerns**
- Configuration centralized in `config.py`
- Data handling in `data_utils.py`
- Model logic in `model_utils.py`
- MLFlow integration in `mlflow_utils.py`

### 2. **Maintainability**
- Easy to modify hyperparameters in one place
- Consistent imports across scripts
- Reusable utilities for future projects

### 3. **Code Reduction**
- Main scripts (`train.py`, `serve.py`) are cleaner and more focused
- No hardcoded values (all in config)
- DRY principle applied throughout

### 4. **Testing Ready**
- Utility functions can be tested independently
- Mocking is easier with separated concerns
- Clear interfaces between modules

## Usage

### Training
```bash
source venv/bin/activate
python train.py
```
**Output**: Trained model logged to MLFlow with metrics

### Serving
```bash
source venv/bin/activate
python serve.py
```
**Output**: API running at http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Predictions: POST to http://localhost:8000/predict

### MLFlow UI
```bash
mlflow ui --backend-store-uri file:./mlruns
```
**Access**: http://localhost:5000

## Statistics

| Metric | Value |
|--------|-------|
| Total Python Files | 7 |
| Total Lines of Code | ~650 |
| Main Scripts | 2 (train.py, serve.py) |
| Utility Modules | 4 (config, data_utils, model_utils, mlflow_utils) |
| Training Samples | 3,998 |
| Test Samples | 1,000 |
| Model Accuracy | 98.50% |

## Dependencies

Installed in `venv/`:
- scikit-learn (ML model)
- mlflow (experiment tracking)
- fastapi (API framework)
- uvicorn (ASGI server)
- pydantic (data validation)

Install with:
```bash
pip install scikit-learn mlflow fastapi uvicorn pydantic
```
