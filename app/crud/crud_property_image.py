from app.crud import crud_property
from app.crud import crud_property_image
from fastapi import Depends
from app.core.security import get_current_user
from app.schemas import user, property_image
from sqlalchemy.orm import Session
from app.db import models
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status

def get_property_image(db: Session, property_image_id: int):
    try:
        return db.query(models.PropertyImage).filter(models.PropertyImage.id == property_image_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Property image not found")

# get data image berdasar property id
def get_property_image_by_property_id(db: Session, property_id: int):
    try:
        return db.query(models.PropertyImage).filter(models.PropertyImage.property_id == property_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Property image not found")


def get_property_images(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PropertyImage).offset(skip).limit(limit).all()


def create_property_image(db: Session, property_image: property_image.PropertyImageCreate, property_id: int, current_user: user.User):
    db_property = db.query(models.Property).filter(models.Property.id == property_id).first()

    if not db_property:
        raise HTTPException(status_code=404, detail="Property not found")
    
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add image to this property",
        )

    db_property_image = models.PropertyImage(**property_image.dict())  # Tambahkan property_id ke model
    db.add(db_property_image)
    db.commit()
    db.refresh(db_property_image)
    return db_property_image

def update_property_image(
    db: Session, property_image_id: int, property_image_update: property_image.PropertyImageUpdate, current_user: user.User = Depends(get_current_user)):
    db_property_image = get_property_image(db, property_image_id)
    if not db_property_image:
        raise HTTPException(status_code=404, detail="Image not found")

    db_property = crud_property.get_property(db, property_id=db_property_image.property_id) # get property data by property image id
    # Periksa otorisasi (hanya pemilik properti atau admin/superadmin yang boleh menghapus gambar)
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete image from this property")

    for key, value in property_image_update.dict(exclude_unset=True).items():
        setattr(db_property_image, key, value)

    db.add(db_property_image)
    db.commit()
    db.refresh(db_property_image)
    return db_property_image

def delete_property_image(
    db: Session, property_image_id: int, current_user: user.User = Depends(get_current_user)
):
    """
    Menghapus gambar dari properti.
    """
    db_image = crud_property_image.get_property_image(db, property_image_id=property_image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    db_property = crud_property.get_property(db, property_id=db_image.property_id)

    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    # Periksa otorisasi (hanya pemilik properti atau admin/superadmin yang boleh menghapus gambar)
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete image from this property")

    db.delete(db_image)
    db.commit()

    return db_image