from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.crud.user import get_user_by_username_or_email, create_user
from app.schemas.auth import UserCreate, LoginRequest, RefreshRequest
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token, create_refresh_token, verify_decode_jwt_token
from app.core.config import settings

router = APIRouter()


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username_or_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    user.password = hash_password(user.password)  # Hash the password
    new_user = create_user(db=db, user=user)
    return {"message": "User registered successfully", "user_id": new_user.id, "username": new_user.username}


@router.post("/login")
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_username_or_email(db, login_data.username)
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Create JWT token
    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})
    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
def refresh_token(payload: RefreshRequest):
    payload = verify_decode_jwt_token(payload.refresh_token, settings.REFRESH_SECRET_KEY)

    # Create new access and refresh tokens
    username = payload.get("id")
    new_access_token = create_access_token({"sub": username})
    new_refresh_token = create_refresh_token({"sub": username})

    return {"access_token": new_access_token, "refresh_token": new_refresh_token}
