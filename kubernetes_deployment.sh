#!/bin/bash

set -e

echo "🚀 Building and Deploying to Kubernetes..."

# 1. Point Docker to Minikube
echo "📌 Connecting to Minikube Docker daemon..."
eval $(minikube docker-env)

# 2. Build images with docker-compose
echo "🔨 Building images with docker-compose..."
docker compose -f docker-compose.yaml build

# 3. Verify images exist
echo ""
echo "✅ Available images:"
docker images | grep -E "ecommerce|REPOSITORY"

# 4. Deploy to Kubernetes
echo ""
echo "🚀 Deploying to Kubernetes..."
cd infra/scripts
./deploy.sh
cd ../../

echo ""
echo "⏳ Waiting for pods to start..."
sleep 20

echo ""
echo "📊 Final status:"
kubectl get all -n ecommerce

echo ""
echo "📝 Pod details:"
kubectl get pods -n ecommerce -o wide

echo ""
echo "🔍 Check specific pod status:"
echo "  kubectl describe pod -n ecommerce <pod-name>"
echo ""
echo "🔍 Check pod logs if any issues:"
echo "  kubectl logs -n ecommerce -l app=users-service"
echo "  kubectl logs -n ecommerce -l app=products-service"
echo "  kubectl logs -n ecommerce -l app=cart-service"
echo "  kubectl logs -n ecommerce -l app=orders-service"

echo ""
MINIKUBE_IP=$(minikube ip)
echo "✅ Services available at:"
echo "  Users:      http://${MINIKUBE_IP}:30001/health"
echo "  Products:   http://${MINIKUBE_IP}:30002/health"
echo "  Cart:       http://${MINIKUBE_IP}:30003/health"
echo "  Orders:     http://${MINIKUBE_IP}:30004/health"
echo "  Prometheus: http://${MINIKUBE_IP}:30090"
echo "  Grafana:    http://${MINIKUBE_IP}:30030 (admin/admin)"
echo "  Loki:    http://${MINIKUBE_IP}:3100"

echo ""
echo "🧪 Test services:"
echo "  curl http://${MINIKUBE_IP}:30001/health"