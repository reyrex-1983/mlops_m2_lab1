# Docker Setup Guide

## Overview

This guide explains how to run the entire MLOps pipeline in Docker containers, including:
- FastAPI server for model serving with Prometheus metrics
- MLFlow tracking server for experiment management
- Prometheus for metrics collection
- Grafana for visualization

## Prerequisites

- Docker (v20.10+)
- Docker Compose (v1.29+)

Install Docker from: https://docs.docker.com/get-docker/

## Project Structure

```
mlops_m2_lab1/
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Multi-container orchestration
├── prometheus.yml          # Prometheus configuration
├── .dockerignore          # Files to exclude from build
├── train.py               # Training script
├── serve.py               # FastAPI server
├── src/                   # Source modules
├── data/                  # Training data
└── requirements.txt       # Python dependencies
```

## Quick Start with Docker Compose

### 1. Start All Services

```bash
# Navigate to project directory
cd mlops_m2_lab1

# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

### 2. Services Running

After `docker-compose up -d`, the following services are available:

| Service | URL | Purpose |
|---------|-----|---------|
| FastAPI | http://localhost:8000 | Model serving + metrics |
| MLFlow UI | http://localhost:5000 | Experiment tracking |
| Prometheus | http://localhost:9090 | Metrics collection |
| Grafana | http://localhost:3000 | Visualization |

### 3. Test the API

```bash
# Health check
curl http://localhost:8000/health

# View Swagger UI
open http://localhost:8000/docs

# Make a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, 
       "petal_length": 1.4, "petal_width": 0.2}'

# View Prometheus metrics
curl http://localhost:8000/metrics | grep "^iris_"
```

### 4. Stop All Services

```bash
docker-compose down

# Remove volumes (data persistence)
docker-compose down -v
```

## Individual Container Management

### Build API Image

```bash
docker build -t iris-api:1.0 .
```

### Run API Container Only

```bash
docker run -d \
  -p 8000:8000 \
  -v $(pwd)/mlruns:/app/mlruns \
  -v $(pwd)/data:/app/data \
  --name iris-api \
  iris-api:1.0
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f mlflow
docker-compose logs -f prometheus
```

### Execute Commands in Container

```bash
# Run training in container
docker-compose exec api python train.py

# Access container shell
docker-compose exec api bash

# Check Python version
docker-compose exec api python --version
```

## Docker Configuration Details

### Dockerfile

- **Base Image**: `python:3.14-slim` (lightweight)
- **Working Directory**: `/app`
- **Exposed Ports**: 8000 (API), 5000 (MLFlow)
- **Health Check**: Verifies API endpoint every 30 seconds
- **Default Command**: Runs `serve.py`

### docker-compose.yml

#### MLFlow Service
- Runs MLFlow UI on port 5000
- Stores experiments in `./mlruns` volume
- Uses shared code volumes for training/serving

#### API Service
- Builds from Dockerfile
- Runs on port 8000
- Mounts data and mlruns volumes
- Depends on MLFlow for health check

#### Prometheus Service
- Scrapes metrics from API every 5 seconds
- Stores data in `prometheus_data` volume
- Configuration: `prometheus.yml`

#### Grafana Service
- Visualization tool on port 3000
- Default credentials: admin/admin
- Connected to Prometheus data source
- Persistent storage in `grafana_data` volume

## Volume Persistence

Docker Compose uses named volumes for data persistence:

```yaml
volumes:
  prometheus_data:   # Prometheus time-series database
  grafana_data:      # Grafana dashboards and settings
```

Mounted paths (shared with host):
- `./mlruns` → `/app/mlruns` (MLFlow experiments)
- `./data` → `/app/data` (Training data)

## Environment Variables

```bash
PYTHONUNBUFFERED=1              # Real-time Python output
MLFLOW_TRACKING_URI=file:./mlruns  # Local MLFlow storage
```

## Production Deployment

### Using Docker Hub

```bash
# Build and tag
docker build -t username/iris-api:1.0 .

# Push to Docker Hub
docker push username/iris-api:1.0

# Pull and run
docker run -p 8000:8000 username/iris-api:1.0
```

### Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml iris-mlops

# View services
docker service ls

# Remove stack
docker stack rm iris-mlops
```

### Kubernetes (via Docker Desktop)

```bash
# Convert compose to Kubernetes manifest
kompose convert -f docker-compose.yml

# Deploy to Kubernetes
kubectl apply -f *.yaml
```

## Networking

All services communicate through Docker's internal network:

```
┌─────────────────────────────────────────────┐
│        Docker Network (iris-mlops)          │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   API    │  │ MLFlow   │  │Prometheus│  │
│  │ :8000    │  │  :5000   │  │  :9090   │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│       ↑              ↑              ↑       │
│       └──────────────┴──────────────┘       │
│                                             │
│  ┌──────────────────────────────────────┐  │
│  │        Grafana (port 3000)           │  │
│  └──────────────────────────────────────┘  │
│                                             │
└─────────────────────────────────────────────┘
```

Service names for internal communication:
- `api:8000` - FastAPI server
- `mlflow:5000` - MLFlow UI
- `prometheus:9090` - Prometheus
- `grafana:3000` - Grafana

## Resource Management

### Limit Container Resources

```bash
# In docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Monitor Resource Usage

```bash
docker stats
docker-compose stats
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs api

# Verify ports aren't in use
lsof -i :8000
lsof -i :5000
lsof -i :9090
lsof -i :3000

# Restart services
docker-compose restart
```

### Data Persistence Issues

```bash
# View volumes
docker volume ls

# Inspect volume
docker volume inspect <volume_name>

# Clean up
docker volume prune
```

### Network Issues

```bash
# Inspect network
docker network inspect <network_name>

# Test connectivity between containers
docker-compose exec api ping mlflow
docker-compose exec prometheus ping api
```

### Clear Everything

```bash
# Stop all containers
docker-compose down

# Remove all volumes
docker volume prune

# Remove dangling images
docker image prune

# Full cleanup (careful!)
docker system prune -a --volumes
```

## Building Custom Images

### Build with Tag

```bash
docker build -t iris-api:1.0 -t iris-api:latest .
```

### Build for Specific Platform

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t iris-api:1.0 .
```

### View Build History

```bash
docker image history iris-api:1.0
```

## Security Best Practices

1. **Never commit secrets**: Use `.env` file for sensitive data
2. **Minimal base image**: Use `slim` or `alpine` variants
3. **Run as non-root**: Add user in Dockerfile
4. **Health checks**: Ensure all services have health checks
5. **Resource limits**: Set CPU and memory limits
6. **Network isolation**: Use dedicated networks per environment

## Monitoring in Docker

### Docker Events

```bash
docker events --filter type=container
```

### Service Logs

```bash
# Follow logs
docker-compose logs -f --tail=100

# Filter by service
docker-compose logs -f api mlflow
```

### Health Status

```bash
# Check health of all services
docker-compose ps

# Inspect service health
docker inspect <container_id> | grep -A 5 Health
```

## Performance Optimization

### Build Cache

```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build -t iris-api:1.0 .
```

### Layer Optimization

- Put frequently changing code last in Dockerfile
- Use multi-stage builds for smaller images
- Combine RUN commands to reduce layers

### Startup Performance

- Use volume mounts for mlruns (faster than copying)
- Pre-download dependencies in Dockerfile
- Use `.dockerignore` to exclude unnecessary files

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Image
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build image
        run: docker build -t iris-api:${{ github.sha }} .
      - name: Push to registry
        run: docker push myregistry/iris-api:${{ github.sha }}
```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Kubernetes with Docker](https://docs.docker.com/get-started/kube-deploy/)

---

**Status**: ✅ Docker setup configured  
**Version**: 1.0.0  
**Last Updated**: January 12, 2026
