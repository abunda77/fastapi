from sqlalchemy.orm import Session
from app.db import models
from app.schemas import user
from fastapi import Depends
#from app.core.security import get_current_user
from fastapi import HTTPException, status





def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user.UserCreate):
    from app.core.security import get_password_hash
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role,
        is_active=user.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: user.UserUpdate):
    from app.core.security import get_password_hash
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        if key == "password":
            value = get_password_hash(value)
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_password(db: Session, user_id: int, hashed_password: str):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.password = hashed_password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int, current_user: user.User):  # Tambahkan current_user sebagai argumen (user.User = Depends(get_current_user)):
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Pengecekan otorisasi
    if current_user.role not in ["superadmin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    db.delete(db_user)
    db.commit()
    return db_user

def get_user_by_remember_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.remember_token == token).first()


def is_active(user: models.User):
    return user.is_active