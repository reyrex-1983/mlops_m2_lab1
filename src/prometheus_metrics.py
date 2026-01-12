"""
Prometheus metrics for monitoring ML model and API performance
"""

from prometheus_client import Counter, Histogram, Gauge
import time

# Request metrics
request_count = Counter(
    'iris_api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'iris_api_request_duration_seconds',
    'API request duration in seconds',
    ['endpoint'],
    buckets=(0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0)
)

# Prediction metrics
prediction_count = Counter(
    'iris_predictions_total',
    'Total number of predictions made',
    ['predicted_class']
)

prediction_confidence = Histogram(
    'iris_prediction_confidence',
    'Confidence score distribution of predictions',
    ['predicted_class'],
    buckets=(0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0)
)

# Model metrics
model_loaded = Gauge(
    'iris_model_loaded',
    'Whether the model is currently loaded (1=yes, 0=no)'
)

model_load_duration = Histogram(
    'iris_model_load_duration_seconds',
    'Time taken to load the model',
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0)
)

# Health metrics
api_health = Gauge(
    'iris_api_health',
    'API health status (1=healthy, 0=unhealthy)'
)

active_requests = Gauge(
    'iris_api_active_requests',
    'Number of currently active requests'
)


class MetricsRecorder:
    """Helper class to record metrics for requests"""
    
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.start_time = None
    
    def start(self):
        """Start timing a request"""
        self.start_time = time.time()
        active_requests.inc()
    
    def end(self, status: int):
        """End timing a request and record metrics"""
        if self.start_time:
            duration = time.time() - self.start_time
            request_duration.labels(endpoint=self.endpoint).observe(duration)
            request_count.labels(method='POST', endpoint=self.endpoint, status=status).inc()
        active_requests.dec()


def record_prediction(predicted_class: str, confidence: float):
    """Record a prediction with its confidence score"""
    prediction_count.labels(predicted_class=predicted_class).inc()
    prediction_confidence.labels(predicted_class=predicted_class).observe(confidence)
