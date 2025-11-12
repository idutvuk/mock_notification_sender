from datetime import datetime
import uuid

import uvicorn
from fastapi import FastAPI, BackgroundTasks
from notifiers import EmailNotificator, SmsNotificator, TelegramNotificator, Message

app = FastAPI(docs_url="/")
db = {"jobs": {"test_job_id": {"created_at": datetime.now(), "status": "success"}}}


@app.get("/health")
def healthcheck():
    return {"status": "healthy"}


async def multiservice_notify(
    message: Message,
    job_id: str = "",
) -> bool:
    notififiers = (
        EmailNotificator(),
        SmsNotificator(),
        TelegramNotificator(),
    )
    for notifier in notififiers:
        response = await notifier.send_with_retry(message)
        if response:
            if job_id:
                db["jobs"][job_id]["status"] = "success"
            return True
    db["jobs"][job_id]["status"] = "failed"
    return False


@app.post("/notify", status_code=202)
async def notify(message: Message, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    db["jobs"][job_id] = {"created_at": datetime.now(), "status": "pending"}

    background_tasks.add_task(multiservice_notify, message, job_id)

    return {"job_id": job_id, "status": "pending"}


@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    return db["jobs"].get(job_id, {"error": "not found"})


if __name__ == "__main__":
    uvicorn.run("main:app", port=8087, reload=True)
