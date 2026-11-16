import uuid
from typing import Any, Dict, List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order, OrderItem


class OrderRepository:
    @staticmethod
    def generate_order_code() -> str:
        return f"ORD-{uuid.uuid4().hex[:6].upper()}"

    async def create_order_atomic(
        self,
        db: AsyncSession,
        order_meta: Dict[str, Any],
        items_meta: List[Dict[str, Any]],
    ) -> Order:
        """
        Creates an Order and associated OrderItems within an atomic database transaction.
        If any step fails, the entire transaction is rolled back.
        """
        order = Order(
            order_code=self.generate_order_code(),
            customer_name=order_meta["customer_name"],
            customer_phone=order_meta.get("customer_phone"),
            special_notes=order_meta.get("special_notes"),
            payment_method=order_meta["payment_method"],
            transaction_ref=order_meta.get("transaction_ref"),
            total_price=order_meta["total_price"],
            status="pending",
        )
        db.add(order)
        await db.flush()  # Populates order.id

        for item_data in items_meta:
            order_item = OrderItem(
                order_id=order.id,
                menu_item_id=item_data["menu_item_id"],
                item_name=item_data["item_name"],
                unit_price=item_data["unit_price"],
                quantity=item_data["quantity"],
                subtotal=item_data["subtotal"],
            )
            db.add(order_item)

        await db.commit()
        await db.refresh(order)
        return order

    async def get_by_id(self, db: AsyncSession, order_id: int) -> Optional[Order]:
        query = select(Order).where(Order.id == order_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_code(self, db: AsyncSession, order_code: str) -> Optional[Order]:
        query = select(Order).where(Order.order_code == order_code)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def list_orders(
        self, db: AsyncSession, limit: int = 50, offset: int = 0
    ) -> List[Order]:
        query = (
            select(Order)
            .order_by(Order.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def update_status(
        self, db: AsyncSession, order: Order, new_status: str
    ) -> Order:
        order.status = new_status
        await db.commit()
        await db.refresh(order)
        return order


order_repo = OrderRepository()
