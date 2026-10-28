"""
Inference module for making predictions with trained models.
"""

import os
import sys
import numpy as np
import cv2
import joblib
import json
from PIL import Image
import tensorflow as tf
from tensorflow import keras

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from training.utils import extract_features_traditional_ml, CLASS_NAMES


class ModelInference:
    """Class for loading models and making predictions."""
    
    def __init__(self, model_dir='models'):
        """
        Initialize inference class.
        
        Args:
            model_dir: Base directory containing model folders
        """
        # Make model_dir absolute to avoid path issues
        if not os.path.isabs(model_dir):
            # If running from app directory, go up one level
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if os.path.basename(current_dir) == 'app':
                parent_dir = os.path.dirname(current_dir)
                self.model_dir = os.path.join(parent_dir, model_dir)
            else:
                self.model_dir = os.path.abspath(model_dir)
        else:
            self.model_dir = model_dir
            
        self.traditional_ml_dir = os.path.join(self.model_dir, 'traditional_ml')
        self.cnn_dir = os.path.join(self.model_dir, 'cnn')
        self.mobilenet_dir = os.path.join(self.model_dir, 'mobilenet')
        
        # Model placeholders
        self.rf_model = None
        self.svm_model = None
        self.cnn_model = None
        self.mobilenet_model = None
        self.scaler = None
        self.label_mapping = None
        self.idx_to_label = None
        
        # Load label mapping
        self._load_label_mapping()
    
    def _load_label_mapping(self):
        """Load label mapping from file."""
        # Try traditional ML directory first
        label_path = os.path.join(self.traditional_ml_dir, 'label_mapping.json')
        
        if not os.path.exists(label_path):
            # Try MobileNet directory
            label_path = os.path.join(self.mobilenet_dir, 'label_mapping.json')
        
        if not os.path.exists(label_path):
            # Try CNN directory
            label_path = os.path.join(self.cnn_dir, 'label_mapping.json')
        
        if os.path.exists(label_path):
            with open(label_path, 'r') as f:
                self.label_mapping = json.load(f)
                self.idx_to_label = {v: k for k, v in self.label_mapping.items()}
        else:
            # Use default mapping
            self.label_mapping = {name: idx for idx, name in enumerate(CLASS_NAMES)}
            self.idx_to_label = {idx: name for idx, name in enumerate(CLASS_NAMES)}
    
    def load_random_forest(self):
        """Load Random Forest model."""
        rf_path = os.path.join(self.traditional_ml_dir, 'random_forest.pkl')
        scaler_path = os.path.join(self.traditional_ml_dir, 'scaler.pkl')
        
        if not os.path.exists(rf_path):
            raise FileNotFoundError(f"Random Forest model not found at {rf_path}")
        
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler not found at {scaler_path}")
        
        print("Loading Random Forest model...")
        self.rf_model = joblib.load(rf_path)
        self.scaler = joblib.load(scaler_path)
        print("Random Forest model loaded successfully!")
        
        return self.rf_model
    
    def load_svm(self):
        """Load SVM model."""
        svm_path = os.path.join(self.traditional_ml_dir, 'svm.pkl')
        scaler_path = os.path.join(self.traditional_ml_dir, 'scaler.pkl')
        
        if not os.path.exists(svm_path):
            raise FileNotFoundError(f"SVM model not found at {svm_path}")
        
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler not found at {scaler_path}")
        
        print("Loading SVM model...")
        self.svm_model = joblib.load(svm_path)
        self.scaler = joblib.load(scaler_path)
        print("SVM model loaded successfully!")
        
        return self.svm_model
    
    def load_cnn(self):
        """Load CNN model."""
        # Try .keras format first (recommended)
        keras_path = os.path.join(self.cnn_dir, 'cnn_model.keras')
        h5_path = os.path.join(self.cnn_dir, 'cnn_model.h5')
        
        model_path = None
        if os.path.exists(keras_path):
            model_path = keras_path
        elif os.path.exists(h5_path):
            model_path = h5_path
        else:
            raise FileNotFoundError(f"CNN model not found in {self.cnn_dir}")
        
        print(f"Loading CNN model from {model_path}...")
        self.cnn_model = keras.models.load_model(model_path)
        print("CNN model loaded successfully!")
        
        return self.cnn_model
    
    def load_mobilenet(self):
        """Load MobileNetV2 model."""
        # Try .keras format first (recommended)
        keras_path = os.path.join(self.mobilenet_dir, 'mobilenet_model.keras')
        h5_path = os.path.join(self.mobilenet_dir, 'mobilenet_model.h5')
        
        model_path = None
        if os.path.exists(keras_path):
            model_path = keras_path
        elif os.path.exists(h5_path):
            model_path = h5_path
        else:
            raise FileNotFoundError(f"MobileNetV2 model not found in {self.mobilenet_dir}")
        
        print(f"Loading MobileNetV2 model from {model_path}...")
        self.mobilenet_model = keras.models.load_model(model_path)
        print("MobileNetV2 model loaded successfully!")
        
        return self.mobilenet_model
    
    def preprocess_image(self, image, target_size=(224, 224)):
        """
        Preprocess image for prediction.
        
        Args:
            image: PIL Image or numpy array
            target_size: Target size (height, width)
            
        Returns:
            Preprocessed image as numpy array
        """
        # Convert PIL Image to numpy array if needed
        if isinstance(image, Image.Image):
            image = np.array(image)
        
        # Convert to RGB if needed
        if len(image.shape) == 2:  # Grayscale
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        elif image.shape[2] == 4:  # RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        
        # Resize
        image = cv2.resize(image, target_size)
        
        return image
    
    def predict_random_forest(self, image):
        """
        Make prediction using Random Forest model.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Dictionary with prediction results
        """
        if self.rf_model is None:
            self.load_random_forest()
        
        # Preprocess image
        img = self.preprocess_image(image)
        
        # Extract features
        features = extract_features_traditional_ml(img)
        features = features.reshape(1, -1)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.rf_model.predict(features_scaled)[0]
        probabilities = self.rf_model.predict_proba(features_scaled)[0]
        
        # Get class name
        predicted_class = self.idx_to_label[prediction]
        
        # Create probability dictionary
        prob_dict = {
            self.idx_to_label[i]: float(prob) 
            for i, prob in enumerate(probabilities)
        }
        
        return {
            'predicted_class': predicted_class,
            'confidence': float(probabilities[prediction]),
            'probabilities': prob_dict,
            'model_used': 'Random Forest'
        }
    
    def predict_svm(self, image):
        """
        Make prediction using SVM model.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Dictionary with prediction results
        """
        if self.svm_model is None:
            self.load_svm()
        
        # Preprocess image
        img = self.preprocess_image(image)
        
        # Extract features
        features = extract_features_traditional_ml(img)
        features = features.reshape(1, -1)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.svm_model.predict(features_scaled)[0]
        probabilities = self.svm_model.predict_proba(features_scaled)[0]
        
        # Get class name
        predicted_class = self.idx_to_label[prediction]
        
        # Create probability dictionary
        prob_dict = {
            self.idx_to_label[i]: float(prob)
            for i, prob in enumerate(probabilities)
        }
        
        return {
            'predicted_class': predicted_class,
            'confidence': float(probabilities[prediction]),
            'probabilities': prob_dict,
            'model_used': 'SVM'
        }
    
    def predict_cnn(self, image):
        """
        Make prediction using CNN model.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Dictionary with prediction results
        """
        if self.cnn_model is None:
            self.load_cnn()
        
        # Preprocess image
        img = self.preprocess_image(image)
        
        # Normalize
        img = img.astype('float32') / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        # Make prediction
        probabilities = self.cnn_model.predict(img, verbose=0)[0]
        prediction = np.argmax(probabilities)
        
        # Get class name
        predicted_class = self.idx_to_label[prediction]
        
        # Create probability dictionary
        prob_dict = {
            self.idx_to_label[i]: float(prob)
            for i, prob in enumerate(probabilities)
        }
        
        return {
            'predicted_class': predicted_class,
            'confidence': float(probabilities[prediction]),
            'probabilities': prob_dict,
            'model_used': 'CNN'
        }
    
    def predict_mobilenet(self, image):
        """
        Make prediction using MobileNetV2 model.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Dictionary with prediction results
        """
        if self.mobilenet_model is None:
            self.load_mobilenet()
        
        # Preprocess image
        img = self.preprocess_image(image)
        
        # Normalize for MobileNetV2 (expects values in [-1, 1])
        img = img.astype('float32') / 255.0
        img = (img * 2) - 1
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        # Make prediction
        probabilities = self.mobilenet_model.predict(img, verbose=0)[0]
        prediction = np.argmax(probabilities)
        
        # Get class name
        predicted_class = self.idx_to_label[prediction]
        
        # Create probability dictionary
        prob_dict = {
            self.idx_to_label[i]: float(prob)
            for i, prob in enumerate(probabilities)
        }
        
        return {
            'predicted_class': predicted_class,
            'confidence': float(probabilities[prediction]),
            'probabilities': prob_dict,
            'model_used': 'MobileNetV2'
        }
    
    def predict_ensemble(self, image):
        """
        Make prediction using ensemble of Random Forest, SVM, and MobileNetV2.
        Uses weighted voting based on model accuracy.
        
        Args:
            image: PIL Image or numpy array
            
        Returns:
            Dictionary with prediction results
        """
        # Get predictions from all models
        rf_result = self.predict_random_forest(image)
        svm_result = self.predict_svm(image)
        
        # Try to get MobileNet prediction, fallback if not available
        try:
            mobilenet_result = self.predict_mobilenet(image)
            use_mobilenet = True
        except:
            use_mobilenet = False
            mobilenet_result = None
        
        # Weighted ensemble based on model accuracy
        # MobileNetV2: 100%, RF: 99.17%, SVM: 97.52%
        if use_mobilenet:
            weights = {
                'mobilenet': 0.50,  # 50% weight for MobileNet (best model)
                'rf': 0.30,         # 30% weight for Random Forest
                'svm': 0.20         # 20% weight for SVM
            }
        else:
            weights = {
                'rf': 0.60,   # 60% weight for Random Forest
                'svm': 0.40   # 40% weight for SVM
            }
        
        # Weighted average of probabilities
        ensemble_probs = { }
        for class_name in rf_result['probabilities'].keys():
            rf_prob = rf_result['probabilities'][class_name]
            svm_prob = svm_result['probabilities'][class_name]
            
            if use_mobilenet:
                mobilenet_prob = mobilenet_result['probabilities'][class_name]
                ensemble_probs[class_name] = (
                    weights['mobilenet'] * mobilenet_prob +
                    weights['rf'] * rf_prob +
                    weights['svm'] * svm_prob
                )
            else:
                ensemble_probs[class_name] = (
                    weights['rf'] * rf_prob +
                    weights['svm'] * svm_prob
                )
        
        # Get the class with highest ensemble probability
        predicted_class = max(ensemble_probs, key=ensemble_probs.get)
        confidence = ensemble_probs[predicted_class]
        
        model_desc = 'Ensemble (MobileNetV2 + RF + SVM)' if use_mobilenet else 'Ensemble (RF + SVM)'
        
        return {
            'predicted_class': predicted_class,
            'confidence': float(confidence),
            'probabilities': ensemble_probs,
            'model_used': model_desc
        }
    
    def predict(self, image, model_type='mobilenet'):
        """
        Make prediction using specified model.
        
        Args:
            image: PIL Image or numpy array
            model_type: Type of model ('rf', 'svm', 'ensemble', 'cnn', or 'mobilenet')
            
        Returns:
            Dictionary with prediction results
        """
        model_type = model_type.lower()
        
        if model_type in ['rf', 'random_forest', 'randomforest']:
            return self.predict_random_forest(image)
        elif model_type == 'svm':
            return self.predict_svm(image)
        elif model_type in ['ensemble', 'traditional_ml', 'traditional']:
            return self.predict_ensemble(image)
        elif model_type == 'cnn':
            return self.predict_cnn(image)
        elif model_type in ['mobilenet', 'mobilenetv2']:
            return self.predict_mobilenet(image)
        else:
            raise ValueError(f"Unknown model type: {model_type}")


def load_image_from_path(image_path):
    """
    Load image from file path.
    
    Args:
        image_path: Path to image file
        
    Returns:
        PIL Image
    """
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        raise ValueError(f"Error loading image: {e}")


def load_image_from_bytes(image_bytes):
    """
    Load image from bytes.
    
    Args:
        image_bytes: Image data as bytes
        
    Returns:
        PIL Image
    """
    try:
        from io import BytesIO
        image = Image.open(BytesIO(image_bytes))
        return image
    except Exception as e:
        raise ValueError(f"Error loading image from bytes: {e}")


if __name__ == "__main__":
    # Test inference
    print("Testing inference module...")
    
    # Initialize inference
    inference = ModelInference()
    
    # Test with a sample image (if available)
    test_image_path = "data/HEALTHY_LEAF"
    
    if os.path.exists(test_image_path):
        # Get first image from directory
        image_files = [f for f in os.listdir(test_image_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if image_files:
            test_img_path = os.path.join(test_image_path, image_files[0])
            print(f"\nTesting with image: {test_img_path}")
            
            # Load image
            image = load_image_from_path(test_img_path)
            
            # Test CNN prediction
            try:
                result = inference.predict(image, model_type='cnn')
                print(f"\nCNN Prediction:")
                print(f"  Predicted class: {result['predicted_class']}")
                print(f"  Confidence: {result['confidence']:.4f}")
                print(f"  All probabilities:")
                for class_name, prob in result['probabilities'].items():
                    print(f"    {class_name}: {prob:.4f}")
            except Exception as e:
                print(f"CNN prediction failed: {e}")
            
            print("\nInference module test complete!")
        else:
            print("No test images found")
    else:
        print("Test data directory not found")
