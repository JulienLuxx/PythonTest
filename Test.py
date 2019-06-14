#!/usr/bin/env python3
# coding=utf-8
'''
Test
'''

import datetime,time,sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Boolean,Text,Date

base=declarative_base()

class articleType(base):
    __tablename__='articletype'

    Id=Column(Integer,primary_key=True)
    Name=Column(String(1024))
    EditerName=Column(String(1024))
    Status=Column(Integer)
    IsDeleted=Column(Boolean)
    CreateTime=Column(Date)
    Timestamp=Column(Date)


# engine=create_engine('mysql+mysqlconnector://root:2134006@localhost:3306/testdb?charset=utf8',encoding='utf-8')

engine=create_engine('mysql+mysqlconnector://root:2134006@localhost:3306/testdb')

DBSession=sessionmaker(bind=engine)

session=DBSession()

at=session.query(articleType).filter(articleType.Id==2).first()

# print(at.CreateTime)

# r=engine.execute('select * from articletype')

# print(r.fetchall())
nowTime=datetime.datetime.today()

new_at=articleType(
    Name='mko2',
    EditerName='py',
    Status=1,
    IsDeleted=False,
    CreateTime=nowTime,
    Timestamp=nowTime
)

try:
    # session.add(new_at)
    # session.commit()
    session.query(articleType).filter(articleType.Id==at.Id).update({articleType.CreateTime:nowTime})
    session.commit()
except ZeroDivisionError as ex:
    print(ex)
    session.close()
finally:
    session.close()

# print(datetime.datetime.today())

