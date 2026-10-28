# Requirements Document

## Introduction

This document outlines the requirements for a Tobacco Leaf Disease Detection System that uses machine learning to identify diseases in tobacco leaves. The system will implement both traditional machine learning and deep learning (CNN) approaches, provide comprehensive model evaluation metrics, and offer a user-friendly web interface for disease prediction from uploaded images.

## Glossary

- **System**: The Tobacco Leaf Disease Detection System
- **Traditional ML Model**: Machine learning models using handcrafted features (e.g., SVM, Random Forest)
- **CNN Model**: Convolutional Neural Network for deep learning-based image classification
- **User**: A person who uploads tobacco leaf images for disease detection
- **Disease Classes**: The four categories - FROG_EYE_LEAF_SPOT, HEALTHY_LEAF, POWDERY_MILDEW, TOBACCO_MOSAIC_VIRUS
- **Training Script**: Python code that trains and evaluates the models
- **Web Interface**: The user-facing application for image upload and prediction
- **Confusion Matrix**: A visualization showing model prediction accuracy across classes
- **Image Preprocessing**: Transformation of raw images into model-ready format

## Requirements

### Requirement 1

**User Story:** As a researcher, I want to train both traditional ML and CNN models on the tobacco leaf dataset, so that I can compare their performance and choose the best approach.

#### Acceptance Criteria

1. WHEN the training script is executed, THE System SHALL load images from all four disease class folders (FROG_EYE_LEAF_SPOT, HEALTHY_LEAF, POWDERY_MILDEW, TOBACCO_MOSAIC_VIRUS)
2. WHEN preprocessing images for traditional ML, THE System SHALL extract handcrafted features including color histograms, texture features, and shape descriptors
3. WHEN training traditional ML models, THE System SHALL train at least two algorithms (Random Forest and Support Vector Machine)
4. WHEN training the CNN model, THE System SHALL use a deep learning architecture with convolutional layers, pooling layers, and fully connected layers
5. WHEN training completes, THE System SHALL save all trained models to disk in a standardized format

### Requirement 2

**User Story:** As a data scientist, I want comprehensive evaluation metrics and visualizations, so that I can assess model performance and identify areas for improvement.

#### Acceptance Criteria

1. WHEN model evaluation is performed, THE System SHALL calculate accuracy, precision, recall, and F1-score for each disease class
2. WHEN evaluation completes, THE System SHALL generate confusion matrices for both traditional ML and CNN models
3. WHEN generating visualizations, THE System SHALL save confusion matrix plots as high-quality image files
4. WHEN displaying metrics, THE System SHALL show per-class performance and overall model accuracy
5. WHEN training history is available, THE System SHALL plot training and validation accuracy curves for the CNN model

### Requirement 3

**User Story:** As a user, I want to upload tobacco leaf images through a web interface, so that I can quickly identify diseases without technical knowledge.

#### Acceptance Criteria

1. WHEN the web interface loads, THE System SHALL display a clean, intuitive upload interface with clear instructions
2. WHEN a user uploads an image file, THE System SHALL accept common image formats (JPG, JPEG, PNG, WEBP)
3. WHEN an image is uploaded, THE System SHALL display a preview of the uploaded image
4. WHEN prediction is requested, THE System SHALL process the image and return results within 5 seconds
5. WHEN displaying results, THE System SHALL show the predicted disease class with confidence percentage

### Requirement 4

**User Story:** As a user, I want to see model performance metrics in the web interface, so that I can understand how reliable the predictions are.

#### Acceptance Criteria

1. WHEN the web interface loads, THE System SHALL display confusion matrices for both model types
2. WHEN viewing confusion matrices, THE System SHALL present them as interactive or high-quality static visualizations
3. WHEN model metrics are displayed, THE System SHALL show accuracy scores for each model type
4. WHEN comparing models, THE System SHALL clearly indicate which model is currently being used for predictions
5. WHERE the user requests model information, THE System SHALL provide details about training data size and model architecture

### Requirement 5

**User Story:** As a user, I want accurate disease predictions from images sourced anywhere (including Google), so that I can use the system with diverse image sources.

#### Acceptance Criteria

1. WHEN an image is uploaded, THE System SHALL normalize and resize the image to match training data specifications
2. WHEN preprocessing external images, THE System SHALL handle various image qualities, resolutions, and aspect ratios
3. WHEN making predictions, THE System SHALL apply the same preprocessing pipeline used during training
4. WHEN the image quality is poor, THE System SHALL still attempt prediction and indicate confidence level
5. WHEN prediction completes, THE System SHALL return the most likely disease class with probability scores for all classes

### Requirement 6

**User Story:** As a developer, I want well-organized training scripts with proper data splitting, so that I can ensure reproducible and unbiased model evaluation.

#### Acceptance Criteria

1. WHEN the training script runs, THE System SHALL split data into training (70%), validation (15%), and test (15%) sets
2. WHEN splitting data, THE System SHALL use stratified sampling to maintain class distribution
3. WHEN training begins, THE System SHALL set random seeds for reproducibility
4. WHEN data augmentation is applied, THE System SHALL use techniques like rotation, flipping, and brightness adjustment
5. WHEN training completes, THE System SHALL evaluate models on the held-out test set and report final metrics

### Requirement 7

**User Story:** As a user, I want a responsive and visually appealing interface, so that I can have a pleasant experience using the system.

#### Acceptance Criteria

1. WHEN the interface loads, THE System SHALL display a modern, professional design with consistent styling
2. WHEN viewing on different devices, THE System SHALL adapt the layout for mobile, tablet, and desktop screens
3. WHEN uploading images, THE System SHALL provide visual feedback (loading indicators, progress bars)
4. WHEN results are displayed, THE System SHALL use color coding and icons to make information easily scannable
5. WHEN errors occur, THE System SHALL display user-friendly error messages with suggested actions
