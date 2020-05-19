from fastapi import APIRouter, Body, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from app.models.dog import Dog, DogRecieved, UpdateDog
from datetime import datetime

from app.db import postgres
import requests


router = APIRouter()


@router.get('/db/')
def get_all_dogs():

    cur, con = postgres.establish_connection()

    all_dogs = postgres.db_get_all_dogs(cur)
    postgres.close_connection(con, cur)

    if not (all_dogs):
        message = 'No dogs found'
        return message

    return {'message': 'all the dogs', 'dogs': all_dogs} 


@router.get('/name/{name}')
def get_dog_by_name(name: str = Path(..., min_length=1, max_length=20)):

    cur, con = postgres.establish_connection()
    print(name)
    dogs_by_name = postgres.db_get_dog_by_name(cur, name)
    postgres.close_connection(con, cur)

    if not(dogs_by_name):
        message = f'No dog found named {name}'
        return message

    return {'message': f'Found dogs named {name}', 'data': dogs_by_name}


@router.get('/id/{dog_id}')
def get_dog_by_id(dog_id: int = Path(..., ge=0)):

    cur, con = postgres.establish_connection()

    dog_by_id = postgres.db_get_dog_by_id(cur, dog_id)
    postgres.close_connection(con, cur)

    if not (dog_by_id):
        message = f'No dog found with id {dog_id}'
        return message

    return {'message': f'Found dog with id {dog_id}', 'dog': dog_by_id} 


@router.get('/db/is_adopted/')
def get_adopted_dogs():

    cur, con = postgres.establish_connection()

    adopted_dogs = postgres.db_get_adopted_dogs(cur)
    postgres.close_connection(con, cur)

    if not(adopted_dogs):
        message = 'No adopted dog'
        return message

    return {'message': 'Adopted dogs', 'data': adopted_dogs}


@router.post('/db/{name}')
def insert_dog(*, name: str, dog_recived: DogRecieved):

    cur, con = postgres.establish_connection()

    picture = (requests.get('https://dog.ceo/api/breeds/image/random').json())['message']
    create_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    is_adopted = dog_recived.is_adopted
    dog_age = dog_recived.age
    dog_weight = dog_recived.weight
    postgres.db_insert_dog(cur, name, picture, create_date, update_date, is_adopted, dog_age, dog_weight)

    postgres.db_commit(con)
    postgres.close_connection(con, cur)

    message = 'Dog successfully added'
    return {'message': message}


@router.put('/db/{dog_id}')
def update_dog(*, dog_id: int = Path(..., gt=0), update_dog: UpdateDog):
    
    cur, con = postgres.establish_connection()

    if (postgres.db_get_dog_by_id(cur, dog_id)):
       
        dog_name = update_dog.name

        if (update_dog.picture):
            picture = (requests.get('https://dog.ceo/api/breeds/image/random').json())['message']
            
        update_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        is_adopted = update_dog.is_adopted
        dog_age = update_dog.age
        dog_weight = update_dog.weight

        postgres.db_update_dog(
                                cur, 
                                dog_name, 
                                picture, 
                                update_date, 
                                is_adopted, 
                                dog_age, 
                                dog_weight,
                                dog_id
                                )

        postgres.db_commit(con)
        postgres.close_connection(con, cur)

        message = f'Dog with id {dog_id} and named {dog_name} was successfully updated'
        return {'message': message}

    postgres.close_connection(con, cur)
    message = f'No dog found with id {dog_id}'
    return message


@router.delete('/db/{dog_id}')
def delete_dog(*, dog_id: int = Path(..., gt=0)):

    cur, con = postgres.establish_connection()

    found_dog = postgres.db_get_dog_by_id(cur, dog_id)

    if (found_dog):
        deleted_name = found_dog[0][1]
        postgres.db_delete_by_id(cur, dog_id)

        postgres.db_commit(con)
        postgres.close_connection(con, cur)

        message = f'Dog with id {dog_id} named {deleted_name} was successfully deleted'
        return message

    postgres.close_connection(con, cur)   
    message = f'No dog found with id {dog_id}'
    return message
