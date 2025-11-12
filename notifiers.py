from abc import ABC, abstractmethod
from loguru import logger
from random import random


class Notificatior(ABC):
    @staticmethod
    @abstractmethod
    def notify(user_id: str, message: str) -> bool:
        """abstract function for mocking email, sms, telegram, takes user_id and message - returns bool - send status
        Simulating imperfect connection by random.random()"""
        ...


class EmailNotificatior(Notificatior):
    @staticmethod
    def notify(user_id: str, message: str) -> bool:
        if random() < 0.7:  # we have very bad email servers
            logger.error("Email seervice is unavailable")
            return False
        logger.debug(f"Sent email notification for {user_id}, {message}")
        return True


class SmsNotificatior(Notificatior):
    @staticmethod
    def notify(user_id: str, message: str) -> bool:
        if random() < 0.4:  # we have very bad sms servers
            logger.error("Sms seervice is unavailable")
            return False
        logger.debug(f"Sent sms notification for {user_id}, {message}")
        return True


class TelegramNotificatior(Notificatior):
    @staticmethod
    def notify(user_id: str, message: str) -> bool:
        if random() < 0.4:  # telegram is blocked again :((
            logger.error("Telegram seervice is unavailable")
            return False
        logger.debug(f"Sent telegram notification for {user_id}, {message}")
        return True
