#!/bin/bash

echo "🎬 E-Commerce Microservices Demo"
echo ""

MINIKUBE_IP=$(minikube ip)

echo "1️⃣ Showing all running services..."
kubectl get all -n ecommerce
sleep 3

echo ""
echo "2️⃣ Testing health endpoints..."
curl http://$MINIKUBE_IP:30001/health | jq '.'
curl http://$MINIKUBE_IP:30002/health | jq '.'

echo ""
echo "3️⃣ Registering a user..."
curl -X POST http://$MINIKUBE_IP:30001/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@example.com","password":"Demo123!","name":"Demo User"}' | jq '.'

echo ""
echo "4️⃣ Creating a product..."
curl -X POST http://$MINIKUBE_IP:30002/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","price":999.99,"stock":50}' | jq '.'

echo ""
echo "5️⃣ Showing Horizontal Pod Autoscaler..."
kubectl get hpa -n ecommerce

echo ""
echo "6️⃣ Opening Grafana Dashboard..."
echo "URL: http://$MINIKUBE_IP:30030"