import uvicorn
from fastapi import FastAPI

from api.api import router as api_router
from config import app_settings

app = FastAPI(title=app_settings.TITLE)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
