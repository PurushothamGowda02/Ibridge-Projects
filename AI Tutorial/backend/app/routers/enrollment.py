from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db, Course as DBCourse, Enrollment as DBEnrollment
from app.core.auth import get_current_user
from datetime import datetime
import json

router = APIRouter(prefix="/enroll", tags=["Enrollment"])

@router.post("/{course_id}", status_code=status.HTTP_201_CREATED)
async def enroll_in_course(course_id: str, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    # Check if course exists
    result = await db.execute(select(DBCourse).where(DBCourse.id == int(course_id)))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    user_id = str(current_user.get("id", current_user.get("_id")))
    user_email = current_user.get("email")
    
    # Check if already enrolled
    result = await db.execute(
        select(DBEnrollment).where(
            DBEnrollment.user_id == user_id,
            DBEnrollment.course_id == course_id
        )
    )
    existing_enrollment = result.scalar_one_or_none()
    
    if existing_enrollment:
        return {"message": "Already enrolled"}
    
    new_enrollment = DBEnrollment(
        user_id=user_id,
        user_email=user_email,
        course_id=course_id,
        progress_percent=0,
        enrolled_at=datetime.utcnow()
    )
    
    db.add(new_enrollment)
    await db.commit()
    
    return {"message": "Enrolled successfully"}

@router.get("/my-courses")
async def get_my_courses(current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_id = str(current_user.get("id", current_user.get("_id")))
    
    # Get enrollments
    result = await db.execute(
        select(DBEnrollment).where(DBEnrollment.user_id == user_id).limit(100)
    )
    enrollments = result.scalars().all()
    
    # Get courses
    course_ids = [int(e.course_id) for e in enrollments]
    result = await db.execute(select(DBCourse).where(DBCourse.id.in_(course_ids)))
    courses = result.scalars().all()
    
    # Merge enrollment data
    results = []
    for course in courses:
        enroll = next((e for e in enrollments if e.course_id == str(course.id)), None)
        results.append({
            "_id": str(course.id),
            "title": course.title,
            "description": course.description,
            "thumbnail": course.thumbnail,
            "category": course.category,
            "difficulty": course.difficulty,
            "modules": json.loads(course.modules) if isinstance(course.modules, str) else course.modules,
            "progress": enroll.progress_percent if enroll else 0
        })
    
    return results
