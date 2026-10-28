# AI Tutorial LMS - Complete Setup & Running Guide

## 📋 Project Overview

Enterprise-grade Learning Management System powered by AI with:
- **Backend:** FastAPI + SQLite
- **Frontend:** React + Vite + TypeScript + Tailwind CSS
- **AI Integration:** Groq, Gemini, Hugging Face
- **Video Integration:** YouTube API
- **Real-time Features:** WebSocket support

---

## 🚀 Quick Start (First Time Setup)

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

### 1. Clone & Navigate
```bash
cd "path/to/AI Tutorial"
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Configure Environment Variables
The `.env` file is already configured with API keys. Verify it contains:
```env
# Database
DATABASE_PATH=ai_tutorial.db

# AI APIs
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
HUGGINGFACE_API_KEY=your_hf_key
YOUTUBE_API_KEY=your_youtube_key

# Security
SECRET_KEY=ai-tutorial-secret-key-change-in-production
```

#### Initialize Database (Optional - Auto-created on first run)
```bash
python -m app.core.database
```

### 3. Frontend Setup

```bash
cd ../lms_frontend
npm install
```

---

## ▶️ Running the Application

### Option 1: Run Both Services Separately (Recommended for Development)

#### Terminal 1 - Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at:
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

#### Terminal 2 - Start Frontend
```bash
cd lms_frontend
npm run dev
```

Frontend will be available at:
- **App:** http://localhost:5173

### Option 2: Production Build

#### Build Frontend
```bash
cd lms_frontend
npm run build
```

#### Run Backend (serves built frontend)
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🎯 Application URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:5173 | Main application (dev mode) |
| Backend API | http://localhost:8000 | REST API endpoints |
| API Documentation | http://localhost:8000/docs | Interactive Swagger UI |
| API Redoc | http://localhost:8000/redoc | Alternative API docs |
| Health Check | http://localhost:8000/health | Service status |

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/signup` | Register new user |
| POST | `/api/v1/auth/login` | User login (returns JWT) |
| GET | `/api/v1/auth/me` | Get current user info |

### Courses
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/courses/` | List all courses |
| GET | `/api/v1/courses/{course_id}` | Get course details |
| POST | `/api/v1/courses/` | Create new course (admin) |
| PUT | `/api/v1/courses/{course_id}` | Update course |
| DELETE | `/api/v1/courses/{course_id}` | Delete course |

### Enrollment
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/enroll/{course_id}` | Enroll in course |
| GET | `/api/v1/enroll/my-courses` | Get enrolled courses |
| GET | `/api/v1/enroll/{course_id}/progress` | Get course progress |

### Progress Tracking
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/progress/` | Update lesson progress |
| GET | `/api/v1/progress/{course_id}` | Get course progress |

### Quizzes
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/quizzes/{course_id}` | Get course quizzes |
| POST | `/api/v1/quizzes/submit` | Submit quiz attempt |
| GET | `/api/v1/quizzes/results/{attempt_id}` | Get quiz results |

### AI Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/ai/generate` | Generate AI course content |
| POST | `/api/v1/ai/chat` | AI tutor chat |
| POST | `/api/v1/ai/explain` | Get AI explanation |

### LMS Features
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/lms/performance` | Get performance analytics |
| GET | `/api/v1/lms/saved-courses` | Get saved courses |
| POST | `/api/v1/lms/save-course` | Save course for later |

---

## 🛠️ Development Commands

### Backend Commands

```bash
# Run with auto-reload (development)
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run without reload (production-like)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run on different port
python -m uvicorn app.main:app --reload --port 8080

# Test database connection
python test_db_connection.py

# Test video service
python test_video_service.py

# Seed database with sample data
python scripts/seed_lms_v2.py
```

### Frontend Commands

```bash
cd lms_frontend

# Development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint

# Install dependencies
npm install

# Update dependencies
npm update
```

---

## 🗄️ Database Management

### SQLite Database
- **Location:** `backend/ai_tutorial.db`
- **Auto-created:** Yes (on first backend startup)
- **Tables:** users, courses, enrollments, progress_records, quizzes, quiz_attempts, performance_records, lms_saved_courses

### View Database
```bash
# Using SQLite CLI
sqlite3 backend/ai_tutorial.db

# Common queries
.tables                          # List all tables
.schema users                    # Show table schema
SELECT * FROM users;             # View all users
SELECT * FROM courses;           # View all courses
```

### Reset Database
```bash
# Delete database file
rm backend/ai_tutorial.db

# Restart backend (will recreate)
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Seed Sample Data
```bash
cd backend
python scripts/seed_lms_v2.py
```

---

## 🔑 Environment Variables

### Required Variables
```env
# Database
DATABASE_PATH=ai_tutorial.db

# Security (Change in production!)
SECRET_KEY=your-secret-key-here

# AI Services
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key

# Video Service
YOUTUBE_API_KEY=your_youtube_api_key
```

### Optional Variables
```env
# Flask (if using legacy app)
FLASK_DEBUG=True
FLASK_PORT=5000

# ChromaDB (if using vector database)
CHROMA_PERSIST_DIR=./vector_db/indexes
ANONYMIZED_TELEMETRY=False
```

---

## 🧪 Testing

### Test Backend
```bash
cd backend

# Test database connection
python test_db_connection.py

# Test video service
python test_video_service.py

# Test API endpoints (requires running server)
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

### Test Frontend
```bash
cd lms_frontend

# Run linter
npm run lint

# Build test
npm run build
```

---

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

**Database locked:**
```bash
# Close all connections and restart backend
rm backend/ai_tutorial.db
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Module not found:**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

### Frontend Issues

**Port 5173 in use:**
```bash
# Edit vite.config.ts to change port
# Or kill process using port 5173
```

**Dependencies error:**
```bash
cd lms_frontend
rm -rf node_modules package-lock.json
npm install
```

**Build errors:**
```bash
npm run lint
npm run build
```

---

## 📦 Project Structure

```
AI Tutorial/
├── backend/
│   ├── app/
│   │   ├── core/          # Config, auth, database
│   │   ├── models/        # Pydantic schemas
│   │   ├── routers/       # API endpoints
│   │   ├── services/      # Business logic
│   │   └── main.py        # FastAPI app
│   ├── scripts/           # Utility scripts
│   ├── requirements.txt   # Python dependencies
│   └── ai_tutorial.db     # SQLite database
├── lms_frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API clients
│   │   └── App.tsx        # Main app
│   ├── package.json       # Node dependencies
│   └── vite.config.ts     # Vite configuration
├── books/                 # PDF textbooks
├── .env                   # Environment variables
└── README.md             # This file
```

---

## 🚀 Deployment

### Backend Deployment
```bash
# Install production dependencies
pip install -r backend/requirements.txt

# Run with production server
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend Deployment
```bash
# Build production bundle
cd lms_frontend
npm run build

# Output in: lms_frontend/dist/
# Deploy to: Vercel, Netlify, or serve with nginx
```

---

## 🔐 Security Notes

1. **Change SECRET_KEY** in production
2. **Use HTTPS** for production deployment
3. **Restrict CORS** origins in `backend/app/main.py`
4. **Secure API keys** - never commit to git
5. **Use environment variables** for sensitive data

---

## 📚 Additional Documentation

- `QUICK_START_GUIDE.md` - Detailed quick start guide
- `SQLITE_MIGRATION_COMPLETE.md` - Database migration details
- `AI_Tutorial_LMS_Report.docx` - Comprehensive technical documentation
- `CHATBOT_FEATURE.md` - Chatbot integration guide
- `GROQ_AI_CHATBOT_INTEGRATION.md` - Groq AI setup

---

## 🎓 Features

### For Students
- ✅ Self-registration and authentication
- ✅ Browse and enroll in courses
- ✅ Track learning progress
- ✅ Take quizzes and tests
- ✅ View performance analytics
- ✅ AI-powered tutoring
- ✅ Video lessons integration
- ✅ Save courses for later

### For Administrators
- ✅ Course management
- ✅ User management
- ✅ Analytics dashboard
- ✅ Content generation with AI
- ✅ Quiz creation and management

### AI Capabilities
- ✅ Course content generation
- ✅ Intelligent tutoring
- ✅ Concept explanations
- ✅ Code generation support
- ✅ Career guidance

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at http://localhost:8000/docs
3. Check additional documentation files
4. Review backend logs for error messages

---

## 📄 License

This project is for educational purposes.

---

**Happy Learning! 🎉**
