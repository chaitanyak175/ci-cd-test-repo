#!/bin/bash

# Setup script for the test repository
# This helps initialize the broken environment

echo "🧪 Setting up CI/CD Test Repository..."

# Create some files that will cause issues
echo "Setting up broken environment..."

# Create an invalid .env file
cat > .env << EOF
# Broken environment file
DATABASE_URL=postgresql://user:@localhost:5432/db  # Missing password
SECRET_KEY=  # Empty secret
API_KEY = invalid key with spaces
PORT=not_a_number
BROKEN_VAR
EOF

echo "✅ Test repository setup complete!"
echo ""
echo "This repository contains intentionally broken code to test:"
echo "  - GitHub Actions workflow failures"
echo "  - Node.js/Python build issues"
echo "  - Docker configuration problems"
echo "  - Missing dependencies"
echo "  - Syntax errors"
echo "  - Environment variable issues"
echo ""
echo "Next steps:"
echo "  1. Push this repo to your GitHub account"
echo "  2. Configure webhooks to point to your CI/CD Fixer Agent"
echo "  3. Trigger the workflows to test the agent"
echo ""
echo "Webhook URL: http://localhost:8000/webhook"
