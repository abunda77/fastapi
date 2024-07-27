from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum
from .region import Region
from pydantic_settings import SettingsConfigDict

class GenderEnum(str, Enum):
    man = "man"
    woman = "woman"

class SocialMedia(BaseModel):
    facebook: Optional[str] = None
    twitter: Optional[str] = None
    instagram: Optional[str] = None
    linkedin: Optional[str] = None
    youtube: Optional[str] = None
    tiktok: Optional[str] = None
    snapchat: Optional[str] = None
    pinterest: Optional[str] = None
    reddit: Optional[str] = None
    zoom: Optional[str] = None

class ProfileBase(BaseModel):
    user_id: int # tambahkan user_id di sini
    title: Optional[str]
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str]
    whatsapp: Optional[str]
    address: Optional[str]
    province_id: Optional[str]
    district_id: Optional[str]
    city_id: Optional[str]
    village_id: Optional[str]
    gender: GenderEnum
    birthday: Optional[datetime]
    avatar: Optional[str]
    company_name: Optional[str] = None  # Menambahkan field company_name
    biodata_company: Optional[str] = None  # Menambahkan field biodata_company
    jobdesk: Optional[str] = None  # Menambahkan jobdesk
    model_config = SettingsConfigDict(from_attributes=True)
    social_media: Optional[SocialMedia] = None  # Menambahkan field social_media

class ProfileCreate(ProfileBase):
      user_id: int # tambahkan user_id di sini


class ProfileUpdate(ProfileBase):
    pass



class ProfileInDBBase(ProfileBase):
    id: int
    province: Optional[Region]
    district: Optional[Region]
    city: Optional[Region]
    village: Optional[Region]


class Profile(ProfileInDBBase):
    pass


class ProfilePublic(ProfileInDBBase):
    user_id: Optional[int] = None  # Sembunyikan user_id untuk profil publik

class ProfileInfo(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str]
    email: EmailStr
    whatsapp: Optional[str]
    company_name: Optional[str]
    avatar: Optional[str]
    biodata_company: Optional[str]
    jobdesk: Optional[str]