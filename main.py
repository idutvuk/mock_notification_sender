import uvicorn
from fastapi import FastAPI, HTTPException
from notifiers import EmailNotificatior, SmsNotificatior, TelegramNotificatior

app = FastAPI(docs_url="/docs")


@app.get("/health")
def healthcheck():
    return {"status": "healthy"}


@app.post("/notify", status_code=200)
def notify_user(user_id: str, message: str):
    notification_methods = (
        EmailNotificatior,
        SmsNotificatior,
        TelegramNotificatior,
    )  # assume we dont need affiliation check
    for notifier in notification_methods:
        if notifier.notify(user_id, message):
            return user_id
    raise HTTPException(status_code=500, detail="all notificators failed")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8004, reload=True)
