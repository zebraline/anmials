# -*- coding: utf-8 -*-
"""

"""

__all__ = ['Farm']

from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer, DateTime, String, Text, NVARCHAR,\
    TIMESTAMP

from datetime import datetime
from animals.model import DeclarativeBase, metadata, DBSession


class Farm(DeclarativeBase):
    __tablename__ = 'farm'

    farm_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(Unicode(16), unique=True, nullable=False)
    password = Column(Unicode(128))
    farm_address = Column(NVARCHAR(1000))
    farm_name = Column(NVARCHAR(100))
    owner_name = Column(NVARCHAR(100))
    owner_phone = Column(String(20))
    status = Column(Integer, default=0) # 0：未审核，1：审核通过，2：审核不通过
    description = Column(NVARCHAR(500)) # 未通过原因
    createtime = Column(DateTime, default=datetime.now)
    updatetime = Column(TIMESTAMP, nullable=False)
