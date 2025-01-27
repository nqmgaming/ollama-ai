from fastapi import FastAPI
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.db import init_db


app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
