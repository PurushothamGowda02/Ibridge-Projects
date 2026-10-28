# Design Document

## Overview

The Tobacco Leaf Disease Detection System is a machine learning application that classifies tobacco leaf diseases using both traditional ML and deep learning approaches. The system consists of three main components: training scripts for model development, trained models for inference, and a web-based user interface built with Streamlit for easy interaction.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│                    (Streamlit Web App)                       │
│  - Image Upload  - Prediction Display  - Metrics Dashboard  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Inference Engine                          │
│  - Image Preprocessing  - Model Loading  - Prediction       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────┬──────────────────────────────────────┐
│  Traditional ML      │         CNN Model                    │
│  Models              │         (TensorFlow/Keras)           │
│  (Scikit-learn)      │                                      │
└──────────────────────┴──────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Training Pipeline                         │
│  - Data Loading  - Preprocessing  - Training  - Evaluation  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Dataset Storage                           │
│  FROG_EYE_LEAF_SPOT / HEALTHY_LEAF / POWDERY_MILDEW /      │
│  TOBACCO_MOSAIC_VIRUS                                        │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
tobacco-disease-detection/
├── data/
│   ├── FROG_EYE_LEAF_SPOT/
│   ├── HEALTHY_LEAF/
│   ├── POWDERY_MILDEW/
│   └── TOBACCO_MOSAIC_VIRUS/
├── models/
│   ├── traditional_ml/
│   │   ├── random_forest.pkl
│   │   ├── svm.pkl
│   │   └── scaler.pkl
│   └── cnn/
│       ├── cnn_model.h5
│       └── cnn_model.keras
├── training/
│   ├── train_traditional_ml.py
│   ├── train_cnn.py
│   └── utils.py
├── evaluation/
│   ├── confusion_matrices/
│   │   ├── traditional_ml_cm.png
│   │   └── cnn_cm.png
│   └── metrics.json
├── app/
│   ├── streamlit_app.py
│   ├── inference.py
│   └── preprocessing.py
├── requirements.txt
└── README.md
```

## Components and Interfaces

### 1. Data Loading and Preprocessing Module

**Purpose**: Load images from disk and prepare them for training or inference

**Key Functions**:
- `load_dataset(data_dir)`: Loads all images and labels from directory structure
- `preprocess_for_traditional_ml(image)`: Extracts handcrafted features
- `preprocess_for_cnn(image)`: Resizes and normalizes images for CNN
- `augment_images(images, labels)`: Applies data augmentation

**Feature Extraction for Traditional ML**:
- Color histograms (RGB and HSV)
- Texture features (GLCM - contrast, dissimilarity, homogeneity, energy, correlation)
- Shape features (Hu moments)
- Statistical features (mean, std, skewness, kurtosis per channel)

**CNN Preprocessing**:
- Resize to 224x224 pixels
- Normalize pixel values to [0, 1]
- Apply data augmentation (rotation, flip, zoom, brightness)

### 2. Traditional ML Training Module

**Purpose**: Train classical machine learning models using extracted features

**Models**:
1. **Random Forest Classifier**
   - n_estimators: 200
   - max_depth: 20
   - min_samples_split: 5
   - class_weight: balanced

2. **Support Vector Machine (SVM)**
   - kernel: RBF
   - C: 10
   - gamma: auto
   - class_weight: balanced

**Training Pipeline**:
```python
1. Load and preprocess images
2. Extract features for all images
3. Split data (70% train, 15% val, 15% test)
4. Scale features using StandardScaler
5. Train Random Forest model
6. Train SVM model
7. Evaluate on test set
8. Generate confusion matrices
9. Save models and scaler
```

### 3. CNN Training Module

**Purpose**: Train deep learning model for end-to-end image classification

**CNN Architecture**:
```
Input Layer (224, 224, 3)
    ↓
Conv2D (32 filters, 3x3) + ReLU + BatchNorm
    ↓
MaxPooling2D (2x2)
    ↓
Conv2D (64 filters, 3x3) + ReLU + BatchNorm
    ↓
MaxPooling2D (2x2)
    ↓
Conv2D (128 filters, 3x3) + ReLU + BatchNorm
    ↓
MaxPooling2D (2x2)
    ↓
Conv2D (256 filters, 3x3) + ReLU + BatchNorm
    ↓
GlobalAveragePooling2D
    ↓
Dense (256) + ReLU + Dropout(0.5)
    ↓
Dense (128) + ReLU + Dropout(0.3)
    ↓
Dense (4) + Softmax
```

**Training Configuration**:
- Optimizer: Adam (learning_rate=0.0001)
- Loss: Categorical Crossentropy
- Metrics: Accuracy
- Batch size: 32
- Epochs: 50
- Early stopping: patience=10, monitor='val_loss'
- Learning rate reduction: factor=0.5, patience=5

**Data Augmentation**:
- Rotation: ±20 degrees
- Width/Height shift: ±10%
- Horizontal flip: True
- Zoom: ±10%
- Brightness: ±20%

### 4. Evaluation Module

**Purpose**: Assess model performance and generate visualizations

**Metrics Calculated**:
- Overall accuracy
- Per-class precision, recall, F1-score
- Confusion matrix
- Classification report

**Visualizations**:
- Confusion matrix heatmap (seaborn)
- Training/validation accuracy curves (CNN only)
- Training/validation loss curves (CNN only)
- Per-class performance bar charts

### 5. Inference Module

**Purpose**: Load trained models and make predictions on new images

**Key Functions**:
- `load_models()`: Loads all trained models into memory
- `predict_traditional_ml(image, model_type)`: Predicts using RF or SVM
- `predict_cnn(image)`: Predicts using CNN model
- `get_prediction_probabilities(image, model_type)`: Returns class probabilities

**Prediction Pipeline**:
```python
1. Receive image from user
2. Validate image format and size
3. Apply appropriate preprocessing
4. Load selected model
5. Generate prediction
6. Return class label and confidence scores
```

### 6. Web Interface (Streamlit)

**Purpose**: Provide user-friendly interface for disease detection

**Pages/Sections**:

1. **Home/Upload Page**
   - Title and description
   - File uploader widget
   - Image preview
   - Model selector (Traditional ML vs CNN)
   - Predict button

2. **Results Section**
   - Predicted disease class (large, prominent display)
   - Confidence percentage
   - Probability distribution for all classes (bar chart)
   - Uploaded image with prediction overlay

3. **Model Performance Dashboard**
   - Tab 1: Traditional ML Metrics
     - Confusion matrix visualization
     - Accuracy, precision, recall, F1-score table
     - Model comparison (RF vs SVM)
   - Tab 2: CNN Metrics
     - Confusion matrix visualization
     - Training history plots
     - Accuracy metrics table
   - Tab 3: Model Comparison
     - Side-by-side performance comparison
     - Recommendations for use cases

4. **About Section**
   - Dataset information
   - Model architectures
   - Usage instructions

**UI Design Principles**:
- Clean, modern layout with consistent color scheme
- Green/blue theme for agricultural context
- Large, readable fonts
- Responsive design for mobile compatibility
- Loading spinners for async operations
- Success/error notifications

## Data Models

### Image Data Structure
```python
{
    'image': numpy.ndarray,  # Shape: (height, width, 3)
    'label': str,            # One of 4 disease classes
    'label_encoded': int,    # 0-3 for model training
    'filename': str,         # Original filename
    'features': numpy.ndarray  # Extracted features for traditional ML
}
```

### Prediction Result Structure
```python
{
    'predicted_class': str,
    'confidence': float,
    'probabilities': {
        'FROG_EYE_LEAF_SPOT': float,
        'HEALTHY_LEAF': float,
        'POWDERY_MILDEW': float,
        'TOBACCO_MOSAIC_VIRUS': float
    },
    'model_used': str,
    'timestamp': datetime
}
```

### Metrics Structure
```python
{
    'model_type': str,
    'accuracy': float,
    'per_class_metrics': {
        'class_name': {
            'precision': float,
            'recall': float,
            'f1_score': float,
            'support': int
        }
    },
    'confusion_matrix': numpy.ndarray,
    'training_time': float
}
```

## Error Handling

### Training Phase
- **Insufficient Data**: Warn if class has fewer than 50 images
- **Memory Errors**: Implement batch processing for large datasets
- **Convergence Issues**: Log warnings and adjust hyperparameters
- **File I/O Errors**: Graceful handling with informative messages

### Inference Phase
- **Invalid Image Format**: Return error message with supported formats
- **Model Loading Failure**: Fallback to alternative model or clear error
- **Preprocessing Errors**: Handle corrupted images gracefully
- **Out of Memory**: Resize images more aggressively

### Web Interface
- **Upload Errors**: Display user-friendly message with retry option
- **Prediction Timeout**: Show loading indicator and timeout message
- **Model Not Found**: Guide user to run training scripts first
- **Network Issues**: Offline mode with cached models

## Testing Strategy

### Unit Tests
- Test feature extraction functions with sample images
- Test preprocessing pipeline with various image sizes
- Test model loading and prediction functions
- Test data augmentation transformations

### Integration Tests
- Test end-to-end training pipeline
- Test inference pipeline with saved models
- Test web interface with mock predictions

### Performance Tests
- Measure prediction latency (target: <2 seconds)
- Test with various image sizes and formats
- Memory usage profiling during training
- Concurrent user simulation for web app

### Validation Tests
- Cross-validation during training (5-fold)
- Test on held-out test set
- Test with external images from Google
- Test with edge cases (blurry, rotated, cropped images)

## Dependencies

### Core Libraries
- Python 3.8+
- TensorFlow 2.x / Keras
- scikit-learn
- NumPy
- Pandas
- OpenCV (cv2)
- Pillow (PIL)

### Visualization
- Matplotlib
- Seaborn
- Plotly (for interactive charts)

### Web Framework
- Streamlit
- streamlit-option-menu (for navigation)

### Utilities
- scikit-image (for feature extraction)
- imbalanced-learn (for handling class imbalance)
- joblib (for model serialization)

## Performance Considerations

### Training Optimization
- Use GPU acceleration for CNN training (CUDA)
- Implement data generators to avoid loading all images in memory
- Use mixed precision training for faster CNN training
- Parallel processing for feature extraction

### Inference Optimization
- Load models once at startup, not per prediction
- Cache preprocessed images temporarily
- Use model quantization for faster inference
- Implement batch prediction for multiple images

### Web App Optimization
- Lazy loading of confusion matrices
- Image compression before upload
- Session state management for model persistence
- Caching of static visualizations

## Security Considerations

- Validate uploaded file types and sizes
- Sanitize filenames to prevent path traversal
- Limit upload size (max 10MB per image)
- Rate limiting for prediction requests
- No storage of uploaded images (privacy)
