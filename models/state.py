#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
import os

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """State class handles all application states"""
    __tablename__ = 'states'

    if STORAGE_TYPE == "db":
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='all, delete, delete-orphan')
    else:
        name = ''

        @property
        def cities(self):
            """getter for list of City instances related to this State"""
            from models import storage
            from models.city import City
            cities = storage.all(City)
            return [city for city in cities.values() if city.state_id == self.id]
