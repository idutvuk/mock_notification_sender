import asyncio
from abc import ABC, abstractmethod
from random import random

from loguru import logger

from app.models.message import Message
from app.models.address import Address, EmailAddress, PhoneAddress, TelegramAddress


class BaseNotificator(ABC):
    def __init__(self, fail_rate: float = 0.6, max_delay: float = 1):
        self.fail_rate = fail_rate
        self.max_delay = max_delay

    async def send_with_retry(
        self, address: Address, message: Message, max_retries: int = 3
    ) -> bool:
        result = await self.send_message(address, message)
        if result:
            return True
        logger.error(
            f"failed to send {self.__class__.__name__}{', retrying' if max_retries > 0 else ''}"
        )
        for i in range(max_retries):
            result = await self.send_message(address, message)
            if result:
                return True
            logger.error(
                f"sending retry {self.__class__.__name__} failed ({i + 1}/{max_retries})"
            )
        return False

    @abstractmethod
    async def send_message(self, address: Address, message: Message) -> bool: ...

    async def _simulate_network(self) -> bool:
        await asyncio.sleep(
            random() * self.max_delay
        )  # wait for the packet to be transmitted
        return random() > self.fail_rate


class EmailNotificator(BaseNotificator):
    def __init__(self):
        super().__init__(
            fail_rate=0.9, max_delay=5
        )  # for demonstrating purposes lets assume we are in runet 2027

    async def send_message(self, address: Address, message: Message) -> bool:
        if not isinstance(address, EmailAddress):
            logger.error(
                f"EmailNotificator received invalid address type: {type(address)}"
            )
            return False

        result = await self._simulate_network()
        if result:
            logger.success(f"Sent email notification to {address.email} - {message}")
        return result


class SmsNotificator(BaseNotificator):
    def __init__(self):
        super().__init__(fail_rate=0.8, max_delay=3)

    async def send_message(self, address: Address, message: Message) -> bool:
        if not isinstance(address, PhoneAddress):
            logger.error(
                f"SmsNotificator received invalid address type: {type(address)}"
            )
            return False

        result = await self._simulate_network()
        if result:
            logger.success(
                f"Sent sms notification to {address.phone_number} - {message}"
            )
        return result


class TelegramNotificator(BaseNotificator):
    def __init__(self):
        super().__init__(fail_rate=0.9, max_delay=2)

    async def send_message(self, address: Address, message: Message) -> bool:
        if not isinstance(address, TelegramAddress):
            logger.error(
                f"TelegramNotificator received invalid address type: {type(address)}"
            )
            return False

        result = await self._simulate_network()
        if result:
            logger.success(f"Sent tg notification to {address.telegram_id} - {message}")
        return result
