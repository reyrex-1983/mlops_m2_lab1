"""
Model training and prediction utilities
"""

import logging
from typing import List, Tuple, Dict, Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logger = logging.getLogger(__name__)

def create_model(params: Dict[str, Any]) -> RandomForestClassifier:
    """Create a Random Forest classifier with given parameters"""
    return RandomForestClassifier(
        n_estimators=params.get("n_estimators", 100),
        max_depth=params.get("max_depth", 10),
        min_samples_split=params.get("min_samples_split", 2),
        min_samples_leaf=params.get("min_samples_leaf", 1),
        random_state=params.get("random_state", 42)
    )

def train_model(
    model: RandomForestClassifier,
    X_train: List[List[float]],
    y_train: List[int]
) -> RandomForestClassifier:
    """Train the model"""
    model.fit(X_train, y_train)
    logger.info("Model training completed")
    return model

def evaluate_model(
    model: RandomForestClassifier,
    X_test: List[List[float]],
    y_test: List[int],
    set_name: str = "test"
) -> Dict[str, float]:
    """
    Evaluate model on test set
    
    Returns:
        Dictionary with metrics: accuracy, precision, recall, f1
    """
    y_pred = model.predict(X_test)
    
    metrics = {
        f"{set_name}_accuracy": accuracy_score(y_test, y_pred),
        f"{set_name}_precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
        f"{set_name}_recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
        f"{set_name}_f1": f1_score(y_test, y_pred, average="weighted", zero_division=0)
    }
    
    logger.info(f"Evaluation metrics ({set_name}): {metrics}")
    return metrics

def make_prediction(model: RandomForestClassifier, features: List[float]) -> Tuple[int, float]:
    """
    Make a prediction for single sample
    
    Args:
        model: Trained classifier
        features: List of 4 iris features
        
    Returns:
        (predicted_class, confidence)
    """
    # Convert to 2D array for sklearn
    sample = [features]
    prediction = model.predict(sample)[0]
    
    # Get confidence (probability of predicted class)
    proba = model.predict_proba(sample)[0]
    confidence = float(proba[prediction])
    
    return prediction, confidence
