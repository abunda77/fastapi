# Isi file mirip dengan users.py, tetapi menggunakan crud_profile dan skema profile
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import crud_profile
from app.schemas import profile
from core.security import get_current_user

from app.schemas import user
from app.db.database import get_db
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page, Params
from app.db import models
from sqlalchemy.orm import selectinload


router = APIRouter()
def get_superadmin_or_admin_user(
    current_user: user.User = Depends(get_current_user),
):
    if current_user.role not in ["superadmin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not permissioned"
        )
    return current_user

@router.get("/", response_model=Page[profile.Profile], dependencies=[Depends(get_superadmin_or_admin_user)]) # GET /api/v1/profile/?page=2&size=20
def read_profiles(params: Params = Depends(), db: Session = Depends(get_db)):
    query = db.query(models.Profile).options(
        selectinload(models.Profile.province),
        selectinload(models.Profile.district),
        selectinload(models.Profile.city),
        selectinload(models.Profile.village)
    )
    return paginate(query, params)


@router.get("/{profile_id}", response_model=profile.Profile)
def read_profile(profile_id: int, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    """
    Mengambil informasi profile berdasarkan profile_id. Hanya user yang bersangkutan atau admin/superadmin yang bisa mengakses.
    """
    
    db_profile = crud_profile.get_profile(db, profile_id=profile_id)
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Cek otorisasi
    if current_user.id == db_profile.user_id or current_user.role in ["admin", "superadmin"]:
        return db_profile
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    




@router.post("/", response_model=profile.Profile)
def create_profile(
    profile_create: profile.ProfileCreate, 
    db: Session = Depends(get_db), 
    current_user: user.User = Depends(get_current_user)  # Tambahkan dependency current_user
):
    # ... (Logika otorisasi) ...
    return crud_profile.create_profile(db=db, profile=profile_create, current_user=current_user)

@router.put("/{profile_id}", response_model=profile.Profile)
def update_profile(
    profile_id: int,
    profile_update: profile.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user),  # Menambahkan dependency current_user
):
    db_profile = crud_profile.update_profile(
        db, profile_id=profile_id, profile_update=profile_update, current_user=current_user
    )
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    # Cek otorisasi
    if current_user.id == db_profile.user_id or current_user.role in ["admin", "superadmin"]:
        return db_profile
    else:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db_profile



# app/api/v1/profile.py

# ... (import lainnya)

@router.delete("/{profile_id}", response_model=profile.Profile, dependencies=[Depends(get_superadmin_or_admin_user)])
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user),  # Menambahkan dependency current_user
):
    db_profile = crud_profile.delete_profile(
        db, profile_id=profile_id, current_user=current_user  # Menambahkan current_user sebagai argumen
    )
    if db_profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


