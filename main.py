from fastapi import FastAPI

from review_app import router as review_router
from settings import settings

app = FastAPI()
app.include_router(review_router.router)


@app.get("/")
async def root():
    return {"message": settings.PROJECT_NAME}
