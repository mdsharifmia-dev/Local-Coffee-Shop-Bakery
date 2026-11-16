from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class MenuItemBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    category: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., ge=0.0)
    description: Optional[str] = None
    is_available: bool = True
    tag: Optional[str] = None
    image_url: Optional[str] = None


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=120)
    category: Optional[str] = Field(None, min_length=2, max_length=50)
    price: Optional[float] = Field(None, ge=0.0)
    description: Optional[str] = None
    is_available: Optional[bool] = None
    tag: Optional[str] = None
    image_url: Optional[str] = None


class MenuItemResponse(MenuItemBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
