from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.contact import ContactMessage
from app.repositories.contact_repo import contact_repo
from app.schemas.contact import ContactCreate
from app.workers.notification_worker import notification_worker


class ContactService:
    async def process_inquiry(
        self,
        db: AsyncSession,
        inquiry_in: ContactCreate,
        background_tasks: BackgroundTasks,
    ) -> ContactMessage:
        message = await contact_repo.create(db, inquiry_in)
        background_tasks.add_task(
            notification_worker.process_contact_inquiry,
            message.name,
            message.email,
            message.subject,
            message.message,
        )
        return message


contact_service = ContactService()
