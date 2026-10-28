from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db, Course as DBCourse
from app.models.schemas import Course, CourseStatus, Role
from app.core.auth import get_current_user
from typing import List
import json

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/")
async def list_courses(category: str = None, db: AsyncSession = Depends(get_db)):
    query = select(DBCourse).where(DBCourse.status == "published")
    if category:
        query = query.where(DBCourse.category == category)
    
    result = await db.execute(query.limit(100))
    courses = result.scalars().all()
    
    return [
        {
            "_id": str(course.id),
            "title": course.title,
            "description": course.description,
            "thumbnail": course.thumbnail,
            "category": course.category,
            "sub_category": course.sub_category,
            "status": course.status,
            "difficulty": course.difficulty,
            "instructor_id": course.instructor_id,
            "modules": json.loads(course.modules) if isinstance(course.modules, str) else course.modules,
            "created_at": course.created_at,
            "updated_at": course.updated_at
        }
        for course in courses
    ]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_course(course: Course, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if current_user["role"] not in [Role.INSTRUCTOR, Role.ADMIN, Role.SUPER_ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized to create courses")
    
    course_dict = course.dict(by_alias=True)
    
    new_course = DBCourse(
        title=course_dict.get("title"),
        description=course_dict.get("description"),
        thumbnail=course_dict.get("thumbnail"),
        category=course_dict.get("category"),
        sub_category=course_dict.get("sub_category"),
        status=course_dict.get("status", "draft"),
        difficulty=course_dict.get("difficulty", "Beginner"),
        instructor_id=str(current_user.get("id", current_user.get("_id"))),
        modules=json.dumps(course_dict.get("modules", []))
    )
    
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    
    return {"id": str(new_course.id), "message": "Course created"}

@router.get("/{course_id}")
async def get_course(course_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBCourse).where(DBCourse.id == int(course_id)))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return {
        "_id": str(course.id),
        "title": course.title,
        "description": course.description,
        "thumbnail": course.thumbnail,
        "category": course.category,
        "sub_category": course.sub_category,
        "status": course.status,
        "difficulty": course.difficulty,
        "instructor_id": course.instructor_id,
        "modules": json.loads(course.modules) if isinstance(course.modules, str) else course.modules,
        "created_at": course.created_at,
        "updated_at": course.updated_at
    }

@router.patch("/{course_id}")
async def update_course(course_id: str, update_data: dict, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBCourse).where(DBCourse.id == int(course_id)))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if str(course.instructor_id) != str(current_user.get("id", current_user.get("_id"))) and current_user["role"] != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    for key, value in update_data.items():
        if hasattr(course, key):
            if key == "modules":
                setattr(course, key, json.dumps(value))
            else:
                setattr(course, key, value)
    
    await db.commit()
    return {"message": "Course updated"}
