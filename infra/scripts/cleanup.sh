#!/bin/bash

echo "🧹 Cleaning up Kubernetes resources..."

kubectl delete namespace ecommerce

echo "✅ Cleanup complete!"