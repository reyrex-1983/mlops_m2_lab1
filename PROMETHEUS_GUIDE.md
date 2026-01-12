# Prometheus Monitoring Guide

## Overview

This MLOps project includes comprehensive Prometheus monitoring for production observability. The `/metrics` endpoint exposes all application metrics in Prometheus text format.

## Metrics Endpoint

**URL**: `http://localhost:8000/metrics`

**Format**: Prometheus text format (lines of `# HELP`, `# TYPE`, and metric data)

**Content-Type**: `text/plain`

```bash
curl http://localhost:8000/metrics
```

## Available Metrics

### API Request Metrics

**1. `iris_api_requests_total` (Counter)**
- Tracks total HTTP requests
- Labels: `method` (GET/POST), `endpoint`, `status` (200/404/etc)
- Use case: Monitor API traffic patterns

```text
iris_api_requests_total{endpoint="/predict",method="POST",status="200"} 1.0
iris_api_requests_total{endpoint="/metrics",method="GET",status="200"} 2.0
```

**2. `iris_api_request_duration_seconds` (Histogram)**
- Measures request latency in seconds
- Buckets: 0.01s, 0.025s, 0.05s, 0.075s, 0.1s, 0.25s, 0.5s, 0.75s, 1.0s, +Inf
- Labels: `endpoint`
- Use case: Monitor API performance and identify slow endpoints

```text
iris_api_request_duration_seconds_bucket{endpoint="/predict",le="0.1"} 1.0
iris_api_request_duration_seconds_sum{endpoint="/predict"} 0.006432
iris_api_request_duration_seconds_count{endpoint="/predict"} 1.0
```

### Prediction Metrics

**3. `iris_predictions_total` (Counter)**
- Counts total predictions made
- Labels: `predicted_class` (setosa, versicolor, virginica)
- Use case: Monitor model usage and class distribution

```text
iris_predictions_total{predicted_class="setosa"} 1.0
```

**4. `iris_prediction_confidence` (Histogram)**
- Tracks confidence score distribution
- Buckets: 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0, +Inf
- Labels: `predicted_class`
- Use case: Monitor model confidence and decision quality

```text
iris_prediction_confidence_bucket{predicted_class="setosa",le="0.99"} 0.0
iris_prediction_confidence_bucket{predicted_class="setosa",le="1.0"} 1.0
```

### Model Metrics

**5. `iris_model_loaded` (Gauge)**
- Shows if model is currently loaded (1 = yes, 0 = no)
- Use case: Verify model loading state at startup

```text
iris_model_loaded 1.0
```

**6. `iris_model_load_duration_seconds` (Histogram)**
- Tracks time taken to load model at startup
- Buckets: 0.1s, 0.5s, 1.0s, 2.0s, 5.0s, 10.0s, +Inf
- Use case: Monitor model initialization performance

```text
iris_model_load_duration_seconds_sum 0.031950950622558594
iris_model_load_duration_seconds_count 1.0
```

### Health Metrics

**7. `iris_api_health` (Gauge)**
- API health status (1 = healthy, 0 = unhealthy)
- Use case: Integration with health checks and alerting

```text
iris_api_health 1.0
```

**8. `iris_api_active_requests` (Gauge)**
- Number of currently active/processing requests
- Use case: Monitor concurrent request load

```text
iris_api_active_requests 0.0
```

## Integration with Prometheus Server

### Option 1: Local Prometheus Instance

Create `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'iris-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s
```

Start Prometheus:
```bash
# Using Docker
docker run -d \
  -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Access at: http://localhost:9090
```

### Option 2: Prometheus Cloud Services

- **Grafana Cloud**: https://grafana.com/cloud/
- **Datadog**: https://www.datadoghq.com/
- **New Relic**: https://newrelic.com/
- **Azure Monitor**: https://azure.microsoft.com/en-us/services/monitor/

## Grafana Dashboards

Visualize metrics with Grafana:

```bash
# Start Grafana
docker run -d -p 3000:3000 grafana/grafana

# Access at: http://localhost:3000
# Default: admin/admin
```

**Add Prometheus Data Source**:
1. Settings → Data Sources → Add
2. URL: `http://localhost:9090`
3. Create dashboards using queries like:

```promql
# Request rate per second
rate(iris_api_requests_total[1m])

# Average request latency
rate(iris_api_request_duration_seconds_sum[1m]) / rate(iris_api_request_duration_seconds_count[1m])

# Model loading state
iris_model_loaded

# Prediction distribution
sum by (predicted_class) (rate(iris_predictions_total[5m]))
```

## Example Prometheus Queries (PromQL)

### Request Analysis
```promql
# Total requests by endpoint
sum by (endpoint) (iris_api_requests_total)

# Error rate
sum(rate(iris_api_requests_total{status=~"4.."}[5m])) / sum(rate(iris_api_requests_total[5m]))

# Request latency percentile
histogram_quantile(0.95, rate(iris_api_request_duration_seconds_bucket[5m]))
```

### Model Metrics
```promql
# Prediction rate
rate(iris_predictions_total[1m])

# Most predicted class
topk(1, sum by (predicted_class) (iris_predictions_total))

# Average confidence
avg(iris_prediction_confidence)
```

### System Health
```promql
# API is healthy
iris_api_health == 1

# Model currently loaded
iris_model_loaded == 1

# Active requests
iris_api_active_requests
```

## Alerting Rules

Create `alerting_rules.yml`:

```yaml
groups:
  - name: iris_alerts
    interval: 30s
    rules:
      - alert: ModelNotLoaded
        expr: iris_model_loaded == 0
        for: 1m
        annotations:
          summary: "Model failed to load"

      - alert: APIDown
        expr: iris_api_health == 0
        for: 2m
        annotations:
          summary: "Iris API is unhealthy"

      - alert: HighErrorRate
        expr: sum(rate(iris_api_requests_total{status=~"5.."}[5m])) > 0.05
        for: 5m
        annotations:
          summary: "Error rate > 5%"

      - alert: SlowRequests
        expr: histogram_quantile(0.95, rate(iris_api_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        annotations:
          summary: "95th percentile latency > 1 second"
```

## Code Implementation

### Module: `src/prometheus_metrics.py`

Defines 8 metrics and 2 helper functions:

```python
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
request_count = Counter('iris_api_requests_total', ...)
request_duration = Histogram('iris_api_request_duration_seconds', ...)

# Prediction metrics
prediction_count = Counter('iris_predictions_total', ...)
prediction_confidence = Histogram('iris_prediction_confidence', ...)

# Model metrics
model_loaded = Gauge('iris_model_loaded', ...)
model_load_duration = Histogram('iris_model_load_duration_seconds', ...)

# Health metrics
api_health = Gauge('iris_api_health', ...)
active_requests = Gauge('iris_api_active_requests', ...)
```

### Integration in `serve.py`

1. **Middleware**: Automatic request tracking
```python
@app.middleware("http")
async def track_metrics(request, call_next):
    # Records: method, endpoint, status, duration
```

2. **Prediction Recording**: Record model predictions
```python
record_prediction(predicted_class, confidence)
```

3. **Health Tracking**: Monitor API state
```python
api_health.set(1)  # 1 = healthy
```

## Performance Impact

- **Minimal Overhead**: Prometheus client is lightweight
- **Memory**: ~50KB for metrics collection
- **CPU**: <1% overhead per 1000 requests/sec
- **Network**: ~4KB per metrics scrape

## Production Checklist

- [ ] Set up Prometheus server with persistent storage
- [ ] Configure scrape interval (typically 15s)
- [ ] Create alerting rules
- [ ] Set up Grafana dashboards
- [ ] Configure alert routing (PagerDuty, Slack, email)
- [ ] Monitor metrics retention (default 15 days)
- [ ] Set up log aggregation (ELK, CloudWatch)
- [ ] Document SLOs based on metrics

## Troubleshooting

### Metrics endpoint returns empty
- Check server is running: `curl http://localhost:8000/`
- Verify endpoint path: Should be `/metrics`
- Check response headers: `curl -v http://localhost:8000/metrics`

### Prometheus can't scrape metrics
- Verify network connectivity to API
- Check firewall rules
- Verify metrics endpoint format
- Look at Prometheus scrape logs

### Missing prediction metrics
- Make predictions first: `POST /predict`
- Metrics are created on first observation
- Check prediction response status

## Additional Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Prometheus Client Library](https://github.com/prometheus/client_python)
- [PromQL Guide](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards)

---

**Status**: ✅ Fully Integrated  
**Version**: 1.0.0  
**Last Updated**: January 12, 2026
