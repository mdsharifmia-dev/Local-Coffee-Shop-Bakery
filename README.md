# Local Coffee Shop & Bakery - Full-Stack Application

A high-performance, asynchronous Full-Stack web application and commercial storefront engineered for artisanal cafes and bakeries. Built with FastAPI, PostgreSQL/SQLite, Redis caching, Nginx reverse proxy, and vanilla frontend architecture.

---

## 1. Core Architectural Capabilities

- Asynchronous Backend: Built with Python FastAPI utilizing an ASGI non-blocking event loop.
- Sub-10ms Redis Caching: Read-heavy menu endpoints (`GET /api/menu`) are accelerated by Redis with automatic invalidation upon catalog mutations.
- Concurrency-Safe Order Pipeline: Atomic transactions (`POST /api/orders`) verify unit prices strictly against backend records, computing totals server-side to eliminate price tampering.
- Traffic Protection & Rate Limiting: IP-based sliding window rate limiter protects endpoints against scraping and DDoS surges (configured for 60 requests/minute per client).
- Non-Blocking Background Tasks: Asynchronous background workers process order audit logging, administrative notifications, and customer confirmations without blocking HTTP requests.
- Health & Observability: Live `/health` probe actively verifies database connection latency, cache status, and application uptime.
- Progressive Frontend Hydration: Preserves the semantic HTML5, CSS design tokens, and Medium Roast Latte palette while dynamically wiring menu and checkout forms via `fetch()` APIs.

---

## 2. API Endpoints Overview

| Method | Endpoint | Description | Cache Status |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | System health and connectivity probe (DB & Cache) | Bypassed |
| `GET` | `/api/menu` | Retrieves menu items filtered by category | Redis Cached (TTL 300s) |
| `POST` | `/api/menu` | Creates a new menu item (Admin Key protected) | Invalidates Cache |
| `PATCH` | `/api/menu/{id}` | Updates existing menu item (Admin Key protected) | Invalidates Cache |
| `DELETE`| `/api/menu/{id}` | Removes a menu item (Admin Key protected) | Invalidates Cache |
| `POST` | `/api/orders` | Submits a customer order with atomic transaction | Non-blocking Worker |
| `GET` | `/api/orders/{code}`| Tracks order status using unique reference code | Live Database Read |
| `POST` | `/api/contact` | Submits contact inquiries and queues alert | Non-blocking Worker |

Interactive API Documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 3. Quickstart: Local Zero-Dependency Run

The application supports immediate local execution using an embedded SQLite database and in-memory TTL caching without requiring external services.

1. Navigate to the project root:
   ```bash
   cd "/home/sharif/Downloads/SHARIF_4044/SHARIF  4044/AI/Local Coffee Shop & Bakery"
   ```

2. Initialize virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

3. Launch the application:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. Verify service health:
   ```bash
   curl http://localhost:8000/health
   ```

5. Access the application in your browser:
   - Web Storefront: `http://localhost:8000/`
   - API Docs: `http://localhost:8000/docs`

---

## 4. Production Deployment: Docker Compose

For high-concurrency production deployments, a four-container orchestration stack is provided:
- `nginx`: Alpine reverse proxy with Gzip compression and static caching.
- `app`: FastAPI application running 4 Gunicorn Uvicorn workers.
- `redis`: High-speed Redis 7 cache and queue engine.
- `postgres`: Persistent PostgreSQL 16 database.

1. Launch the stack:
   ```bash
   docker compose up --build -d
   ```

2. Monitor container statuses:
   ```bash
   docker compose ps
   ```

3. View live application logs:
   ```bash
   docker compose logs -f app
   ```

4. Access the production application at:
   - Web application: `http://localhost:80`
   - API Docs: `http://localhost:80/docs`
   - Health Probe: `http://localhost:80/health`

---

## 5. Automated Verification & Testing

Execute the comprehensive test suite verifying health probes, cache hits, atomic order placement, and rate limiting:

```bash
pytest -v
```

---

## 6. Project Architecture Map

See [CODEBASE_MAP.md](file:///home/sharif/Downloads/SHARIF_4044/SHARIF%20%204044/AI/Local%20Coffee%20Shop%20%26%20Bakery/CODEBASE_MAP.md) for full directory structure details, entity relationships, and architectural governance.

## 7. License
Licensed under the [MIT License](LICENSE).
