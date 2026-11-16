# Quickstart & Verification Guide

Feature: specs/001-fullstack-upgrade
Date: 2026-11-16

## 1. Prerequisites
- Python 3.12+ (or `uv` package manager)
- (Optional for containers) Docker and Docker Compose

## 2. Local Zero-Dependency Run (SQLite + In-Memory/Redis Fallback)

1. Clone or navigate to the repository:
   ```bash
   cd "/home/sharif/Downloads/SHARIF_4044/SHARIF  4044/AI/Local Coffee Shop & Bakery"
   ```

2. Create virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

3. Seed database and launch the asynchronous server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. Verify server health:
   ```bash
   curl http://localhost:8000/health
   ```

5. Test cached menu:
   ```bash
   curl http://localhost:8000/api/menu
   ```

6. Test atomic order creation:
   ```bash
   curl -X POST http://localhost:8000/api/orders \
     -H "Content-Type: application/json" \
     -d '{"customer_name":"Dev Test","payment_method":"bKash","items":[{"menu_item_id":1,"quantity":2}]}'
   ```

## 3. Production Multi-Container Run (Docker Compose)

1. Build and boot all services:
   ```bash
   docker compose up --build -d
   ```

2. Inspect running services (App, Nginx, Redis, PostgreSQL):
   ```bash
   docker compose ps
   ```

3. Access the application:
   - Web application: `http://localhost:80`
   - API Docs: `http://localhost:80/docs`
   - Health Probe: `http://localhost:80/health`
