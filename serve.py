"""
Clean FastAPI Server for Model Serving
Loads trained model from MLFlow and serves predictions
Uses source modules for configuration and model utilities
"""

import logging
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import mlflow.sklearn

from src.config import (
    MLFLOW_TRACKING_URI,
    MLFLOW_EXPERIMENT_NAME,
    API_HOST,
    API_PORT,
    FEATURE_NAMES,
    CLASS_NAMES
)
from src.model_utils import make_prediction
from src.mlflow_utils import get_latest_run

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="Iris Classifier API",
    description="Serves predictions from MLFlow-trained Random Forest model",
    version="1.0.0"
)

# Global model
MODEL = None

# Request/Response models
class IrisFeatures(BaseModel):
    """Iris flower features"""
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class PredictionResponse(BaseModel):
    """Prediction response"""
    prediction: str
    confidence: float

# Startup event - load model
@app.on_event("startup")
async def startup():
    """Load model from MLFlow on startup"""
    global MODEL
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        
        # Get latest run from experiment
        latest_run = get_latest_run(MLFLOW_EXPERIMENT_NAME)
        
        if latest_run is None:
            raise Exception(f"Experiment '{MLFLOW_EXPERIMENT_NAME}' not found. Run train.py first!")
        
        run_id = latest_run.info.run_id
        
        # Load model
        model_uri = f"runs:/{run_id}/iris-model"
        MODEL = mlflow.sklearn.load_model(model_uri)
        
        logger.info(f"✅ Model loaded successfully from run: {run_id}")
        logger.info(f"📂 Model type: {type(MODEL).__name__}")
    
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        raise

# Health check endpoint
@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": MODEL is not None
    }

# Prediction endpoint
@app.post("/predict", response_model=PredictionResponse)
async def predict(features: IrisFeatures):
    """
    Make a prediction on iris features
    
    Example:
    ```json
    {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    ```
    """
    if MODEL is None:
        raise Exception("Model not loaded")
    
    # Prepare features
    feature_list = [
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width
    ]
    
    # Make prediction using model_utils
    pred_class, confidence = make_prediction(MODEL, feature_list)
    
    # Get species name from class index
    species = CLASS_NAMES[pred_class]
    
    return PredictionResponse(
        prediction=species,
        confidence=confidence
    )

# Root endpoint
@app.get("/")
async def root():
    """API information"""
    return {
        "name": "Iris Classifier API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict"
    }

if __name__ == "__main__":
    logger.info("🚀 Starting Iris Classifier API...")
    logger.info(f"📚 Swagger UI: http://{API_HOST}:{API_PORT}/docs")
    logger.info(f"📖 ReDoc: http://{API_HOST}:{API_PORT}/redoc\n")
    
    uvicorn.run(
        app,
        host=API_HOST,
        port=API_PORT,
        log_level="info"
    )
