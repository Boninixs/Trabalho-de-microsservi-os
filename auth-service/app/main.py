from fastapi import FastAPI
from app.db.database import engine, Base
from app.api.user import router as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}