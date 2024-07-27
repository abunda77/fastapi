from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    name_category: str
    slug: str
    icon_url: Optional[str] = None

    model_config = SettingsConfigDict(from_attributes=True)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryInDBBase(CategoryBase):
    id: int


class Category(CategoryInDBBase):
    pass
