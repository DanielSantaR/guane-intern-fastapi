from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .database import Base
import datetime


class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    picture = Column(String)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    update_date = Column(DateTime, default=datetime.datetime.utcnow)
    is_adopted = Column(Boolean)
    age = Column(Integer)
    weight = Column(Integer)
