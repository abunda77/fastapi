from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .property_image import PropertyImage

from pydantic_settings import BaseSettings, SettingsConfigDict 
from .facility import Facility
from .specification import Specification
from .region import Region
from app.schemas.profile import Profile  # Import skema Profile
from . import user, profile
# ... (Skema untuk Facility, Specification, dll.)

class PropertyBase(BaseModel):
    user_id: int # diubah ke int
    category_id: int
    title: str
    short_desc: str
    description: str
    price: int
    period: str
    # facility_id: Optional[int]
    # specification_id: Optional[int]
    address: str
    province_id: Optional[str] = None
    district_id: Optional[str] = None
    city_id: Optional[str] = None
    village_id: Optional[str] = None
    coordinates: Optional[str] = None
    nearby: Optional[str] = None
    #image_id: Optional[int] = None
    #images: Optional[List[PropertyImage]] = []  # Ubah ini
    ads: str
    status: str
    views_count: Optional[int] = 0
    #featured: Optional[bool] = False
    meta_title: Optional[str]
    meta_description: Optional[str]
    keywords: Optional[str]
 
    model_config = SettingsConfigDict(from_attributes=True)

class PropertyCreate(PropertyBase):
    pass # Tambahkan user_id di sini


class PropertyUpdate(PropertyBase):
    pass


class PropertyInDBBase(PropertyBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class Property(PropertyInDBBase):
    facility: Optional[Facility]
    specification: Optional[Specification]
    images: Optional[List[PropertyImage]]  # Ubah menjadi List
    #images: Optional[PropertyImage] 
    province: Optional[Region]
    district: Optional[Region]
    city: Optional[Region]
    village: Optional[Region]
    user: user.User  # Tambahkan relasi ke User
    #profile: profile.Profile

class PropertyPublic(PropertyInDBBase):
    pass  # Skema untuk response publik, sesuaikan jika perlu