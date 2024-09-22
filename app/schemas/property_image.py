# app/schemas/property_image.py
from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from typing import List  # Tambahkan import ini

class PropertyImageBase(BaseModel):
    
    image_url: Optional[str] = None
    image_remote_url: Optional[str] = None
    is_primary: Optional[bool] = False

class PropertyImageCreate(PropertyImageBase):
    property_id: int

class PropertyImageUpdate(PropertyImageBase):
    pass

class PropertyImage(PropertyImageBase):
    id: int
    class Config:
        from_attributes = True

class PropertyImageCreateList(BaseModel):
    images: List[PropertyImageCreate]
