import asyncio
from abc import ABC, abstractmethod
from loguru import logger
from random import random


class BaseNotificator(ABC):
    def __init__(self, fail_rate: float = 0.3, max_delay: float = 1):
        self.fail_rate = fail_rate
        self.max_delay = max_delay

    @abstractmethod
    def send_message(self, user_id: str, message: str) -> bool:
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
        super().__init__(fail_rate=0.7, max_delay=5)

    async def send_message(self, user_id: str, message: str) -> bool:
        result = await self._simulate_network()
        if result:
            logger.debug(f"Sent email notification for {user_id}, {message}")
        return result


class SmsNotificator(BaseNotificator):
    def __init__(self):
        super().__init__(fail_rate=0.5, max_delay=3)

    async def send_message(self, user_id: str, message: str) -> bool:
        result = await self._simulate_network()
        if result:
            logger.debug(f"Sent sms notification for {user_id}, {message}")
        return result


class TelegramNotificator(BaseNotificator):
    def __init__(self):
        super().__init__(fail_rate=0.5, max_delay=1)

    async def send_message(self, user_id: str, message: str) -> bool:
        result = await self._simulate_network()
        if result:
            logger.debug(f"Sent tg notification for {user_id}, {message}")
        return result
