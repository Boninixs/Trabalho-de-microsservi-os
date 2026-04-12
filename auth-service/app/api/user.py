from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import create_user_service, login_user_service
from app.db.session import get_db
from app.core.dependencies import get_current_user


router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user_service(db, user.email, user.password)
        return {"id": new_user.id, "email": new_user.email}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        token = login_user_service(db, user.email, user.password)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me")
def get_me(user=Depends(get_current_user)):
    return {"user": user}