# -*- coding: utf-8 -*-
"""

"""

__all__ = ['FarmAnimals']

from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Text, NVARCHAR,\
    TIMESTAMP

from datetime import datetime
from animals.model import DeclarativeBase, metadata, DBSession


class FarmAnimals(DeclarativeBase):
    __tablename__ = 'farm_animals'

    farm_id = Column(Integer, default=0)
    type_id = Column(Integer, default=0) # 种类
    animal_id = Column(Integer, autoincrement=True, primary_key=True)
    animal_name = Column(NVARCHAR(100))
    animal_color = Column(NVARCHAR(100))
    animal_birthday = Column(String(20))
    animal_varieties = Column(Integer, default=0) # 品种
    sell_status = Column(Integer, default=0) # 0：未售，1：已售
    animal_healthy = Column(Integer, default=0) # 0：健康，1：死亡，2：生病
    animal_photo = Column(String(100))
    animal_price = Column(Integer, default=0)
    animal_gender = Column(Integer, default=0) # 0：公， 1：母
    createtime = Column(DateTime, default=datetime.now)
    updatetime = Column(TIMESTAMP, nullable=False)
