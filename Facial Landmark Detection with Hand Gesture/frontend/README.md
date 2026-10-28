# 🎭 AI Vision Command Center - Frontend

## React + Vite + MediaPipe Frontend

This is the frontend application for the AI Vision Command Center, built with React, Vite, and MediaPipe for real-time facial emotion detection and hand gesture recognition.

## 🚀 Quick Start

### Prerequisites
- **Node.js** (v16 or higher)
- **Modern web browser** (Chrome recommended for best MediaPipe support)
- **Webcam** for real-time detection

### Installation & Running

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint
```

## 🛠️ Available Scripts

- **`npm run dev`** - Start development server with hot reload
- **`npm run build`** - Build for production
- **`npm run preview`** - Preview production build locally
- **`npm run lint`** - Run ESLint for code quality

## 📦 Key Dependencies

### **Core Framework**
- **React 19.2.5** - UI framework
- **Vite 8.0.10** - Build tool and dev server

### **Computer Vision**
- **@mediapipe/tasks-vision** - Google's ML framework for face and hand detection
- **react-webcam** - Webcam integration for React

### **UI & Styling**
- **lucide-react** - Modern icon library
- **Custom CSS** - Glassmorphism design with gradients

### **HTTP Client**
- **axios** - API communication with FastAPI backend

## 🎯 Features

- **Real-time facial emotion detection** (16+ emotions)
- **Advanced hand gesture recognition** (15 gestures)
- **Live camera overlays** with gesture and emotion display
- **Voice feedback system** with speech synthesis
- **Snapshot capture** with countdown timer
- **Gallery system** for saved snapshots
- **Responsive design** with modern UI

## 🔧 Configuration

### **MediaPipe Settings**
Located in `src/components/Detector.jsx`:
```javascript
// Model loading with GPU/CPU fallback
const vision = await FilesetResolver.forVisionTasks(
  "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
);
```

### **Emotion Detection Thresholds**
Located in `src/utils/ARFilters.js`:
```javascript
// Adjust sensitivity (lower = more sensitive)
const smileScore = 0.15;  // Smile detection threshold
const frownScore = 0.15;  // Frown detection threshold
const angerScore = 0.15;  // Anger detection threshold
```

### **API Configuration**
Located in `src/components/Detector.jsx`:
```javascript
const API_URL = "http://localhost:8000";  // Backend URL
```

## 🐛 Troubleshooting

### **Model Loading Issues**
- Ensure stable internet connection (models load from CDN)
- Check browser console (F12) for error messages
- Try disabling browser extensions
- Use Chrome for best compatibility

### **Camera Issues**
- Grant camera permissions when prompted
- Ensure no other apps are using the camera
- Check browser camera settings
- Try refreshing the page

### **Performance Issues**
- Close other browser tabs using camera
- Ensure adequate lighting for better detection
- Check if GPU acceleration is available

## 🏗️ Build Configuration

### **Vite Configuration**
The project uses Vite for fast development and optimized builds:

```javascript
// vite.config.js
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true
  }
})
```

### **ESLint Configuration**
Code quality is maintained with ESLint:
- React hooks rules
- React refresh rules
- Modern JavaScript standards

## 🔗 Backend Integration

The frontend communicates with a FastAPI backend running on `http://localhost:8000`:

- **POST /snapshots/** - Save captured snapshots
- **GET /snapshots/** - Retrieve snapshot gallery
- **GET /stats/** - Get detection statistics
- **DELETE /snapshots/{id}** - Delete snapshots

## 📱 Browser Compatibility

### **Recommended Browsers**
- **Chrome 90+** (Best MediaPipe support)
- **Firefox 88+** (Good support)
- **Safari 14+** (Limited support)
- **Edge 90+** (Good support)

### **Required Browser Features**
- WebRTC for camera access
- WebAssembly for MediaPipe
- ES6+ JavaScript support
- Canvas API for drawing overlays

## 🚀 Deployment

### **Production Build**
```bash
npm run build
```
Creates optimized build in `dist/` directory.

### **Environment Variables**
Create `.env` file for configuration:
```env
VITE_API_URL=http://localhost:8000
VITE_ENABLE_DEBUG=false
```

## 🤝 Development

### **Project Structure**
```
src/
├── components/
│   ├── Detector.jsx    # Main detection component
│   ├── Gallery.jsx     # Snapshots gallery
│   └── Sidebar.jsx     # Navigation sidebar
├── utils/
│   └── ARFilters.js    # Emotion detection algorithms
├── assets/             # Static assets
├── App.jsx            # Main application component
└── main.jsx           # Application entry point
```

### **Adding New Features**
1. Create components in `src/components/`
2. Add utilities in `src/utils/`
3. Update routing in `App.jsx`
4. Test with `npm run dev`

---

For more information, see the main project README.md