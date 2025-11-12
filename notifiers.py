import asyncio
from abc import ABC, abstractmethod
from typing import Optional

from loguru import logger
from random import random

from pydantic import BaseModel


class Message(BaseModel):
    user_id: str
    title: Optional[str]
    message: str
    # def __repr__(self) -> str:
    #     return f"message for {self.user_id} with title: {self.title[:50]}: {self.message[:50]}"


class BaseNotificator(ABC):
    def __init__(self, fail_rate: float = 0.3, max_delay: float = 1):
        self.fail_rate = fail_rate
        self.max_delay = max_delay

    async def send_with_retry(self, message: Message, max_retries=3) -> bool:
        result = await self.send_message(message)
        if result:
            return True
        logger.error("failed to send")
        for i in range(max_retries):
            logger.error(f"sending retry failed ({i}/{max_retries})")
            result = await self.send_message(message)
            if result:
                return True
        return False

        # for try_id in range(max_retries):

    @abstractmethod
    async def send_message(self, message: Message) -> bool:
        """abstract function for mocking email, sms, telegram, takes user_id and message - returns bool - send status
        Simulating imperfect connection by random.random()"""
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
        super().__init__(fail_rate=0.9, max_delay=5)

    async def send_message(self, message: Message) -> bool:
        result = await self._simulate_network()
        if result:
            logger.debug(f"Sent email notification - {message}")
        return result


class SmsNotificator(BaseNotificator):
    def __init__(self):
        super().__init__(fail_rate=0.6, max_delay=3)

    async def send_message(self, message: Message) -> bool:
        result = await self._simulate_network()
        if result:
            logger.debug(f"Sent sms notification - {message}")
        return result


class TelegramNotificator(BaseNotificator):
    def __init__(self):
        super().__init__(fail_rate=0.3, max_delay=2)

    async def send_message(self, message: Message) -> bool:
        result = await self._simulate_network()
        if result:
            logger.debug(f"Sent tg notification - {message}")
        return result
