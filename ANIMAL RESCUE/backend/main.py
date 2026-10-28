from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import timedelta
import uvicorn
from typing import List, Optional
import os
from pathlib import Path

import models, schemas, database, auth
from database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(title="Animal Rescue API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# --- AUTH ENDPOINTS ---

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_password = auth.get_password_hash(user.password)
    # First user is admin for demo purposes
    role = "admin" if db.query(models.User).count() == 0 else "user"
    
    new_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# --- ANIMAL ENDPOINTS ---

@app.get("/animals", response_model=List[schemas.Animal])
def get_animals(species: str = None, db: Session = Depends(get_db)):
    query = db.query(models.Animal)
    if species:
        query = query.filter(models.Animal.species == species)
    return query.all()

@app.get("/animals/{animal_id}", response_model=schemas.Animal)
def get_animal(animal_id: int, db: Session = Depends(get_db)):
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    return animal

@app.post("/animals", response_model=schemas.Animal)
def create_animal(animal: schemas.AnimalCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    db_animal = models.Animal(**animal.model_dump())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

@app.delete("/animals/{animal_id}")
def delete_animal(animal_id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    animal = db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    db.delete(animal)
    db.commit()
    return {"message": "Animal deleted successfully"}

# --- ADOPTION ENDPOINTS ---

@app.post("/adoptions", response_model=schemas.AdoptionRequest)
def create_adoption_request(request: schemas.AdoptionRequestCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Check if animal exists
    animal = db.query(models.Animal).filter(models.Animal.id == request.animal_id).first()
    if not animal:
        raise HTTPException(status_code=404, detail="Animal not found")
    
    db_request = models.AdoptionRequest(
        user_id=current_user.id,
        animal_id=request.animal_id,
        message=request.message
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request

@app.get("/adoptions/me", response_model=List[schemas.AdoptionRequest])
def get_my_adoptions(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.AdoptionRequest).filter(models.AdoptionRequest.user_id == current_user.id).all()

@app.get("/adoptions", response_model=List[schemas.AdoptionRequest])
def get_all_adoptions(db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    return db.query(models.AdoptionRequest).all()

# --- RESCUE REPORT ENDPOINTS ---

@app.post("/reports", response_model=schemas.RescueReport)
async def create_rescue_report(
    animal_name: str = Form(None),
    description: str = Form(...),
    location: str = Form(...),
    contact_info: str = Form(...),
    images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    image_url = None
    
    # Handle image upload
    if images and len(images) > 0:
        image = images[0]  # Use first image
        if image.filename:
            # Save image
            file_path = UPLOAD_DIR / image.filename
            with open(file_path, "wb") as f:
                content = await image.read()
                f.write(content)
            image_url = f"http://localhost:8000/uploads/{image.filename}"
    
    # Create rescue report
    db_report = models.RescueReport(
        user_id=current_user.id,
        description=description,
        location=location,
        contact_info=contact_info,
        image_url=image_url,
        status="reported"
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    
    # Create an Animal entry from the report so it shows in Adopt page
    # Use provided animal_name or generate one from location
    animal_name_to_use = animal_name if animal_name and animal_name.strip() else f"Stray - {location}"
    
    db_animal = models.Animal(
        name=animal_name_to_use,
        species="Unknown",
        breed="Mixed",
        age="Unknown",
        gender="Unknown",
        description=description,
        image_url=image_url,
        status="available"
    )
    db.add(db_animal)
    db.commit()
    
    return db_report

@app.get("/reports", response_model=List[schemas.RescueReport])
def get_reports(db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    return db.query(models.RescueReport).all()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
