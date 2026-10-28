from pydantic import BaseModel, Field, EmailStr, ConfigDict
from pydantic_core import core_schema
from typing import List, Optional, Any
from datetime import datetime
from enum import Enum
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.any_schema(),
        )

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: Any, _handler: Any) -> dict[str, Any]:
        return {"type": "string"}

class Role(str, Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class CourseStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class LessonType(str, Enum):
    VIDEO = "video"
    TEXT = "text"
    PDF = "pdf"
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"
    LIVE = "live"

# --- Models ---

class Profile(BaseModel):
    avatar: Optional[str] = None
    bio: Optional[str] = None
    interests: List[str] = []
    streak: int = 0
    total_points: int = 0

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    full_name: str
    password_hash: str
    role: Role = Role.STUDENT
    profile: Profile = Field(default_factory=Profile)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class Resource(BaseModel):
    name: str
    url: str

class Lesson(BaseModel):
    title: str
    type: LessonType
    content: Optional[str] = None
    youtube_url: Optional[str] = None
    order: int
    resources: List[Resource] = []

class Module(BaseModel):
    title: str
    order: int
    lessons: List[Lesson] = []

class Course(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: str
    thumbnail: Optional[str] = None
    category: str
    sub_category: Optional[str] = None
    status: CourseStatus = CourseStatus.DRAFT
    difficulty: str = "Beginner"
    instructor_id: str
    modules: List[Module] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )

class Enrollment(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: str
    course_id: str
    progress_percent: int = 0
    enrolled_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        json_encoders={ObjectId: str}
    )
