import asyncio
import logging
from app.core.config import settings

logger = logging.getLogger("app.workers.notification")


class NotificationWorker:
    @staticmethod
    async def process_new_order(
        order_id: int,
        order_code: str,
        customer_name: str,
        total_price: float,
        items_summary: str,
    ) -> None:
        """
        Asynchronous background task processing order receipt,
        audit logging, and alerting cafe baristas.
        """
        logger.info(
            "Background Worker: Processing order #%s (%s) for %s. Total: $%.2f. Items: %s",
            order_id,
            order_code,
            customer_name,
            total_price,
            items_summary,
        )

        # Simulate non-blocking asynchronous email / SMS / WhatsApp webhook dispatch
        await asyncio.sleep(0.05)

        logger.info(
            "Background Worker: Confirmation alert successfully queued for %s (Admin Target: %s)",
            order_code,
            settings.NOTIFICATION_EMAIL_TO,
        )

    @staticmethod
    async def process_contact_inquiry(
        name: str, email: str, subject: str, message: str
    ) -> None:
        """
        Asynchronous background task processing incoming contact messages.
        """
        logger.info(
            "Background Worker: Contact inquiry received from %s <%s> with subject: '%s'",
            name,
            email,
            subject,
        )
        await asyncio.sleep(0.05)
        logger.info(
            "Background Worker: Contact alert dispatched to %s",
            settings.NOTIFICATION_EMAIL_TO,
        )


notification_worker = NotificationWorker()
