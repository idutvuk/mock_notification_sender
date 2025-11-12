from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    telegram_id: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    name: str
