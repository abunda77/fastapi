from sqlalchemy.orm import Session
from app.db import models
from app.schemas import category
from sqlalchemy.orm.exc import NoResultFound
from fastapi import HTTPException, status

def get_category(db: Session, category_id: int):
    try:
        return db.query(models.Category).filter(models.Category.id == category_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Category not found")


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: category.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(db: Session, category_id: int, category_update: category.CategoryUpdate):
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    for key, value in category_update.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    db.delete(db_category)
    db.commit()
    return db_category
