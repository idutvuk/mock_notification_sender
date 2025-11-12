from typing import Literal, Optional, Any

from pydantic import BaseModel


# decided to design own solution for this


class JobStatus(BaseModel):
    task_id: str
    state: Literal["PENDING", "IN_PROGRESS", "SUCCESS", "FAILURE"]
    result: Optional[Any] = None
