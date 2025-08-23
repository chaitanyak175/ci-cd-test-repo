# CI/CD Test Repository 🧪

This repository is designed to test the **CI/CD Fixer Agent** with various failure scenarios.

## Purpose

This repo contains intentionally broken CI/CD workflows and code to test:
- GitHub Actions failure detection
- AI-powered error analysis (Gemini 2.5 Pro)
- Automated fix generation
- Human-in-the-loop approval workflow
- Portia AI agent orchestration

## Test Scenarios

1. **Node.js Build Failures** - Missing dependencies, syntax errors
2. **Python Test Failures** - Import errors, missing packages
3. **Docker Build Issues** - Invalid Dockerfile syntax
4. **Linting Failures** - Code style violations
5. **Environment Variable Issues** - Missing secrets, config problems

## How to Use

1. Push this repo to your GitHub account
2. Configure the CI/CD Fixer Agent webhook endpoint
3. Trigger the broken workflows
4. Watch the AI agent analyze and propose fixes
5. Test the approval workflow

## Webhook Configuration

Point your GitHub webhook to:
```
https://ci-cd-fixer-agent-backend.onrender.com/webhook
```

Event types: `workflow_run`, `push`, `pull_request`

---

**Built for testing the CI/CD Fixer Agent with Gemini API + Portia AI** 🤖✨
