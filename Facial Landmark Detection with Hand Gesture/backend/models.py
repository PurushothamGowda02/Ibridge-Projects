from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from database import Base

class Snapshot(Base):
    __tablename__ = "snapshots"

    id = Column(Integer, primary_key=True, index=True)
    image_data = Column(Text)  # Base64 encoded image
    gesture_detected = Column(String)
    emotion_detected = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    landmarks_count = Column(Integer)
