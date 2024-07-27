from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from typing import Optional 

class FacilityBase(BaseModel):
    certificate: str
    electricity: int
    line_phone: str
    internet: str
    road_width: str
    water_source: str
    hook: Optional[str] = None
    condition: Optional[str] = None
    security: Optional[str] = None
    wastafel: Optional[str] = None

    model_config = SettingsConfigDict(from_attributes=True)


class FacilityCreate(FacilityBase):
    pass


class FacilityUpdate(FacilityBase):
    pass


class FacilityInDBBase(FacilityBase):
    id: int


class Facility(FacilityInDBBase):
    pass
