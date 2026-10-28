from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime
import enum


class UserRole(str, enum.Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"


class Hospital(Base):
    __tablename__ = "hospitals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    description = Column(Text, nullable=True)

    doctors = relationship("Doctor", back_populates="hospital")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    phone_number = Column(String, nullable=True)
    role = Column(String, default=UserRole.PATIENT)

    appointments = relationship("Appointment", back_populates="patient")
    analysis_audits = relationship("AnalysisAudit", back_populates="patient")


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.id"))
    specialty = Column(String)
    bio = Column(String)
    experience = Column(Integer)
    rating = Column(Integer, default=5)

    user = relationship("User")
    hospital = relationship("Hospital", back_populates="doctors")
    appointments = relationship("Appointment", back_populates="doctor")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    appointment_date = Column(DateTime)
    status = Column(String, default="scheduled")
    symptoms = Column(String)
    notes = Column(String, nullable=True)

    patient = relationship("User", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")


class AnalysisAudit(Base):
    __tablename__ = "analysis_audits"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    raw_symptoms = Column(Text, nullable=False)
    normalized_symptoms = Column(Text, nullable=False)
    input_language = Column(String, default="en")
    predicted_condition = Column(String, nullable=False)
    predicted_specialist = Column(String, nullable=False)
    predicted_severity = Column(String, nullable=False)
    model_source = Column(String, nullable=False)
    confidence = Column(Float, nullable=True)
    review_status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    patient = relationship("User", back_populates="analysis_audits")
    reviews = relationship("ClinicianReview", back_populates="analysis", cascade="all, delete-orphan")


class ClinicianReview(Base):
    __tablename__ = "clinician_reviews"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_audits.id"), nullable=False)
    reviewer_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    verdict = Column(String, nullable=False)
    corrected_condition = Column(String, nullable=True)
    corrected_severity = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    analysis = relationship("AnalysisAudit", back_populates="reviews")
    reviewer = relationship("User")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String, default="info")  # info, appointment, alert
    is_read = Column(Integer, default=0)  # 0 = unread, 1 = read
    related_appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")
    appointment = relationship("Appointment")
