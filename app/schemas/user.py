from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
import uuid
from pydantic_settings import BaseSettings, SettingsConfigDict
from .profile import ProfileInfo  # Added this line to import the Profile class


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "customer"
    is_active: Optional[bool] = True
    
    
    model_config = SettingsConfigDict(from_attributes=True)

class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True # diubah ke from_attributes
        from_attributes = True


class User(UserInDBBase):
    pass  # Skema untuk response lengkap
    updated_at: Optional[datetime]
    profile: Optional[ProfileInfo]

class UserPublic(UserInDBBase):
    email: Optional[EmailStr] = None  # Sembunyikan email untuk pengguna publik

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int  # Menambahkan field user_id

class TokenData(BaseModel):
    name: Optional[str] = None

class UserLogin(BaseModel):
    name: str
    password: str

class UserPasswordUpdate(BaseModel):
  password: str

