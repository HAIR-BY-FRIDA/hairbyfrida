import sqlalchemy.orm
from sqlalchemy import create_engine, Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = sqlalchemy.orm.declarative_base()


# User Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    gender = Column(String, nullable=False)

    # Relationship to the Appointment model
    appointments = relationship('Appointment', back_populates='user')


# Appointment Model
class Appointment(Base):
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(Date, nullable=False)
    service = Column(String, nullable=False)
    time = Column(String, nullable=False)
    status = Column(String, default='Pending')

    # Relationship back to the User
    user = relationship('User', back_populates='appointments')


# Set up the database
def setup_database():
    engine = create_engine('sqlite:///HairbyFrida.db')
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)  # Create all tables


# Only run the database setup if this script is run directly
if __name__ == '__main__':
    setup_database()
