from sqlalchemy.orm import Session
from app.db import models
from app.schemas import specification
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status
from app.crud import crud_property  
from app.schemas import user

# def get_specification(db: Session, specification_id: int):
#     try:
#         return db.query(models.Specification).filter(models.Specification.id == specification_id).one()
#     except NoResultFound:
#         raise HTTPException(status_code=404, detail="Specification not found")


# def get_specifications(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Specification).offset(skip).limit(limit).all()


# def create_specification(db: Session, specification: specification.SpecificationCreate):
#     db_specification = models.Specification(**specification.dict())
#     db.add(db_specification)
#     db.commit()
#     db.refresh(db_specification)
#     return db_specification


# def update_specification(db: Session, specification_id: int, specification_update: specification.SpecificationUpdate):
#     db_specification = get_specification(db, specification_id)
#     if not db_specification:
#         return None
#     for key, value in specification_update.dict(exclude_unset=True).items():
#         setattr(db_specification, key, value)
#     db.add(db_specification)
#     db.commit()
#     db.refresh(db_specification)
#     return db_specification


# def delete_specification(db: Session, specification_id: int):
#     db_specification = get_specification(db, specification_id)
#     if not db_specification:
#         return None
#     db.delete(db_specification)
#     db.commit()
#     return db_specification
def get_specification(db: Session, specification_id: int):
    try:
        return db.query(models.Specification).filter(models.Specification.id == specification_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Specification not found")

def get_specification_by_property_id(db: Session, property_id: int):
    try:
        return db.query(models.Specification).filter(models.Specification.property_id == property_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Specification not found")

def get_specifications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Specification).offset(skip).limit(limit).all()

def create_specification(db: Session, specification: specification.SpecificationCreate, property_id: int, current_user: user.User):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()

    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add specification to this property",
        )

    db_specification = models.Specification(**specification.dict(), property_id=property_id)  # Tambahkan property_id ke model
    db.add(db_specification)
    db.commit()
    db.refresh(db_specification)
    return db_specification

def update_specification(
    db: Session, specification_id: int, specification_update: specification.SpecificationUpdate, current_user: user.User):
    db_specification = get_specification(db, specification_id)
    if not db_specification:
        raise HTTPException(status_code=404, detail="Specification not found")

    db_property = crud_property.get_property(db, property_id=db_specification.property_id) # get property data by specification id
    # Periksa otorisasi (hanya pemilik properti atau admin/superadmin yang boleh menghapus spesifikasi)
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to update specification of this property")

    for key, value in specification_update.dict(exclude_unset=True).items():
        setattr(db_specification, key, value)

    db.add(db_specification)
    db.commit()
    db.refresh(db_specification)
    return db_specification

def delete_specification(
    db: Session, specification_id: int, current_user: user.User):
    """
    Menghapus spesifikasi dari properti.
    """
    db_specification = get_specification(db, specification_id=specification_id)
    if db_specification is None:
        raise HTTPException(status_code=404, detail="Specification not found")

    db_property = crud_property.get_property(db, property_id=db_specification.property_id)

    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    # Periksa otorisasi (hanya pemilik properti atau admin/superadmin yang boleh menghapus spesifikasi)
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete specification from this property")

    db.delete(db_specification)
    db.commit()

    return db_specification