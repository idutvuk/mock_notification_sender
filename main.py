from datetime import datetime
import uuid
from enum import Enum
from typing import Optional

import uvicorn
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from notifiers import (
    EmailNotificator,
    SmsNotificator,
    TelegramNotificator,
    Message,
    EmailAddress,
    PhoneAddress,
    TelegramAddress,
)

from loguru import logger


class JobStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


class User(BaseModel):
    telegram_id: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    name: str


class Job(BaseModel):
    created_at: datetime
    status: JobStatus


app = FastAPI(docs_url="/")
db = {
    "jobs": {"test_job": Job(created_at=datetime.now(), status=JobStatus.SUCCESS)},
    "users": {
        "user_1": User(
            phone_number="+79001234567", email="ivan@gmail.com", name="Ivan"
        ),
        "user_2": User(telegram_id="987654321", name="Divan"),
    },
}  # fake db, in-memory storage


@app.get("/health")
def healthcheck():
    return {"status": "healthy"}


async def multiservice_notify(
    user_id: str,
    message: Message,
    job_id: str = "",
) -> bool:
    user = db["users"].get(user_id)
    if not user:
        if job_id:
            db["jobs"][job_id].status = JobStatus.FAILED
        return False

    notifiers_with_addresses = []

    if user.email:
        notifiers_with_addresses.append((EmailNotificator(), EmailAddress(user.email)))
    if user.phone_number:
        notifiers_with_addresses.append(
            (SmsNotificator(), PhoneAddress(user.phone_number))
        )
    if user.telegram_id:
        notifiers_with_addresses.append(
            (TelegramNotificator(), TelegramAddress(user.telegram_id))
        )

    for notifier, address in notifiers_with_addresses:
        response = await notifier.send_with_retry(address, message)
        if response:
            if job_id:
                db["jobs"][job_id].status = JobStatus.SUCCESS
            return True

    logger.error(f"failed to send notifications to {user_id}")
    if job_id:
        db["jobs"][job_id].status = JobStatus.FAILED
    return False


@app.post("/notify/{user_id}", status_code=202)
async def notify(user_id: str, message: Message, background_tasks: BackgroundTasks):
    if user_id not in db["users"]:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    job_id = str(uuid.uuid4())
    db["jobs"][job_id] = Job(created_at=datetime.now(), status=JobStatus.PENDING)

    background_tasks.add_task(multiservice_notify, user_id, message, job_id)

    return {"job_id": job_id, "status": "pending"}


@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = db["jobs"].get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"created_at": job.created_at, "status": job.status}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8057, reload=True)
