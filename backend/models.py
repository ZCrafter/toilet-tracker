from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from .database import Base
from datetime import datetime

class Pee(Base):
    __tablename__ = 'pee'
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, default=datetime.utcnow)
    location = Column(String)

class Poo(Base):
    __tablename__ = 'poo'
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, default=datetime.utcnow)
    location = Column(String)

class Sum(Base):
    __tablename__ = 'sum'
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime, default=datetime.utcnow)
    vr = Column(Boolean)
    names = Column(JSON)  # List of names
