from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db, Quiz as DBQuiz, QuizAttempt as DBQuizAttempt, ProgressRecord as DBProgressRecord
from app.core.auth import get_current_user
from datetime import datetime
import json

router = APIRouter(prefix="/quizzes", tags=["Quizzes"])

@router.get("/{lesson_id}")
async def get_quiz(lesson_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(DBQuiz).where(DBQuiz.lesson_id == lesson_id))
    quiz = result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found for this lesson")
    
    return {
        "_id": str(quiz.id),
        "lesson_id": quiz.lesson_id,
        "questions": json.loads(quiz.questions) if isinstance(quiz.questions, str) else quiz.questions,
        "created_at": quiz.created_at
    }

@router.post("/attempt", status_code=status.HTTP_201_CREATED)
async def submit_quiz_attempt(attempt_data: dict, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """
    attempt_data: {
        "lesson_id": str,
        "course_id": str,
        "answers": { question_idx: option_idx }
    }
    """
    result = await db.execute(select(DBQuiz).where(DBQuiz.lesson_id == attempt_data["lesson_id"]))
    quiz = result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    questions = json.loads(quiz.questions) if isinstance(quiz.questions, str) else quiz.questions
    
    score = 0
    total_points = 0
    
    for i, question in enumerate(questions):
        total_points += question.get("points", 1)
        user_answer_idx = attempt_data["answers"].get(str(i))
        
        if user_answer_idx is not None:
            correct_idx = next((idx for idx, opt in enumerate(question.get("options", [])) if opt.get("is_correct")), -1)
            if user_answer_idx == correct_idx:
                score += question.get("points", 1)
    
    new_attempt = DBQuizAttempt(
        user_email=current_user["email"],
        quiz_id=str(quiz.id),
        lesson_id=attempt_data["lesson_id"],
        score=score,
        total_points=total_points,
        completed_at=datetime.utcnow()
    )
    
    db.add(new_attempt)
    await db.commit()
    
    # Mark lesson as completed if passed (50% threshold)
    if (score / total_points) >= 0.5 if total_points > 0 else True:
        result = await db.execute(
            select(DBProgressRecord).where(
                DBProgressRecord.user_email == current_user["email"],
                DBProgressRecord.lesson_id == attempt_data["lesson_id"]
            )
        )
        progress = result.scalar_one_or_none()
        
        if progress:
            progress.is_completed = True
            progress.updated_at = datetime.utcnow()
        else:
            new_progress = DBProgressRecord(
                user_email=current_user["email"],
                lesson_id=attempt_data["lesson_id"],
                is_completed=True,
                updated_at=datetime.utcnow()
            )
            db.add(new_progress)
        
        await db.commit()
    
    return {
        "score": score,
        "total": total_points,
        "percent": int((score/total_points)*100) if total_points > 0 else 0
    }

@router.get("/my-attempts/{lesson_id}")
async def get_my_attempts(lesson_id: str, current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(DBQuizAttempt).where(
            DBQuizAttempt.user_email == current_user["email"],
            DBQuizAttempt.lesson_id == lesson_id
        ).order_by(DBQuizAttempt.completed_at.desc()).limit(10)
    )
    attempts = result.scalars().all()
    
    return [
        {
            "_id": str(a.id),
            "user_email": a.user_email,
            "quiz_id": a.quiz_id,
            "lesson_id": a.lesson_id,
            "score": a.score,
            "total_points": a.total_points,
            "completed_at": a.completed_at
        }
        for a in attempts
    ]
