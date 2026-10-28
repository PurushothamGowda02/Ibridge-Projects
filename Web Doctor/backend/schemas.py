from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class HospitalBase(BaseModel):
    name: str
    address: str
    city: str
    phone: str
    email: Optional[str] = None
    description: Optional[str] = None


class HospitalCreate(HospitalBase):
    pass


class Hospital(HospitalBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone_number: Optional[str] = None
    role: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


class DoctorBase(BaseModel):
    specialty: str
    bio: str
    experience: int


class DoctorCreate(DoctorBase):
    user_id: int
    hospital_id: int


class Doctor(DoctorBase):
    id: int
    user: User
    hospital: Hospital
    rating: int

    class Config:
        from_attributes = True


class AppointmentBase(BaseModel):
    doctor_id: int
    appointment_date: datetime
    symptoms: str


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(AppointmentBase):
    id: int
    patient_id: int
    status: str
    notes: Optional[str] = None
    doctor: Doctor

    class Config:
        from_attributes = True


class SymptomInput(BaseModel):
    symptoms: str
    language: str = "en"


class SymptomAnalysis(BaseModel):
    condition: str
    specialist: str
    severity: str
    recommendation: str
    first_aid: List[str]
    precaution: List[str]
    model_source: str
    confidence: Optional[float] = None
    input_language: str
    normalized_symptoms: str
    audit_id: Optional[int] = None


class ModelInfo(BaseModel):
    name: str
    type: str
    clinical_scope: str
    datasets: List[str]
    intended_use: str
    limitations: str
    emergency_notice: str
    multilingual_support: List[str]


class AnalysisAuditOut(BaseModel):
    id: int
    patient_id: Optional[int] = None
    raw_symptoms: str
    normalized_symptoms: str
    input_language: str
    predicted_condition: str
    predicted_specialist: str
    predicted_severity: str
    model_source: str
    confidence: Optional[float] = None
    review_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ClinicianReviewCreate(BaseModel):
    verdict: str
    corrected_condition: Optional[str] = None
    corrected_severity: Optional[str] = None
    notes: Optional[str] = None


class ClinicianReviewOut(BaseModel):
    id: int
    analysis_id: int
    reviewer_user_id: int
    verdict: str
    corrected_condition: Optional[str] = None
    corrected_severity: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class NotificationBase(BaseModel):
    title: str
    message: str
    type: str = "info"


class NotificationCreate(NotificationBase):
    user_id: int
    related_appointment_id: Optional[int] = None


class Notification(NotificationBase):
    id: int
    user_id: int
    is_read: int
    related_appointment_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True
