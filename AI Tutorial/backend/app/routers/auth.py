from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.auth import verify_password, create_access_token, get_password_hash, get_current_user
from app.core.database import get_db, User as DBUser
from app.models.schemas import Role
from datetime import timedelta, datetime
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    mobile: str = "0000000000"
    role: str = "student"

class EligibilityTestSubmission(BaseModel):
    score: int
    total: int
    answers: dict

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: SignupRequest, db: AsyncSession = Depends(get_db)):
    try:
        # Check if user exists
        result = await db.execute(select(DBUser).where(DBUser.email == user_data.email))
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        new_user = DBUser(
            email=user_data.email,
            full_name=user_data.name,
            password_hash=get_password_hash(user_data.password),
            role=user_data.role or "student",
            mobile=user_data.mobile,
            is_active=True,
            eligibility_test_passed=False,
            eligibility_test_score=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return {
            "message": "User created successfully",
            "user_id": str(new_user.id),
            "email": new_user.email,
            "role": new_user.role,
            "eligibility_test_required": True
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print(f"Signup error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    try:
        # Find user by email
        result = await db.execute(select(DBUser).where(DBUser.email == form_data.username))
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role}, 
            expires_delta=access_token_expires
        )
        
        return {
            "access_token": access_token, 
            "token_type": "bearer",
            "user": {
                "email": user.email,
                "name": user.full_name,
                "role": user.role,
                "eligibility_test_passed": user.eligibility_test_passed,
                "eligibility_test_score": user.eligibility_test_score
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.post("/eligibility-test/submit")
async def submit_eligibility_test(
    submission: EligibilityTestSubmission,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit eligibility test results. Minimum 60% required to pass."""
    try:
        user_email = current_user["email"]
        
        # Find user
        result = await db.execute(select(DBUser).where(DBUser.email == user_email))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Calculate percentage
        percentage = (submission.score / submission.total) * 100 if submission.total > 0 else 0
        passed = percentage >= 60
        
        # Update user record
        user.eligibility_test_score = int(percentage)
        user.eligibility_test_passed = passed
        user.eligibility_test_taken_at = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        
        await db.commit()
        
        return {
            "passed": passed,
            "score": submission.score,
            "total": submission.total,
            "percentage": int(percentage),
            "message": "Congratulations! You passed the eligibility test." if passed else "You need at least 60% to pass. Please try again."
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        print(f"Eligibility test submission error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to submit test")

@router.get("/eligibility-test/status")
async def get_eligibility_status(
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's eligibility test status"""
    try:
        user_email = current_user["email"]
        
        result = await db.execute(select(DBUser).where(DBUser.email == user_email))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {
            "eligibility_test_passed": user.eligibility_test_passed,
            "eligibility_test_score": user.eligibility_test_score,
            "eligibility_test_taken_at": user.eligibility_test_taken_at,
            "can_access_tutorials": user.eligibility_test_passed
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Get eligibility status error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get status")
