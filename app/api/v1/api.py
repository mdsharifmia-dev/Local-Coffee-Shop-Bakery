from fastapi import APIRouter
from app.api.v1.endpoints import contact, menu, orders

api_router = APIRouter()
api_router.include_router(menu.router, tags=["Menu"])
api_router.include_router(orders.router, tags=["Orders"])
api_router.include_router(contact.router, tags=["Contact"])
