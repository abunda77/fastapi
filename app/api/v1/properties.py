# Isi from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud import crud_property
from app.schemas import property
from app.schemas import facility
from app.schemas import specification
from app.db.database import get_db
from sqlalchemy.orm import selectinload
from fastapi_pagination.ext.sqlalchemy import paginate
from app.db import models
from fastapi_pagination import Page, Params
from app.schemas import user
from core.security import get_current_user
from typing import List, Optional
from app.schemas import property_image 
#from app.schemas.property_image import PropertyImageCreate
from app.crud import crud_property_image 
from app.crud import crud_facility
from app.crud import crud_spesification 
from app.api.v1.users import get_superadmin_or_admin_user
router = APIRouter()


@router.get("/", response_model=Page[property.Property])
def read_properties(params: Params = Depends(), db: Session = Depends(get_db)):
    query = db.query(models.Property).options(selectinload(models.Property.images))
    return paginate(query, params)  # Return hasil paginate langsung


@router.get("/{property_id}", response_model=property.Property)
def read_property(property_id: int, db: Session = Depends(get_db)):
    db_property = crud_property.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property


@router.get("/user/{user_id}", response_model=Page[property.Property])
def read_user_properties(
    user_id: int,
    params: Params = Depends(),
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user)
):
    """
    Mengambil daftar properti milik pengguna tertentu.
    Hanya pengguna yang sedang login atau admin/superadmin yang dapat mengakses.
    """
    if current_user.id != user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to view these properties")
    
    query = db.query(models.Property).filter(models.Property.user_id == user_id).options(selectinload(models.Property.images))
    return paginate(query, params)


@router.post("/", response_model=property.Property)
def create_property(
    property_create: property.PropertyCreate, 
    db: Session = Depends(get_db), 
    current_user: user.User = Depends(get_current_user),
):
    return crud_property.create_property(db=db, property=property_create, current_user=current_user)

@router.put("/{property_id}", response_model=property.Property)
def update_property(
    property_id: int,
    property_update: property.PropertyUpdate,
    db: Session = Depends(get_db),
):
    db_property = crud_property.update_property(
        db, property_id=property_id, property_update=property_update
    )
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property


@router.delete("/{property_id}", response_model=property.Property)
def delete_property(property_id: int, db: Session = Depends(get_db)):
    db_property = crud_property.delete_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    return db_property

@router.get("/search/", response_model=Page[property.Property])
def search_properties(
    category: Optional[str] = Query(None, description="Filter berdasarkan kategori"),
    price: Optional[str] = Query(None, description="Urutkan berdasarkan harga (high/low)"),  # Ubah tipe data price menjadi str
    location: Optional[str] = Query(None, description="Filter berdasarkan nama lokasi"),  # Ubah deskripsi
    ads: Optional[str] = Query(None, description="Filter berdasarkan tipe iklan (sell/rent)"),
    keyword: Optional[str] = Query(None, description="Kata kunci pencarian di title atau description"),
    params: Params = Depends(),
    db: Session = Depends(get_db),
):
    """
    Mencari properti berdasarkan filter.
    """
    query = db.query(models.Property)

    if category:
        query = query.filter(models.Property.category_id == category)
    if price:
        if price == "high":
            query = query.order_by(models.Property.price.desc())
        elif price == "low":
            query = query.order_by(models.Property.price.asc())
    if location:
        # Cari kode region berdasarkan nama lokasi
        region_codes = db.query(models.Region.code).filter(models.Region.name.ilike(f"%{location}%")).all()
        region_codes = [code[0] for code in region_codes]  # Ambil hanya nilai code
        query = query.filter(
            (models.Property.province_id.in_(region_codes))
            | (models.Property.district_id.in_(region_codes))
            | (models.Property.city_id.in_(region_codes))
            | (models.Property.village_id.in_(region_codes))
        )
    if ads:
        query = query.filter(models.Property.ads == ads)
    if keyword:
        query = query.filter(
            (models.Property.title.ilike(f"%{keyword}%"))
            | (models.Property.description.ilike(f"%{keyword}%"))
        )

    query = query.options(selectinload(models.Property.images))
    return paginate(query, params)


@router.post("/{property_id}/images/", response_model=property_image.PropertyImage)
def create_property_image(
    property_id: int,
    image: property_image.PropertyImageCreate,
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user),
):
    """
    Menambahkan gambar baru ke properti.
    """
    db_property = crud_property.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    # Periksa otorisasi (hanya pemilik properti atau admin/superadmin yang boleh menambahkan gambar)
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to add image to this property")

    return crud_property_image.create_property_image(db=db, property_image=image, current_user=current_user, property_id=property_id)

@router.post("/{property_id}/bulk-images/", response_model=List[property_image.PropertyImage])  
def create_property_images(
    property_id: int,
    images: property_image.PropertyImageCreateList,
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user),
):
    """
    Menambahkan beberapa gambar baru ke properti.
    """
    db_property = crud_property.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    # Periksa otorisasi (hanya pemilik properti atau admin/superadmin yang boleh menambahkan gambar)
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to add image to this property")

    created_images = []
    for image_data in images.images:
        db_property_image = models.PropertyImage(**image_data.dict())  # Hapus property_id=property_id
        db.add(db_property_image)
        db.commit()
        db.refresh(db_property_image)
        created_images.append(db_property_image)

    return created_images



@router.delete("/{property_id}/images/{image_id}", response_model=property_image.PropertyImage)
def delete_property_image(
    property_id: int,
    image_id: int,
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user),
):
    """
    Menghapus gambar dari properti.
    """
    db_image = crud_property_image.get_property_image(db, property_image_id=image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    db_property = crud_property.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")

    # Periksa otorisasi (hanya pemilik properti atau admin/superadmin yang boleh menghapus gambar)
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete image from this property")

    # return crud_property_image.delete_property_image(db=db, property_image_id=image_id)
    return crud_property_image.delete_property_image(db=db, property_image_id=image_id, current_user=current_user)

@router.post("/{property_id}/facilities/", response_model=facility.Facility)
def create_facility(
    property_id: int,
    facility: facility.FacilityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Menambahkan fasilitas baru ke properti.
    """
    db_property = crud_property.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to add facility to this property")
    return crud_facility.create_facility(db=db, facility=facility, current_user=current_user, property_id=property_id)

@router.post("/{property_id}/specifications/", response_model=specification.Specification)
def create_specification(
    property_id: int,
    specification: specification.SpecificationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Menambahkan spesifikasi baru ke properti.
    """
    db_property = crud_property.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to add specification to this property")
    return crud_spesification.create_specification(db=db, specification=specification, current_user=current_user, property_id=property_id)

@router.delete("/{property_id}/facilities/{facility_id}", response_model=facility.Facility)
def delete_facility(
    property_id: int,
    facility_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Menghapus fasilitas dari properti.
    """
    db_facility = crud_facility.get_facility(db, facility_id=facility_id)
    if db_facility is None:
        raise HTTPException(status_code=404, detail="Facility not found")
    db_property = crud_property.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete facility from this property")
    return crud_facility.delete_facility(db=db, facility_id=facility_id, current_user=current_user)

@router.delete("/{property_id}/specifications/{specification_id}", response_model=specification.Specification)
def delete_specification(
    property_id: int,
    specification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Menghapus spesifikasi dari properti.
    """
    db_specification = crud_spesification.get_specification(db, specification_id=specification_id)
    if db_specification is None:
        raise HTTPException(status_code=404, detail="Specification not found")
    db_property = crud_property.get_property(db, property_id=property_id)
    if db_property is None:
        raise HTTPException(status_code=404, detail="Property not found")
    if current_user.id != db_property.user_id and current_user.role not in ["admin", "superadmin"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete specification from this property")
    return crud_spesification.delete_specification(db=db, specification_id=specification_id, current_user=current_user)

# app/api/v1/properties.py


