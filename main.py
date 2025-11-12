import uvicorn
from fastapi import FastAPI, HTTPException
from notifiers import EmailNotificator, SmsNotificator, TelegramNotificator, Message

app = FastAPI(docs_url="/")


@app.get("/health")
def healthcheck():
    return {"status": "healthy"}


@app.post("/notify", status_code=200)
async def notify_user(message: Message):
    notififiers = (
        EmailNotificator(),
        SmsNotificator(),
        TelegramNotificator(),
    )
    for notifier in notififiers:
        response = await notifier.send_with_retry(message)
        if response:
            return message
    raise HTTPException(status_code=500, detail="all notificators failed")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8089, reload=True)
