#!/usr/bin/python3
"""This module defines the DBStorage engine"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User

class DBStorage:
    """hbnb models in a MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """new instance of DBStorage"""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(os.getenv('HBNB_MYSQL_USER'),
                                              os.getenv('HBNB_MYSQL_PWD'),
                                              os.getenv('HBNB_MYSQL_HOST'),
                                              os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

        self.__session = scoped_session(sessionmaker(
                    bind=self.__engine, expire_on_commit=False))

    def all(self, cls=None):
        """Queries all objects"""

        objects_dict = {}

        session = self.__session
        obj_dict = {}

        if cls:
            query = session.query(cls).all()
        else:
            classes = [State, City, User]
            query = []
            for cls in classes:
                query.extend(session.query(cls).all())

        for obj in query:
            key = '{}.{}'.format(obj.__class__.__name__, obj.id)
            obj_dict[key] = obj

        return obj_dict

    def new(self, obj):
        """Adds a new object"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commits all changes to db"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from db"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Creates all tables in the database"""
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                              expire_on_commit=False))
        self.__session = scoped_session(Session)

    def close(self):
        """Closes the current session"""
        self.__session.remove()
