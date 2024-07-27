from sqlalchemy.orm import Session, selectinload  # Import selectinload
from sqlalchemy.exc import IntegrityError, NoResultFound
from fastapi import HTTPException, status
from app.db import models
from app.schemas import user, profile
from app.core.security import get_current_user
from fastapi import Depends


# ...

def get_profile(db: Session, profile_id: int):
    try:
        profile = (
            db.query(models.Profile)
            .filter(models.Profile.user_id == profile_id)
            .options(
                selectinload(models.Profile.province),
                selectinload(models.Profile.district),
                selectinload(models.Profile.city),
                selectinload(models.Profile.village)
            )
            .one()
        )
        return profile
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Profile not found")

def get_profile_by_user_id(db: Session, user_id: int):
    try:
        profile = (
            db.query(models.Profile)
            .filter(models.Profile.user_id == user_id)
            .options(
                selectinload(models.Profile.province),
                selectinload(models.Profile.district),
                selectinload(models.Profile.city),
                selectinload(models.Profile.village)
            )
            .one()
        )
        return profile
    except NoResultFound:
        return None  # Return None jika profil tidak ditemukan
def get_profile_by_email(db: Session, email: str):
    try:
        profile = (
            db.query(models.Profile)
            .filter(models.Profile.email == email)
            .options(
                selectinload(models.Profile.province),
                selectinload(models.Profile.district),
                selectinload(models.Profile.city),
                selectinload(models.Profile.village)
            )
            .one()
        )
        return profile
    except NoResultFound:
        return None

def get_profiles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Profile).offset(skip).limit(limit).all()


def create_profile(db: Session, profile: profile.ProfileCreate, current_user: user.User = Depends(get_current_user)):
    # Periksa apakah user sudah memiliki profil
    existing_profile = get_profile_by_user_id(db, current_user.id)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user",
        )
    
   # Periksa apakah email sudah terdaftar
    existing_profile = get_profile_by_email(db, profile.email)
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Ambil objek Region berdasarkan code (jika ada)
    province = db.query(models.Region).filter(models.Region.code == profile.province_id).first()
    district = db.query(models.Region).filter(models.Region.code == profile.district_id).first()
    city = db.query(models.Region).filter(models.Region.code == profile.city_id).first()
    village = db.query(models.Region).filter(models.Region.code == profile.village_id).first()

    # Periksa otorisasi (hanya superadmin dan admin yang boleh membuatkan profil untuk user lain)
    if current_user.role not in ["superadmin", "admin"] and profile.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create a profile for this user",
        )

    db_profile = models.Profile(
        user_id=profile.user_id,
        title=profile.title,
        first_name=profile.first_name,
        last_name=profile.last_name,
        email=profile.email,
        phone=profile.phone,
        whatsapp=profile.whatsapp,
        address=profile.address,
        province=province,
        district=district,
        city=city,
        village=village,
        gender=profile.gender,
        birthday=profile.birthday,
        avatar=profile.avatar,
        company_name=profile.company_name,  # Menambahkan company_name
        biodata_company=profile.biodata_company,  # Menambahkan biodata_company
        jobdesk=profile.jobdesk,  # Menambahkan jobdesk 
    )
    try:
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
    except IntegrityError as e:
        db.rollback()  # Rollback jika terjadi error
    # Penanganan error (seperti pada solusi sebelumnya)
    else:
    # Jalankan kode ini jika tidak ada IntegrityError
        return db_profile


def update_profile(db: Session, profile_id: int, profile_update: profile.ProfileUpdate, current_user: user.User = Depends(get_current_user)):
    db_profile = get_profile(db, profile_id)
    if not db_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    
    # Periksa otorisasi (hanya user yang bersangkutan atau superadmin dan admin yang boleh mengubah profil)
    if current_user.role not in ["superadmin", "admin"] and db_profile.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this profile")

     # Periksa apakah user_id akan diubah
    if profile_update.user_id and profile_update.user_id != db_profile.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change user_id on existing profile",
        )
    
      # Periksa apakah email akan diubah dan apakah email baru sudah terdaftar pada pengguna lain
    if profile_update.email and profile_update.email != db_profile.email:
        existing_profile = get_profile_by_email(db, profile_update.email)
        if existing_profile:
            raise HTTPException(status_code=400, detail="Email already registered")

        
    # Update field-field yang ada di profile_update
    update_data = profile_update.dict(exclude_unset=True, exclude={'user_id'})

    # Dapatkan objek Region berdasarkan code (jika ada)
    if "province_id" in update_data:
        update_data["province"] = db.query(models.Region).filter(models.Region.code == update_data["province_id"]).first()
        del update_data["province_id"]  # Hapus province_id dari update_data
    if "district_id" in update_data:
        update_data["district"] = db.query(models.Region).filter(models.Region.code == update_data["district_id"]).first()
        del update_data["district_id"]
    if "city_id" in update_data:
        update_data["city"] = db.query(models.Region).filter(models.Region.code == update_data["city_id"]).first()
        del update_data["city_id"]
    if "village_id" in update_data:
        update_data["village"] = db.query(models.Region).filter(models.Region.code == update_data["village_id"]).first()
        del update_data["village_id"]

    for key, value in update_data.items():
        setattr(db_profile, key, value)

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def delete_profile(db: Session, profile_id: int, current_user: user.User):  # Hapus Depends(get_current_user)
    db_profile = get_profile(db, profile_id)
    if not db_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    # Periksa otorisasi (hanya user yang bersangkutan atau superadmin dan admin yang boleh mengubah profil)
    if current_user.role not in ["superadmin", "admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this profile")

    db.delete(db_profile)
    db.commit()
    return db_profile