"""
MLFlow utilities and helpers
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any

import mlflow
from mlflow.entities import Run

logger = logging.getLogger(__name__)

def setup_mlflow_tracking(tracking_uri: str, experiment_name: str) -> None:
    """
    Configure MLFlow tracking
    
    Args:
        tracking_uri: Path to MLFlow backend (e.g., 'file:./mlruns')
        experiment_name: Name of the experiment
    """
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    logger.info(f"MLFlow tracking configured: {tracking_uri}")

def get_or_create_experiment(experiment_name: str) -> str:
    """Get experiment ID, creating if necessary"""
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment:
        return experiment.experiment_id
    else:
        return mlflow.create_experiment(experiment_name)

def get_latest_run(experiment_name: str) -> Optional[Run]:
    """Get the latest completed run from an experiment"""
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if not experiment:
        return None
    
    runs = mlflow.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["start_time DESC"],
        max_results=1
    )
    return runs[0] if runs else None

def log_params_and_metrics(params: Dict[str, Any], metrics: Dict[str, float]) -> None:
    """Log parameters and metrics to MLFlow"""
    if params:
        mlflow.log_params(params)
    if metrics:
        mlflow.log_metrics(metrics)
