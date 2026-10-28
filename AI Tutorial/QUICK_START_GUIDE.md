# 🚀 Quick Start Guide - AI Tutorial LMS

## ✅ Project is Ready!

Your AI Tutorial LMS is now running with **SQLite** database (no Docker/MongoDB needed!)

---

## 🎯 Current Status

### Running Services:
- ✅ **Frontend:** http://localhost:5173 (React + Vite)
- ✅ **Backend:** http://localhost:8000 (FastAPI + SQLite)
- ✅ **Database:** SQLite file at `backend/ai_tutorial.db`

### What's Working:
- ✅ User registration (tested successfully!)
- ✅ SQLite database auto-created
- ✅ All API endpoints converted from MongoDB to SQLite
- ✅ No external dependencies required

---

## 📝 How to Use

### 1. Register a New Student

**Option A: Use the Frontend**
1. Open http://localhost:5173 in your browser
2. You'll see the registration page (landing page)
3. Fill in:
   - Full Name
   - Email
   - Password
   - Mobile Number
4. Click "Create Student Account"
5. You'll be redirected to login page after 3 seconds

**Option B: Use API Directly**
```bash
POST http://localhost:8000/api/v1/auth/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepass123",
  "mobile": "9876543210",
  "role": "student"
}
```

### 2. Login

**Frontend:**
1. Go to http://localhost:5173/login
2. Enter your email and password
3. Click "Sign In"
4. You'll be redirected to the student dashboard

**API:**
```bash
POST http://localhost:8000/api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=john@example.com&password=securepass123
```

### 3. Explore Features

After logging in, you can:
- Browse courses
- Enroll in courses
- Track progress
- Take quizzes
- Generate AI-powered courses
- View performance analytics

---

## 🔧 Managing the Project

### Stop All Services
```bash
# Stop frontend (Ctrl+C in frontend terminal)
# Stop backend (Ctrl+C in backend terminal)
```

### Restart Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Restart Frontend
```bash
cd lms_frontend
npm run dev
```

### Reset Database
If you want to start fresh:
```bash
# Delete the database file
rm backend/ai_tutorial.db

# Restart backend (will recreate empty database)
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 📊 Database Management

### View Database
You can use any SQLite browser to view the database:
- **DB Browser for SQLite** (https://sqlitebrowser.org/)
- **SQLite Viewer** (VS Code extension)
- **Command line:** `sqlite3 backend/ai_tutorial.db`

### Database Tables:
- `users` - User accounts
- `courses` - Course catalog
- `enrollments` - Student enrollments
- `progress_records` - Lesson completion
- `quizzes` - Quiz questions
- `quiz_attempts` - Quiz submissions
- `performance_records` - Test scores
- `lms_saved_courses` - Saved courses

---

## 🐛 Troubleshooting

### Registration Not Working?
1. Check backend is running: http://localhost:8000/health
2. Check browser console for errors (F12)
3. Verify database file exists: `backend/ai_tutorial.db`
4. Check backend logs for error messages

### Frontend Not Loading?
1. Verify frontend is running on port 5173
2. Check for port conflicts
3. Clear browser cache
4. Restart frontend: `npm run dev`

### Backend Errors?
1. Check Python version (3.8+)
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check database file permissions
4. View logs in backend terminal

---

## 📚 API Documentation

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI)

### Key Endpoints:
- `POST /api/v1/auth/signup` - Register new user
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/courses/` - List courses
- `POST /api/v1/enroll/{course_id}` - Enroll in course
- `GET /api/v1/enroll/my-courses` - Get enrolled courses
- `POST /api/v1/ai/generate` - Generate AI course
- `GET /api/v1/lms/performance` - Get performance data

---

## 🎓 Student Registration Flow

```
1. User visits http://localhost:5173
   ↓
2. Sees registration page (landing page)
   ↓
3. Fills registration form
   ↓
4. Submits form → POST /api/v1/auth/signup
   ↓
5. Backend creates user in SQLite database
   ↓
6. Success message shown
   ↓
7. Auto-redirect to login page after 3 seconds
   ↓
8. User logs in → POST /api/v1/auth/login
   ↓
9. Receives JWT token
   ↓
10. Redirected to student dashboard
```

---

## ✨ Key Features

### For Students:
- ✅ Self-registration
- ✅ Browse course catalog
- ✅ Enroll in courses
- ✅ Track learning progress
- ✅ Take quizzes and tests
- ✅ View performance analytics
- ✅ AI-generated personalized courses

### For System:
- ✅ JWT authentication
- ✅ Role-based access (student only for now)
- ✅ SQLite database (no external services)
- ✅ Async operations
- ✅ Auto-reload on code changes
- ✅ CORS enabled for frontend

---

## 🎉 Success!

Your AI Tutorial LMS is fully operational with:
- ✅ No Docker required
- ✅ No MongoDB installation
- ✅ Simple SQLite database
- ✅ Registration working
- ✅ Ready for students!

**Just open http://localhost:5173 and start registering students!**

---

## 📞 Need Help?

Check these files for more information:
- `SQLITE_MIGRATION_COMPLETE.md` - Details about the database migration
- `README.md` - Project overview
- `AI_Tutorial_LMS_Report.docx` - Comprehensive technical documentation

**Happy Learning! 🚀**
