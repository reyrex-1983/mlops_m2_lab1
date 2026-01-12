"""
Clean FastAPI Server for Model Serving
Loads trained model from MLFlow and serves predictions
Uses source modules for configuration and model utilities
Includes Prometheus metrics for monitoring
"""

import logging
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import mlflow.sklearn
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

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
from src.prometheus_metrics import (
    model_loaded, api_health, record_prediction, 
    request_duration, request_count, model_load_duration
)

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
    import time
    start_time = time.time()
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
        
        # Record metrics
        load_time = time.time() - start_time
        model_load_duration.observe(load_time)
        model_loaded.set(1)
        api_health.set(1)
        
        logger.info(f"✅ Model loaded successfully from run: {run_id}")
        logger.info(f"📂 Model type: {type(MODEL).__name__}")
        logger.info(f"⏱️  Model load time: {load_time:.2f}s")
    
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        model_loaded.set(0)
        api_health.set(0)
        raise


# Middleware for tracking request metrics
@app.middleware("http")
async def track_metrics(request: Request, call_next):
    """Track request metrics using Prometheus"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # Record metrics
    endpoint = request.url.path
    request_duration.labels(endpoint=endpoint).observe(process_time)
    request_count.labels(
        method=request.method, 
        endpoint=endpoint, 
        status=response.status_code
    ).inc()
    
    return response


import time

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
    
    # Record prediction metrics
    species = CLASS_NAMES[pred_class]
    record_prediction(species, confidence)
    
    # Get species name from class index
    species = CLASS_NAMES[pred_class]
    
    return PredictionResponse(
        prediction=species,
        confidence=confidence
    )

# Prometheus metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return generate_latest()

# Root endpoint
@app.get("/")
async def root():
    """API information"""
    return {
        "name": "Iris Classifier API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict",
        "metrics": "/metrics"
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
