#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Amenity for database"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)
    places = relationship(
        "Place",
        secondary="place_amenity",
        back_populates='amenities'
    )
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
