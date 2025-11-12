from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class JobStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class Job(BaseModel):
    created_at: datetime
    status: JobStatus
