from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.crud import crud_region
from app.schemas.region import Region
from app.db.database import get_db

router = APIRouter()

@router.get("/allregions", response_model=List[Region])
def read_regions(
    skip: int = 0,
    limit: int = 100,
    level: Optional[str] = None,
    code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    regions = crud_region.get_regions(db, skip=skip, limit=limit, level=level, code=code)
    return regions

@router.get("/regions/{code}", response_model=Region)
def read_region(code: str, db: Session = Depends(get_db)):
    region = crud_region.get_region(db, code=code)
    if region is None:
        raise HTTPException(status_code=404, detail="Region tidak ditemukan")
    return region

@router.get("/regions/{code}/parent", response_model=Optional[Region])
def read_parent_region(code: str, db: Session = Depends(get_db)):
    region = crud_region.get_region(db, code=code)
    if region is None:
        raise HTTPException(status_code=404, detail="Region tidak ditemukan")
    parent_region = crud_region.get_parent_region(db, region)
    return parent_region

@router.get("/regions/{code}/children", response_model=List[Region])
def read_child_regions(code: str, db: Session = Depends(get_db)):
    region = crud_region.get_region(db, code=code)
    if region is None:
        raise HTTPException(status_code=404, detail="Region tidak ditemukan")
    child_regions = crud_region.get_child_regions(db, region)
    return child_regions

