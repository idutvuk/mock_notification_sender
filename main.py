import uvicorn
from fastapi import FastAPI, HTTPException
from notifiers import EmailNotificator, SmsNotificator, TelegramNotificator
import random

app = FastAPI(docs_url="/docs")


@app.get("/health")
def healthcheck():
    return {"status": "healthy"}


@app.post("/notify", status_code=200)
async def notify_user(user_id: str, message: str):
    notififiers = (
        EmailNotificator(),
        SmsNotificator(),
        TelegramNotificator(),
    )
    for notifier in notififiers:
        response = await notifier.send_message(user_id, message)
        if response:
            return user_id
    raise HTTPException(status_code=500, detail="all notificators failed")


if __name__ == "__main__":
    random.seed(42)
    uvicorn.run("main:app", port=8088, reload=True)
