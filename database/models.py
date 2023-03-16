from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, relationship
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    medications = relationship('Medication', backref='user', lazy='subquery')
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(Date, default=date.today)
    updated_at = Column(Date)


class Medication(Base):
    __tablename__ = 'medication'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(Date)
    updated_at = Column(Date)