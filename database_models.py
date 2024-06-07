from sqlalchemy import Column, Integer, String  # SQLAlchemy components for defining database table columns and their types
from sqlalchemy.ext.declarative import declarative_base  # Base class for declarative SQLAlchemy table definitions


Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
