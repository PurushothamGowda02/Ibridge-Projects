from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db, Course as DBCourse, ProgressRecord as DBProgressRecord, Enrollment as DBEnrollment
from app.core.auth import get_current_user
from datetime import datetime
import json

router = APIRouter(prefix="/progress", tags=["Progress Tracking"])

@router.patch("/{lesson_id}")
async def toggle_lesson_completion(lesson_id: str, course_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    user_email = current_user["email"]
    
    # Check current status
    result = await db.execute(
        select(DBProgressRecord).where(
            DBProgressRecord.user_email == user_email,
            DBProgressRecord.lesson_id == lesson_id
        )
    )
    progress = result.scalar_one_or_none()
    
    new_status = not progress.is_completed if progress else True
    
    if progress:
        progress.is_completed = new_status
        progress.updated_at = datetime.utcnow()
    else:
        new_progress = DBProgressRecord(
            user_email=user_email,
            lesson_id=lesson_id,
            is_completed=new_status,
            updated_at=datetime.utcnow()
        )
        db.add(new_progress)
    
    await db.commit()
    
    # Recalculate course progress
    result = await db.execute(select(DBCourse).where(DBCourse.id == int(course_id)))
    course = result.scalar_one_or_none()
    
    if course:
        modules = json.loads(course.modules) if isinstance(course.modules, str) else course.modules
        total_lessons = sum(len(m.get("lessons", [])) for m in modules)
        
        # Get all lesson IDs
        lesson_ids = []
        for m in modules:
            for l in m.get("lessons", []):
                lesson_ids.append(l.get("id"))
        
        # Count completed lessons
        result = await db.execute(
            select(func.count(DBProgressRecord.id)).where(
                DBProgressRecord.user_email == user_email,
                DBProgressRecord.lesson_id.in_(lesson_ids),
                DBProgressRecord.is_completed == True
            )
        )
        completed_count = result.scalar()
        
        new_progress_percent = int((completed_count / total_lessons) * 100) if total_lessons > 0 else 0
        
        # Update enrollment
        result = await db.execute(
            select(DBEnrollment).where(
                DBEnrollment.user_email == user_email,
                DBEnrollment.course_id == course_id
            )
        )
        enrollment = result.scalar_one_or_none()
        if enrollment:
            enrollment.progress_percent = new_progress_percent
            await db.commit()
        
        return {"status": "success", "is_completed": new_status, "progress": new_progress_percent}
    
    return {"status": "success", "is_completed": new_status, "progress": 0}

@router.get("/{course_id}")
async def get_course_progress(course_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    # Fetch course
    result = await db.execute(select(DBCourse).where(DBCourse.id == int(course_id)))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    modules = json.loads(course.modules) if isinstance(course.modules, str) else course.modules
    lesson_ids = []
    for m in modules:
        for l in m.get("lessons", []):
            lesson_ids.append(l.get("id"))
    
    # Get progress records
    result = await db.execute(
        select(DBProgressRecord).where(
            DBProgressRecord.user_email == current_user["email"],
            DBProgressRecord.lesson_id.in_(lesson_ids)
        )
    )
    records = result.scalars().all()
    
    return {r.lesson_id: r.is_completed for r in records}
