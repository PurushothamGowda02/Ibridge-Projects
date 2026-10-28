from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import models, database
from pydantic import BaseModel
from datetime import datetime

# Initialize Database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Facial Landmark Detection API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class SnapshotCreate(BaseModel):
    image_data: str
    gesture_detected: str
    emotion_detected: str
    landmarks_count: int

class SnapshotResponse(SnapshotCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

@app.post("/snapshots/", response_model=SnapshotResponse)
def create_snapshot(snapshot: SnapshotCreate, db: Session = Depends(database.get_db)):
    db_snapshot = models.Snapshot(**snapshot.model_dump())
    db.add(db_snapshot)
    db.commit()
    db.refresh(db_snapshot)
    return db_snapshot

@app.get("/snapshots/", response_model=List[SnapshotResponse])
def get_snapshots(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return db.query(models.Snapshot).order_by(models.Snapshot.timestamp.desc()).offset(skip).limit(limit).all()

@app.delete("/snapshots/{snapshot_id}")
def delete_snapshot(snapshot_id: int, db: Session = Depends(database.get_db)):
    db_snapshot = db.query(models.Snapshot).filter(models.Snapshot.id == snapshot_id).first()
    if not db_snapshot:
        raise HTTPException(status_code=404, detail="Snapshot not found")
    db.delete(db_snapshot)
    db.commit()
    return {"message": "Snapshot deleted"}

@app.get("/stats/")
def get_stats(db: Session = Depends(database.get_db)):
    total_snapshots = db.query(models.Snapshot).count()
    gestures = db.query(models.Snapshot.gesture_detected).distinct().all()
    return {
        "total_snapshots": total_snapshots,
        "unique_gestures": [g[0] for g in gestures]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
