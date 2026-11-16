from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    menu_item_id: int = Field(..., gt=0, description="Target menu item ID")
    quantity: int = Field(..., ge=1, le=100, description="Quantity of item (1 to 100)")


class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=120)
    customer_phone: Optional[str] = Field(None, max_length=30)
    special_notes: Optional[str] = Field(None, max_length=500)
    payment_method: str = Field(..., min_length=2, max_length=50)
    transaction_ref: Optional[str] = Field(None, max_length=100)
    items: List[OrderItemCreate] = Field(..., min_length=1)


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: Optional[int]
    item_name: str
    unit_price: float
    quantity: int
    subtotal: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    order_code: str
    customer_name: str
    customer_phone: Optional[str]
    special_notes: Optional[str]
    payment_method: str
    transaction_ref: Optional[str]
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: str = Field(
        ...,
        pattern="^(pending|confirmed|preparing|ready|completed|cancelled)$",
        description="New order status",
    )
