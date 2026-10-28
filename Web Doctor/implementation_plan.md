# Implementation Plan - Web Doctor

Web Doctor is a premium, end-to-end healthcare platform designed as a BCA final year project. It enables patients to check symptoms using AI, book appointments with doctors, and manage their health records, while providing doctors with a streamlined dashboard to manage consultations.

## User Review Required

> [!IMPORTANT]
> The application will use **FastAPI** for the backend and **React (Vite)** for the frontend. Please confirm if you have any specific database preferences (SQLite is planned for ease of setup).

> [!TIP]
> I will implement a "Smart Symptom Checker" that uses a simulated AI model to suggest specialists based on user input.

## Proposed Architecture

### 1. Backend (FastAPI)
- **Auth**: JWT-based authentication with role-based access control (RBAC).
- **Database**: SQLAlchemy with SQLite for persistence.
- **Endpoints**:
  - `/auth`: Register/Login for Patients and Doctors.
  - `/doctors`: List doctors, search by specialty.
  - `/appointments`: Book, cancel, and view appointments.
  - `/ai/analyze`: Symptom analysis engine.

### 2. Frontend (React + Vite)
- **Design System**: Vanilla CSS with modern aesthetics (glassmorphism, CSS variables, smooth transitions).
- **State Management**: React Context API.
- **Pages**:
  - `Home`: Marketing landing page.
  - `Login/Register`: Unified auth portal.
  - `Patient Dashboard`: Symptom checker, appointment history, doctor search.
  - `Doctor Dashboard`: Patient list, upcoming consultations.

---

## Proposed Changes

### [NEW] Backend Structure
#### `backend/main.py`
Entry point for FastAPI.
#### `backend/models.py`
SQLAlchemy models (User, Doctor, Appointment).
#### `backend/schemas.py`
Pydantic schemas for data validation.
#### `backend/database.py`
Database connection and session management.

### [NEW] Frontend Structure
#### `frontend/src/App.jsx`
Main routing and layout logic.
#### `frontend/src/index.css`
Core design system with CSS variables for colors, spacing, and animations.
#### `frontend/src/components/`
Reusable UI components (Navbar, DoctorCard, SymptomChecker, Modal).
#### `frontend/src/pages/`
PatientDashboard, DoctorDashboard, LandingPage.

---

## Verification Plan

### Automated Tests
- Run `pytest` for backend endpoint validation.
- Browser-based verification for the booking flow and AI analysis.

### Manual Verification
1. Register as a Patient.
2. Use the Symptom Checker to find a specialist.
3. Book an appointment with a Doctor.
4. Log in as a Doctor and verify the appointment appears in the dashboard.
