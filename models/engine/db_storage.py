#!/usr/bin/python3
""" DBStorage module """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from os import getenv


class DBStorage:
    """ Database storage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Initialize DBStorage """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session """
        from models import classes
        objects = {}
        if cls:
            query = self.__session.query(classes[cls])
            for obj in query.all():
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        else:
            for cls in classes.values():
                query = self.__session.query(cls)
                for obj in query.all():
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """ Add the object to the current database session """
        if obj:
            self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
