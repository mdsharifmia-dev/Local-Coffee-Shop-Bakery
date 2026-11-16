from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.contact import ContactMessage
from app.schemas.contact import ContactCreate


class ContactRepository:
    async def create(
        self, db: AsyncSession, contact_data: ContactCreate
    ) -> ContactMessage:
        message = ContactMessage(**contact_data.model_dump())
        db.add(message)
        await db.commit()
        await db.refresh(message)
        return message

    async def list_messages(
        self, db: AsyncSession, limit: int = 50, offset: int = 0
    ) -> List[ContactMessage]:
        query = (
            select(ContactMessage)
            .order_by(ContactMessage.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await db.execute(query)
        return list(result.scalars().all())


contact_repo = ContactRepository()
