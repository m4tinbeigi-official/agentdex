---
name: docker-lean-containerization
description: Production-grade multi-stage Docker build patterns for minimal footprint, rootless security, and caching.
version: 1.0.0
category: devops
author: AgentDex Community
source: https://github.com/docker/awesome-compose
---

# Docker Lean Containerization

Use when packaging services into minimal, secure, non-root OCI containers.

## Best Practice Pattern
```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final minimal runtime
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
USER 10001
CMD ["python", "main.py"]
```
