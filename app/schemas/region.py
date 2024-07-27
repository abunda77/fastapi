from pydantic import BaseModel

class Region(BaseModel):
    code: str
    name: str
    level: str

    class Config:
        from_attributes = True
