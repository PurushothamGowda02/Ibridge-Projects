from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="user") # "admin" or "user"
    is_active = Column(Boolean, default=True)

    adoptions = relationship("AdoptionRequest", back_populates="user")
    reports = relationship("RescueReport", back_populates="user")

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    species = Column(String) # Dog, Cat, etc.
    breed = Column(String)
    age = Column(String) # Puppy, Adult, etc.
    gender = Column(String)
    description = Column(String)
    image_url = Column(String)
    status = Column(String, default="available") # available, adopted, pending
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    applications = relationship("AdoptionRequest", back_populates="animal")

class AdoptionRequest(Base):
    __tablename__ = "adoption_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    animal_id = Column(Integer, ForeignKey("animals.id"))
    message = Column(String)
    status = Column(String, default="pending") # pending, approved, rejected
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="adoptions")
    animal = relationship("Animal", back_populates="applications")

class RescueReport(Base):
    __tablename__ = "rescue_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    description = Column(String)
    location = Column(String)
    contact_info = Column(String)
    image_url = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    status = Column(String, default="reported") # reported, rescued, closed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="reports")
