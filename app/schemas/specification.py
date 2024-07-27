from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from typing import Optional 

class SpecificationBase(BaseModel):
    land_size: int
    building_size: int
    bedroom: int
    carport: Optional[int] = None
    bathroom: Optional[int] = None
    dining_room: Optional[int] = None
    living_room: Optional[int] = None
    floors: Optional[int] = None

    model_config = SettingsConfigDict(from_attributes=True)

class SpecificationCreate(SpecificationBase):
    pass


class SpecificationUpdate(SpecificationBase):
    pass


class SpecificationInDBBase(SpecificationBase):
    id: int


class Specification(SpecificationInDBBase):
    pass
