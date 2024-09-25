from sqlalchemy.orm import Session
from typing import List, Optional
from app.db import models
from app.schemas.region import Region as RegionSchema

def get_regions(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    level: Optional[str] = None, 
    code: Optional[str] = None
) -> List[models.Region]:
    query = db.query(models.Region)
    
    if level:
        query = query.filter(models.Region.level == level)
    if code:
        query = query.filter(models.Region.code.startswith(code))
    
    return query.offset(skip).limit(limit).all()

def get_region(db: Session, code: str) -> Optional[models.Region]:
    return db.query(models.Region).filter(models.Region.code == code).first()

def create_region(db: Session, region: RegionSchema) -> models.Region:
    db_region = models.Region(**region.dict())
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region

def update_region(db: Session, code: str, region: RegionSchema) -> Optional[models.Region]:
    db_region = db.query(models.Region).filter(models.Region.code == code).first()
    if db_region:
        for key, value in region.dict(exclude_unset=True).items():
            setattr(db_region, key, value)
        db.commit()
        db.refresh(db_region)
    return db_region

def delete_region(db: Session, code: str) -> bool:
    db_region = db.query(models.Region).filter(models.Region.code == code).first()
    if db_region:
        db.delete(db_region)
        db.commit()
        return True
    return False

def get_parent_region(db: Session, region: models.Region) -> Optional[models.Region]:
    parent_level = get_parent_level(region.level)
    if parent_level:
        return db.query(models.Region).filter(
            models.Region.code == region.code[:len(region.code)-2],
            models.Region.level == parent_level
        ).first()
    return None

def get_child_regions(db: Session, region: models.Region) -> List[models.Region]:
    child_level = get_child_level(region.level)
    if child_level:
        return db.query(models.Region).filter(
            models.Region.code.startswith(region.code),
            models.Region.level == child_level
        ).all()
    return []

def get_parent_level(level: str) -> Optional[str]:
    levels = {
        'district': 'province',
        'city': 'district',
        'village': 'city'
    }
    return levels.get(level)

def get_child_level(level: str) -> Optional[str]:
    levels = {
        'province': 'district',
        'district': 'city',
        'city': 'village'
    }
    return levels.get(level)