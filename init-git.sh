#!/bin/bash

# Initial Git Setup for Drought Platform
echo "🚀 Setting up Git repository for Drought Platform..."

git init
git add .
git commit -m "feat: initial project scaffold

- Project structure for 3 dashboards + 1 mobile app
- Collector, Sarpanch, Field Officer, Driver roles defined
- Docker Compose setup (frontend, backend, ml-service, db, redis)
- Tech stack: React, Node.js, Python FastAPI, PostgreSQL
- Core features: rainfall analysis, WSI, tanker allocation, route optimization
- Documentation: README, architecture, data models"

echo "✅ Initial commit done!"
echo ""
echo "Next steps:"
echo "  git remote add origin https://github.com/your-org/drought-platform.git"
echo "  git push -u origin main"
