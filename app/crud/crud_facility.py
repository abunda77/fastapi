from sqlalchemy.orm import Session
from app.db import models
from app.schemas import facility
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status
from app.crud import crud_property
from app.schemas import user  

# def get_facility(db: Session, facility_id: int):
#     try:
#         return db.query(models.Facility).filter(models.Facility.id == facility_id).one()
#     except NoResultFound:
#         raise HTTPException(status_code=404, detail="Facility not found")


# def get_facilities(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Facility).offset(skip).limit(limit).all()


# def create_facility(db: Session, facility: facility.FacilityCreate):
#     db_facility = models.Facility(**facility.dict())
#     db.add(db_facility)
#     db.commit()
#     db.refresh(db_facility)
#     return db_facility


# def update_facility(db: Session, facility_id: int, facility_update: facility.FacilityUpdate):
#     db_facility = get_facility(db, facility_id)
#     if not db_facility:
#         return None
#     for key, value in facility_update.dict(exclude_unset=True).items():
#         setattr(db_facility, key, value)
#     db.add(db_facility)
#     db.commit()
#     db.refresh(db_facility)
#     return db_facility


# def delete_facility(db: Session, facility_id: int):
#     db_facility = get_facility(db, facility_id)
#     if not db_facility:
#         return None
#     db.delete(db_facility)
#     db.commit()
#     return db_facility
def get_facility(db: Session, facility_id: int):
    try:
        return db.query(models.Facility).filter(models.Facility.id == facility_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Facility not found")

def get_facility_by_property_id(db: Session, property_id: int):
    try:
        return db.query(models.Facility).filter(models.Facility.property_id == property_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Facility not found")

def get_facilities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Facility).offset(skip).limit(limit).all()

def create_facility(db: Session, facility: facility.FacilityCreate, property_id: int, current_user: user.User):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()

    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add facility to this property",
        )

    db_facility = models.Facility(**facility.dict(), property_id=property_id)  # Tambahkan property_id ke model
    db.add(db_facility)
    db.commit()
    db.refresh(db_facility)
    return db_facility

def update_facility(
    db: Session, facility_id: int, facility_update: facility.FacilityUpdate, current_user: user.User):
    db_facility = get_facility(db, facility_id)
    if not db_facility:
        raise HTTPException(status_code=404, detail="Facility not found")

    db_property = crud_property.get_property(db, property_id=db_facility.property_id) # get property data by facility id
    # Periksa otorisasi (hanya pemilik properti atau admin/superadmin yang boleh menghapus fasilitas)
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to update facility of this property")

    for key, value in facility_update.dict(exclude_unset=True).items():
        setattr(db_facility, key, value)

    db.add(db_facility)
    db.commit()
    db.refresh(db_facility)
    return db_facility

def delete_facility(
    db: Session, facility_id: int, current_user: user.User):
    """
    Menghapus fasilitas dari properti.
    """
    db_facility = get_facility(db, facility_id=facility_id)
    if db_facility is None:
        raise HTTPException(status_code=404, detail="Facility not found")

    db_property = crud_property.get_property(db, property_id=db_facility.property_id)

    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    # Periksa otorisasi (hanya pemilik properti atau admin/superadmin yang boleh menghapus fasilitas)
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete facility from this property")

    db.delete(db_facility)
    db.commit()

    return db_facility