from sqlalchemy import Boolean, Column, Date, ForeignKey, Numeric, SmallInteger, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from src.api import db
from sqlalchemy.orm import relationship

Base = db.Model




# User model
class User(Base):
    __tablename__ = 'user'

    id_user = Column(Integer, primary_key=True)
    email = Column(String(50), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    password = Column(String(50), nullable=False)

    def __init__(self, email, first_name, last_name, is_admin, password=None):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.password = password


# Project model
class Project(Base):
    __tablename__ = 'project'

    id_project = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_archived = Column(Boolean, nullable=False)

    def __init__(self, code, name,start_date, id_project='', description=None, end_date=None, is_archived=False):
        if id_project != '':
            self.id_project = id_project
        self.code = code
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.is_archived = is_archived


# Action model
class Action(Base):
    __tablename__ = 'action'

    id_action = Column(Integer, primary_key=True)
    numero_action = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    id_project = Column(Integer, ForeignKey('project.id_project'), nullable=False)
    user_actions = relationship('UserAction', back_populates='action', cascade='all, delete-orphan')
    def __init__(self, name, numero_action, id_project, description=None):
        self.name = name
        self.numero_action = numero_action
        self.description = description
        self.id_project = id_project


# UserAction model
class UserAction(Base):
    __tablename__ = 'user_action'

    id_user = Column(Integer, ForeignKey('user.id_user', ), primary_key=True)
    id_action = Column(Integer, ForeignKey('action.id_action', ondelete='CASCADE'), primary_key=True)
    action = relationship('Action', back_populates='user_actions')
    def __init__(self, id_user, id_action):
        self.id_user = id_user
        self.id_action = id_action


# UserActionTime model
class UserActionTime(Base):
    __tablename__ = 'user_action_time'

    id_user_action_time = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    duration = Column(Numeric, nullable=False)
    id_user = Column(Integer, ForeignKey('user.id_user'), nullable=False)
    id_action = Column(Integer, ForeignKey('action.id_action'), nullable=False)

    def __init__(self, date, duration, id_user, id_action):
        self.date = date
        self.duration = duration
        self.id_user = id_user
        self.id_action = id_action


# Travel model
class Travel(Base):
    __tablename__ = 'travel'

    id_travel = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    start_place = Column(String(50), nullable=False)
    return_place = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    purpose = Column(String(50), nullable=False)
    start_municipality = Column(String(50), nullable=False)
    destination = Column(String(50), nullable=False)
    night_count = Column(SmallInteger, nullable=False)
    meal_count = Column(SmallInteger, nullable=False)
    comment = Column(Text, nullable=True)
    license_vehicle = Column(String(12), nullable=False)
    comment_vehicle = Column(Text, nullable=True)
    start_km = Column(SmallInteger, nullable=False)
    end_km = Column(SmallInteger, nullable=False)
    id_user = Column(Integer, ForeignKey('user.id_user'), nullable=False)
    id_project = Column(Integer, ForeignKey('project.id_project'), nullable=False)

    def __init__(self, start_date, end_date, start_place, return_place, status, purpose, id_user, id_project,
                 start_municipality, destination, night_count, meal_count, start_km, end_km,
                 license_vehicle, comment=None, comment_vehicle=None):
        self.start_date = start_date
        self.end_date = end_date
        self.start_place = start_place
        self.return_place = return_place
        self.status = status
        self.purpose = purpose
        self.id_user = id_user
        self.id_project = id_project
        self.start_municipality = start_municipality
        self.destination = destination
        self.night_count = night_count
        self.meal_count = meal_count
        self.comment = comment
        self.license_vehicle = license_vehicle
        self.comment_vehicle = comment_vehicle
        self.start_km = start_km
        self.end_km = end_km


# Expense model
class Expense(Base):
    __tablename__ = 'expense'

    id_expense = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    comment = Column(Text, nullable=True)
    amount = Column(Numeric, nullable=False)
    id_travel = Column(Integer, ForeignKey('travel.id_travel'), nullable=False)

    def __init__(self, name, amount, id_travel, comment=None):
        self.name = name
        self.amount = amount
        self.id_travel = id_travel
        self.comment = comment
