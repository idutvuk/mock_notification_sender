import uvicorn
from fastapi import FastAPI


app = FastAPI(docs_url="/docs")


@app.get("/health")
def healthcheck():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)
