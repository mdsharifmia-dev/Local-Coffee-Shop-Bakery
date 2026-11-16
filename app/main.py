import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.health import router as health_router
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.database import AsyncSessionLocal, engine, init_db
from app.core.rate_limiter import RateLimitMiddleware
from app.core.redis import cache
from app.repositories.menu_repo import menu_repo
from app.services.menu_service import menu_service

logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup sequence
    logger.info("Initializing Local Coffee Shop & Bakery Backend...")
    await init_db()
    await cache.initialize()

    # Seed initial menu and warm cache
    async with AsyncSessionLocal() as session:
        seeded_count = await menu_repo.seed_initial_data_if_empty(session)
        if seeded_count > 0:
            logger.info("Database initialized with %d default menu items.", seeded_count)

        # Pre-warm Redis cache
        await menu_service.get_menu(session, category="all")
        await menu_service.get_menu(session, category="coffee")
        await menu_service.get_menu(session, category="pastry")
        logger.info("Menu cache pre-warmed for high-concurrency throughput.")

    yield

    # Shutdown sequence
    logger.info("Shutting down backend services...")
    await cache.close()
    await engine.dispose()
    logger.info("Connections closed cleanly.")


app = FastAPI(
    title=settings.APP_NAME,
    description="High-performance, asynchronous REST API for Local Coffee Shop & Bakery.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# 1. GZip Compression Middleware (payload optimization)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# 2. IP Rate Limiting Middleware (DDoS & scrapers protection)
app.add_middleware(RateLimitMiddleware)

# 3. Cross-Origin Resource Sharing (CORS)
origins = settings.ALLOWED_ORIGINS
if isinstance(origins, str):
    origins = [origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route registration
app.include_router(health_router)
app.include_router(api_router, prefix="/api")

# Static frontend assets serving
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.mount("/", StaticFiles(directory=base_dir, html=True), name="static")
