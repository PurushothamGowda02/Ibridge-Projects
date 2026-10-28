from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.database import init_db, close_db
from app.routers import auth, courses, enrollment, progress, quizzes, ai_agent, lms

app = FastAPI(
    title="Enterprise AI LMS API",
    description="Scalable Learning Management System powered by AI",
    version="1.0.0"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await init_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_db()

# Register Routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(enrollment.router, prefix="/api/v1")
app.include_router(progress.router, prefix="/api/v1")
app.include_router(quizzes.router, prefix="/api/v1")
app.include_router(ai_agent.router, prefix="/api/v1")
app.include_router(lms.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to the Enterprise LMS API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "SQLite"}
