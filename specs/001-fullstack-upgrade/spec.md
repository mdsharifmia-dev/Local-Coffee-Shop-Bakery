# Feature Specification: Full-Stack High-Performance Upgrade

Feature Directory: specs/001-fullstack-upgrade
Status: Draft
Ratification: 2026-11-16
Version: 1.0.0

## 1. Overview and Business Goals
The Local Coffee Shop & Bakery currently operates as a static front-end website. To support business expansion, online customer ordering, dynamic pricing updates, and robust traffic surges without downtime or data corruption, the application is being upgraded to a high-concurrency, production-ready full-stack architecture.

The core goal is to deliver sub-10ms response times for menu browsing, atomic and concurrency-safe order placement, automated background notifications, and enterprise-grade rate-limiting while preserving the existing, approved user interface styling and visual identity.

## 2. User Scenarios & Acceptance Criteria

### Scenario 1: High-Traffic Menu Browsing (User Story 1 - P1)
- Context: Hundreds of simultaneous customers access `menu.html` or `index.html` during peak morning cafe hours.
- Action: The browser requests the active menu catalogue via `GET /api/menu`.
- Outcome: The backend serves the cached menu payload from Redis with sub-10ms response latency. If items are modified or stocked out by the cafe manager, cache invalidation guarantees fresh data on subsequent requests.

### Scenario 2: Concurrent Online Order Placement (User Story 2 - P1)
- Context: A customer selects one or more coffee drinks and bakery goods, enters their details, chooses a payment method (Cash, bKash, Nagad, Card), and clicks "Place Order".
- Action: The front-end issues an atomic `POST /api/orders` request with structured line items and customer contact details.
- Outcome:
  1. The server validates line item existence and verifies unit prices against server records (preventing client-side price tampering).
  2. The server calculates subtotals and totals within an atomic database transaction.
  3. The order record is persisted with a pending status and unique reference code.
  4. An asynchronous background task is triggered to dispatch confirmation notifications.
  5. The client receives a 201 Created response containing the finalized order details.

### Scenario 3: Customer Inquiry Submission (User Story 3 - P2)
- Context: A visitor fills out the contact form on `contact.html`.
- Action: The browser sends a `POST /api/contact` request with name, email, subject, and message text.
- Outcome:
  1. The inquiry is validated and persisted to the primary database.
  2. A background worker logs and queues the administrative email notification.
  3. The user receives a clean, non-blocking confirmation message.

### Scenario 4: DDoS and Scraping Protection (User Story 4 - P2)
- Context: An automated bot or malicious script attempts to overwhelm the ordering or menu endpoints.
- Action: The IP address exceeds the configured rate limit (60 requests per minute).
- Outcome: The backend intercepts subsequent requests and immediately returns an HTTP 429 Too Many Requests response with a standard Retry-After header, protecting upstream resources.

### Scenario 5: Operational Health & Observability (User Story 5 - P2)
- Context: An orchestrator, monitoring probe, or site administrator checks system status via `GET /health`.
- Action: The endpoint performs active connectivity checks against the primary database and Redis cache.
- Outcome: Returns HTTP 200 with status indicators for database, cache, and system uptime when all services are healthy.

## 3. Functional Requirements

- FR-001 [Backend Engine]: The backend service must be built on an asynchronous, non-blocking framework (FastAPI) utilizing an ASGI event loop.
- FR-002 [Data Persistence]: The system must support persistent storage with relational schema models for Menu Items, Orders, Order Items, and Contact Messages.
- FR-003 [Database Flexibility]: The system must function seamlessly with SQLite for local development and PostgreSQL for production environments via standard connection string configuration.
- FR-004 [Cache Acceleration]: The `/api/menu` endpoint must read from Redis cache by default, automatically falling back to the database if the cache is cold, and populating Redis with a configurable TTL.
- FR-005 [Cache Invalidation]: Any modification to menu items must invalidate the active Redis cache tag/key immediately.
- FR-006 [Rate Limiting]: Public endpoints must enforce an IP-based sliding window or token bucket rate limit of 60 requests per minute.
- FR-007 [Server-Side Pricing]: Order total calculation must strictly occur on the backend based on database-stored prices, ignoring any client-provided price fields to prevent tampering.
- FR-008 [Background Task Worker]: Dispatching notifications, confirmation logs, and webhooks must run asynchronously without delaying the HTTP response cycle.
- FR-009 [Frontend Dynamic Hydration]: The existing `menu.html` and `index.html` must dynamically fetch and render menu items from `/api/menu`, providing fallback graceful degradation if the network fails.
- FR-010 [Containerized Deployment]: The application must include production-grade `Dockerfile` and `docker-compose.yml` configurations with Nginx reverse proxy, App Service, Redis, and PostgreSQL.

## 4. Success Criteria

- SC-001: `/api/menu` response time is under 10ms when served from Redis cache under concurrent load.
- SC-002: Zero price tampering vulnerabilities: order totals must be verified strictly by backend record lookups.
- SC-003: 100% of valid orders result in persistent database records with atomic transactions.
- SC-004: Rate limiting reliably blocks requests exceeding 60 per minute per IP with HTTP 429.
- SC-005: `/health` endpoint accurately reports status of both database and cache layers.
- SC-006: Complete compliance with Universal Software Master Standards: zero emojis, zero female representations, zero hardcoded credentials.

## 5. Entities and Data Models

### Menu Item
- id: Integer (Primary Key, autoincrement)
- name: String (Unique, required)
- category: String (e.g., "coffee", "pastry", required)
- price: Decimal (Precision 10, scale 2, required)
- description: Text (optional)
- is_available: Boolean (default true)
- tag: String (e.g., "POPULAR", "SPECIALTY", optional)
- image_url: String (optional)
- created_at: DateTime (UTC)

### Order
- id: Integer (Primary Key, autoincrement)
- order_code: String (Unique alphanumeric reference, e.g., "ORD-7K2P9")
- customer_name: String (required)
- customer_phone: String (optional)
- special_notes: Text (optional)
- payment_method: String (e.g., "Cash", "bKash", "Nagad", "Card", required)
- transaction_ref: String (optional)
- total_price: Decimal (Precision 10, scale 2, required)
- status: String ("pending", "confirmed", "preparing", "ready", "completed", "cancelled")
- created_at: DateTime (UTC)

### Order Item
- id: Integer (Primary Key, autoincrement)
- order_id: Integer (Foreign Key -> Order.id)
- menu_item_id: Integer (Foreign Key -> MenuItem.id)
- item_name: String (Snapshot of item name at purchase)
- unit_price: Decimal (Snapshot of unit price at purchase)
- quantity: Integer (Minimum 1)
- subtotal: Decimal (unit_price * quantity)

### Contact Message
- id: Integer (Primary Key, autoincrement)
- name: String (required)
- email: String (Valid email format, required)
- subject: String (required)
- message: Text (required)
- created_at: DateTime (UTC)

## 6. Assumptions and Edge Cases

- Edge Case 1: Redis is temporarily unreachable.
  - Behavior: System must log a warning and fall back to direct database reads without failing customer requests.
- Edge Case 2: Out-of-stock item ordered.
  - Behavior: System rejects order payload with HTTP 400 Bad Request detailing which item is unavailable.
- Edge Case 3: Database transaction failure during order creation.
  - Behavior: Full transaction rollback ensuring no partial orders are written, returning HTTP 500 with user-friendly message.
- Edge Case 4: Client browser has JavaScript disabled.
  - Behavior: Static semantic HTML fallback retains core presentation and phone/location details.
