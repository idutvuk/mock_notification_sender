from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    title: Optional[str] = None
    message: str
