from typing import List, Optional
from fastapi import APIRouter, Depends, Header, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.database import get_db
from app.schemas.menu import MenuItemCreate, MenuItemResponse, MenuItemUpdate
from app.services.menu_service import menu_service

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


@router.get(
    "/menu",
    response_model=List[MenuItemResponse],
    summary="Get Menu Items (Redis-Cached)",
    description="Delivers menu items with sub-10ms latency via Redis caching engine.",
)
async def list_menu_items(
    response: Response,
    category: Optional[str] = Query(None, description="Filter by category: coffee, pastry, or all"),
    db: AsyncSession = Depends(get_db),
):
    items, cache_status = await menu_service.get_menu(db, category)
    response.headers["X-Cache-Status"] = cache_status
    return items


@router.post(
    "/menu",
    response_model=MenuItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Menu Item (Admin)",
)
async def create_menu_item(
    item_in: MenuItemCreate,
    db: AsyncSession = Depends(get_db),
    _authorized: bool = Depends(verify_admin_key),
):
    created = await menu_service.create_item(db, item_in)
    return created


@router.patch(
    "/menu/{item_id}",
    response_model=MenuItemResponse,
    summary="Update Menu Item (Admin)",
)
async def update_menu_item(
    item_id: int,
    item_update: MenuItemUpdate,
    db: AsyncSession = Depends(get_db),
    _authorized: bool = Depends(verify_admin_key),
):
    updated = await menu_service.update_item(db, item_id, item_update)
    return updated


@router.delete(
    "/menu/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Menu Item (Admin)",
)
async def delete_menu_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    _authorized: bool = Depends(verify_admin_key),
):
    await menu_service.delete_item(db, item_id)
    return None
