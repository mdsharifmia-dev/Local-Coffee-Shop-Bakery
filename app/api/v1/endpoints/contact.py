from fastapi import APIRouter, BackgroundTasks, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.contact import ContactCreate, ContactSuccessResponse
from app.services.contact_service import contact_service

router = APIRouter()


@router.post(
    "/contact",
    response_model=ContactSuccessResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit Contact Inquiry",
    description="Validates inquiry, persists message to database, and triggers background email notification.",
)
async def submit_contact_form(
    inquiry_in: ContactCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    await contact_service.process_inquiry(db, inquiry_in, background_tasks)
    return ContactSuccessResponse()
