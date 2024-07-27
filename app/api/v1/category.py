from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from app.db import models
from app.schemas import category 
from app.crud import crud_category
 


router = APIRouter()

@router.get("/", response_model=Page[category.Category])
def read_categories(params: Params = Depends(), db: Session = Depends(get_db)):
    query = db.query(models.Category)
    return paginate(query, params)

@router.get("/{category_id}", response_model=category.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    db_category = crud_category.get_category(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


