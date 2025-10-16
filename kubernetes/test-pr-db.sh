#!/bin/bash
set -euo pipefail

# Script pour tester la configuration DB locale

PR_NUMBER=${1:-123}

echo "🧪 Testing PR Database Setup for PR #${PR_NUMBER}"
echo ""

# Check if prod deployment exists
echo "📍 Checking production deployment..."
if ! kubectl get deployment city-api-prod-db -n cityapi-prod &>/dev/null; then
    echo "❌ Production deployment not found!"
    echo "   Deploy prod first: helm install cityapi-prod ./kubernetes/helm --namespace cityapi-prod --create-namespace"
    exit 1
fi

echo "✅ Production deployment found"
echo ""

# Get DB service
DB_SERVICE=$(kubectl get svc city-api-prod-db -n cityapi-prod -o jsonpath='{.metadata.name}' 2>/dev/null || echo "")

if [ -z "$DB_SERVICE" ]; then
    echo "❌ Database service not found!"
    exit 1
fi

echo "✅ Database service: ${DB_SERVICE}"
echo ""

# Deploy PR environment
echo "🚀 Deploying PR #${PR_NUMBER} environment..."
helm upgrade --install cityapi-pr-${PR_NUMBER} ./kubernetes/helm \
    -f ./kubernetes/helm/values-pr.yaml \
    --set prNumber=${PR_NUMBER} \
    --set app.tag=latest \
    --namespace cityapi-pr-${PR_NUMBER} \
    --create-namespace \
    --wait

echo ""
echo "✅ PR environment deployed!"
echo ""

# Check database creation
echo "🔍 Verifying database pr_${PR_NUMBER}..."
kubectl run -it --rm psql-check --image=postgres:16 --restart=Never -n cityapi-prod -- \
    psql -h city-api-prod-db -U city_api -d postgres -c "\l" | grep "pr_${PR_NUMBER}" || true

echo ""
echo "📊 Summary:"
echo "  - Production DB: city_api"
echo "  - PR DB: pr_${PR_NUMBER}"
echo "  - Namespace: cityapi-pr-${PR_NUMBER}"
echo ""
echo "🧹 To cleanup:"
echo "  helm uninstall cityapi-pr-${PR_NUMBER} -n cityapi-pr-${PR_NUMBER}"
echo "  kubectl delete namespace cityapi-pr-${PR_NUMBER}"
echo ""
