"""
Clean Training Script with MLFlow Tracking
Trains Random Forest on Iris dataset and logs to MLFlow
Uses source modules for configuration, data loading, and model utilities
"""

import logging
import mlflow
import mlflow.sklearn

from src.config import (
    MLFLOW_TRACKING_URI,
    MLFLOW_EXPERIMENT_NAME,
    TRAIN_DATA_PATH,
    TEST_DATA_PATH,
    TRAIN_PARAMS
)
from src.data_utils import prepare_dataset
from src.model_utils import create_model, train_model, evaluate_model
from src.mlflow_utils import setup_mlflow_tracking

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def main():
    """Train model with MLFlow tracking"""
    
    # Setup MLFlow
    setup_mlflow_tracking(MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME)
    
    logger.info("📚 Loading iris training data...")
    X_train, y_train = prepare_dataset(TRAIN_DATA_PATH)
    X_test, y_test = prepare_dataset(TEST_DATA_PATH)
    
    logger.info(f"   ✓ Training samples: {len(X_train)}")
    logger.info(f"   ✓ Test samples: {len(X_test)}")
    
    # Start MLFlow run
    with mlflow.start_run(run_name="iris-random-forest"):
        logger.info("\n🤖 Training Random Forest model...")
        logger.info(f"   ✓ Parameters: {TRAIN_PARAMS}")
        
        # Create, train, and evaluate model
        model = create_model(TRAIN_PARAMS)
        model = train_model(model, X_train, y_train)
        
        # Log parameters to MLFlow
        mlflow.log_params(TRAIN_PARAMS)
        
        # Evaluate on train and test sets
        train_metrics = evaluate_model(model, X_train, y_train, "train")
        test_metrics = evaluate_model(model, X_test, y_test, "test")
        
        # Combine metrics
        all_metrics = {**train_metrics, **test_metrics}
        
        # Log metrics to MLFlow
        mlflow.log_metrics(all_metrics)
        
        logger.info(f"\n📊 Metrics:")
        logger.info(f"   ✓ Train Accuracy: {train_metrics['train_accuracy']:.4f} ({train_metrics['train_accuracy']*100:.2f}%)")
        logger.info(f"   ✓ Test Accuracy:  {test_metrics['test_accuracy']:.4f} ({test_metrics['test_accuracy']*100:.2f}%)")
        logger.info(f"   ✓ Test Precision: {test_metrics['test_precision']:.4f}")
        logger.info(f"   ✓ Test Recall:    {test_metrics['test_recall']:.4f}")
        logger.info(f"   ✓ Test F1:        {test_metrics['test_f1']:.4f}")
        
        # Log model to MLFlow
        mlflow.sklearn.log_model(model, "iris-model")
        
        logger.info(f"\n✅ Training complete!")
        logger.info(f"📂 MLFlow tracking URI: {MLFLOW_TRACKING_URI}")
        logger.info(f"📊 Experiment: {MLFLOW_EXPERIMENT_NAME}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
