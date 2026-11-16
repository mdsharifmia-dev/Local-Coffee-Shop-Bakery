# Technical Research & Architectural Decisions

Feature: specs/001-fullstack-upgrade (Full-Stack High-Performance Upgrade)
Date: 2026-11-16

## 1. Backend Framework Selection
- Options Evaluated:
  1. Python (FastAPI): Native async/await support, Pydantic v2 high-speed Rust-core validation, automatic OpenAPI documentation, clean dependency injection system, low memory footprint.
  2. Node.js (Express / Fastify): Fast I/O, but typing requires heavy TypeScript toolchain setup and Prisma/Drizzle overhead.
  3. Python (Django): High overhead, synchronous ORM complexity, unnecessary admin bloat for this specific scope.
- Decision: FastAPI (Python 3.12+ / 3.14).
  - Rationale: Exceptional asynchronous concurrency, high throughput, zero-boilerplate validation with Pydantic v2, and seamless background task integration.

## 2. Database & ORM Strategy
- Options Evaluated:
  1. SQLAlchemy 2.0 (Async Engine) with `aiosqlite` and `asyncpg`.
  2. Raw `sqlite3` and `psycopg2`.
  3. Tortoise ORM.
- Decision: SQLAlchemy 2.0 Async Session + declarative models with dual-driver support (`sqlite+aiosqlite` for zero-setup local dev/testing, `postgresql+asyncpg` for production containerized deployment).
  - Connection Pooling: QueuePool configured with `pool_size=20`, `max_overflow=10`, `pool_timeout=30`, `pool_pre_ping=True` to eliminate stale connections under load surges.

## 3. Caching & Latency Architecture
- Strategy: Cache-Aside pattern with Redis async client (`redis.asyncio`).
- Cache Key: `cache:menu:all`
- TTL: 300 seconds (5 minutes) default.
- Invalidation: Cache key deleted immediately upon any menu mutation (create, update, delete, stock toggle).
- Resilience: If Redis is disconnected, the caching layer logs a warning and falls back to an in-memory LRU/TTL cache or direct database read, preventing cascading HTTP 500 outages.

## 4. Rate Limiting Strategy
- Implementation: Token-bucket or sliding window rate limiter integrated into FastAPI middleware.
- Limit: 60 requests per minute per client IP address.
- Headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`.
- Exemption: Static assets and `/health` probe endpoints can bypass rate limiting to prevent probe flapping.

## 5. Background Tasks & Concurrency
- Implementation: FastAPI native `BackgroundTasks` supplemented by an extensible queue worker interface.
- Tasks:
  1. Logging order audit trails.
  2. Dispatching simulated email notifications (with SMTP / SendGrid configuration support).
  3. Triggering webhook notifications for admin order reception.

## 6. Reverse Proxy & Container Blueprint
- Nginx reverse proxy fronting FastAPI app workers:
  - Gzip compression for JSON, CSS, JS, SVG, and HTML.
  - Proxy buffer tuning (`proxy_buffers 16 16k`, `proxy_buffer_size 32k`).
  - Cache-Control headers for static assets (`max-age=86400`).
  - Upstream load balancing over Uvicorn workers (`gunicorn -k uvicorn.workers.UvicornWorker -w 4`).
