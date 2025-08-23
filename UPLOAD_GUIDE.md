# 🧪 CI/CD Test Repository Upload Guide

## Quick Upload to GitHub

### 1. Create GitHub Repository
```bash
# Go to github.com and create a new repository named "ci-cd-test-repo"
# Don't initialize with README (we already have one)
```

### 2. Initialize and Push
```bash
cd test-repo
git init
git add .
git commit -m "Initial commit: Broken CI/CD setup for testing"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ci-cd-test-repo.git
git push -u origin main
```

### 3. Configure Webhook
In your GitHub repository settings:
- Go to Settings → Webhooks → Add webhook
- Payload URL: `http://your-domain.com/webhook` (or use ngrok for local testing)
- Content type: `application/json`
- Events: Select "Workflow runs" and "Push"

### 4. Test the Agent
```bash
# Trigger a workflow by pushing changes
git add .
git commit -m "Trigger CI/CD failure for testing"
git push

# Or manually trigger workflows in GitHub Actions tab
```

## What Will Happen

1. **GitHub Actions will fail** (intentionally broken workflows)
2. **Webhook will trigger** your CI/CD Fixer Agent
3. **Gemini AI will analyze** the failure logs
4. **Portia will orchestrate** the fix workflow
5. **Human approval** will be requested
6. **Fixes will be proposed** via the API

## Testing Scenarios

- **Node.js failures**: Missing package.json, dependency issues
- **Python failures**: Import errors, syntax problems
- **Docker failures**: Invalid Dockerfile, missing files
- **Environment issues**: Missing secrets, config problems

Perfect for comprehensive testing! 🚀
