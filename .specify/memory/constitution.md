# Local Coffee Shop & Bakery - Project Constitution

Ratification Date: 2026-11-16
Version: 1.0.0
Project: Local Coffee Shop & Bakery Full-Stack Upgrade

## 1. Core Principles & Governance

### 1.1 Spec-Driven Development (SDD)
- All development must follow the Spec-Kit pipeline: Constitution, Specify, Plan, Tasks, Implement, and Converge.
- No production code shall be created without approved specifications in the `specs/` directory.
- Implementation changes must be mapped directly to task checklist items in `tasks.md`.

### 1.2 Multi-Tier Clean Architecture
- Software components must be strictly decoupled across four distinct architectural layers:
  1. API Routes and Controllers (`app/api/`): HTTP request parsing, status codes, route definitions.
  2. Business Services (`app/services/`): Business logic, pricing calculations, transactional operations.
  3. Repositories and Data Access (`app/repositories/`): Raw database and cache queries.
  4. Models and Validation Schemas (`app/models/`, `app/schemas/`): Persistent schema and validation models.
- Controllers must never perform direct database queries or raw calculations.

### 1.3 High-Performance & Concurrency Standards
- The backend must be fully asynchronous, utilizing Python FastAPI with non-blocking I/O.
- Database connection pooling must be configured with defined minimum and maximum pool limits.
- High-read endpoints (e.g., `/api/menu`) must utilize Redis caching to ensure sub-10ms response latency.
- Rate limiting (e.g., maximum 60 requests per minute per IP address) must be enforced on all public endpoints.
- Heavy operations such as customer confirmation dispatch and notifications must be executed via background workers.

### 1.4 Zero-Trust Security & Secrets Management
- No API keys, credentials, tokens, or sensitive client data may ever be hardcoded.
- All secrets and configuration values must be loaded from environment variables using typed settings (`pydantic-settings`).
- A comprehensive `.env.example` file must be maintained and tracked.
- All client-supplied payloads must be strictly validated with Pydantic schemas before processing.

### 1.5 Strict Zero-Emoji Policy
- Emojis are strictly prohibited in all documentation, code, comments, commit messages, API payloads, and agent responses.
- All user-facing and internal communications must maintain a clean, text-only, professional engineering standard.

### 1.6 Cultural & Visual Safety Standards
- Zero female representations: Any image, illustration, or placeholder assets used across the application must strictly refrain from female depictions.
- Authentic coffee, tea, pastry, and architectural cafe imagery must be preserved.

### 1.7 Health & Observability
- The system must provide a public `/health` endpoint that dynamically inspects:
  1. Primary Database connection status and latency.
  2. Redis Cache connection status and latency.
  3. Overall system runtime metrics.

### 1.8 Frontend Preservation & Progressive Enhancement
- The existing HTML structure, CSS design tokens, and Medium Roast Latte palette must be preserved.
- Frontend JavaScript must progressively enhance static pages using asynchronous `fetch()` API calls to hydrate menu items, submit orders, and handle contact inquiries seamlessly.
