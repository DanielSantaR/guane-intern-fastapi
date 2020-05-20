from sqlalchemy.orm import Session
from app.sql_app import models, schemas

from datetime import datetime
import requests


def get_all_dogs(db: Session):
    return db.query(models.Dog).all()


def get_dog_by_id(db: Session, dog_id: int):
    return db.query(models.Dog).filter(models.Dog.id == dog_id).first()


def get_dog_by_name(db: Session, dog_name: str):
    return db.query(models.Dog).filter(models.Dog.name == dog_name).all()


def get_adopted_dogs(db: Session):
    return db.query(models.Dog).filter(models.Dog.is_adopted == True).all()


def insert_dog(db: Session, dog: schemas.DogRecieved, dog_name: str):
    picture = (requests.get(
        'https://dog.ceo/api/breeds/image/random').json())['message']
    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    db_dog = models.Dog(name=dog_name, picture=picture,
                        create_date=create_date, update_date=update_date, **dog.dict())
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    message = f'{dog_name} was successfully added'
    return {'message': message, 'data': db_dog}


def delete_dog(db: Session, dog_id: int):
    dog_deleted = db.query(models.Dog).filter(models.Dog.id == dog_id).delete()
    if (dog_deleted != 0):
        db.execute('ALTER SEQUENCE dogs_id_seq RESTART;')
        db.execute("UPDATE dogs SET id = DEFAULT;")
        db.commit()
        message = f'Dog with id {dog_id} was successfully deleted'
        return {'message': message}
    message = f'Dog with id {dog_id} not found'
    return {'message': message}


def delete_all_dogs(db: Session):
    db.query(models.Dog).delete()
    db.execute('ALTER SEQUENCE dogs_id_seq RESTART;')
    db.commit()
    message = 'All dogs deleted successfully'
    return {'message': message}


def update_dog(db: Session, dog: schemas.UpdateDog, dog_id: int):
    update_dog = db.query(models.Dog).filter(models.Dog.id == dog_id).first()
    if (update_dog):
        update_dog.name = dog.name
        update_dog.update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        if(dog.picture):
            update_dog.picture = (requests.get(
                'https://dog.ceo/api/breeds/image/random').json())['message']
        update_dog.is_adopted = dog.is_adopted
        update_dog.age = dog.age
        update_dog.weight = dog.weight
        db.commit()

        message = f'Dog with id {dog_id} and named {update_dog.name} was successfully updated'
        return {'message': message}

    return None


def test_data(db: Session):
    db_dog = models.Dog(
        name='Lazy',
        picture='https://images.dog.ceo/breeds/papillon/n02086910_6483.jpg',
        create_date=datetime.now().strftime('2020-05-21 10:58:55.104954'),
        update_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        is_adopted=True,
        age=10,
        weight=9.3
    )
    db.add(db_dog)
    db_dog = models.Dog(
        name='Bruna',
        picture='https://dog.ceo/api/breeds/image/random',
        create_date=datetime.now().strftime('2020-04-21 11:45:55.104954'),
        update_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        is_adopted=False,
        age=8,
        weight=5.5
    )
    db.add(db_dog)
    db_dog = models.Dog(
        name='Lazy',
        picture='https://images.dog.ceo/breeds/hound-ibizan/n02091244_5943.jpg',
        create_date=datetime.now().strftime('2019-11-21 11:45:55.104954'),
        update_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
        is_adopted=False,
        age=7,
        weight=6.2
    )
    db.add(db_dog)
    db.commit()
    db.refresh(db_dog)
    message = 'test data generated correctly'
    return {'message': message}
