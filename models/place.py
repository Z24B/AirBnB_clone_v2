#!/usr/bin/python3
"""Defines the Place class."""
import models
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship

try:
    place_amenity
except NameError:
    place_amenity = Table(
            "place_amenity", Base.metadata,
            Column("place_id", String(60),
                ForeignKey("places.id"), primary_key=True, nullable=False),
            Column("amenity_id", String(60),
                ForeignKey("amenities.id"), primary_key=True, nullable=False)
)   


class Place(BaseModel, Base):
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenity_ids = []

    amenities = relationship(
            "Amenity",
            secondary=place_amenity,
            back_populates="places"
    )

    if getenv("HBNB_TYPE_STORAGE") != 'db':
        @property
        def reviews(self):
            """ Place reviews """
            rv = models.storage.all(Review).values()
            return {re for re in rv if re.place_id == self.id}

        @property
        def amenities(self):
            """ Place amenities """
            ob = models.storage.all(Amenity).values()
            return [obj for obj in ob if obj.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, value):
            """ Amenities setter """
            if type(value) is Amenity:
                self.amenity_ids.append(value.id)
