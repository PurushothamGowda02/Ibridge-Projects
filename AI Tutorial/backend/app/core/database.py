from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, JSON
from datetime import datetime
from app.core.config import settings
import os

# Get absolute path for SQLite database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, settings.DATABASE_PATH)

# SQLite database URL
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# Create session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Base class for models
Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="student")
    mobile = Column(String, default="0000000000")
    is_active = Column(Boolean, default=True)
    eligibility_test_passed = Column(Boolean, default=False)  # New field
    eligibility_test_score = Column(Integer, default=0)  # New field
    eligibility_test_taken_at = Column(DateTime, nullable=True)  # New field
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    thumbnail = Column(String)
    category = Column(String)
    sub_category = Column(String)
    status = Column(String, default="draft")
    difficulty = Column(String, default="Beginner")
    instructor_id = Column(String, nullable=False)
    modules = Column(JSON, default=[])  # Store as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, nullable=False)
    user_email = Column(String, nullable=False)
    course_id = Column(String, nullable=False)
    progress_percent = Column(Integer, default=0)
    enrolled_at = Column(DateTime, default=datetime.utcnow)

class ProgressRecord(Base):
    __tablename__ = "progress_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_email = Column(String, nullable=False)
    lesson_id = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_id = Column(String, nullable=False)
    questions = Column(JSON, default=[])  # Store as JSON
    created_at = Column(DateTime, default=datetime.utcnow)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_email = Column(String, nullable=False)
    quiz_id = Column(String, nullable=False)
    lesson_id = Column(String, nullable=False)
    score = Column(Integer, default=0)
    total_points = Column(Integer, default=0)
    completed_at = Column(DateTime, default=datetime.utcnow)

class PerformanceRecord(Base):
    __tablename__ = "performance_records"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_email = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)
    percentage = Column(Float, default=0.0)
    test_type = Column(String, default="mcq")
    completed_at = Column(DateTime, default=datetime.utcnow)

class SavedCourse(Base):
    __tablename__ = "lms_saved_courses"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_email = Column(String, nullable=False)
    title = Column(String, nullable=False)
    course = Column(JSON, default={})  # Store as JSON
    joined = Column(Boolean, default=False)
    progress_percent = Column(Integer, default=0)
    pretest_percent = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database connection functions
async def init_db():
    """Initialize database and create tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print(f"✅ SQLite database initialized at: {DB_PATH}")

async def close_db():
    """Close database connection"""
    await engine.dispose()
    print("Closed SQLite database connection")

async def get_db():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
