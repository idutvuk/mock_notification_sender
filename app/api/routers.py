import uuid
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, HTTPException

from app.models.message import Message
from app.models.job import Job, JobStatus
from app.services.notification_service import NotificationService
from app.db.storage import storage

router = APIRouter()
notification_service = NotificationService()


@router.get("/health")
def healthcheck():
    return {"status": "healthy"}


@router.post("/notify/{user_id}", status_code=202)
async def notify(user_id: str, message: Message, background_tasks: BackgroundTasks):
    if not storage.user_exists(user_id):
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    job_id = str(uuid.uuid4())
    storage.create_job(job_id, Job(created_at=datetime.now(), status=JobStatus.PENDING))

    background_tasks.add_task(
        notification_service.send_multiservice_notify, user_id, message, job_id
    )

    return {"job_id": job_id, "status": JobStatus.PENDING}


@router.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    job = storage.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"created_at": job.created_at, "status": job.status}
