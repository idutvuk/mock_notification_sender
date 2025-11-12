from loguru import logger

from app.models.message import Message
from app.models.address import EmailAddress, PhoneAddress, TelegramAddress
from app.models.job import JobStatus
from app.services.notifiers import (
    EmailNotificator,
    SmsNotificator,
    TelegramNotificator,
)
from app.db.storage import storage


class NotificationService:
    async def send_multiservice_notify(
        self,
        user_id: str,
        message: Message,
        job_id: str = "",
    ) -> bool:
        user = storage.get_user(user_id)
        if not user:
            if job_id:
                storage.update_job_status(job_id, JobStatus.FAILED)
            return False

        notifiers_with_addresses = []

        if user.email:
            notifiers_with_addresses.append(
                (EmailNotificator(), EmailAddress(user.email))
            )
        if user.phone_number:
            notifiers_with_addresses.append(
                (SmsNotificator(), PhoneAddress(user.phone_number))
            )
        if user.telegram_id:
            notifiers_with_addresses.append(
                (TelegramNotificator(), TelegramAddress(user.telegram_id))
            )

        for notifier, address in notifiers_with_addresses:
            response = await notifier.send_with_retry(address, message)
            if response:
                if job_id:
                    storage.update_job_status(job_id, JobStatus.SUCCESS)
                return True

        logger.error(f"failed to send notifications to {user_id}")
        if job_id:
            storage.update_job_status(job_id, JobStatus.FAILED)
        return False
