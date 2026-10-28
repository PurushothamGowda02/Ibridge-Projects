from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import database
import models
import schemas
from medical_triage import MEDICAL_TRIAGE_DATASET
from nlp_pipeline import HybridClinicalNLPPipeline


SECRET_KEY = "webdoctor_secret_key_change_me_in_production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
app = FastAPI(title="Web Doctor API")
triage_pipeline = HybridClinicalNLPPipeline()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme_optional),
    db: Session = Depends(database.get_db),
):
    if not token:
        return None

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
    except JWTError:
        return None

    return db.query(models.User).filter(models.User.email == email).first()


@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = models.User(
        email=user.email,
        full_name=user.full_name,
        phone_number=user.phone_number,
        hashed_password=get_password_hash(user.password),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.get("/doctors", response_model=List[schemas.Doctor])
def get_doctors(db: Session = Depends(database.get_db)):
    return db.query(models.Doctor).all()


@app.get("/hospitals", response_model=List[schemas.Hospital])
def get_hospitals(db: Session = Depends(database.get_db)):
    return db.query(models.Hospital).all()


@app.post("/appointments", response_model=schemas.Appointment)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Create appointment
    db_appointment = models.Appointment(**appointment.dict(), patient_id=current_user.id, status="scheduled")
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    # Get doctor info
    doctor = db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id).first()
    if doctor:
        # Create notification for doctor
        notification = models.Notification(
            user_id=doctor.user_id,
            title="New Appointment Booked",
            message=f"New appointment from {current_user.full_name} on {appointment.appointment_date.strftime('%B %d, %Y at %I:%M %p')}. Symptoms: {appointment.symptoms}",
            type="appointment",
            related_appointment_id=db_appointment.id
        )
        db.add(notification)
        
        # Create notification for patient
        patient_notification = models.Notification(
            user_id=current_user.id,
            title="Appointment Confirmed",
            message=f"Your appointment with Dr. {doctor.user.full_name} has been confirmed for {appointment.appointment_date.strftime('%B %d, %Y at %I:%M %p')}",
            type="appointment",
            related_appointment_id=db_appointment.id
        )
        db.add(patient_notification)
        db.commit()

    return db_appointment


@app.get("/appointments", response_model=List[schemas.Appointment])
def get_user_appointments(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role == "doctor":
        doctor = db.query(models.Doctor).filter(models.Doctor.user_id == current_user.id).first()
        if doctor is None:
            return []
        return db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor.id).all()

    return db.query(models.Appointment).filter(models.Appointment.patient_id == current_user.id).all()


@app.get("/hospitals/{hospital_id}/appointments", response_model=List[schemas.Appointment])
def get_hospital_appointments(hospital_id: int, db: Session = Depends(database.get_db)):
    """Get all appointments for a specific hospital"""
    doctors = db.query(models.Doctor).filter(models.Doctor.hospital_id == hospital_id).all()
    doctor_ids = [doctor.id for doctor in doctors]
    
    appointments = db.query(models.Appointment).filter(
        models.Appointment.doctor_id.in_(doctor_ids)
    ).order_by(models.Appointment.appointment_date.desc()).all()
    
    return appointments


@app.get("/notifications", response_model=List[schemas.Notification])
def get_notifications(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """Get all notifications for current user"""
    return db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id
    ).order_by(models.Notification.created_at.desc()).limit(50).all()


@app.get("/notifications/unread/count")
def get_unread_count(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """Get count of unread notifications"""
    count = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id,
        models.Notification.is_read == 0
    ).count()
    return {"count": count}


@app.put("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    """Mark a notification as read"""
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = 1
    db.commit()
    return {"message": "Notification marked as read"}


@app.post("/ai/analyze", response_model=schemas.SymptomAnalysis)
def analyze_symptoms(
    payload: schemas.SymptomInput,
    db: Session = Depends(database.get_db),
    current_user: Optional[models.User] = Depends(get_current_user_optional),
):
    analysis = triage_pipeline.analyze(payload.symptoms, payload.language)

    audit = models.AnalysisAudit(
        patient_id=current_user.id if current_user else None,
        raw_symptoms=payload.symptoms,
        normalized_symptoms=analysis["normalized_symptoms"],
        input_language=analysis["input_language"],
        predicted_condition=analysis["condition"],
        predicted_specialist=analysis["specialist"],
        predicted_severity=analysis["severity"],
        model_source=analysis["model_source"],
        confidence=analysis.get("confidence"),
        review_status="pending",
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)

    analysis["audit_id"] = audit.id
    return analysis


@app.get("/ai/model-info", response_model=schemas.ModelInfo)
def model_info():
    return triage_pipeline.model_info()


@app.get("/ai/audits/me", response_model=List[schemas.AnalysisAuditOut])
def my_audits(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "patient":
        raise HTTPException(status_code=403, detail="Only patients can access personal audit history")

    return (
        db.query(models.AnalysisAudit)
        .filter(models.AnalysisAudit.patient_id == current_user.id)
        .order_by(models.AnalysisAudit.created_at.desc())
        .limit(50)
        .all()
    )


@app.get("/ai/reviews/pending", response_model=List[schemas.AnalysisAuditOut])
def pending_reviews(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can review analyses")

    return (
        db.query(models.AnalysisAudit)
        .filter(models.AnalysisAudit.review_status == "pending")
        .order_by(models.AnalysisAudit.created_at.desc())
        .limit(100)
        .all()
    )


@app.post("/ai/reviews/{analysis_id}", response_model=schemas.ClinicianReviewOut)
def submit_review(
    analysis_id: int,
    payload: schemas.ClinicianReviewCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can submit reviews")

    audit = db.query(models.AnalysisAudit).filter(models.AnalysisAudit.id == analysis_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Analysis record not found")

    review = models.ClinicianReview(
        analysis_id=analysis_id,
        reviewer_user_id=current_user.id,
        verdict=payload.verdict,
        corrected_condition=payload.corrected_condition,
        corrected_severity=payload.corrected_severity,
        notes=payload.notes,
    )
    db.add(review)
    audit.review_status = "reviewed"
    db.commit()
    db.refresh(review)
    return review


@app.on_event("startup")
def seed_data():
    db = database.SessionLocal()

    # Seed hospitals with Indian addresses
    if db.query(models.Hospital).count() == 0:
        hospitals = [
            models.Hospital(
                name="Apollo Multispecialty Hospital",
                address="154, Bannerghatta Road, Opposite IIM",
                city="Bangalore",
                phone="+91-80-2692-2222",
                email="info@apollobangalore.com",
                description="Leading multi-specialty hospital with 24/7 emergency services, advanced ICU, and state-of-the-art diagnostic facilities."
            ),
            models.Hospital(
                name="Fortis Healthcare Center",
                address="Sector 62, Phase VIII, Mohali",
                city="Chandigarh",
                phone="+91-172-4621-000",
                email="contact@fortismohali.com",
                description="Comprehensive healthcare center with expertise in cardiology, orthopedics, and preventive care programs."
            ),
            models.Hospital(
                name="Max Super Specialty Hospital",
                address="1, Press Enclave Road, Saket",
                city="New Delhi",
                phone="+91-11-2651-5050",
                email="info@maxhealthcare.com",
                description="Premier hospital offering specialized care in neurology, oncology, cardiology, and advanced surgical procedures."
            ),
            models.Hospital(
                name="Manipal Hospital",
                address="98, HAL Airport Road, Old Airport Road",
                city="Bangalore",
                phone="+91-80-2502-4444",
                email="contact@manipalhospitals.com",
                description="Trusted healthcare provider with centers of excellence in gastroenterology, nephrology, and emergency medicine."
            ),
        ]
        for hospital in hospitals:
            db.add(hospital)
        db.commit()

    # Seed doctors - 2-3 specialists per hospital
    if db.query(models.Doctor).count() == 0:
        apollo = db.query(models.Hospital).filter(models.Hospital.name == "Apollo Multispecialty Hospital").first()
        fortis = db.query(models.Hospital).filter(models.Hospital.name == "Fortis Healthcare Center").first()
        max_hospital = db.query(models.Hospital).filter(models.Hospital.name == "Max Super Specialty Hospital").first()
        manipal = db.query(models.Hospital).filter(models.Hospital.name == "Manipal Hospital").first()

        # Apollo Hospital Doctors
        doctor1_user = models.User(
            email="dr.sharma@apollo.com",
            full_name="Dr. Rajesh Sharma",
            phone_number="+91-98765-43210",
            hashed_password=get_password_hash("doctor123"),
            role="doctor",
        )
        db.add(doctor1_user)
        db.commit()
        db.refresh(doctor1_user)
        
        db.add(models.Doctor(
            user_id=doctor1_user.id,
            hospital_id=apollo.id,
            specialty="Cardiology",
            bio="Senior cardiologist with 15 years of experience in interventional cardiology and heart disease management.",
            experience=15,
            rating=5,
        ))

        doctor2_user = models.User(
            email="dr.priya@apollo.com",
            full_name="Dr. Priya Menon",
            phone_number="+91-98765-43211",
            hashed_password=get_password_hash("doctor123"),
            role="doctor",
        )
        db.add(doctor2_user)
        db.commit()
        db.refresh(doctor2_user)
        
        db.add(models.Doctor(
            user_id=doctor2_user.id,
            hospital_id=apollo.id,
            specialty="Pediatrics",
            bio="Child specialist focusing on newborn care, vaccinations, and pediatric infectious diseases.",
            experience=10,
            rating=5,
        ))

        doctor3_user = models.User(
            email="dr.kumar@apollo.com",
            full_name="Dr. Anil Kumar",
            phone_number="+91-98765-43212",
            hashed_password=get_password_hash("doctor123"),
            role="doctor",
        )
        db.add(doctor3_user)
        db.commit()
        db.refresh(doctor3_user)
        
        db.add(models.Doctor(
            user_id=doctor3_user.id,
            hospital_id=apollo.id,
            specialty="Orthopedics",
            bio="Orthopedic surgeon specializing in joint replacement, sports injuries, and spine surgery.",
            experience=12,
            rating=4,
        ))

        # Fortis Hospital Doctors
        doctor4_user = models.User(
            email="dr.singh@fortis.com",
            full_name="Dr. Harpreet Singh",
            phone_number="+91-98765-43213",
            hashed_password=get_password_hash("doctor123"),
            role="doctor",
        )
        db.add(doctor4_user)
        db.commit()
        db.refresh(doctor4_user)
        
        db.add(models.Doctor(
            user_id=doctor4_user.id,
            hospital_id=fortis.id,
            specialty="General Medicine",
            bio="General physician with expertise in diabetes management, hypertension, and preventive healthcare.",
            experience=14,
            rating=5,
        ))

        doctor5_user = models.User(
            email="dr.reddy@fortis.com",
            full_name="Dr. Lakshmi Reddy",
            phone_number="+91-98765-43214",
            hashed_password=get_password_hash("doctor123"),
            role="doctor",
        )
        db.add(doctor5_user)
        db.commit()
        db.refresh(doctor5_user)
        
        db.add(models.Doctor(
            user_id=doctor5_user.id,
            hospital_id=fortis.id,
            specialty="Dermatology",
            bio="Skin specialist for acne, eczema, psoriasis, hair loss treatment, and cosmetic dermatology.",
            experience=9,
            rating=4,
        ))

        doctor6_user = models.User(
            email="dr.patel@fortis.com",
            full_name="Dr. Amit Patel",
            phone_number="+91-98765-43215",
            hashed_password=get_password_hash("doctor123"),
            role="doctor",
        )
        db.add(doctor6_user)
        db.commit()
        db.refresh(doctor6_user)
        
        db.add(models.Doctor(
            user_id=doctor6_user.id,
            hospital_id=fortis.id,
            specialty="ENT (Ear, Nose, Throat)",
            bio="ENT specialist treating sinusitis, hearing problems, tonsillitis, and voice disorders.",
            experience=11,
            rating=5,
        ))

        # Max Hospital Doctors
        doctor7_user = models.User(
            email="dr.gupta@maxhealthcare.com",
            full_name="Dr. Neha Gupta",
            phone_number="+91-98765-43216",
            hashed_password=get_password_hash("doctor123"),
            role="doctor",
        )
        db.add(doctor7_user)
        db.commit()
        db.refresh(doctor7_user)
        
        db.add(models.Doctor(
            user_id=doctor7_user.id,
            hospital_id=max_hospital.id,
            specialty="Neurology",
            bio="Neurologist specializing in stroke, epilepsy, Parkinson's disease, and migraine management.",
            experience=13,
            rating=5,
        ))

        doctor8_user = models.User(
            email="dr.verma@maxhealthcare.com",
            full_name="Dr. Vikram Verma",
            phone_number="+91-98765-43217",
            hashed_password=get_password_hash("doctor123"),
            role="doctor",
        )
        db.add(doctor8_user)
        db.commit()
        db.refresh(doctor8_user)
        
        db.add(models.Doctor(
            user_id=doctor8_user.id,
            hospital_id=max_hospital.id,
            specialty="Gastroenterology",
            bio="Gastroenterologist treating digestive disorders, liver diseases, and performing endoscopy procedures.",
            experience=16,
            rating=5,
        ))

        # Manipal Hospital Doctors
        doctor9_user = models.User(
            email="dr.iyer@manipal.com",
            full_name="Dr. Sunita Iyer",
            phone_number="+91-98765-43218",
            hashed_password=get_password_hash("doctor123"),
            role="doctor",
        )
        db.add(doctor9_user)
        db.commit()
        db.refresh(doctor9_user)
        
        db.add(models.Doctor(
            user_id=doctor9_user.id,
            hospital_id=manipal.id,
            specialty="Obstetrics & Gynecology",
            bio="Women's health specialist for pregnancy care, high-risk deliveries, and gynecological surgeries.",
            experience=12,
            rating=5,
        ))

        doctor10_user = models.User(
            email="dr.nair@manipal.com",
            full_name="Dr. Ramesh Nair",
            phone_number="+91-98765-43219",
            hashed_password=get_password_hash("doctor123"),
            role="doctor",
        )
        db.add(doctor10_user)
        db.commit()
        db.refresh(doctor10_user)
        
        db.add(models.Doctor(
            user_id=doctor10_user.id,
            hospital_id=manipal.id,
            specialty="Pulmonology",
            bio="Lung specialist treating asthma, COPD, tuberculosis, and respiratory infections.",
            experience=10,
            rating=4,
        ))

        doctor11_user = models.User(
            email="dr.desai@manipal.com",
            full_name="Dr. Kavita Desai",
            phone_number="+91-98765-43220",
            hashed_password=get_password_hash("doctor123"),
            role="doctor",
        )
        db.add(doctor11_user)
        db.commit()
        db.refresh(doctor11_user)
        
        db.add(models.Doctor(
            user_id=doctor11_user.id,
            hospital_id=manipal.id,
            specialty="Ophthalmology",
            bio="Eye specialist for cataract surgery, LASIK, glaucoma treatment, and diabetic retinopathy.",
            experience=14,
            rating=5,
        ))

        db.commit()

    db.close()
