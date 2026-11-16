# Implementation Plan: Full-Stack High-Performance Upgrade

Feature Directory: specs/001-fullstack-upgrade
Date: 2026-11-16
Status: Approved

## 1. Executive Summary
This plan outlines the surgical transition of the Local Coffee Shop & Bakery from a static web document collection to a production-hardened full-stack application. The implementation establishes an asynchronous FastAPI backend layered cleanly across Controllers, Services, Repositories, and Models. Redis caching guarantees sub-10ms read performance, an atomic order pipeline safeguards revenue and pricing integrity, and an Nginx reverse proxy fronting multi-worker containers enables seamless handling of traffic spikes.

## 2. Multi-Tier Project Architecture

```
.
├── .specify/                      # Spec-Kit governance & constitution
├── specs/001-fullstack-upgrade/   # SDD specifications, research, contracts, tasks
├── app/                           # Backend Application Root
│   ├── __init__.py
│   ├── main.py                    # FastAPI entrypoint, lifespan, middleware
│   ├── core/                      # Core configuration and cross-cutting concerns
│   │   ├── config.py              # Pydantic Settings (.env management)
│   │   ├── database.py            # Async engine, connection pooling, session maker
│   │   ├── redis.py               # Redis async client & fallback cache
│   │   ├── rate_limiter.py        # Sliding window / token bucket rate limiter
│   │   └── security.py            # Sanitization and validation utilities
│   ├── models/                    # SQLAlchemy Declarative Models
│   │   ├── base.py
│   │   ├── menu.py
│   │   ├── order.py
│   │   └── contact.py
│   ├── schemas/                   # Pydantic Validation & Serialization Schemas
│   │   ├── menu.py
│   │   ├── order.py
│   │   ├── contact.py
│   │   └── health.py
│   ├── repositories/              # Data Access Layer (DB & Cache)
│   │   ├── menu_repo.py
│   │   ├── order_repo.py
│   │   └── contact_repo.py
│   ├── services/                  # Business Logic Layer
│   │   ├── menu_service.py
│   │   ├── order_service.py
│   │   └── contact_service.py
│   ├── workers/                   # Background Task Workers
│   │   └── notification_worker.py
│   └── api/                       # API Controllers & Route Definitions
│       ├── v1/
│       │   ├── api.py             # Router aggregation
│       │   ├── endpoints/
│       │   │   ├── menu.py
│       │   │   ├── orders.py
│       │   │   └── contact.py
│       └── health.py              # Health check endpoint
├── nginx/                         # Nginx Reverse Proxy Config
│   └── default.conf
├── tests/                         # Automated Test Suite
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_menu.py
│   ├── test_orders.py
│   └── test_rate_limit.py
├── index.html                     # Frontend Pages (Preserved & Enhanced)
├── menu.html
├── about.html
├── contact.html
├── gallery.html
├── script.js                      # Progressive fetch() integration
├── style.css                      # Preserved Medium Roast Latte design system
├── requirements.txt               # Locked backend dependencies
├── Dockerfile                     # Multi-stage production container
├── docker-compose.yml             # App + Nginx + Redis + PostgreSQL
├── CODEBASE_MAP.md                # System architectural map
├── .env.example                   # Complete configuration contract
└── README.md                      # Comprehensive developer and operations manual
```

## 3. Technology Stack & Key Dependencies
- Language / Runtime: Python 3.12+ (managed with `uv`)
- Framework: FastAPI 0.115+
- ASGI Server: Uvicorn & Gunicorn (`uvicorn.workers.UvicornWorker`)
- ORM: SQLAlchemy 2.0+ (Async engine with connection pool)
- Database Drivers: `aiosqlite` (local) and `asyncpg` (production)
- Cache & Queue: `redis` (asyncio) with in-memory fallback
- Data Validation: Pydantic v2
- Web Server / Reverse Proxy: Nginx (Alpine) with Gzip compression and proxy caching

## 4. Risk Mitigation & Edge Cases
- Risk 1: Cold Cache Herd on Service Start.
  - Mitigation: Application lifespan automatically runs initial menu warm-up on startup.
- Risk 2: Client Price Manipulation.
  - Mitigation: Order payloads only accept `menu_item_id` and `quantity`. Prices are looked up strictly inside the database transaction.
- Risk 3: Network Failure on Frontend API calls.
  - Mitigation: Frontend JavaScript maintains cached fallback elements and displays informative, friendly status banners.
