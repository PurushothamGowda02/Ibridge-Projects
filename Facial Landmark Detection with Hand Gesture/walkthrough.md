# Project Walkthrough - VisionAI

VisionAI is a premium, real-time computer vision application that detects 468 facial landmarks and recognizes hand gestures to control the interface.

## Key Features
- **Face Mesh Visualization**: Real-time overlay of facial landmarks using MediaPipe.
- **Gesture Recognition**: 
  - `Thumb_Up`: Triggers an automatic snapshot saved to the database.
  - `Victory` (Peace Sign): Toggles the landmark mesh visibility.
- **Snapshots Gallery**: View and manage all captured detections with metadata.
- **High-End UI**: Responsive glassmorphic design built with React.

## How to Run the Project

### 1. Start the Backend
Open a terminal in the `backend` folder and run:
```bash
pip install -r requirements.txt
python main.py
```
The server will run at `http://localhost:8000`.

### 2. Start the Frontend
Open a new terminal in the `frontend` folder and run:
```bash
npm install
npm run dev
```
Open the provided URL (usually `http://localhost:5173`) in your browser.

## Technical Implementation
- **MediaPipe Tasks Vision**: Used for ultra-low latency detection in the browser.
- **FastAPI**: Provides a lightweight and fast backend for data persistence.
- **SQLite**: Local database for storing snapshot metadata and base64 image data.
- **Canvas API**: Used for drawing high-performance overlays on the webcam feed.

---
*Created for BCA Final Year Project*
