# 🎭 AI Vision Command Center

## Advanced Facial Landmark & Hand Gesture Detection System

A cutting-edge real-time computer vision application that combines facial emotion detection with advanced hand gesture recognition. Built with React frontend and FastAPI backend, featuring MediaPipe integration for accurate AI-powered detection.

![Project Demo](https://img.shields.io/badge/Status-Active-brightgreen)
![React](https://img.shields.io/badge/React-18.x-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange)

## 🌟 Features

### 🎭 **Advanced Emotion Detection (16+ Emotions)**
- **Happy Spectrum:** Smiling 🙂 → Happy 😊 → Very Happy 😄 → Laughing 😂
- **Sad Spectrum:** Slightly Sad 😔 → Sad 😢 → Very Sad 😭
- **Surprise:** Surprised 😲 → Shocked 😱
- **Anger:** Angry 😠 → Very Angry 😡
- **Special Emotions:** Thinking 🤔, Worried 😟, Winking 😉, Yawning 🥱, Talking 😮, Sleepy 😴, Disgusted 🤢
- **Real-time detection** with optimized thresholds for accuracy

### 🖐️ **15 Advanced Hand Gestures**
- **Basic Gestures:** Thumbs Up 👍, Thumbs Down 👎, Victory ✌️, High Five 🖐️, Fist ✊
- **Number Gestures:** One ☝️, Two 2️⃣, Three 3️⃣, Four 4️⃣
- **Cultural Gestures:** Rock & Roll 🤘, Call Me 🤙, OK Sign 👌, I Love You 🤟
- **Fun Gestures:** Finger Gun 🔫, Finger Heart 💖, Spiderman 🕷️
- **Custom actions** for each gesture with voice feedback

### 📹 **Real-time Camera Interface**
- **Live webcam feed** with MediaPipe overlay
- **Smart overlays** showing current gesture and emotion
- **Confidence indicators** for gesture recognition
- **3-second countdown** for snapshot capture
- **Glassmorphism UI** with modern design

### 🎯 **Interactive Features**
- **Voice feedback** for all detections
- **Gesture guide** with visual instructions
- **Snapshot capture** with thumbs up gesture
- **Gallery system** for saved snapshots
- **Real-time statistics** and analytics
- **Debug console** for development

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v16 or higher) - Required for frontend development
- **Python** (v3.8 or higher) - Required for backend API
- **Modern web browser** (Chrome recommended)
- **Webcam** for real-time detection

### System Requirements & Installation

#### **Installing Node.js (Required for Frontend)**

**Windows:**
1. Download from [nodejs.org](https://nodejs.org/)
2. Run the installer (.msi file)
3. Follow installation wizard
4. Verify installation:
```cmd
node --version
npm --version
```

**macOS:**
```bash
# Using Homebrew (recommended)
brew install node

# Or download from nodejs.org
# Verify installation
node --version
npm --version
```

**Linux (Ubuntu/Debian):**
```bash
# Using NodeSource repository (recommended)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Or using package manager
sudo apt update
sudo apt install nodejs npm

# Verify installation
node --version
npm --version
```

**Linux (CentOS/RHEL/Fedora):**
```bash
# Using NodeSource repository
curl -fsSL https://rpm.nodesource.com/setup_18.x | sudo bash -
sudo dnf install nodejs npm

# Verify installation
node --version
npm --version
```

#### **Installing Python (Required for Backend)**

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer and **check "Add Python to PATH"**
3. Verify installation:
```cmd
python --version
pip --version
```

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python

# Verify installation
python3 --version
pip3 --version
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL/Fedora
sudo dnf install python3 python3-pip

# Verify installation
python3 --version
pip3 --version
```

### Installation

#### **Step 1: Clone the Repository**
```bash
git clone <repository-url>
cd "Facial Landmark Detection with Hand Gesture"
```

#### **Step 2: Setup Backend (FastAPI)**
```bash
cd backend

# For Windows
python -m pip install fastapi uvicorn sqlalchemy pydantic python-multipart

# For macOS/Linux
python3 -m pip install fastapi uvicorn sqlalchemy pydantic python-multipart

# Alternative: Install from requirements file
# Windows
python -m pip install -r requirements.txt
# macOS/Linux  
python3 -m pip install -r requirements.txt

# Run the backend server
# Windows
python main.py
# macOS/Linux
python3 main.py
```
✅ Backend will run on: **http://localhost:8000**

#### **Step 3: Setup Frontend (React + Vite)**
```bash
# Open new terminal/command prompt
cd frontend

# Install Node.js dependencies (same for all systems)
npm install

# Start the development server
npm run dev
```
✅ Frontend will run on: **http://localhost:5173**

#### **Step 4: Open the Application**
Navigate to **http://localhost:5173** in your browser

### Quick Setup for Different Systems

#### **Windows Setup:**
```cmd
# 1. Install Node.js from nodejs.org
# 2. Install Python from python.org
# 3. Clone and setup project
git clone <repository-url>
cd "Facial Landmark Detection with Hand Gesture"

# Backend
cd backend
python -m pip install -r requirements.txt
python main.py

# Frontend (new command prompt)
cd frontend
npm install
npm run dev
```

#### **macOS Setup:**
```bash
# 1. Install dependencies
brew install node python

# 2. Clone and setup project
git clone <repository-url>
cd "Facial Landmark Detection with Hand Gesture"

# Backend
cd backend
python3 -m pip install -r requirements.txt
python3 main.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

#### **Linux Setup:**
```bash
# 1. Install dependencies
sudo apt update
sudo apt install nodejs npm python3 python3-pip

# 2. Clone and setup project
git clone <repository-url>
cd "Facial Landmark Detection with Hand Gesture"

# Backend
cd backend
python3 -m pip install -r requirements.txt
python3 main.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Running the Project

#### **Start Backend Server:**
```bash
cd backend

# Windows
python main.py

# macOS/Linux
python3 main.py
```
The FastAPI server will start on port 8000 with auto-reload enabled.

#### **Start Frontend Development Server:**
```bash
cd frontend
npm run dev
```
The Vite development server will start on port 5173 with hot module replacement.

#### **Alternative Frontend Commands:**
```bash
# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint
```

### **Verification Steps:**
1. **Check Node.js:** `node --version` (should show v16+)
2. **Check Python:** `python --version` or `python3 --version` (should show v3.8+)
3. **Backend Check:** Visit http://localhost:8000/docs for API documentation
4. **Frontend Check:** Visit http://localhost:5173 for the main application
5. **Camera Access:** Allow camera permissions when prompted
6. **Model Loading:** Wait for "Ready ✓" status in the application

### **First Time Setup Checklist:**
- [ ] Node.js installed and working (`node --version`)
- [ ] Python installed and working (`python --version`)
- [ ] Git installed for cloning repository
- [ ] Webcam connected and working
- [ ] Modern browser installed (Chrome recommended)
- [ ] Internet connection for MediaPipe model downloads

## 📁 Project Structure

```
📦 Facial Landmark Detection with Hand Gesture
├── 📂 backend/                 # FastAPI Backend
│   ├── 📄 main.py             # FastAPI application
│   ├── 📄 models.py           # Database models
│   ├── 📄 database.py         # Database configuration
│   ├── 📄 requirements.txt    # Python dependencies
│   └── 📄 facial_landmarks.db # SQLite database
├── 📂 frontend/               # React Frontend
│   ├── 📂 src/
│   │   ├── 📂 components/
│   │   │   ├── 📄 Detector.jsx    # Main detection component
│   │   │   ├── 📄 Gallery.jsx     # Snapshots gallery
│   │   │   └── 📄 Sidebar.jsx     # Navigation sidebar
│   │   ├── 📂 utils/
│   │   │   └── 📄 ARFilters.js    # Emotion detection logic
│   │   ├── 📄 App.jsx         # Main application
│   │   └── 📄 main.jsx        # Entry point
│   ├── 📄 package.json        # Node.js dependencies
│   └── 📄 vite.config.js      # Vite configuration
├── 📄 README.md               # This file
├── 📄 implementation_plan.md  # Development plan
└── 📄 walkthrough.md          # Feature walkthrough
```

## 🎮 How to Use

### 🎭 **Emotion Detection**
1. **Look at the camera** - The system detects your facial expressions in real-time
2. **Try different expressions:**
   - **Smile** for happy emotions
   - **Frown** for sad emotions  
   - **Raise eyebrows** for surprise
   - **Furrow brows** for anger
3. **View results** in the top-right overlay

### 🖐️ **Gesture Recognition**
1. **Show your hand** to the camera
2. **Make gestures:**
   - **👍 Thumbs Up** - Triggers 3-second countdown, then captures snapshot
   - **✌️ Victory** - Peace sign recognition
   - **🖐️ Open Palm** - High five gesture
   - **🤘 Rock & Roll** - Rock on gesture
   - **And 11 more gestures!**
3. **Click the hand icon** for full gesture guide

### 📸 **Snapshot Capture**
1. **Make thumbs up gesture** 👍
2. **Wait for 3-second countdown**
3. **Snapshot automatically captured** and saved to gallery
4. **View in Gallery tab** on the sidebar

## 🛠️ Technical Details

### **Frontend Technologies**
- **React 18** - Modern UI framework
- **Vite** - Fast build tool and dev server
- **MediaPipe** - Google's ML framework for real-time detection
- **Axios** - HTTP client for API communication
- **Lucide React** - Modern icon library

### **Backend Technologies**
- **FastAPI** - High-performance Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Lightweight database
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### **AI/ML Features**
- **MediaPipe Face Landmarker** - 468 facial landmarks
- **MediaPipe Gesture Recognizer** - Hand gesture detection
- **Custom gesture algorithms** - Advanced gesture recognition
- **Blendshape analysis** - Facial expression quantification
- **Real-time processing** - 30+ FPS detection

## 🎯 API Endpoints

### **Snapshots**
- `POST /snapshots/` - Create new snapshot
- `GET /snapshots/` - Get all snapshots (paginated)
- `DELETE /snapshots/{id}` - Delete specific snapshot

### **Statistics**
- `GET /stats/` - Get detection statistics

### **Example API Usage**
```javascript
// Capture snapshot
const response = await axios.post('http://localhost:8000/snapshots/', {
  image_data: base64Image,
  gesture_detected: "Thumb_Up",
  emotion_detected: "Happy 😊",
  landmarks_count: 468
});

// Get statistics
const stats = await axios.get('http://localhost:8000/stats/');
```

## 🎨 UI Features

### **Modern Design**
- **Glassmorphism effects** with blur and transparency
- **Gradient backgrounds** for visual appeal
- **Responsive layout** for different screen sizes
- **Dark theme** optimized for camera usage

### **Real-time Overlays**
- **Gesture display** (top-left) - Shows current gesture and action
- **Emotion display** (top-right) - Shows detected emotion
- **Countdown timer** (center) - For snapshot capture
- **Instructions** (bottom) - Quick help and tips

### **Interactive Elements**
- **Voice toggle** - Enable/disable audio feedback
- **Wireframe toggle** - Show/hide landmark visualization
- **Gesture guide** - Modal with all available gestures
- **Gallery view** - Browse captured snapshots

## 🔧 Configuration

### **Emotion Detection Thresholds**
Located in `frontend/src/utils/ARFilters.js`:
```javascript
// Adjust sensitivity (0.0 - 1.0)
const smileThreshold = 0.15;  // Lower = more sensitive
const frownThreshold = 0.15;
const angerThreshold = 0.15;
```

### **Gesture Recognition Settings**
Located in `frontend/src/components/Detector.jsx`:
```javascript
// Gesture cooldown (milliseconds)
const gestureCooldown = 2000;

// Snapshot countdown (seconds)
const snapshotCountdown = 3;
```

## 🐛 Troubleshooting

### **Common Issues**

**Models not loading:**
- Check internet connection (models load from CDN)
- Try different browser (Chrome recommended)
- Disable browser extensions that might block requests
- Check browser console (F12) for error messages

**Camera not working:**
- Grant camera permissions when prompted
- Ensure no other applications are using the camera
- Try refreshing the page
- Check browser camera settings

**Poor detection accuracy:**
- Ensure good lighting conditions
- Position face/hands clearly in camera view
- Avoid background clutter
- Check if webcam resolution is adequate

**Backend connection issues:**
- Verify backend is running on http://localhost:8000
- Check for CORS errors in browser console
- Ensure no firewall blocking local connections

### **Debug Mode**
1. Open browser console (F12)
2. Check for blendshape values and detection scores
3. Monitor API requests in Network tab
4. Look for error messages in Console tab

## 🚀 Performance Optimization

### **Frontend Optimizations**
- **GPU acceleration** for MediaPipe (with CPU fallback)
- **Efficient rendering** with React hooks
- **Debounced gesture actions** to prevent spam
- **Optimized canvas drawing** for landmarks

### **Backend Optimizations**
- **Async FastAPI** for concurrent requests
- **SQLite** for lightweight data storage
- **Efficient database queries** with SQLAlchemy
- **CORS optimization** for frontend communication

## 🔮 Future Enhancements

### **Planned Features**
- [ ] **Multi-person detection** - Support multiple faces/hands
- [ ] **Custom gesture training** - User-defined gestures
- [ ] **Emotion analytics** - Historical emotion tracking
- [ ] **Export functionality** - Download snapshots and data
- [ ] **Mobile app** - React Native version
- [ ] **Cloud deployment** - Web-hosted version

### **Advanced Features**
- [ ] **3D face reconstruction** - Depth estimation
- [ ] **Augmented reality filters** - Real-time face filters
- [ ] **Voice commands** - Speech recognition integration
- [ ] **Machine learning training** - Custom model training
- [ ] **Multi-language support** - Internationalization

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support, questions, or feature requests:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the debug console for error messages

## 🙏 Acknowledgments

- **MediaPipe** - Google's ML framework for computer vision
- **React** - Facebook's UI library
- **FastAPI** - Modern Python web framework
- **Vite** - Next generation frontend tooling

---

**Built with ❤️ for computer vision enthusiasts and developers**

*Last updated: April 2026*