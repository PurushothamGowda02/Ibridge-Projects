# Walkthrough - Web Doctor

Web Doctor is a full-stack healthcare platform designed as a BCA final year project. It provides a seamless experience for patients and doctors to interact, diagnose, and manage health records.

## Features Implemented

### 1. AI Symptom Checker
Patients can enter their symptoms in natural language. The system uses a rule-based AI logic (simulating an LLM) to:
- Identify potential conditions.
- Recommend the appropriate specialist.
- Suggest immediate next steps.

### 2. Appointment Management
- **Patient View**: Search for doctors by specialty, book appointments for the next day, and view history.
- **Doctor View**: A comprehensive dashboard showing upcoming consultations, patient details, and symptoms.

### 3. Premium UI/UX
- **Glassmorphism Design**: Modern, translucent UI elements with blurred backgrounds.
- **Responsive Layout**: Works seamlessly on mobile and desktop.
- **Interactive States**: Smooth hover effects, transitions, and loading states.

## Technical Stack
- **Frontend**: React 18, Vite, Lucide Icons, Vanilla CSS.
- **Backend**: FastAPI, SQLAlchemy (SQLite), JWT Authentication.
- **Security**: Password hashing with Bcrypt, protected routes via JWT.

## How to Run

### Backend
1. Navigate to `backend/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Start the server: `uvicorn main:app --reload`.

### Frontend
1. Navigate to `frontend/`.
2. Install dependencies: `npm install`.
3. Start the dev server: `npm run dev`.

---

## Screenshots & Flows

### Landing Page
The landing page greets users with a high-impact hero section and a clear value proposition.

![Web Doctor Landing Page Preview](C:/Users/ADMIN/.gemini/antigravity/brain/5d34d9e2-5756-4ff9-a5f9-950eac05328e/web_doctor_landing_preview_1777263006014.png)

### Symptom Analysis
The patient dashboard features a specialized section for symptom analysis, providing instant feedback.

### Doctor Dashboard
Doctors have a clean, focused view of their schedule, allowing them to prepare for consultations.
