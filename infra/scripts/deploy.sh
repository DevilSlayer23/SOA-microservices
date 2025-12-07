#!/bin/bash

set -e

echo "🚀 Deploying E-Commerce Microservices to Kubernetes..."

# Verify we're in the right directory
if [ ! -f "../k8s/namespace.yaml" ]; then
    echo "❌ Error: Cannot find k8s files. Make sure you're running from infra/scripts/"
    exit 1
fi

# Create namespace
echo "📦 Creating namespace..."
kubectl apply -f ../k8s/namespace.yaml  

# Apply secrets
echo "🔐 Creating secrets..."
kubectl apply -f ../k8s/secrets/ -n ecommerce

# Apply configmaps
echo "⚙️  Creating configmaps..."
kubectl apply -f ../k8s/configs/ -n ecommerce

# Deploy databases
echo "💾 Deploying databases..."
kubectl apply -f ../k8s/databases/ -n ecommerce

# Wait for databases
echo "⏳ Waiting for databases to be ready..."
echo "  - Waiting for PostgreSQL..."
kubectl wait --for=condition=ready pod -l app=postgres-service -n ecommerce --timeout=120s || true
echo "  - Waiting for MongoDB..."
kubectl wait --for=condition=ready pod -l app=mongo-service -n ecommerce --timeout=120s || true

# Deploy services
echo "🌐 Deploying microservices..."
kubectl apply -f ../k8s/services/ -n ecommerce

# Wait for services
echo "⏳ Waiting for services to be ready (this may take a minute)..."

kubectl wait --for=condition=ready pod -l app=users-service -n ecommerce --timeout=10s || echo "⚠️  Users service not ready yet"
kubectl wait --for=condition=ready pod -l app=products-service -n ecommerce --timeout=10s || echo "⚠️  Products service not ready yet"
kubectl wait --for=condition=ready pod -l app=cart-service -n ecommerce --timeout=10s || echo "⚠️  Cart service not ready yet"
kubectl wait --for=condition=ready pod -l app=orders-service -n ecommerce --timeout=10s || echo "⚠️  Orders service not ready yet"

# Apply HPA
echo "📊 Configuring autoscaling (HPA)..."
kubectl apply -f ../k8s/hpa/ -n ecommerce

# Deploy monitoring if exists
# .
cd  ../../monitoring
kubectl apply -f ./grafana/grafana.yaml
kubectl apply -f ./prometheus/prometheus.yaml
kubectl apply -f ./loki/loki.yaml



echo ""
echo "✅ Deployment complete!"
echo ""
echo "📊 Current status:"
kubectl get pods -n ecommerce
echo ""
kubectl get svc -n ecommerce