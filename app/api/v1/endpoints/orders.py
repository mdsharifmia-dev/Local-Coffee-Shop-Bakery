from typing import List, Optional
from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import order_service

router = APIRouter()


def verify_admin_key(x_admin_key: Optional[str] = Header(None)) -> bool:
    if settings.APP_ENV == "development" and not x_admin_key:
        return True
    if x_admin_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing admin security key.",
        )
    return True


@router.post(
    "/orders",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Order (Atomic Transaction)",
    description="Validates items, computes totals from server pricing records, and atomically creates the order.",
)
async def create_order(
    order_in: OrderCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    created_order = await order_service.place_order(db, order_in, background_tasks)
    return created_order


@router.get(
    "/orders/{order_code}",
    response_model=OrderResponse,
    summary="Track Order by Code",
    description="Enables customers to inspect order status using their unique reference code.",
)
async def track_order(
    order_code: str,
    db: AsyncSession = Depends(get_db),
):
    return await order_service.get_order_by_code(db, order_code)


@router.get(
    "/orders",
    response_model=List[OrderResponse],
    summary="List Orders (Admin)",
)
async def list_orders(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    _authorized: bool = Depends(verify_admin_key),
):
    return await order_service.list_all_orders(db, limit=limit, offset=offset)


@router.patch(
    "/orders/{order_id}/status",
    response_model=OrderResponse,
    summary="Update Order Status (Admin)",
)
async def update_order_status(
    order_id: int,
    status_in: OrderStatusUpdate,
    db: AsyncSession = Depends(get_db),
    _authorized: bool = Depends(verify_admin_key),
):
    return await order_service.update_status(db, order_id, status_in)
