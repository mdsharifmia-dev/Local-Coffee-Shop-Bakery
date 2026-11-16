import time
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.redis import cache
from app.schemas.health import HealthResponse

router = APIRouter()
START_TIME = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health & Observability Probe",
    tags=["Health"],
)
async def check_health(db: AsyncSession = Depends(get_db)):
    db_status = "connected"
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        db_status = f"unhealthy: {exc}"

    cache_connected = await cache.ping()
    cache_status = "connected" if cache_connected else "in-memory-fallback"

    uptime = round(time.time() - START_TIME, 2)
    overall_status = "healthy" if db_status == "connected" else "degraded"

    status_code = status.HTTP_200_OK if overall_status == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE

    return JSONResponse(
        status_code=status_code,
        content={
            "status": overall_status,
            "database": db_status,
            "cache": cache_status,
            "uptime_seconds": uptime,
        },
    )
