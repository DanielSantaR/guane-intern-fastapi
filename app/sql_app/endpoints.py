from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @router.post("/{name}", response_model=schemas.Dog)
# def inset_dog(name: str, dog: schemas.DogRecieved, db: Session = Depends(get_db)):
#     return crud.insert_dog(db=db, dog=dog, dog_id=3, dog_name=name)


@router.get("/", response_model=List[schemas.Dog])
def get_all_dogs(db: Session = Depends(get_db)):
    return crud.get_all_dogs(db)

@router.get("/{name}", response_model=List[schemas.Dog])
def get_dog_by_name(name: str, db: Session = Depends(get_db)):
    return crud.get_dog_by_name(db, name)



""" @router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@router.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items """