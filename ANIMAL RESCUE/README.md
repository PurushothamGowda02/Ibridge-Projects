# 🐾 Animal Rescue Platform

A full-stack web application for reporting stray animals, managing adoptions, and coordinating rescue efforts. Built with React, FastAPI, and SQLite.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Usage Guide](#usage-guide)

## ✨ Features

### For Regular Users
- 🏠 **Home** - Landing page with hero section
- 🐾 **Adopt** - Browse all animals and submit adoption requests
- 📝 **Report** - Report stray animals with:
  - Custom animal name
  - Description
  - Location
  - Contact information
  - Image upload
- 💝 **Donate** - Interactive donation system with animations
- 🔐 **Authentication** - User registration and login

### For Admins
- 👨‍💼 **Admin Dashboard** - Real-time management interface with:
  - Live statistics (Total Animals, Rescue Reports, Adoption Requests)
  - Auto-refresh every 2 seconds
  - Manual refresh button
  - Recent rescue reports
  - Adoption request tracking
  - Animal management with delete functionality
  - System status monitoring

### Key Features
- ✅ Custom animal names for reported strays
- ✅ Image upload for reports
- ✅ Real-time animal count updates
- ✅ Real-time adoption request tracking
- ✅ Auto-refresh dashboard
- ✅ Interactive donation system
- ✅ Full admin management panel
- ✅ User authentication with JWT

## 🛠 Tech Stack

### Frontend
- **React 19** - UI library
- **Vite** - Build tool
- **Axios** - HTTP client
- **Framer Motion** - Animations
- **React Router** - Routing
- **Lucide React** - Icons

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **SQLite** - Database
- **Pydantic** - Data validation
- **Python-Jose** - JWT authentication
- **Bcrypt** - Password hashing

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download](https://www.python.org/)
- **npm** (comes with Node.js)
- **pip** (comes with Python)

### Installing Node.js

#### Windows
1. Go to [nodejs.org](https://nodejs.org/)
2. Download the **LTS (Long Term Support)** version
3. Run the installer (.msi file)
4. Follow the installation wizard (accept all defaults)
5. Restart your computer
6. Verify installation:
   ```bash
   node --version
   npm --version
   ```

#### macOS
**Using Homebrew (Recommended):**
```bash
brew install node
```

**Or download from nodejs.org:**
1. Go to [nodejs.org](https://nodejs.org/)
2. Download the macOS installer
3. Run the installer and follow the wizard
4. Verify installation:
   ```bash
   node --version
   npm --version
   ```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install nodejs npm
```

Verify installation:
```bash
node --version
npm --version
```

### Installing Python

#### Windows
1. Go to [python.org](https://www.python.org/)
2. Download Python 3.8 or higher
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Click "Install Now"
6. Verify installation:
   ```bash
   python --version
   pip --version
   ```

#### macOS
**Using Homebrew (Recommended):**
```bash
brew install python3
```

**Or download from python.org:**
1. Go to [python.org](https://www.python.org/)
2. Download the macOS installer
3. Run the installer and follow the wizard
4. Verify installation:
   ```bash
   python3 --version
   pip3 --version
   ```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip
```

Verify installation:
```bash
python3 --version
pip3 --version
```

### Verify All Prerequisites

Run these commands to confirm everything is installed:

```bash
# Check Node.js
node --version    # Should show v16.0.0 or higher

# Check npm
npm --version     # Should show 7.0.0 or higher

# Check Python
python --version  # Should show 3.8.0 or higher
# On macOS/Linux, use: python3 --version

# Check pip
pip --version     # Should show 20.0.0 or higher
# On macOS/Linux, use: pip3 --version
```

If all commands show version numbers, you're ready to proceed!

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ANIMAL\ RESCUE
```

### 2. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
cd ..
```

## ▶️ Running the Project

### Option 1: Run Both Servers (Recommended)

#### Terminal 1 - Start Frontend Dev Server
```bash
cd frontend
npm run dev
```
Frontend will be available at: **http://localhost:5173**

#### Terminal 2 - Start Backend API Server
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Backend will be available at: **http://localhost:8000**

### Option 2: Run Individual Commands

#### Frontend Only
```bash
cd frontend
npm run dev          # Development server with hot reload
npm run build        # Build for production
npm run preview      # Preview production build
npm run lint         # Run ESLint
```

#### Backend Only
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000  # Development server
python seed_db.py                                                  # Seed database with sample data
```

### Option 3: Using Python Virtual Environment (Recommended for Backend)

```bash
# Create virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📁 Project Structure

```
ANIMAL RESCUE/
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── pages/              # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── Adopt.jsx
│   │   │   ├── Report.jsx
│   │   │   ├── Donate.jsx
│   │   │   ├── Login.jsx
│   │   │   └── AdminDashboard.jsx
│   │   ├── components/         # Reusable components
│   │   │   ├── Navbar.jsx
│   │   │   └── PetCard.jsx
│   │   ├── context/            # React context
│   │   │   ├── AuthContext.jsx
│   │   │   └── ToastContext.jsx
│   │   ├── services/           # API services
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── backend/                     # FastAPI backend
│   ├── main.py                 # Main application file
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic schemas
│   ├── database.py             # Database configuration
│   ├── auth.py                 # Authentication logic
│   ├── seed_db.py              # Database seeding
│   ├── requirements.txt         # Python dependencies
│   ├── animal_rescue.db        # SQLite database
│   └── uploads/                # Uploaded images
│
└── README.md                    # This file
```

## 🔌 API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /token` - Login and get JWT token
- `GET /users/me` - Get current user info

### Animals
- `GET /animals` - Get all animals (with optional species filter)
- `GET /animals/{id}` - Get animal by ID
- `POST /animals` - Create animal (admin only)
- `DELETE /animals/{id}` - Delete animal (admin only)

### Adoption Requests
- `POST /adoptions` - Create adoption request
- `GET /adoptions/me` - Get user's adoption requests
- `GET /adoptions` - Get all adoption requests (admin only)

### Rescue Reports
- `POST /reports` - Create rescue report with image upload
- `GET /reports` - Get all reports (admin only)

### Static Files
- `GET /uploads/{filename}` - Get uploaded images

## 📖 Usage Guide

### For Regular Users

#### 1. Register/Login
- Go to http://localhost:5173/login
- Click "Register" to create a new account
- Fill in username, email, and password
- Login with your credentials

#### 2. Report a Stray Animal
- Navigate to **Report** page
- Fill in the form:
  - **Animal Name** (optional): Give the animal a name
  - **Description**: Describe the animal and its condition
  - **Location**: Where you found the animal
  - **Contact Info**: Your phone number or email
  - **Upload Photos**: Click "Choose Files" to upload images
- Click "Submit Report"
- The animal will appear in the Adopt page

#### 3. Browse and Adopt
- Go to **Adopt** page
- Browse available animals
- Filter by species (Dogs, Cats, All)
- Click "Adopt {Animal Name}" to submit an adoption request
- Your request will be sent to the admin

#### 4. Donate
- Go to **Donate** page
- Choose a donation tier:
  - **Starter** ($10) - Food for one pet for a week
  - **Advocate** ($50) - Full medical checkup and vaccination
  - **Guardian** ($150) - Full care until adoption
- Click "Donate Now"
- See the success animation

### For Admins

#### 1. Access Admin Dashboard
- Login with admin account (first registered user is admin)
- Navigate to **Admin Dashboard**

#### 2. Monitor Statistics
- View real-time stats:
  - Total Animals
  - Rescue Reports
  - Adoption Requests
- Stats auto-refresh every 2 seconds

#### 3. Manage Animals
- Scroll to "Manage Animals" section
- View all animals in a table
- See animal details: Name, Species, Breed, Description, Status
- Click "Delete" button to remove an animal
- Confirm deletion in the popup

#### 4. View Adoption Requests
- Check "Adoption Requests" section
- See all pending adoption requests
- View user ID and animal ID for each request
- Status indicators: Pending, Approved, Rejected

#### 5. View Rescue Reports
- Check "Recent Rescue Reports" section
- See latest stray animal reports
- View report description and location
- Track report status

#### 6. Manual Refresh
- Click "🔄 Refresh" button anytime
- Dashboard will fetch latest data
- Button shows "Refreshing..." while loading

## 🔐 Authentication

The application uses JWT (JSON Web Tokens) for authentication:

- **First registered user** becomes an admin
- **Subsequent users** are regular users
- Admin can access the Admin Dashboard
- Regular users can report, adopt, and donate

## 📸 Image Upload

- Images are uploaded to the `backend/uploads/` directory
- Supported formats: JPG, PNG, GIF, WebP
- Images are served at: `http://localhost:8000/uploads/{filename}`
- Images are displayed in the Adopt page and Admin Dashboard

## 🗄️ Database

The application uses SQLite with the following tables:

- **users** - User accounts and authentication
- **animals** - All animals (both seeded and reported)
- **adoption_requests** - Adoption requests from users
- **rescue_reports** - Stray animal reports

### Seed Database

To populate the database with sample animals:

```bash
cd backend
python seed_db.py
```

This will add 4 sample animals if the database is empty.

## 🐛 Troubleshooting

### Frontend won't start
```bash
cd frontend
npm install
npm run dev
```

### Backend won't start
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Database issues
```bash
# Delete the database and reseed
cd backend
rm animal_rescue.db
python seed_db.py
```

### Port already in use
- Frontend (5173): Change in `frontend/vite.config.js`
- Backend (8000): Change in the uvicorn command: `--port 8001`

## 📝 Environment Variables

Create a `.env` file in the backend directory if needed:

```
DATABASE_URL=sqlite:///./animal_rescue.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For issues or questions, please create an issue in the repository.

---

**Happy rescuing! 🐾**
