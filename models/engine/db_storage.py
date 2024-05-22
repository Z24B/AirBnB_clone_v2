#!/usr/bin/python3
"""This module defines the DBStorage class for HBNB project"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from sqlalchemy.orm import configure_mappers


class DBStorage:
    """This class manages storage of hbnb models in MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            getenv("HBNB_MYSQL_USER"),
            getenv("HBNB_MYSQL_PWD"),
            getenv("HBNB_MYSQL_HOST"),
            getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)

        if getenv('HBNB_ENV') == "test":
            Base.metadata.drop_all(self.__engine)

        self.__session = scoped_session(sessionmaker(bind=self.__engine))

        # Call configure_mappers to ensure all mappers are configured
        configure_mappers()

    def all(self, cls=None):
        """Query on the current database session"""
        if cls:
            if isinstance(cls, str):
                cls = eval(cls)
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for model_class in [State, City, User, Place, Review, Amenity]:
                objs.extend(self.__session.query(model_class).all())
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize the session"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
        """Remove the current session"""
        self.__session.remove()
