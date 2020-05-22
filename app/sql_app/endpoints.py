from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[schemas.Dog])
def get_all_dogs(db: Session = Depends(get_db)):
    db_dogs = crud.get_all_dogs(db)
    if not db_dogs:
        raise HTTPException(
            status_code=404, detail=f"No dogs found"
        )
    return db_dogs


@router.get("/name/{name}", response_model=List[schemas.Dog])
def get_dog_by_name(name: str = Path(..., min_length=2), db: Session = Depends(get_db)):
    db_dog_name = crud.get_dog_by_name(db, name)
    if not db_dog_name:
        raise HTTPException(
            status_code=404, detail=f"Dog named {name} not found"
        )
    return db_dog_name


@router.get("/id/{dog_id}", response_model=schemas.Dog)
def get_dog_by_id(dog_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    db_dog_id = crud.get_dog_by_id(db, dog_id)
    if db_dog_id is None:
        raise HTTPException(
            status_code=404, detail=f"Dog with id {dog_id} not found"
        )
    return db_dog_id


@router.get("/is_adopted/", response_model=List[schemas.Dog])
def get_adopted_dogs(db: Session = Depends(get_db)):
    db_adopted_dog = crud.get_adopted_dogs(db)
    if not db_adopted_dog:
        raise HTTPException(
            status_code=404, detail=f"No adopted dogs found"
        )
    return db_adopted_dog


@router.post("/test_data/")
def generate_test_data(db: Session = Depends(get_db)):
    return crud.test_data(db=db)


@router.post("/insert/{name}")
def inset_dog(dog: schemas.DogRecieved, name: str = Path(..., min_length=2), db: Session = Depends(get_db)):
    return crud.insert_dog(db=db, dog=dog, dog_name=name)


@router.put("/update/{dog_id}")
def update_dog(dog: schemas.UpdateDog, dog_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    db_dog_id = crud.update_dog(db, dog, dog_id)
    if db_dog_id is None:
        raise HTTPException(
            status_code=404, detail=f"Dog with id {dog_id} not found"
        )
    return db_dog_id


@router.delete("/{dog_id}")
def delete_dog(dog_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    return crud.delete_dog(db, dog_id)


@router.delete("/delete_all/")
def delete_all(db: Session = Depends(get_db)):
    return crud.delete_all_dogs(db)
