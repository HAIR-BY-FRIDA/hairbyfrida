import sqlalchemy.orm
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = sqlalchemy.orm.declarative_base()


# I am creating a base class from which all the mapped classes will inherit

# User Model
class User(Base):
    # This class represents a table in the database
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    # Defines this id column as the unique identifier for the table and it as an integer data type
    username = Column(String, nullable=False)
    # your username must be unique and cannot be empty. the data type is string
    password = Column(String, nullable=False)
    # cannot be empty
    role = Column(String, nullable=False)
    # either customer, staff or Admin and it cannot be null.


# Appointment Model
class Appointment(Base):
    __tablename__ = 'Appointments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    # This colum references the id column in the Users table
    staff_id = Column(Integer, ForeignKey('Users.id'), nullable=True)
    # It aso references the id column in the Users table. it can be empty.
    date_time = Column(DateTime, nullable=False)
    # This will be the column to know the date and time of the appointment
    status = Column(String, default='Pending')
    # This will show appointment status with the default being 'pending'
    # could be pending, accepted or rejected
    customer = relationship("User", foreign_keys=[user_id])
    # this establishes a relationship between Appointment and Users classes using the foreign key
    staff = relationship("User", foreign_keys=[staff_id])
    # same as before


# Creating the SQLite Database
engine = create_engine('sqlite:///HairbyFrida.db')
# this will create a new SQLite Database or connect to it once it already exists. In this case, once created this
# will ensure that it will connect to it when run again
# The 'engine' object is the starting point for any SQLALCHEMY application


# To create tables
Base.metadata.create_all(engine)

# To create a session
Session = sessionmaker(bind=engine)
session = Session()
# A session is used to interact with the database. Examples are to add, update, etc
