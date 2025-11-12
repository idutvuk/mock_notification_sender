from abc import ABC


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
