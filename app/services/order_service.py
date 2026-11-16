import logging
from typing import List, Optional
from fastapi import BackgroundTasks, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order
from app.repositories.menu_repo import menu_repo
from app.repositories.order_repo import order_repo
from app.schemas.order import OrderCreate, OrderStatusUpdate
from app.workers.notification_worker import notification_worker

logger = logging.getLogger("app.services.order")


class OrderService:
    async def place_order(
        self,
        db: AsyncSession,
        order_in: OrderCreate,
        background_tasks: BackgroundTasks,
    ) -> Order:
        """
        Validates items and verifies unit prices strictly from backend records
        (preventing client-side price tampering), calculates total, and executes
        atomic persistence.
        """
        items_meta = []
        total_price = 0.0

        for req_item in order_in.items:
            menu_item = await menu_repo.get_by_id(db, req_item.menu_item_id)
            if not menu_item:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Menu item with ID {req_item.menu_item_id} does not exist.",
                )

            if not menu_item.is_available:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"'{menu_item.name}' is currently out of stock.",
                )

            unit_price = float(menu_item.price)
            subtotal = round(unit_price * req_item.quantity, 2)
            total_price += subtotal

            items_meta.append(
                {
                    "menu_item_id": menu_item.id,
                    "item_name": menu_item.name,
                    "unit_price": unit_price,
                    "quantity": req_item.quantity,
                    "subtotal": subtotal,
                }
            )

        total_price = round(total_price, 2)

        order_meta = {
            "customer_name": order_in.customer_name,
            "customer_phone": order_in.customer_phone,
            "special_notes": order_in.special_notes,
            "payment_method": order_in.payment_method,
            "transaction_ref": order_in.transaction_ref,
            "total_price": total_price,
        }

        # Atomic transaction execution
        order = await order_repo.create_order_atomic(db, order_meta, items_meta)

        # Enqueue non-blocking background notification
        summary = ", ".join(
            f"{i['quantity']}x {i['item_name']}" for i in items_meta
        )
        background_tasks.add_task(
            notification_worker.process_new_order,
            order.id,
            order.order_code,
            order.customer_name,
            order.total_price,
            summary,
        )

        return order

    async def get_order_by_code(
        self, db: AsyncSession, order_code: str
    ) -> Optional[Order]:
        order = await order_repo.get_by_code(db, order_code)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order '{order_code}' not found.",
            )
        return order

    async def list_all_orders(
        self, db: AsyncSession, limit: int = 50, offset: int = 0
    ) -> List[Order]:
        return await order_repo.list_orders(db, limit=limit, offset=offset)

    async def update_status(
        self, db: AsyncSession, order_id: int, status_in: OrderStatusUpdate
    ) -> Order:
        order = await order_repo.get_by_id(db, order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with ID {order_id} not found.",
            )
        return await order_repo.update_status(db, order, status_in.status)


order_service = OrderService()
