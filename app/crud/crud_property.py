from sqlalchemy.orm import Session, selectinload  # Import selectinload
from app.db import models
from app.schemas import property, user
from fastapi import HTTPException, status
from sqlalchemy.orm.exc import NoResultFound
from app.db import models
from fastapi import Depends
from app.core.security import get_current_active_user


def get_property(db: Session, property_id: int):
    try:
        property = (
            db.query(models.Property)
            .filter(models.Property.id == property_id)
            .options(
                selectinload(models.Property.province),
                selectinload(models.Property.district),
                selectinload(models.Property.city),
                selectinload(models.Property.village),
                selectinload(models.Property.category),
                selectinload(models.Property.facility),
                selectinload(models.Property.specification),
                selectinload(models.Property.images)
            )
            .one()
        )
        return property
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Property not found")


def get_properties(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Property)
        .options(selectinload(models.Property.images)),  # Eager load images
                selectinload(models.Property.user_id).joinedload(models.Profile.user_id)  # Eager load profile
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_property(
    db: Session, property: property.PropertyCreate, current_user: user.User = Depends(get_current_active_user)
):
    db_property = models.Property(**property.dict(exclude={"user_id"}), user_id=current_user.id) 
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

def update_property(
    db: Session, property_id: int, property_update: property.PropertyUpdate
):
    db_property = get_property(db, property_id)
    if not db_property:
        return None
    for key, value in property_update.dict(exclude_unset=True).items():
        setattr(db_property, key, value)
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


def delete_property(db: Session, property_id: int):
    db_property = get_property(db, property_id)
    if not db_property:
        return None
    db.delete(db_property)
    db.commit()
    return db_property