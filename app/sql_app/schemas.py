from typing import Optional
from pydantic import BaseModel
from datetime import datetime

import requests

class DogRecieved(BaseModel):
    is_adopted: Optional[bool]
    age: Optional[int]
    weight: Optional[float]

class UpdateDog(BaseModel):
    name: Optional[str]
    picture: Optional[bool]
    is_adopted: Optional[bool]
    age: Optional[int]
    weight: Optional[float]

class Dog(DogRecieved):
    id: int
    name: str 
    picture: str = (requests.get('https://dog.ceo/api/breeds/image/random').json())['message']
    create_date: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    update_date: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f") 

    class Config:
        orm_mode = True


""" class Dog():
    def __init__(self, dog_received, name, id):
        self.id: int = id 
        self.name = name
        self.picture: str = (requests.get('https://dog.ceo/api/breeds/image/random').json())['message']
        self.create_date: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.update_date: Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.is_adopted = dog_received.is_adopted
        self.age = dog_received.age
        self.weight = dog_received.weight
 """