import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
# class Champion(Base):
#     __tablename__ = 'champion'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#     updated_utc = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

class Summoner(Base):
    __tablename__ = 'summoner'
    account_id = Column(String(56), nullable=False)
    profile_icon_id = Column(Integer, nullable=False)
    revision_date = Column(Integer, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    piid = Column(Integer, nullable=False)
    summoner_level = Column(Integer)

# class Match(Base):
#     __tablename__ = 'match'
 
# class Address(Base):
#     __tablename__ = 'address'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     street_name = Column(String(250))
#     street_number = Column(String(250))
#     post_code = Column(String(250), nullable=False)
#     person_id = Column(Integer, ForeignKey('person.id'))
#     person = relationship(Person)
 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///abcdtft.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)