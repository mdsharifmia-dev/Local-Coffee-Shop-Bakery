from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.menu import MenuItem
from app.schemas.menu import MenuItemCreate, MenuItemUpdate

INITIAL_MENU_DATA = [
    # Coffee & Drinks
    {
        "name": "Espresso",
        "category": "coffee",
        "price": 3.50,
        "description": "Rich single-origin extraction with hazelnut crema and dark chocolate finish.",
        "is_available": True,
        "tag": "CLASSIC",
        "image_url": "https://images.unsplash.com/photo-1510707577719-ae7c14805e3a?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Caffe Latte",
        "category": "coffee",
        "price": 4.50,
        "description": "Double shot espresso with silky microfoam steamed whole milk and latte art.",
        "is_available": True,
        "tag": "POPULAR",
        "image_url": "https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Cappuccino",
        "category": "coffee",
        "price": 4.00,
        "description": "Equal thirds espresso, velvety steamed milk, and airy dusted chocolate foam.",
        "is_available": True,
        "tag": "FAVORITE",
        "image_url": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Artisan Hot Chocolate",
        "category": "coffee",
        "price": 4.00,
        "description": "Valrhona Dutch cocoa with whole steamed milk and dark chocolate shavings.",
        "is_available": True,
        "tag": "WARM",
        "image_url": "https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Cold Brew Iced Coffee",
        "category": "coffee",
        "price": 3.50,
        "description": "18-hour cold steeped Ethiopian single origin beans served over crystal ice.",
        "is_available": True,
        "tag": "REFRESHING",
        "image_url": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Spiced Chai Latte",
        "category": "coffee",
        "price": 4.50,
        "description": "Stone-ground organic Assam tea infused with cardamom, ginger, and Ceylon cinnamon.",
        "is_available": True,
        "tag": "SPECIALTY",
        "image_url": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80",
    },
    # Artisan Bakery & Pastries
    {
        "name": "French Butter Croissant",
        "category": "pastry",
        "price": 3.00,
        "description": "Handmade with high-fat Normandy butter, laminated 27 times and baked golden daily.",
        "is_available": True,
        "tag": "BESTSELLER",
        "image_url": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Wild Blueberry Muffin",
        "category": "pastry",
        "price": 3.50,
        "description": "Bursting with sweet wild Maine blueberries and crowned with brown butter streusel.",
        "is_available": True,
        "tag": "FRESH",
        "image_url": "https://images.unsplash.com/photo-1607958996333-41aef7caefaa?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Glazed Cinnamon Roll",
        "category": "pastry",
        "price": 4.00,
        "description": "Fluffy yeast brioche dough rolled with Korintje cinnamon, drizzled with vanilla glaze.",
        "is_available": True,
        "tag": "SWEET",
        "image_url": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Chunky Chocolate Cookie",
        "category": "pastry",
        "price": 2.50,
        "description": "Crisp edge with molten chewy center packed with 70% dark Belgian chocolate chunks.",
        "is_available": True,
        "tag": "INDULGENT",
        "image_url": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "English Butter Scone",
        "category": "pastry",
        "price": 3.00,
        "description": "Traditional crumbly recipe served with clotted cream and strawberry preserves.",
        "is_available": True,
        "tag": "CLASSIC",
        "image_url": "https://images.unsplash.com/photo-1586985289688-ca3cf47d3e6e?auto=format&fit=crop&w=600&q=80",
    },
    {
        "name": "Raspberry Danish Pastry",
        "category": "pastry",
        "price": 3.50,
        "description": "Crispy laminated puff pastry centered with organic tart raspberry compote.",
        "is_available": True,
        "tag": "ARTISAN",
        "image_url": "https://images.unsplash.com/photo-1509365465985-25d11c17e812?auto=format&fit=crop&w=600&q=80",
    },
]


class MenuRepository:
    async def get_all(
        self,
        db: AsyncSession,
        category: Optional[str] = None,
        only_available: bool = False,
    ) -> List[MenuItem]:
        query = select(MenuItem)
        if category and category.lower() != "all":
            query = query.where(MenuItem.category == category.lower())
        if only_available:
            query = query.where(MenuItem.is_available.is_(True))
        query = query.order_by(MenuItem.id.asc())

        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, item_id: int) -> Optional[MenuItem]:
        query = select(MenuItem).where(MenuItem.id == item_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[MenuItem]:
        query = select(MenuItem).where(MenuItem.name == name)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, item_data: MenuItemCreate) -> MenuItem:
        item = MenuItem(**item_data.model_dump())
        db.add(item)
        await db.commit()
        await db.refresh(item)
        return item

    async def update(
        self, db: AsyncSession, item: MenuItem, update_data: MenuItemUpdate
    ) -> MenuItem:
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        await db.commit()
        await db.refresh(item)
        return item

    async def delete(self, db: AsyncSession, item: MenuItem) -> None:
        await db.delete(item)
        await db.commit()

    async def seed_initial_data_if_empty(self, db: AsyncSession) -> int:
        result = await db.execute(select(MenuItem))
        existing = result.scalars().first()
        if existing:
            return 0

        count = 0
        for item_data in INITIAL_MENU_DATA:
            item = MenuItem(**item_data)
            db.add(item)
            count += 1
        await db.commit()
        return count


menu_repo = MenuRepository()
