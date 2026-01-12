"""
Configuration module for ML pipeline and serving
"""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
MLRUNS_DIR = PROJECT_ROOT / "mlruns"

# MLFlow settings
MLFLOW_TRACKING_URI = f"file:{MLRUNS_DIR}"
MLFLOW_EXPERIMENT_NAME = "iris_classification"

# Training settings
TRAIN_DATA_PATH = DATA_DIR / "iris_train.json"
TEST_DATA_PATH = DATA_DIR / "iris_test.json"

# Model settings
MODEL_NAME = "iris-model"
MODEL_TYPE = "RandomForestClassifier"

# Training hyperparameters
TRAIN_PARAMS = {
    "n_estimators": 100,
    "max_depth": 10,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "random_state": 42
}

# API settings
API_HOST = "0.0.0.0"
API_PORT = 8000
API_TITLE = "Iris Classifier API"

# Feature names
FEATURE_NAMES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
CLASS_NAMES = ["setosa", "versicolor", "virginica"]
