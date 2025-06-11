from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Any

from app.core.config import settings
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.schemas.auth import Token, Login, PasswordReset, PasswordResetConfirm
from app.schemas.base import UserCreate, User
from app.models.user import User as UserModel
from app.services.email import send_password_reset_email

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=User)
def register(*, db: Session = Depends(get_db), user_in: UserCreate) -> Any:
    """
    Register a new user.
    """
    user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = UserModel(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        phone_number=user_in.phone_number,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/password-reset", response_model=dict)
def password_reset(
    *,
    db: Session = Depends(get_db),
    password_reset: PasswordReset
) -> Any:
    """
    Request password reset.
    """
    user = db.query(UserModel).filter(UserModel.email == password_reset.email).first()
    if user:
        # In a real application, you would generate a token and send an email
        # For this example, we'll just simulate it
        token = create_access_token(data={"sub": user.email})
        send_password_reset_email(email_to=user.email, token=token)
    return {"msg": "Password recovery email sent"}

@router.post("/password-reset/confirm", response_model=dict)
def password_reset_confirm(
    *,
    db: Session = Depends(get_db),
    password_reset: PasswordResetConfirm
) -> Any:
    """
    Reset password.
    """
    # In a real application, you would verify the token
    # For this example, we'll just simulate it
    return {"msg": "Password updated successfully"} 