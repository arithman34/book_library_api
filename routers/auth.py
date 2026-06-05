from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import hash_password, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db
from models import UserDB
from schemas import Token, UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserDB).filter(
        (UserDB.username == user.username) | (UserDB.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered.")
    
    hashed_password = hash_password(user.password)
    new_user = UserDB(**user.model_dump(exclude={"password"}), hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
