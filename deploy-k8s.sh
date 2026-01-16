#!/bin/bash
# Kubernetes Deployment Script for MLOps Iris Project

set -e  # Exit on error

echo "🚀 Starting Kubernetes Deployment..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found. Please install kubectl first.${NC}"
    exit 1
fi

# Check if cluster is running
echo -e "${BLUE}📡 Checking Kubernetes cluster...${NC}"
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}❌ Kubernetes cluster not running.${NC}"
    echo -e "${YELLOW}Please enable Kubernetes in Docker Desktop:${NC}"
    echo "  1. Open Docker Desktop"
    echo "  2. Settings → Kubernetes"
    echo "  3. Enable Kubernetes"
    echo "  4. Apply & Restart"
    exit 1
fi

echo -e "${GREEN}✅ Kubernetes cluster is running${NC}"
echo ""

# Step 1: Create namespace
echo -e "${BLUE}📦 Step 1: Creating namespace 'mlops'...${NC}"
kubectl apply -f k8s/namespace.yaml
echo -e "${GREEN}✅ Namespace created${NC}"
echo ""

# Step 2: Apply all manifests
echo -e "${BLUE}🔧 Step 2: Deploying all services...${NC}"
kubectl apply -f k8s/prometheus-configmap.yaml
kubectl apply -f k8s/prometheus-deployment.yaml
kubectl apply -f k8s/grafana-deployment.yaml
kubectl apply -f k8s/mlflow-deployment.yaml
kubectl apply -f k8s/api-deployment.yaml
echo -e "${GREEN}✅ All manifests applied${NC}"
echo ""

# Step 3: Wait for deployments
echo -e "${BLUE}⏳ Step 3: Waiting for pods to be ready...${NC}"
echo "This may take a minute..."
kubectl wait --for=condition=ready pod -l app=iris-api -n mlops --timeout=120s 2>/dev/null || true
kubectl wait --for=condition=ready pod -l app=mlflow -n mlops --timeout=120s 2>/dev/null || true
kubectl wait --for=condition=ready pod -l app=prometheus -n mlops --timeout=120s 2>/dev/null || true
kubectl wait --for=condition=ready pod -l app=grafana -n mlops --timeout=120s 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ Pods are ready!${NC}"
echo ""

# Display status
echo -e "${BLUE}📊 Deployment Status:${NC}"
kubectl get pods -n mlops
echo ""
kubectl get svc -n mlops
echo ""

# Port forwarding instructions
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo ""
echo -e "${YELLOW}📍 To access the services, run these port-forward commands:${NC}"
echo ""
echo -e "${BLUE}# In separate terminals:${NC}"
echo "kubectl -n mlops port-forward svc/iris-api 8001:8000"
echo "kubectl -n mlops port-forward svc/mlflow 5001:5000"
echo "kubectl -n mlops port-forward svc/prometheus 9091:9090"
echo "kubectl -n mlops port-forward svc/grafana 3001:3000"
echo ""
echo -e "${BLUE}# Or run them all in background:${NC}"
echo "kubectl -n mlops port-forward svc/iris-api 8001:8000 &"
echo "kubectl -n mlops port-forward svc/mlflow 5001:5000 &"
echo "kubectl -n mlops port-forward svc/prometheus 9091:9090 &"
echo "kubectl -n mlops port-forward svc/grafana 3001:3000 &"
echo ""
echo -e "${YELLOW}📱 Service URLs (after port-forwarding):${NC}"
echo "  • Iris API:    http://localhost:8001/docs"
echo "  • MLFlow UI:   http://localhost:5001"
echo "  • Prometheus:  http://localhost:9091"
echo "  • Grafana:     http://localhost:3001 (admin/admin)"
echo ""
echo -e "${BLUE}🧪 Test the API:${NC}"
echo 'curl -X POST http://localhost:8001/predict -H "Content-Type: application/json" -d '"'"'{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'"'"
echo ""
echo -e "${YELLOW}💡 Useful commands:${NC}"
echo "  • View logs:     kubectl -n mlops logs -f deployment/iris-api"
echo "  • Delete all:    kubectl delete namespace mlops"
echo "  • Stop port-fwd: pkill -f 'kubectl.*port-forward'"
echo ""
