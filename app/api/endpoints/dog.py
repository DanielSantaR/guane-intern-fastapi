from fastapi import APIRouter, Body, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from app.models.dog import Dog, DogRecieved, UpdateDog
from datetime import datetime
import requests


router = APIRouter()

storage = []

global_id = 0


@router.get('/')
def get_all_dogs():
    return storage

@router.get('/{name}')
def get_dog_by_name(*, name: str):

    found_dogs_by_name = []
    for i in range(len(storage)):  
        if(storage[i]['name'] == name):
            dog = storage[i]
            found_dogs_by_name.append(dog)
    
    if not(found_dogs_by_name):
        message = f'No dog found named {name}'
        return message

    return {'message': f'Found dogs named {name}', 'data': found_dogs_by_name}


@router.get('/is_adopted/')
def get_adopted_dogs():

    adopted_dogs = []
    for i in range(len(storage)):
        if(storage[i]['is_adopted']):
            dog_adopted = storage[i]
            adopted_dogs.append(dog_adopted)

    if not(adopted_dogs):
        message = 'No adopted dog'
        return message

    return {'message': 'Adopted dogs', 'data': adopted_dogs}


@router.post('/{name}')
def insert_dog(*, name: str, dog_recived: DogRecieved):

    global global_id 
    global_id += 1
    dog = Dog(dog_recived, name, global_id)
    storage.extend([dog.__dict__])
    message = 'Dog successfully added'
    return {'message': message, 'dog': dog.__dict__}


@router.put('/{dog_id}')
def update_dog(
    *, 
    dog_id: int = Path(..., gt=0), 
    update_dog: UpdateDog
    ):

    for i in range(len(storage)):
        if(storage[i]['id']==dog_id):
            storage[i]['name'] = update_dog.name
            if(update_dog.picture):
                storage[i]['picture'] = (requests.get('https://dog.ceo/api/breeds/image/random').json())['message']
            storage[i]['update_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            storage[i]['is_adopted'] = update_dog.is_adopted
            uptade_name = storage[i]['name']
            message = f'Dog named {uptade_name} was successfully updated'
            return message
    
    message = f'No dog found with id {dog_id}'
    return message


@router.delete('/{dog_id}')
def delete_dog(*, dog_id: int = Path(..., gt=0)):

    for i in range(len(storage)):
        if(storage[i]['id']==dog_id):
            delete_name = storage[i]['name']
            storage.pop(i)
            message = f'Dog with id {dog_id} named {delete_name} was successfully deleted'
            return message
    
    message = f'No dog found with id {dog_id}'
    return message
    

@router.get('/get_test_data/')
def get_test_data():

    global global_id 
    global_id += 1
    dog_test1 = {
        "id": global_id,
        "name": "Lazy",
        "picture": "https://images.dog.ceo/breeds/papillon/n02086910_6483.jpg",
        "create_date": "2020-02-20 20:58:55.164954",
        "update_date": "2020-05-21 10:58:55.104954",
        "is_adopted": True,
        "weight": 12.5
    }

    global_id += 1
    dog_test2 = {
        "id": global_id,
        "name": "Bruna",
        "picture": "https://images.dog.ceo/breeds/hound-ibizan/n02091244_5943.jpg",
        "create_date": "2020-05-21 10:58:55.104954",
        "update_date": "2020-05-21 10:58:55.104954",
        "is_adopted": True,
        "age": 2
    }

    global_id += 1
    dog_test3 = {
        "id": global_id,
        "name": "Martina",
        "picture": "https://images.dog.ceo/breeds/hound-basset/n02088238_11136.jpg",
        "create_date": "2020-05-21 10:58:55.104954",
        "update_date": "2020-05-21 10:58:55.104954",
        "is_adopted": False,
        "age": 10,
        "weight": 8.8
    }

    global_id += 1
    dog_test4 = {
        "id": global_id,
        "name": "Lazy",
        "picture": "https://images.dog.ceo/breeds/terrier-westhighland/n02098286_4364.jpg",
        "create_date": "2020-05-21 10:58:55.104954",
        "update_date": "2020-05-21 10:58:55.104954",
        "is_adopted": False
    }

    storage.extend([dog_test1, dog_test2, dog_test3, dog_test4])
    message = 'successfully generated test data'
    return message
