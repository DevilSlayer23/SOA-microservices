#!/bin/bash

MINIKUBE_IP=$(minikube ip)

echo "🧪 Testing E-Commerce Microservices on Kubernetes..."
echo ""

# Test health endpoints
echo "1️⃣  Testing health endpoints..."
curl -s http://$MINIKUBE_IP:30001/health | jq '.'
curl -s http://$MINIKUBE_IP:30002/health | jq '.'
curl -s http://$MINIKUBE_IP:30003/health | jq '.'
curl -s http://$MINIKUBE_IP:30004/health | jq '.'

echo ""
echo "2️⃣  Registering test user..."
USER_RESPONSE=$(curl -s -X POST http://$MINIKUBE_IP:30001/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "k8s-test@example.com",
    "password": "TestPass123!",
    "name": "K8s Test User"
  }')
echo $USER_RESPONSE | jq '.'

echo ""
echo "✅ Basic tests complete!"