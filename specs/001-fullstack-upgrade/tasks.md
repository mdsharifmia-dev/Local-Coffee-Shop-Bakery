# Tasks Checklist: Full-Stack High-Performance Upgrade

Feature Directory: specs/001-fullstack-upgrade
Date: 2026-11-16
Status: Completed

## Phase 1: Setup & Project Initialization
- [x] T001 [P] [Setup] Create locked dependencies in `requirements.txt` including FastAPI, Uvicorn, SQLAlchemy, aiosqlite, asyncpg, redis, pydantic, and pydantic-settings
- [x] T002 [P] [Setup] Create configuration settings module with Pydantic in `app/core/config.py` and write `.env.example`
- [x] T003 [P] [Setup] Initialize Python virtual environment using `uv` and install backend dependencies

## Phase 2: Foundational Architecture & Core Infrastructure
- [x] T004 [P] [Foundational] Implement async database engine with QueuePool connection pooling in `app/core/database.py`
- [x] T005 [P] [Foundational] Implement declarative base and models for Menu Item, Order, Order Item, and Contact Message in `app/models/`
- [x] T006 [P] [Foundational] Implement asynchronous Redis cache engine with graceful in-memory fallback in `app/core/redis.py`
- [x] T007 [P] [Foundational] Implement IP-based sliding window rate limiter in `app/core/rate_limiter.py`
- [x] T008 [P] [Foundational] Implement `/health` endpoint checking DB and Redis connectivity in `app/api/health.py`

## Phase 3: User Story 1 - High-Performance Cached Menu (P1)
- [x] T009 [P] [US1] Create Pydantic validation schemas for Menu Items in `app/schemas/menu.py`
- [x] T010 [P] [US1] Create Menu Repository for DB reads, queries, and initial seed data in `app/repositories/menu_repo.py`
- [x] T011 [P] [US1] Create Menu Service with Redis cache-aside reads and automatic invalidation in `app/services/menu_service.py`
- [x] T012 [P] [US1] Implement `GET /api/menu` and administrative menu endpoints in `app/api/v1/endpoints/menu.py`
- [x] T013 [P] [US1] Wire startup lifespan in `app/main.py` to auto-seed initial menu items and pre-warm Redis cache

## Phase 4: User Story 2 - Concurrency-Safe Order Placement & Worker (P1)
- [x] T014 [P] [US2] Create Pydantic schemas for Order input, line items, and responses in `app/schemas/order.py`
- [x] T015 [P] [US2] Implement Order Repository executing atomic database transactions in `app/repositories/order_repo.py`
- [x] T016 [P] [US2] Implement Background Notification Worker for order receipt and alerts in `app/workers/notification_worker.py`
- [x] T017 [P] [US2] Implement Order Service with server-side price validation and background worker dispatch in `app/services/order_service.py`
- [x] T018 [P] [US2] Implement `POST /api/orders` endpoint in `app/api/v1/endpoints/orders.py`

## Phase 5: User Story 3 - Customer Inquiries & Background Email Alerts (P2)
- [x] T019 [P] [US3] Create Contact Pydantic schemas in `app/schemas/contact.py`
- [x] T020 [P] [US3] Implement Contact Repository in `app/repositories/contact_repo.py` and Service in `app/services/contact_service.py`
- [x] T021 [P] [US3] Implement `POST /api/contact` endpoint in `app/api/v1/endpoints/contact.py`

## Phase 6: User Story 4 - Frontend Progressive Hydration & API Wiring (P1)
- [x] T022 [P] [US4] Update `script.js` to dynamically fetch `/api/menu` and populate cards on `menu.html` and `index.html` with graceful fallback
- [x] T023 [P] [US4] Wire order submission form in `menu.html` to `POST /api/orders` with live order code confirmation
- [x] T024 [P] [US4] Wire contact inquiry form in `contact.html` to `POST /api/contact` with non-blocking status banner

## Phase 7: Deployment & Container Blueprint (P1)
- [x] T025 [P] [Deploy] Create multi-worker production container configuration in `Dockerfile`
- [x] T026 [P] [Deploy] Create Nginx configuration with reverse proxy, Gzip compression, and asset caching in `nginx/default.conf`
- [x] T027 [P] [Deploy] Create multi-container stack in `docker-compose.yml` (App, Nginx, Redis, PostgreSQL)
- [x] T028 [P] [Deploy] Create architectural map in `CODEBASE_MAP.md` and update `README.md` with complete operation guide

## Phase 8: Verification & Automated Test Suite (P1)
- [x] T029 [P] [Verify] Create test suite for `/health`, `/api/menu`, `/api/orders`, and rate limiter in `tests/`
- [x] T030 [P] [Verify] Execute automated test suite using `pytest` and verify 100% green passing status
- [x] T031 [P] [Verify] Verify compliance against Master Standards (Zero Secrets, Zero Emoji, Zero Female representation)
