from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role: str
    is_active: bool

    class Config:
        from_attributes = True

# Animal Schemas
class AnimalBase(BaseModel):
    name: str
    species: str
    breed: str
    age: str
    gender: str
    description: str
    image_url: Optional[str] = None

class AnimalCreate(AnimalBase):
    pass

class Animal(AnimalBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Adoption Request Schemas
class AdoptionRequestBase(BaseModel):
    animal_id: Optional[int] = None
    message: Optional[str] = None

class AdoptionRequestCreate(AdoptionRequestBase):
    pass

class AdoptionRequest(AdoptionRequestBase):
    id: int
    user_id: Optional[int] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Rescue Report Schemas
class RescueReportBase(BaseModel):
    description: str
    location: str
    contact_info: str
    image_url: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

class RescueReportCreate(RescueReportBase):
    pass

class RescueReport(RescueReportBase):
    id: int
    user_id: Optional[int]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
