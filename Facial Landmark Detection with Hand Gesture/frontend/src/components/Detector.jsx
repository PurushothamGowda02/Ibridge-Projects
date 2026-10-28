import React, { useRef, useEffect, useState } from 'react';
import Webcam from 'react-webcam';
import { FaceLandmarker, GestureRecognizer, HandLandmarker, FilesetResolver, DrawingUtils } from "@mediapipe/tasks-vision";
import axios from 'axios';
import { Camera, RefreshCw, Zap, Smile, Volume2, Layout, Maximize, Hand } from 'lucide-react';
import { detectEmotion } from '../utils/ARFilters';

const API_URL = "http://localhost:8000";

const Detector = () => {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);
  
  const [faceLandmarker, setFaceLandmarker] = useState(null);
  const [gestureRecognizer, setGestureRecognizer] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [status, setStatus] = useState("Initializing Advanced Models...");
  const [detectedGesture, setDetectedGesture] = useState("None");
  const [detectedEmotion, setDetectedEmotion] = useState("Neutral");
  const [showLandmarks, setShowLandmarks] = useState(true);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [lastAnnounced, setLastAnnounced] = useState("");
  const lastAnnouncedRef = useRef("");
  const [showGestureGuide, setShowGestureGuide] = useState(false);
  const [loadError, setLoadError] = useState(false);
  const [gestureCountdown, setGestureCountdown] = useState(0);
  const [pendingGesture, setPendingGesture] = useState(null);

  useEffect(() => {
    const initModels = async () => {
      try {
        setStatus("Loading Vision Tasks...");
        const vision = await FilesetResolver.forVisionTasks(
          "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm"
        );
        
        setStatus("Loading Face Landmarker...");
        let flm;
        try {
          // Try with GPU first
          flm = await FaceLandmarker.createFromOptions(vision, {
            baseOptions: {
              modelAssetPath: "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
              delegate: "GPU"
            },
            outputFaceBlendshapes: true,
            runningMode: "VIDEO",
            numFaces: 1
          });
        } catch (gpuError) {
          console.warn("GPU not available, falling back to CPU:", gpuError);
          // Fallback to CPU
          flm = await FaceLandmarker.createFromOptions(vision, {
            baseOptions: {
              modelAssetPath: "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",
              delegate: "CPU"
            },
            outputFaceBlendshapes: true,
            runningMode: "VIDEO",
            numFaces: 1
          });
        }

        setStatus("Loading Gesture Recognizer...");
        let gr;
        try {
          // Try with GPU first
          gr = await GestureRecognizer.createFromOptions(vision, {
            baseOptions: {
              modelAssetPath: "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
              delegate: "GPU"
            },
            runningMode: "VIDEO"
          });
        } catch (gpuError) {
          console.warn("GPU not available for gestures, falling back to CPU:", gpuError);
          // Fallback to CPU
          gr = await GestureRecognizer.createFromOptions(vision, {
            baseOptions: {
              modelAssetPath: "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
              delegate: "CPU"
            },
            runningMode: "VIDEO"
          });
        }

        setFaceLandmarker(flm);
        setGestureRecognizer(gr);
        setIsLoaded(true);
        setStatus("Ready ✓");
        setLoadError(false);
        console.log("Models loaded successfully!");
      } catch (error) {
        console.error("Model loading error:", error);
        setStatus(`Error: ${error.message || 'Failed to load models. Check console for details.'}`);
        setLoadError(true);
      }
    };
    initModels();
  }, []);

  const retryLoadModels = () => {
    setIsLoaded(false);
    setLoadError(false);
    setStatus("Retrying...");
    window.location.reload();
  };

  // Custom gesture detection using hand landmarks
  const detectCustomGestures = (landmarks) => {
    if (!landmarks || landmarks.length < 21) return null;

    // Get key landmark points
    const thumb_tip = landmarks[4];
    const thumb_ip = landmarks[3];
    const index_tip = landmarks[8];
    const index_pip = landmarks[6];
    const middle_tip = landmarks[12];
    const middle_pip = landmarks[10];
    const ring_tip = landmarks[16];
    const ring_pip = landmarks[14];
    const pinky_tip = landmarks[20];
    const pinky_pip = landmarks[18];
    const wrist = landmarks[0];

    // Calculate if fingers are extended
    const thumb_up = thumb_tip.y < thumb_ip.y;
    const index_up = index_tip.y < index_pip.y;
    const middle_up = middle_tip.y < middle_pip.y;
    const ring_up = ring_tip.y < ring_pip.y;
    const pinky_up = pinky_tip.y < pinky_pip.y;

    const fingers_up = [thumb_up, index_up, middle_up, ring_up, pinky_up];
    const fingers_count = fingers_up.filter(Boolean).length;

    // Custom gesture detection
    
    // Rock and Roll (index and pinky up, others down)
    if (!thumb_up && index_up && !middle_up && !ring_up && pinky_up) {
      return "Rock_And_Roll 🤘";
    }

    // Call Me (thumb and pinky up, others down)
    if (thumb_up && !index_up && !middle_up && !ring_up && pinky_up) {
      return "Call_Me 🤙";
    }

    // OK Sign (thumb and index forming circle)
    const thumb_index_distance = Math.sqrt(
      Math.pow(thumb_tip.x - index_tip.x, 2) + 
      Math.pow(thumb_tip.y - index_tip.y, 2)
    );
    if (thumb_index_distance < 0.05 && middle_up && ring_up && pinky_up) {
      return "OK_Sign 👌";
    }

    // Three fingers (index, middle, ring up)
    if (!thumb_up && index_up && middle_up && ring_up && !pinky_up) {
      return "Three 3️⃣";
    }

    // Four fingers (all except thumb)
    if (!thumb_up && index_up && middle_up && ring_up && pinky_up) {
      return "Four 4️⃣";
    }

    // Gun/Pistol (index up, thumb up, others down)
    if (thumb_up && index_up && !middle_up && !ring_up && !pinky_up) {
      return "Gun 🔫";
    }

    // Finger Heart (thumb and index crossed)
    const thumb_index_cross = Math.abs(thumb_tip.x - index_tip.x) < 0.03 && 
                             Math.abs(thumb_tip.y - index_tip.y) < 0.03;
    if (thumb_index_cross && !middle_up && !ring_up && !pinky_up) {
      return "Heart 💖";
    }

    // Spiderman (thumb, index, pinky up)
    if (thumb_up && index_up && !middle_up && !ring_up && pinky_up) {
      return "Spiderman 🕷️";
    }

    // Number One (only index up)
    if (!thumb_up && index_up && !middle_up && !ring_up && !pinky_up) {
      return "One 1️⃣";
    }

    // Number Two (index and middle up)
    if (!thumb_up && index_up && middle_up && !ring_up && !pinky_up) {
      return "Two 2️⃣";
    }

    // Thumbs Down
    if (thumb_tip.y > thumb_ip.y && !index_up && !middle_up && !ring_up && !pinky_up) {
      return "Thumbs_Down 👎";
    }

    // Stop/High Five (all fingers up)
    if (fingers_count === 5) {
      return "High_Five 🖐️";
    }

    // Fist (no fingers up)
    if (fingers_count === 0) {
      return "Fist ✊";
    }

    return null; // No custom gesture detected
  };

  // Get the action description for each gesture
  const getGestureAction = (gesture) => {
    const actions = {
      "Thumb_Up": "📸 Capture Snapshot",
      "Thumbs_Down 👎": "👎 Negative Feedback",
      "Thumb_Down": "👎 Negative Feedback",
      "Victory": "✌️ Peace Sign",
      "Two 2️⃣": "✌️ Number Two",
      "Open_Palm": "🖐️ High Five",
      "High_Five 🖐️": "🖐️ High Five",
      "Closed_Fist": "✊ Power Fist",
      "Fist ✊": "✊ Power Fist",
      "Pointing_Up": "☝️ Number One",
      "One 1️⃣": "☝️ Number One",
      "ILoveYou": "🤟 Love Sign",
      "Rock_And_Roll 🤘": "🤘 Rock On!",
      "Call_Me 🤙": "🤙 Call Gesture",
      "OK_Sign 👌": "👌 Perfect Sign",
      "Three 3️⃣": "3️⃣ Number Three",
      "Four 4️⃣": "4️⃣ Number Four",
      "Gun 🔫": "🔫 Finger Gun",
      "Heart 💖": "💖 Love Heart",
      "Spiderman 🕷️": "🕷️ Web Slinger",
      "None": "🔍 Searching for gesture..."
    };
    
    return actions[gesture] || "🤔 Unknown action";
  };

  const speak = (text) => {
    if (!voiceEnabled || lastAnnounced === text) return;
    
    // Cancel any ongoing speech before starting new one
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.2;
    window.speechSynthesis.speak(utterance);
    setLastAnnounced(text);
    
    // Reset lastAnnounced after a delay to allow re-announcement if emotion changes back
    setTimeout(() => setLastAnnounced(""), 3000);
  };

  useEffect(() => {
    let animationFrameId;
    const runDetection = async () => {
      if (isLoaded && webcamRef.current && webcamRef.current.video.readyState === 4) {
        const video = webcamRef.current.video;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const startTimeMs = performance.now();
        const faceResults = faceLandmarker.detectForVideo(video, startTimeMs);
        const gestureResults = gestureRecognizer.recognizeForVideo(video, startTimeMs);

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const drawingUtils = new DrawingUtils(ctx);

        // Process Face Results
        if (faceResults.faceLandmarks && faceResults.faceLandmarks.length > 0) {
          const landmarks = faceResults.faceLandmarks[0];
          
          // Emotion Detection
          const emotion = detectEmotion(faceResults.faceBlendshapes);
          if (emotion !== detectedEmotion) {
            setDetectedEmotion(emotion);
            // Only speak if emotion changed and it's not neutral
            if (emotion !== "Neutral 😐" && lastAnnouncedRef.current !== emotion) {
              speak(emotion);
              lastAnnouncedRef.current = emotion;
            }
          }

          // Draw Landmarks
          if (showLandmarks) {
            drawingUtils.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_TESSELATION, { color: "#C0C0C070", lineWidth: 1 });
            drawingUtils.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_RIGHT_EYE, { color: "#FF3030" });
            drawingUtils.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_LEFT_EYE, { color: "#30FF30" });
            drawingUtils.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_FACE_OVAL, { color: "#E0E0E0" });
            drawingUtils.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_LIPS, { color: "#E0E0E0" });
            drawingUtils.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_RIGHT_IRIS, { color: "#FF3030" });
            drawingUtils.drawConnectors(landmarks, FaceLandmarker.FACE_LANDMARKS_LEFT_IRIS, { color: "#30FF30" });
          }
        }

        // Handle Gestures
        if (gestureResults.gestures.length > 0) {
          const topGesture = gestureResults.gestures[0][0];
          const gestureName = topGesture.categoryName;
          const confidence = Math.round(topGesture.score * 100);
          
          // Also detect custom gestures using landmarks
          let customGesture = null;
          if (gestureResults.landmarks && gestureResults.landmarks.length > 0) {
            customGesture = detectCustomGestures(gestureResults.landmarks[0]);
          }
          
          // Use custom gesture if detected, otherwise use MediaPipe gesture
          const finalGesture = customGesture || gestureName;
          setDetectedGesture(finalGesture);

          // Draw confidence indicator on canvas
          if (confidence > 70) {
            ctx.fillStyle = 'rgba(0, 255, 0, 0.8)';
            ctx.fillRect(10, 10, confidence * 2, 10);
            ctx.fillStyle = 'white';
            ctx.font = '14px Arial';
            ctx.fillText(`${confidence}%`, 15, 35);
          }

          // Draw Hand Landmarks
          if (showLandmarks && gestureResults.landmarks) {
            for (const landmarks of gestureResults.landmarks) {
              drawingUtils.drawConnectors(landmarks, HandLandmarker.HAND_CONNECTIONS, {
                color: "#00FF00",
                lineWidth: 2
              });
              drawingUtils.drawLandmarks(landmarks, {
                color: "#FF3030",
                lineWidth: 1,
                radius: 3
              });
            }
          }

          // Handle different gestures with custom actions
          handleGestureAction(finalGesture);
        } else {
          setDetectedGesture("None");
        }
      }
      animationFrameId = requestAnimationFrame(runDetection);
    };

    if (isLoaded) runDetection();
    return () => cancelAnimationFrame(animationFrameId);
  }, [isLoaded, showLandmarks, voiceEnabled, detectedEmotion]);

  const captureSnapshot = async (gesture, emotion) => {
    const imageSrc = webcamRef.current.getScreenshot();
    try {
      await axios.post(`${API_URL}/snapshots/`, {
        image_data: imageSrc,
        gesture_detected: gesture,
        emotion_detected: emotion,
        landmarks_count: 468
      });
      setStatus("Snapshot Saved!");
      setTimeout(() => setStatus("Ready"), 2000);
    } catch (error) {
      console.error("Save error:", error);
    }
  };

  const handleGestureAction = (gesture) => {
    // Prevent rapid repeated actions
    const now = Date.now();
    if (now - lastAnnouncedRef.current < 2000) return;

    // Start countdown for important gestures
    if (gesture === "Thumb_Up" && gestureCountdown === 0) {
      setPendingGesture(gesture);
      setGestureCountdown(3);
      
      const countdown = setInterval(() => {
        setGestureCountdown(prev => {
          if (prev <= 1) {
            clearInterval(countdown);
            executeGestureAction(gesture);
            setPendingGesture(null);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      
      return;
    }

    // Execute other gestures immediately
    executeGestureAction(gesture);
  };

  const executeGestureAction = (gesture) => {
    lastAnnouncedRef.current = Date.now();

    switch(gesture) {
      case "Thumb_Up":
        captureSnapshot(gesture, detectedEmotion);
        speak("Snapshot captured");
        setStatus("📸 Snapshot Captured!");
        break;
      
      case "Thumb_Down":
      case "Thumbs_Down 👎":
        speak("Thumbs down detected");
        setStatus("👎 Thumbs Down");
        break;
      
      case "Victory":
      case "Two 2️⃣":
        speak("Peace sign detected");
        setStatus("✌️ Victory!");
        break;
      
      case "Open_Palm":
      case "High_Five 🖐️":
        speak("High five");
        setStatus("🖐️ High Five!");
        break;
      
      case "Closed_Fist":
      case "Fist ✊":
        speak("Fist detected");
        setStatus("✊ Power Fist!");
        break;
      
      case "Pointing_Up":
      case "One 1️⃣":
        speak("Number one");
        setStatus("☝️ Number One!");
        break;
      
      case "ILoveYou":
        speak("I love you");
        setStatus("🤟 I Love You!");
        break;

      // New custom gestures
      case "Rock_And_Roll 🤘":
        speak("Rock and roll");
        setStatus("🤘 Rock On!");
        break;

      case "Call_Me 🤙":
        speak("Call me");
        setStatus("🤙 Call Me!");
        break;

      case "OK_Sign 👌":
        speak("OK sign");
        setStatus("👌 Perfect!");
        break;

      case "Three 3️⃣":
        speak("Number three");
        setStatus("3️⃣ Three!");
        break;

      case "Four 4️⃣":
        speak("Number four");
        setStatus("4️⃣ Four!");
        break;

      case "Gun 🔫":
        speak("Finger gun");
        setStatus("🔫 Pew Pew!");
        break;

      case "Heart 💖":
        speak("Finger heart");
        setStatus("💖 Love!");
        break;

      case "Spiderman 🕷️":
        speak("Spiderman web");
        setStatus("🕷️ Web Slinger!");
        break;
      
      default:
        break;
    }
    
    setTimeout(() => setStatus("Ready"), 2000);
  };

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', gap: '20px' }} className="animate-fade">
      <header className="glass" style={{ padding: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '1.5rem', fontWeight: 700 }}>AI Vision Command Center</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Emotion: {detectedEmotion} | Gesture: {detectedGesture}</p>
        </div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className={`btn-secondary ${voiceEnabled ? 'active' : ''}`} onClick={() => setVoiceEnabled(!voiceEnabled)} title="Toggle Voice Feedback">
            <Volume2 size={20} color={voiceEnabled ? "var(--primary)" : "white"} />
          </button>
          <button className="btn-secondary" onClick={() => setShowGestureGuide(!showGestureGuide)} title="Gesture Guide">
            <Hand size={20} />
          </button>
          <button className="btn-primary" onClick={() => setShowLandmarks(!showLandmarks)}>
            {showLandmarks ? 'Disable Wireframe' : 'Enable Wireframe'}
          </button>
        </div>
      </header>

      <div style={{ flex: 1, position: 'relative', display: 'flex', gap: '20px' }}>
        <div style={{ flex: 3, position: 'relative' }} className="glass">
          {!isLoaded && (
            <div style={{ position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '20px', zIndex: 10, background: 'rgba(0,0,0,0.7)' }}>
              {!loadError ? (
                <>
                  <RefreshCw className="animate-spin" size={40} color="var(--primary)" />
                  <p style={{ textAlign: 'center', padding: '0 20px' }}>{status}</p>
                </>
              ) : (
                <>
                  <div style={{ fontSize: '3rem' }}>⚠️</div>
                  <p style={{ textAlign: 'center', padding: '0 20px', maxWidth: '400px' }}>{status}</p>
                  <button className="btn-primary" onClick={retryLoadModels}>
                    <RefreshCw size={20} /> Retry Loading Models
                  </button>
                  <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', textAlign: 'center', maxWidth: '400px' }}>
                    <p>Common fixes:</p>
                    <ul style={{ textAlign: 'left', marginTop: '10px' }}>
                      <li>Check your internet connection</li>
                      <li>Disable browser extensions</li>
                      <li>Try a different browser (Chrome recommended)</li>
                      <li>Clear browser cache</li>
                    </ul>
                  </div>
                </>
              )}
            </div>
          )}
          <Webcam ref={webcamRef} screenshotFormat="image/jpeg" videoConstraints={{ facingMode: "user" }} style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '16px' }} />
          <canvas ref={canvasRef} style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', objectFit: 'cover' }} />
          
          {/* Gesture Action Overlay */}
          <div style={{ 
            position: 'absolute', 
            top: '20px', 
            left: '20px', 
            background: 'rgba(0, 0, 0, 0.8)', 
            color: 'white', 
            padding: '15px 20px', 
            borderRadius: '12px', 
            fontSize: '1.1rem', 
            fontWeight: '600',
            backdropFilter: 'blur(10px)',
            border: '2px solid rgba(255, 255, 255, 0.2)',
            minWidth: '250px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <span style={{ fontSize: '1.5rem' }}>🖐️</span>
              <span>Current Gesture:</span>
            </div>
            <div style={{ fontSize: '1.3rem', color: '#4ade80', marginBottom: '10px' }}>
              {detectedGesture}
            </div>
            <div style={{ fontSize: '0.9rem', color: '#94a3b8' }}>
              Action: {getGestureAction(detectedGesture)}
            </div>
          </div>

          {/* Emotion Overlay */}
          <div style={{ 
            position: 'absolute', 
            top: '20px', 
            right: '20px', 
            background: 'rgba(0, 0, 0, 0.8)', 
            color: 'white', 
            padding: '15px 20px', 
            borderRadius: '12px', 
            fontSize: '1.1rem', 
            fontWeight: '600',
            backdropFilter: 'blur(10px)',
            border: '2px solid rgba(255, 255, 255, 0.2)',
            textAlign: 'center',
            minWidth: '200px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
              <span style={{ fontSize: '1.5rem' }}>😊</span>
              <span>Emotion:</span>
            </div>
            <div style={{ fontSize: '1.3rem', color: '#f59e0b' }}>
              {detectedEmotion}
            </div>
          </div>

          {/* Instructions Overlay */}
          <div style={{ 
            position: 'absolute', 
            bottom: '20px', 
            left: '50%', 
            transform: 'translateX(-50%)',
            background: 'rgba(0, 0, 0, 0.8)', 
            color: 'white', 
            padding: '12px 20px', 
            borderRadius: '25px', 
            fontSize: '0.9rem', 
            backdropFilter: 'blur(10px)',
            border: '2px solid rgba(255, 255, 255, 0.2)',
            textAlign: 'center'
          }}>
            👍 Thumbs up to capture • 🖐️ Click hand icon for full gesture guide
          </div>

          {/* Countdown Overlay */}
          {gestureCountdown > 0 && (
            <div style={{ 
              position: 'absolute', 
              top: '50%', 
              left: '50%', 
              transform: 'translate(-50%, -50%)',
              background: 'rgba(255, 0, 0, 0.9)', 
              color: 'white', 
              padding: '30px', 
              borderRadius: '50%', 
              fontSize: '3rem', 
              fontWeight: 'bold',
              backdropFilter: 'blur(10px)',
              border: '4px solid white',
              textAlign: 'center',
              minWidth: '120px',
              minHeight: '120px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              animation: 'pulse 1s infinite'
            }}>
              {gestureCountdown}
            </div>
          )}
        </div>

        {/* Stats Panel */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <div className="glass" style={{ padding: '20px' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '15px' }}><Smile size={20} color="var(--primary)"/> Emotion Hub</h3>
            <div style={{ fontSize: '2rem', textAlign: 'center', margin: '20px 0' }}>{detectedEmotion.split(' ')[1] || '😐'}</div>
            <p style={{ textAlign: 'center', fontWeight: 600 }}>{detectedEmotion.split(' ')[0]}</p>
          </div>
          
          <div className="glass" style={{ padding: '20px' }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '15px' }}><Zap size={20} color="#fbbf24"/> Active Gesture</h3>
            <div style={{ background: 'var(--glass)', padding: '15px', borderRadius: '12px', textAlign: 'center' }}>
              <span style={{ fontSize: '0.9rem', fontWeight: 700, letterSpacing: '1px' }}>{detectedGesture}</span>
            </div>
          </div>

          <div className="glass" style={{ padding: '20px', flex: 1 }}>
            <h3 style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '15px' }}><Maximize size={20} color="#3b82f6"/> Wireframe Engine</h3>
            <ul style={{ listStyle: 'none', fontSize: '0.85rem', display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <li>• Face Points: 468</li>
              <li>• Hand Skeleton: {detectedGesture !== "None" ? 'Rendering' : 'Searching...'}</li>
              <li>• Iris Tracking: Active</li>
              <li>• Voice Engine: {voiceEnabled ? 'Online' : 'Muted'}</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Gesture Guide Modal */}
      {showGestureGuide && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }} onClick={() => setShowGestureGuide(false)}>
          <div className="glass" style={{ padding: '30px', maxWidth: '600px', width: '90%', maxHeight: '80vh', overflow: 'auto' }} onClick={(e) => e.stopPropagation()}>
            <h2 style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Hand size={24} color="var(--primary)" />
              Available Hand Gestures
            </h2>
            <div style={{ display: 'grid', gap: '15px' }}>
              {[
                { name: 'Thumb_Up', emoji: '👍', action: 'Captures a snapshot' },
                { name: 'Thumbs_Down', emoji: '👎', action: 'Thumbs down feedback' },
                { name: 'Victory / Two', emoji: '✌️', action: 'Peace sign / Number 2' },
                { name: 'High_Five', emoji: '🖐️', action: 'High five gesture' },
                { name: 'Fist', emoji: '✊', action: 'Power fist' },
                { name: 'One', emoji: '☝️', action: 'Number one' },
                { name: 'Three', emoji: '3️⃣', action: 'Number three' },
                { name: 'Four', emoji: '4️⃣', action: 'Number four' },
                { name: 'Rock_And_Roll', emoji: '🤘', action: 'Rock and roll sign' },
                { name: 'Call_Me', emoji: '🤙', action: 'Call me gesture' },
                { name: 'OK_Sign', emoji: '👌', action: 'Perfect/OK sign' },
                { name: 'Gun', emoji: '🔫', action: 'Finger gun' },
                { name: 'Heart', emoji: '💖', action: 'Finger heart' },
                { name: 'Spiderman', emoji: '🕷️', action: 'Web slinger' },
                { name: 'ILoveYou', emoji: '🤟', action: 'I love you sign' }
              ].map(gesture => (
                <div key={gesture.name} style={{ display: 'flex', alignItems: 'center', gap: '15px', padding: '15px', background: 'var(--glass)', borderRadius: '12px', border: detectedGesture === gesture.name ? '2px solid var(--primary)' : '2px solid transparent' }}>
                  <div style={{ fontSize: '2rem' }}>{gesture.emoji}</div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, marginBottom: '5px' }}>{gesture.name.replace('_', ' ')}</div>
                    <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{gesture.action}</div>
                  </div>
                  {detectedGesture === gesture.name && (
                    <div style={{ color: 'var(--primary)', fontSize: '0.8rem', fontWeight: 600 }}>ACTIVE</div>
                  )}
                </div>
              ))}
            </div>
            <button className="btn-primary" style={{ marginTop: '20px', width: '100%' }} onClick={() => setShowGestureGuide(false)}>
              Close Guide
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Detector;
