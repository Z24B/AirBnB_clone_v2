#!/usr/bin/python3
"""Defines the Place class."""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
import os

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')

if STORAGE_TYPE == "db":
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True, nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """Place class handles all application places"""
    __tablename__ = 'places'

    if STORAGE_TYPE == "db":
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

        amenities = relationship('Amenity', secondary='place_amenity',
                                 back_populates='place_amenities')
        reviews = relationship('Review', backref='place', cascade='delete')
    else:
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
        review_ids = []

        @property
        def amenities(self):
            """
                getter for amenities list, i.e. amenities attribute of self
            """
            from models import storage
            amenities = storage.all(Amenity)
            return [amenity for amenity in amenities.values()
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, amenity_obj):
            """
                setter for amenity_ids
            """
            if amenity_obj and amenity_obj.id not in self.amenity_ids:
                self.amenity_ids.append(amenity_obj.id)

        @property
        def reviews(self):
            """
                getter for reviews list, i.e. reviews attribute of self
            """
            from models import storage
            reviews = storage.all(Review)
            return [review for review in reviews.values()
                    if review.place_id == self.id]
