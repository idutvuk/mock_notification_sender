import asyncio
from abc import ABC, abstractmethod
from typing import Optional

from loguru import logger
from random import random

from pydantic import BaseModel


class Message(BaseModel):
    title: Optional[str]
    message: str


class Address(ABC):
    pass


class EmailAddress(Address):
    def __init__(self, email: str):
        self.email = email


class PhoneAddress(Address):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number


class TelegramAddress(Address):
    def __init__(self, telegram_id: str):
        self.telegram_id = telegram_id


class BaseNotificator(ABC):
    def __init__(self, fail_rate: float = 0.6, max_delay: float = 1):
        self.fail_rate = fail_rate
        self.max_delay = max_delay

    async def send_with_retry(
        self, address: Address, message: Message, max_retries=3
    ) -> bool:
        result = await self.send_message(address, message)
        if result:
            return True
        logger.error("failed to send")
        for i in range(max_retries):
            result = await self.send_message(address, message)
            if result:
                return True
            logger.error(f"sending retry failed ({i}/{max_retries})")
        return False

    @abstractmethod
    async def send_message(self, address: Address, message: Message) -> bool:
        """abstract mock function"""
        ...

    async def _simulate_network(self) -> bool:
        await asyncio.sleep(
            random() * self.max_delay
        )  # wait for the packet to be transmitted
        if not random() > self.fail_rate:
            logger.error(f"{self.__class__.__name__} failed")
            return False
        return True


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
        super().__init__(fail_rate=0.7, max_delay=2)

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
