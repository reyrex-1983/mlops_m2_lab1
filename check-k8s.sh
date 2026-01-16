#!/bin/bash
# Kubernetes Setup Checker and Helper Script

set -e

echo "🔍 Kubernetes Installation Checker"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Check kubectl
echo -e "${BLUE}1. Checking kubectl...${NC}"
if command -v kubectl &> /dev/null; then
    VERSION=$(kubectl version --client --short 2>/dev/null | grep -i client || kubectl version --client 2>/dev/null | head -1)
    echo -e "${GREEN}   ✅ kubectl is installed${NC}"
    echo "      $VERSION"
else
    echo -e "${RED}   ❌ kubectl is NOT installed${NC}"
    echo -e "${YELLOW}   Install with: brew install kubectl${NC}"
    exit 1
fi
echo ""

# 2. Check Docker
echo -e "${BLUE}2. Checking Docker...${NC}"
if command -v docker &> /dev/null; then
    if docker info &> /dev/null; then
        echo -e "${GREEN}   ✅ Docker is running${NC}"
        DOCKER_VERSION=$(docker version --format '{{.Server.Version}}' 2>/dev/null)
        echo "      Docker version: $DOCKER_VERSION"
    else
        echo -e "${RED}   ❌ Docker is installed but NOT running${NC}"
        echo -e "${YELLOW}   Please start Docker Desktop${NC}"
        exit 1
    fi
else
    echo -e "${RED}   ❌ Docker is NOT installed${NC}"
    exit 1
fi
echo ""

# 3. Check Kubernetes Cluster
echo -e "${BLUE}3. Checking Kubernetes cluster...${NC}"
if kubectl cluster-info &> /dev/null; then
    echo -e "${GREEN}   ✅ Kubernetes cluster is running!${NC}"
    
    # Get cluster info
    CONTEXT=$(kubectl config current-context 2>/dev/null)
    echo "      Current context: $CONTEXT"
    
    # Get nodes
    echo ""
    echo -e "${BLUE}   Cluster Nodes:${NC}"
    kubectl get nodes
    
    echo ""
    echo -e "${GREEN}🎉 SUCCESS! Kubernetes is ready to use!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Deploy your project: ./deploy-k8s.sh"
    echo "  2. Or manually apply: kubectl apply -f k8s/"
    echo ""
    
else
    echo -e "${RED}   ❌ Kubernetes cluster is NOT running${NC}"
    echo ""
    echo -e "${YELLOW}📝 To enable Kubernetes:${NC}"
    echo ""
    echo "   ${BLUE}Option 1: Docker Desktop (Recommended)${NC}"
    echo "   ────────────────────────────────────────"
    echo "   1. Open Docker Desktop"
    echo "   2. Click Settings (gear icon)"
    echo "   3. Go to 'Kubernetes' section"
    echo "   4. Check 'Enable Kubernetes'"
    echo "   5. Click 'Apply & Restart'"
    echo "   6. Wait 2-5 minutes for Kubernetes to start"
    echo "   7. Run this script again to verify"
    echo ""
    echo "   ${BLUE}Option 2: Install Minikube${NC}"
    echo "   ────────────────────────────────────────"
    echo "   $ brew install minikube"
    echo "   $ minikube start"
    echo ""
    echo "   ${BLUE}Option 3: Install Kind${NC}"
    echo "   ────────────────────────────────────────"
    echo "   $ brew install kind"
    echo "   $ kind create cluster --name mlops-cluster"
    echo ""
    
    # Check available contexts
    echo -e "${BLUE}   Available kubectl contexts:${NC}"
    kubectl config get-contexts 2>/dev/null || echo "      (none found)"
    echo ""
    
    exit 1
fi
