from fastapi import FastAPI

from app.api.routers import router

app = FastAPI(docs_url="/")

app.include_router(router)
