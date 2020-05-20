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
    picture: str
    create_date: datetime
    update_date: datetime

    class Config:
        orm_mode = True
