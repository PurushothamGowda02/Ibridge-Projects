// AR Utilities for calculating filter positions
export const getSunglassesTransform = (landmarks) => {
  if (!landmarks || landmarks.length === 0) return null;

  // Landmark IDs for eyes in MediaPipe Face Mesh
  // Left eye outer: 33, Right eye outer: 263
  // Left eye inner: 133, Right eye inner: 362
  
  const leftEye = landmarks[33];
  const rightEye = landmarks[263];
  
  const dx = rightEye.x - leftEye.x;
  const dy = rightEye.y - leftEye.y;
  
  const angle = Math.atan2(dy, dx);
  const distance = Math.sqrt(dx * dx + dy * dy);
  
  // Center point between eyes
  const centerX = (leftEye.x + rightEye.x) / 2;
  const centerY = (leftEye.y + rightEye.y) / 2;
  
  return {
    x: centerX,
    y: centerY,
    width: distance * 2.5, // Scale factor
    angle: angle
  };
};

export const detectEmotion = (blendshapes) => {
  if (!blendshapes || blendshapes.length === 0) return "Neutral 😐";
  
  const shapes = {};
  blendshapes[0].categories.forEach(c => {
    shapes[c.categoryName] = c.score;
  });

  // Debug: Log some key blendshape values
  console.log("Blendshapes:", {
    smileLeft: shapes['mouthSmileLeft'],
    smileRight: shapes['mouthSmileRight'],
    frownLeft: shapes['mouthFrownLeft'],
    frownRight: shapes['mouthFrownRight'],
    eyeWideLeft: shapes['eyeWideLeft'],
    eyeWideRight: shapes['eyeWideRight'],
    browDown: shapes['browDownLeft'],
    jawOpen: shapes['jawOpen']
  });

  // Calculate combined scores with lower thresholds
  const smileScore = (shapes['mouthSmileLeft'] || 0) + (shapes['mouthSmileRight'] || 0);
  const frownScore = (shapes['mouthFrownLeft'] || 0) + (shapes['mouthFrownRight'] || 0);
  const eyeWideScore = (shapes['eyeWideLeft'] || 0) + (shapes['eyeWideRight'] || 0);
  const browDownScore = (shapes['browDownLeft'] || 0) + (shapes['browDownRight'] || 0);
  const browInnerUpScore = shapes['browInnerUp'] || 0;
  const jawOpenScore = shapes['jawOpen'] || 0;
  const eyeBlinkScore = (shapes['eyeBlinkLeft'] || 0) + (shapes['eyeBlinkRight'] || 0);

  // Simplified emotion detection with lower thresholds
  
  // Happy emotions (check first as they're most common)
  if (smileScore > 0.15) {
    if (smileScore > 0.4 && jawOpenScore > 0.2) {
      return "Laughing 😂";
    }
    if (smileScore > 0.3) {
      return "Very Happy 😄";
    }
    if (smileScore > 0.2) {
      return "Happy 😊";
    }
    return "Smiling 🙂";
  }

  // Surprised - wide eyes
  if (eyeWideScore > 0.3) {
    if (jawOpenScore > 0.2) {
      return "Shocked 😱";
    }
    return "Surprised 😲";
  }

  // Sad emotions
  if (frownScore > 0.15) {
    if (frownScore > 0.3 && browInnerUpScore > 0.2) {
      return "Very Sad 😭";
    }
    if (frownScore > 0.2) {
      return "Sad 😢";
    }
    return "Slightly Sad 😔";
  }

  // Angry - brows down
  if (browDownScore > 0.15) {
    if (browDownScore > 0.3) {
      return "Very Angry 😡";
    }
    return "Angry 😠";
  }

  // Sleepy - eyes closing
  if (eyeBlinkScore > 0.4) {
    return "Sleepy 😴";
  }

  // Talking/Yawning - mouth open without smile or frown
  if (jawOpenScore > 0.3 && smileScore < 0.1 && frownScore < 0.1) {
    if (jawOpenScore > 0.6) {
      return "Yawning 🥱";
    }
    return "Talking 😮";
  }

  // Worried - inner brows up without smile
  if (browInnerUpScore > 0.2 && smileScore < 0.1) {
    return "Worried 😟";
  }

  // Winking - asymmetric eye blink
  const eyeBlinkDiff = Math.abs((shapes['eyeBlinkLeft'] || 0) - (shapes['eyeBlinkRight'] || 0));
  if (eyeBlinkDiff > 0.3) {
    return "Winking 😉";
  }

  // Thinking - mouth pucker
  if ((shapes['mouthPucker'] || 0) > 0.2) {
    return "Thinking 🤔";
  }

  // Disgusted - nose sneer
  if ((shapes['noseSneerLeft'] || 0) > 0.2 || (shapes['noseSneerRight'] || 0) > 0.2) {
    return "Disgusted 🤢";
  }

  return "Neutral 😐";
};
