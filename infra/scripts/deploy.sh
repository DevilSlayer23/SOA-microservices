#!/bin/bash

echo "🚀 Deploying E-Commerce Microservices to Kubernetes..."

# Create namespace
echo "📦 Creating namespace..."
kubectl apply -f k8s/namespace.yaml

# Apply secrets
echo "🔐 Creating secrets..."
kubectl apply -f k8s/secrets/

# Apply configmaps
echo "⚙️  Creating configmaps..."
kubectl apply -f k8s/configs/

# Deploy databases
echo "💾 Deploying databases..."
kubectl apply -f k8s/databases/

# Wait for databases to be ready
echo "⏳ Waiting for databases..."
kubectl wait --for=condition=ready pod -l app=postgres -n ecommerce --timeout=120s
kubectl wait --for=condition=ready pod -l app=mongo -n ecommerce --timeout=120s

# Deploy services
echo "🌐 Deploying microservices..."
kubectl apply -f k8s/services/

# Wait for services to be ready
echo "⏳ Waiting for services..."
kubectl wait --for=condition=ready pod -l app=users-ecommerce -n ecommerce --timeout=120s
kubectl wait --for=condition=ready pod -l app=products-ecommerce -n ecommerce --timeout=120s
kubectl wait --for=condition=ready pod -l app=cart-ecommerce -n ecommerce --timeout=120s
kubectl wait --for=condition=ready pod -l app=orders-ecommerce -n ecommerce --timeout=120s

# Apply HPA
echo "📊 Configuring autoscaling..."
kubectl apply -f k8s/hpa/

# Apply network policies (optional)
# echo "🔒 Applying network policies..."
# kubectl apply -f k8s/network-policies/

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📍 Access services:"
echo "  Users:    http://$(minikube ip):30001"
echo "  Products: http://$(minikube ip):30002"
echo "  Cart:     http://$(minikube ip):30003"
echo "  Orders:   http://$(minikube ip):30004"
echo ""
echo "📊 Check status:"
echo "  kubectl get all -n ecommerce"