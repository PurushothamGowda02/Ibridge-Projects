import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_

from app.core.auth import get_current_user_optional
from app.core.database import get_db, SavedCourse as DBSavedCourse, PerformanceRecord as DBPerformanceRecord, ProgressRecord as DBProgressRecord
from app.services.ai_service import ai_service
from app.services.video_service import video_service
import json

router = APIRouter(prefix="/lms", tags=["LMS"])


@router.post("/videos")
async def get_videos(payload: dict, current_user=Depends(get_current_user_optional)):
    topic = payload.get("topic", "General Science")
    subject = payload.get("subject", "General")

    search_terms = [
        f"{subject} {topic} tutorial",
        f"{topic} full course",
        f"{topic} practice problems",
    ]

    videos = []
    for term in search_terms:
        video = await video_service.find_lesson_video(term)
        if not video:
            continue
        videos.append(
            {
                "id": video.get("id", uuid.uuid4().hex[:8]),
                "title": video.get("title") or term,
                "thumbnail": video.get("thumbnail"),
                "link": video.get("youtube_url"),
                "duration": video.get("duration") or 0,
                "viewCount": video.get("view_count") or 0,
                "uploader": "",
                "quality_score": 1,
            }
        )

    return {
        "topic": topic,
        "subject": subject,
        "personalized_for": [],
        "search_queries": search_terms,
        "video_clusters": {"Recommended": videos},
        "videos": videos,
    }


@router.post("/generate-course")
async def generate_course(payload: dict, current_user=Depends(get_current_user_optional)):
    topic = payload.get("topic", "Digital Marketing")
    difficulty = payload.get("difficulty", "Beginner")
    fallback = {
        "title": f"{topic} Learning Path",
        "description": f"A practical {difficulty} roadmap for {topic}.",
        "modules": [
            {"title": f"{topic} Fundamentals", "search_term": f"{topic} basics"},
            {"title": f"{topic} Intermediate Concepts", "search_term": f"{topic} intermediate tutorial"},
            {"title": f"{topic} Projects", "search_term": f"{topic} project tutorial"},
        ],
    }

    try:
        syllabus = await ai_service.generate_syllabus(topic, difficulty)
    except Exception as e:
        print(f"AI syllabus generation failed, using fallback: {e}")
        syllabus = fallback

    if not isinstance(syllabus, dict):
        syllabus = fallback

    modules = syllabus.get("modules")
    if not isinstance(modules, list) or not modules:
        modules = fallback["modules"]
        syllabus["modules"] = modules

    normalized_modules = []
    for raw_module in modules:
        module = raw_module if isinstance(raw_module, dict) else {}
        title = module.get("title") or f"{topic} Module"
        search_term = module.get("search_term") or f"{topic} {title}"

        result = {
            "title": title,
            "description": module.get("description"),
            "search_term": search_term,
            "videos": [],
            "module_test": {
                "topic": title,
                "endpoint": "/api/v1/lms/generate-test",
            },
        }

        try:
            video = await video_service.find_lesson_video(search_term)
            if video:
                result["videos"].append(
                    {
                        "id": video.get("id", uuid.uuid4().hex[:8]),
                        "title": video.get("title") or search_term,
                        "thumbnail": video.get("thumbnail"),
                        "link": video.get("youtube_url"),
                        "quality_score": 1,
                    }
                )
        except Exception as e:
            print(f"Video lookup failed for '{search_term}': {e}")

        normalized_modules.append(result)

    syllabus["title"] = syllabus.get("title") or fallback["title"]
    syllabus["description"] = syllabus.get("description") or fallback["description"]
    syllabus["modules"] = normalized_modules
    return syllabus


@router.post("/generate-test")
async def generate_test(payload: dict, current_user=Depends(get_current_user_optional)):
    topic = payload.get("topic", "Python Programming")
    difficulty = payload.get("difficulty", "Intermediate")
    test_type = payload.get("type", "mixed")
    try:
        result = await ai_service.generate_test(topic, difficulty, test_type)
        if isinstance(result, dict) and isinstance(result.get("questions"), list):
            return result
    except Exception as e:
        print(f"AI test generation failed, using fallback: {e}")

    return {
        "title": f"{topic} Test",
        "questions": [
            {
                "id": 1,
                "type": "mcq",
                "question": f"Which statement is true about {topic}?",
                "options": ["It requires practice", "It is a database", "It is an OS", "It is a browser"],
                "correct_answer": "It requires practice",
            },
            {
                "id": 2,
                "type": "coding",
                "task": f"Write a simple function to demonstrate a {topic} concept.",
            },
        ],
    }


@router.post("/generate-coding-practice")
async def generate_coding_practice(payload: dict, current_user=Depends(get_current_user_optional)):
    subject = payload.get("subject", "Programming")
    topic = payload.get("topic", "Python Basics")
    difficulty = payload.get("difficulty", "Intermediate")
    try:
        result = await ai_service.generate_coding_practice(subject, topic, difficulty)
        if isinstance(result, dict) and isinstance(result.get("problems"), list) and result["problems"]:
            return result
    except Exception as e:
        print(f"AI coding generation failed, using fallback: {e}")

    return {
        "problems": [
            {
                "id": "p1",
                "title": f"{topic} Warmup",
                "description": f"Solve a coding task on {topic}. Write code, handle input, and return correct output.",
                "input_format": "Standard input",
                "output_format": "Standard output",
                "constraints": "Optimize for time and space where possible",
                "sample_input": "5",
                "sample_output": "25",
                "hints": ["Break into steps", "Test edge cases"],
            },
            {
                "id": "p2",
                "title": f"{topic} Intermediate",
                "description": f"Solve an intermediate coding problem related to {topic}.",
                "input_format": "Standard input",
                "output_format": "Standard output",
                "constraints": "n up to 10^5",
                "sample_input": "6",
                "sample_output": "36",
                "hints": ["Use efficient loops", "Avoid redundant recomputation"],
            },
            {
                "id": "p3",
                "title": f"{topic} Challenge",
                "description": f"Solve a challenge-level coding problem for {topic}.",
                "input_format": "Standard input",
                "output_format": "Standard output",
                "constraints": "Consider worst-case complexity",
                "sample_input": "10",
                "sample_output": "100",
                "hints": ["Think about data structures", "Validate boundary values"],
            },
        ]
    }


@router.post("/submit-coding")
async def submit_coding(payload: dict, current_user=Depends(get_current_user_optional)):
    code = payload.get("code", "") or ""
    passed = len(code.strip()) > 0
    score = 80 if passed else 0
    return {
        "passed": passed,
        "score": score,
        "feedback": "Good effort. Keep refining edge-case handling." if passed else "Submit non-empty code.",
        "improvements": ["Add input validation", "Cover edge cases"],
    }


@router.post("/complete-module")
async def complete_module(payload: dict, current_user=Depends(get_current_user_optional)):
    course_title = payload.get("course_title", "Untitled Course")
    module_title = payload.get("module_title", "Untitled Module")
    score = int(payload.get("score", 0))
    pass_mark = int(payload.get("pass_mark", 60))
    passed = score >= pass_mark
    return {
        "course_title": course_title,
        "module_title": module_title,
        "score": score,
        "pass_mark": pass_mark,
        "passed": passed,
        "next_action": "next_module" if passed else "retake_test_and_practice",
    }


@router.post("/submit-test-result")
async def submit_test_result(payload: dict, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user_optional)):
    user_email = current_user["email"] if current_user else "guest@example.com"
    topic = payload.get("topic", "General")
    score = int(payload.get("score", 0))
    total = int(payload.get("total", 1)) or 1
    percent = round((score / total) * 100, 2)
    
    new_record = DBPerformanceRecord(
        user_email=user_email,
        topic=topic,
        score=score,
        total_questions=total,
        percentage=percent,
        test_type="mcq",
        completed_at=datetime.utcnow()
    )
    
    db.add(new_record)
    await db.commit()
    
    return {"status": "saved", "percentage": percent}


@router.post("/join-course")
async def join_course(payload: dict, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user_optional)):
    user_email = current_user["email"] if current_user else "guest@example.com"
    course = payload.get("course")
    pretest = payload.get("pretest", {})
    if not isinstance(course, dict):
        raise HTTPException(status_code=400, detail="course payload is required")

    score = int(pretest.get("correct", 0))
    total = int(pretest.get("total", 1)) or 1
    percent = int(round((score / total) * 100))
    if percent < 60:
        raise HTTPException(status_code=400, detail="Pre-course test not passed (minimum 60%)")

    result = await db.execute(
        select(DBSavedCourse).where(
            and_(DBSavedCourse.user_email == user_email, DBSavedCourse.title == course.get("title"))
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.course = json.dumps(course)
        existing.joined = True
        existing.progress_percent = 0
        existing.pretest_percent = percent
        existing.updated_at = datetime.utcnow()
        await db.commit()
        course_id = str(existing.id)
    else:
        new_course = DBSavedCourse(
            user_email=user_email,
            title=course.get("title", "AI Course"),
            course=json.dumps(course),
            joined=True,
            progress_percent=0,
            pretest_percent=percent,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_course)
        await db.commit()
        await db.refresh(new_course)
        course_id = str(new_course.id)

    perf_record = DBPerformanceRecord(
        user_email=user_email,
        topic=course.get("title", "AI Course"),
        score=score,
        total_questions=total,
        percentage=percent,
        test_type="pre_course",
        completed_at=datetime.utcnow()
    )
    db.add(perf_record)
    await db.commit()
    
    return {"message": "Course joined successfully", "course_id": course_id}


@router.post("/save-course")
async def save_course(payload: dict, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user_optional)):
    user_email = current_user["email"] if current_user else "guest@example.com"
    course = payload.get("course")
    if not isinstance(course, dict):
        raise HTTPException(status_code=400, detail="course payload is required")
    
    result = await db.execute(
        select(DBSavedCourse).where(
            and_(DBSavedCourse.user_email == user_email, DBSavedCourse.title == course.get("title"))
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.course = json.dumps(course)
        existing.joined = False
        existing.progress_percent = 0
        existing.updated_at = datetime.utcnow()
        await db.commit()
        return {"message": "Course updated", "course_id": str(existing.id)}
    
    new_course = DBSavedCourse(
        user_email=user_email,
        title=course.get("title", "AI Course"),
        course=json.dumps(course),
        joined=False,
        progress_percent=0,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)
    
    return {"message": "Course saved", "course_id": str(new_course.id)}


@router.get("/my-courses")
async def my_courses(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user_optional)):
    user_email = current_user["email"] if current_user else "guest@example.com"
    
    result = await db.execute(
        select(DBSavedCourse).where(DBSavedCourse.user_email == user_email).order_by(DBSavedCourse.updated_at.desc()).limit(100)
    )
    docs = result.scalars().all()
    
    out = []
    for d in docs:
        course_data = json.loads(d.course) if isinstance(d.course, str) else d.course
        out.append(
            {
                "id": str(d.id),
                "title": d.title,
                "joined": bool(d.joined),
                "progress_percent": int(d.progress_percent),
                "pretest_percent": int(d.pretest_percent),
                "course": course_data,
            }
        )
    return out


@router.get("/performance")
async def get_performance(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user_optional)):
    user_email = current_user["email"] if current_user else "guest@example.com"

    # Get history
    result = await db.execute(
        select(DBPerformanceRecord).where(DBPerformanceRecord.user_email == user_email).order_by(DBPerformanceRecord.completed_at.desc()).limit(10)
    )
    history_docs = result.scalars().all()

    history = []
    for doc in history_docs:
        completed_at = doc.completed_at
        if isinstance(completed_at, datetime):
            date_str = completed_at.strftime("%Y-%m-%d")
        else:
            date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        score = doc.percentage if doc.percentage is not None else 0

        history.append(
            {
                "date": date_str,
                "score": float(score),
                "topic": doc.topic,
            }
        )

    # Get weak topics (simplified - SQLite doesn't have full aggregation pipeline)
    weak_topics = []

    # Get saved courses count
    result = await db.execute(
        select(func.count(DBSavedCourse.id)).where(
            and_(DBSavedCourse.user_email == user_email, DBSavedCourse.joined == True)
        )
    )
    saved_courses = result.scalar()
    mastery = [{"label": "Joined Courses", "value": saved_courses}]

    return {
        "history": history,
        "mastery": mastery,
        "weak_topics": weak_topics,
    }


@router.get("/streak")
async def get_streak(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user_optional)):
    user_email = current_user["email"] if current_user else "guest@example.com"

    # Get progress records
    result = await db.execute(
        select(DBProgressRecord).where(
            and_(DBProgressRecord.user_email == user_email, DBProgressRecord.is_completed == True)
        )
    )
    progress_docs = result.scalars().all()

    date_set = set()
    for doc in progress_docs:
        ts = doc.updated_at
        if isinstance(ts, datetime):
            date_set.add(ts.date())
    
    # Get performance records
    result = await db.execute(
        select(DBPerformanceRecord).where(DBPerformanceRecord.user_email == user_email)
    )
    perf_docs = result.scalars().all()
    
    for doc in perf_docs:
        ts = doc.completed_at
        if isinstance(ts, datetime):
            date_set.add(ts.date())

    if not date_set:
        return {"streak": 0}

    streak = 0
    day = datetime.now(timezone.utc).date()
    while day in date_set:
        streak += 1
        day = day - timedelta(days=1)

    return {"streak": streak}
