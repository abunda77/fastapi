from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud import crud_user
from app.schemas import user
from app.db.database import get_db
from app.core.security import get_current_user
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from app.db import models
router = APIRouter()

# Dependency untuk memeriksa apakah pengguna adalah superadmin atau admin
def get_superadmin_or_admin_user(
    current_user: user.User = Depends(get_current_user),
):
    if current_user.role not in ["superadmin", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not permissioned"
        )
    return current_user




@router.get("/", response_model=Page[user.User], dependencies=[Depends(get_superadmin_or_admin_user)]) # GET /api/v1/users/?page=2&size=20
def read_users(params: Params = Depends(), db: Session = Depends(get_db)):
    query = db.query(models.User)
    return paginate(query, params)
    


@router.get("/{user_id}", response_model=user.User)  # Hapus dependency yang tidak diperlukan
def read_user(user_id: int, db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    """
    Mengambil informasi user berdasarkan user_id. Hanya user yang bersangkutan atau admin/superadmin yang bisa mengakses.
    """

    if current_user.id == user_id or current_user.role in ["admin", "superadmin"]:
        db_user = crud_user.get_user(db, user_id=user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )


@router.put("/{user_id}", response_model=user.User)  
def update_user(
    user_id: int, 
    user_update: user.UserUpdate, 
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user)  
):
    """
    Memperbarui informasi user berdasarkan user_id. Hanya user yang bersangkutan atau admin/superadmin yang bisa mengakses.
    """

    if current_user.id == user_id or current_user.role in ["admin", "superadmin"]:
        db_user = crud_user.update_user(db, user_id=user_id, user_update=user_update)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )


@router.delete("/{user_id}", response_model=user.User, dependencies=[Depends(get_superadmin_or_admin_user)])
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user),
):
    db_user = crud_user.delete_user(db, user_id=user_id, current_user=current_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



