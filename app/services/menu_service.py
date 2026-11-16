import logging
from typing import Any, Dict, List, Optional, Tuple
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.core.redis import cache
from app.models.menu import MenuItem
from app.repositories.menu_repo import menu_repo
from app.schemas.menu import MenuItemCreate, MenuItemResponse, MenuItemUpdate

logger = logging.getLogger("app.services.menu")


class MenuService:
    @staticmethod
    def _get_cache_key(category: Optional[str]) -> str:
        cat = category.lower() if category else "all"
        return f"cache:menu:{cat}"

    async def invalidate_cache(self) -> None:
        """Invalidates all cached menu categories."""
        keys = ["cache:menu:all", "cache:menu:coffee", "cache:menu:pastry"]
        for k in keys:
            await cache.delete(k)
        logger.info("Menu cache invalidated for keys: %s", keys)

    async def get_menu(
        self, db: AsyncSession, category: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], str]:
        """
        Retrieves active menu items.
        First checks Redis cache (sub-10ms latency). If cold, queries DB and caches result.
        Returns: (items_list, cache_status: 'HIT' | 'MISS')
        """
        cache_key = self._get_cache_key(category)
        cached_data = await cache.get_json(cache_key)

        if cached_data is not None:
            return cached_data, "HIT"

        # Cache MISS: Read from primary database
        items = await menu_repo.get_all(db, category=category)
        serialized_items = [
            {
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "price": float(item.price),
                "description": item.description,
                "is_available": item.is_available,
                "tag": item.tag,
                "image_url": item.image_url,
                "created_at": item.created_at.isoformat() if item.created_at else None,
            }
            for item in items
        ]

        # Warm up the cache
        await cache.set_json(
            cache_key, serialized_items, ttl=settings.REDIS_CACHE_TTL_SECONDS
        )
        return serialized_items, "MISS"

    async def create_item(
        self, db: AsyncSession, item_data: MenuItemCreate
    ) -> MenuItem:
        existing = await menu_repo.get_by_name(db, item_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Menu item '{item_data.name}' already exists.",
            )

        new_item = await menu_repo.create(db, item_data)
        await self.invalidate_cache()
        return new_item

    async def update_item(
        self, db: AsyncSession, item_id: int, update_data: MenuItemUpdate
    ) -> MenuItem:
        item = await menu_repo.get_by_id(db, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with ID {item_id} not found.",
            )

        updated = await menu_repo.update(db, item, update_data)
        await self.invalidate_cache()
        return updated

    async def delete_item(self, db: AsyncSession, item_id: int) -> None:
        item = await menu_repo.get_by_id(db, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item with ID {item_id} not found.",
            )

        await menu_repo.delete(db, item)
        await self.invalidate_cache()


menu_service = MenuService()
