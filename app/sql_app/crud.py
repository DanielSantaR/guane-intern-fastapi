from sqlalchemy.orm import Session

from app.sql_app import models, schemas


def get_all_dogs(db: Session):
    dogs = db.query(models.Dog).all()
    return dogs

def get_dog_by_id(db: Session, dog_id: int):
    return db.query(models.Dog).filter(models.Dog.id == dog_id).first()

def get_dog_by_name(db: Session, dog_name: str):
    return db.query(models.Dog).filter(models.Dog.name == dog_name).all()

def get_adopted_dogs(db: Session):
    return db.query(models.Dog).filter(models.Dog.is_adopted == True)

# def insert_dog(db: Session, dog: dog.Dog):
#     db_dog = models.Dog(
#                         name=dog.name, 
#                         picture=dog.picture, 
#                         create_date=dog.create_date, 
#                         update_dato=dog.update_date, 
#                         is_adopte=dog.is_adopted, 
#                         age=dog.age,
#                         weight=dog.weight
#                         )
#     db.add(db_dog)
#     db.commit()
#     db.refresh(db_dog)
#     return db_dog

def insert_dog(db: Session, dog: schemas.DogRecieved, dog_id: int, dog_name: str):
    db_dog = models.Dog(**dog.dict(), id=dog_id, name=dog_name)
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    return db_dog

def delete_dog(db: Session, dog_id: int):
    return db.delete(models.Dog).filter(models.Dog.id == dog_id)

def update_dog(db: Session, dog_id: int):
    pass