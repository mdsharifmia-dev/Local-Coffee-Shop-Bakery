# Codebase Map: Local Coffee Shop & Bakery Full-Stack Application

## Overview
This document outlines the architectural structure, file responsibilities, and layer boundaries of the Local Coffee Shop & Bakery high-performance system.

## Directory Structure & Responsibilities

### 1. Specification & Governance (`.specify/` & `specs/`)
- `.specify/memory/constitution.md`: Core architectural standards, Zero-Trust security rules, clean architecture principles, and zero-emoji enforcement.
- `.specify/feature.json`: Active feature metadata pointer.
- `specs/001-fullstack-upgrade/spec.md`: User stories, functional requirements, and measurable success criteria.
- `specs/001-fullstack-upgrade/research.md`: Technology evaluation and architectural trade-offs.
- `specs/001-fullstack-upgrade/data-model.md`: Relational schema definitions and entity diagrams.
- `specs/001-fullstack-upgrade/contracts/api.yaml`: OpenAPI 3.0 specification for all REST endpoints.
- `specs/001-fullstack-upgrade/quickstart.md`: Developer guide for running locally and via Docker.
- `specs/001-fullstack-upgrade/plan.md`: Master technical architecture roadmap.
- `specs/001-fullstack-upgrade/tasks.md`: Granular, testable implementation checklist.

### 2. Backend Application (`app/`)
- `app/main.py`: ASGI entrypoint with lifespan startup (auto-seeding, cache pre-warming), Gzip, Rate Limiting, CORS, and static file mounting.
- `app/core/`:
  - `config.py`: Typed environment settings using Pydantic Settings.
  - `database.py`: Async SQLAlchemy engine with QueuePool pooling and session management.
  - `redis.py`: Asynchronous Redis cache engine with seamless in-memory fallback.
  - `rate_limiter.py`: IP-based sliding window rate limiter (60 req/min).
- `app/models/`: Declarative SQLAlchemy models.
  - `base.py`: Declarative Base and TimestampMixin.
  - `menu.py`: MenuItem persistent entity.
  - `order.py`: Order and OrderItem relational entities.
  - `contact.py`: ContactMessage entity.
- `app/schemas/`: Pydantic validation and serialization models.
  - `menu.py`: Request and response schemas for menu management.
  - `order.py`: Schemas for atomic order creation and tracking.
  - `contact.py`: Inquiry input and response validation.
  - `health.py`: Healthcheck probe response model.
- `app/repositories/`: Data access layer.
  - `menu_repo.py`: Menu item querying, creation, and initial database seeding.
  - `order_repo.py`: Atomic database transactions for order and line item creation.
  - `contact_repo.py`: Inquiry persistence.
- `app/services/`: Business logic layer.
  - `menu_service.py`: Redis cache-aside reads, TTL warm-up, and automatic invalidation.
  - `order_service.py`: Server-side price verification, inventory validation, and background notification queuing.
  - `contact_service.py`: Inquiry processing and notification queuing.
- `app/workers/`:
  - `notification_worker.py`: Non-blocking background worker for order receipt, emails, and alerts.
- `app/api/`:
  - `health.py`: Live health probe endpoint checking DB and Redis.
  - `v1/api.py`: Route aggregation.
  - `v1/endpoints/menu.py`: Cached menu retrieval and admin endpoints.
  - `v1/endpoints/orders.py`: Atomic order placement and tracking endpoints.
  - `v1/endpoints/contact.py`: Inquiry submission endpoint.

### 3. Frontend Web Assets (Root)
- `index.html`: Home page featuring hero section, specialty cards, and responsive navigation.
- `menu.html`: Menu page with category filters, live pricing hydration, and order modal.
- `about.html`: Heritage story, artisanal values, and craft bakery timeline.
- `gallery.html`: Visual photo gallery showcasing latte art, bakery goods, and cafe ambience.
- `contact.html`: Location map, contact information, and asynchronous inquiry form.
- `404.html`: Custom error page with fallback navigation.
- `script.js`: Progressive enhancement engine connecting UI forms and modals to REST APIs.
- `style.css`: Preserved Medium Roast Latte design system tokens and responsive layouts.
- `favicon-coffee.svg`, `favicon.ico`, `favicon-32x32.png`: Standalone steaming cup branding assets.

### 4. Infrastructure & Containerization
- `Dockerfile`: Multi-stage build producing an unprivileged, multi-worker runtime container.
- `docker-compose.yml`: Full stack orchestration for App, Nginx, Redis, and PostgreSQL.
- `nginx/default.conf`: Production reverse proxy with Gzip compression and asset caching.
- `requirements.txt`: Python package dependencies.
- `.env.example`: Configuration reference template.
- `tests/`: Automated unit and integration test suite.
