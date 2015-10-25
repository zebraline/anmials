# -*- coding: utf-8 -*-
"""

"""

__all__ = ['UserAnimals']

from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Text, NVARCHAR,\
    TIMESTAMP

from datetime import datetime
from animals.model import DeclarativeBase, metadata, DBSession


class UserAnimals(DeclarativeBase):
    __tablename__ = 'user_animals'

    user_animals_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, default=0)
    animal_id = Column(Integer, default=0)
    createtime = Column(DateTime, default=datetime.now)
