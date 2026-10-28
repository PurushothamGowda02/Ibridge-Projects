import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from datetime import datetime
import bcrypt  # Using bcrypt directly to fix passlib bug

# Mocking config for seeding
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "lms_enterprise"

async def seed():
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]

    # 1. Clear existing data
    await db.users.delete_many({})
    await db.courses.delete_many({})
    await db.enrollments.delete_many({})
    await db.progress_records.delete_many({})
    await db.quizzes.delete_many({})
    await db.quiz_attempts.delete_many({})

    # 2. Create Admin & Instructor
    password = "password123".encode('utf-8')
    salt = bcrypt.gensalt()
    instructor_password = bcrypt.hashpw(password, salt).decode('utf-8')
    
    instructor = {
        "email": "instr@example.com",
        "full_name": "Dr. Sarah Expert",
        "password_hash": instructor_password,
        "role": "instructor",
        "profile": {"streak": 5, "total_points": 1200},
        "created_at": datetime.utcnow()
    }
    result = await db.users.insert_one(instructor)
    instructor_id = str(result.inserted_id)

    # 3. Define Seed Courses
    courses = [
        {
            "title": "Quantum Physics for Beginners",
            "description": "Understand the fundamental principles of quantum mechanics through simple visualizations and real-world examples.",
            "category": "Science",
            "difficulty": "Beginner",
            "instructor_id": instructor_id,
            "status": "published",
            "modules": [
                {
                    "title": "Introduction to Atoms",
                    "order": 0,
                    "lessons": [
                        {"id": "l1", "title": "What is an Atom?", "type": "video", "youtube_url": "https://www.youtube.com/watch?v=L2Q2qd9f0RI", "order": 0},
                        {"id": "l2", "title": "History of Quantum Theory", "type": "text", "content": "Detailed notes on Heisenberg and Schrödinger.", "order": 1}
                    ]
                }
            ]
        },
        {
            "title": "Full-Stack Development with FastAPI & React",
            "description": "Build high-performance web applications using modern Python backends and TypeScript frontends.",
            "category": "Programming",
            "difficulty": "Advanced",
            "instructor_id": instructor_id,
            "status": "published",
            "modules": [
                {
                    "title": "FastAPI Foundations",
                    "order": 0,
                    "lessons": [
                        {"id": "l3", "title": "Async in Python", "type": "video", "youtube_url": "https://www.youtube.com/watch?v=K56nAtVn7e4", "order": 0},
                        {"id": "l4", "title": "Dependency Injection", "type": "video", "youtube_url": "https://www.youtube.com/watch?v=5vTCHZc-7Xo", "order": 1},
                        {"id": "l4_quiz", "title": "FastAPI Knowledge Check", "type": "quiz", "order": 2}
                    ]
                }
            ]
        },
         {
            "title": "UPSC Civil Services Preparation: Ancient History",
            "description": "Comprehensive guide to ancient civilizations and Indian history for UPSC aspirants.",
            "category": "UPSC",
            "difficulty": "Intermediate",
            "instructor_id": instructor_id,
            "status": "published",
            "modules": [
                {
                    "title": "The Indus Valley Civilization",
                    "order": 0,
                    "lessons": [
                        {"id": "l5", "title": "Major Sites & Archeology", "type": "video", "youtube_url": "https://www.youtube.com/watch?v=fV66AD7xX7Q", "order": 0}
                    ]
                }
            ]
        },
        {
            "title": "Ace Your Technical Interview",
            "description": "Master data structures, algorithms, and system design for FAANG-level interviews.",
            "category": "Interview Prep",
            "difficulty": "Advanced",
            "instructor_id": instructor_id,
            "status": "published",
            "modules": [
                {
                    "title": "Array & String Manipulation",
                    "order": 0,
                    "lessons": [
                        {"id": "l6", "title": "Two-Pointer Technique", "type": "video", "youtube_url": "https://www.youtube.com/watch?v=On03HWe2t6E", "order": 0}
                    ]
                }
            ]
        }
    ]

    for course in courses:
        course["created_at"] = datetime.utcnow()
        await db.courses.insert_one(course)

    # 4. Create Sample Quiz
    sample_quiz = {
        "course_id": "WILL_BE_UPDATED", # Optional in schema if lesson_id is unique enough
        "lesson_id": "l4_quiz",
        "title": "FastAPI Foundations Quiz",
        "questions": [
            {
                "text": "What is the primary benefit of using 'async' in FastAPI?",
                "points": 1,
                "options": [
                    {"text": "It makes the code run in parallel on more CPUs", "is_correct": False},
                    {"text": "It allows the server to handle more concurrent requests without blocking", "is_correct": True},
                    {"text": "It automatically converts Python to Javascript", "is_correct": False}
                ]
            },
            {
                "text": "FastAPI is built on top of which two major libraries?",
                "points": 1,
                "options": [
                    {"text": "Django and Flask", "is_correct": False},
                    {"text": "Starlette and Pydantic", "is_correct": True},
                    {"text": "Pandas and Numpy", "is_correct": False}
                ]
            }
        ]
    }
    await db.quizzes.insert_one(sample_quiz)

    print("Successfully seeded MongoDB with users and courses for global subjects.")

if __name__ == "__main__":
    asyncio.run(seed())
