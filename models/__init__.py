#!/usr/bin/python3
"""Initializes the models package"""
from os import getenv

STORAGE_TYPE = getenv('HBNB_TYPE_STORAGE')

if STORAGE_TYPE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
