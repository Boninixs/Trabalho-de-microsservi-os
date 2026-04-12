from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.services.user_service import create_user_service
from app.db.session import get_db

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user_service(db, user.email, user.password)
        return {"id": new_user.id, "email": new_user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))