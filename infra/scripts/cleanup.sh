#!/bin/bash

echo "🧹 Cleaning up Kubernetes resources..."

kubectl delete namespace ecommerce

echo "✅ Cleanup complete!"
echo ""
echo "To restart fresh:"
echo "  ./kubernetes_deployment.sh"