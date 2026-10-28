# Implementation Plan

- [x] 1. Set up project structure and dependencies



  - Create directory structure for data, models, training, evaluation, and app folders
  - Create requirements.txt with all necessary dependencies (TensorFlow, scikit-learn, Streamlit, OpenCV, etc.)
  - Create README.md with project overview and setup instructions
  - _Requirements: 1.1, 6.1_

- [x] 2. Implement data loading and preprocessing utilities


  - Create utils.py with functions to load images from the four disease class folders
  - Implement stratified train/validation/test split (70/15/15) with random seed for reproducibility
  - Implement image preprocessing for CNN (resize to 224x224, normalize to [0,1])
  - Implement feature extraction for traditional ML (color histograms, GLCM texture features, Hu moments, statistical features)
  - Implement data augmentation pipeline (rotation, flip, zoom, brightness adjustment)
  - _Requirements: 1.1, 6.1, 6.2, 6.3, 6.4, 5.1, 5.2, 5.3_


- [x] 3. Implement traditional ML training script

  - [x] 3.1 Create train_traditional_ml.py with data loading and feature extraction

    - Load all images from dataset folders
    - Extract handcrafted features for all images
    - Split data into train/val/test sets with stratification
    - Apply StandardScaler to features and save scaler
    - _Requirements: 1.1, 1.2, 6.1, 6.2, 6.3_


  - [ ] 3.2 Implement Random Forest and SVM model training
    - Train Random Forest classifier with 200 estimators, max_depth=20, balanced class weights
    - Train SVM classifier with RBF kernel, C=10, balanced class weights
    - Save both trained models using joblib
    - _Requirements: 1.3, 1.5_


  - [ ] 3.3 Implement evaluation and metrics generation
    - Evaluate both models on test set
    - Calculate accuracy, precision, recall, F1-score for each class
    - Generate and save confusion matrices as PNG images
    - Save metrics to JSON file

    - Print classification reports
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 6.6_



- [ ] 4. Implement CNN training script
  - [ ] 4.1 Create train_cnn.py with CNN architecture
    - Build CNN model with 4 convolutional blocks (32, 64, 128, 256 filters)
    - Add BatchNormalization after each Conv2D layer
    - Add MaxPooling2D after each block
    - Add GlobalAveragePooling2D and Dense layers (256, 128, 4)

    - Add Dropout layers (0.5, 0.3) for regularization
    - Use softmax activation for output layer
    - _Requirements: 1.4_

  - [ ] 4.2 Implement CNN training pipeline
    - Load and preprocess images for CNN
    - Create ImageDataGenerator for data augmentation
    - Split data into train/val/test sets
    - Compile model with Adam optimizer (lr=0.0001), categorical crossentropy loss

    - Add callbacks: EarlyStopping (patience=10), ReduceLROnPlateau (factor=0.5, patience=5)
    - Train model for 50 epochs with batch size 32
    - Save trained model in both .h5 and .keras formats
    - _Requirements: 1.4, 1.5, 6.1, 6.2, 6.3, 6.4_

  - [ ] 4.3 Implement CNN evaluation and visualization
    - Evaluate CNN on test set
    - Calculate accuracy, precision, recall, F1-score for each class


    - Generate and save confusion matrix as PNG
    - Plot and save training/validation accuracy curves
    - Plot and save training/validation loss curves
    - Save metrics to JSON file
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 6.6_


- [ ] 5. Implement inference module for predictions
  - Create inference.py with model loading functions


  - Implement predict_traditional_ml() function that loads RF/SVM models and makes predictions
  - Implement predict_cnn() function that loads CNN model and makes predictions
  - Implement preprocessing functions that match training pipeline
  - Implement get_prediction_probabilities() to return confidence scores for all classes
  - Handle various image formats (JPG, JPEG, PNG, WEBP) and sizes

  - _Requirements: 3.2, 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 6. Build Streamlit web interface
  - [ ] 6.1 Create main Streamlit app structure
    - Create streamlit_app.py with page configuration and layout
    - Implement sidebar with navigation and model selector
    - Add title, description, and instructions
    - Apply custom CSS for modern, professional styling with green/blue agricultural theme
    - _Requirements: 3.1, 7.1, 7.4_


  - [ ] 6.2 Implement image upload and prediction interface
    - Add file uploader widget accepting JPG, JPEG, PNG, WEBP formats
    - Display uploaded image preview
    - Add model selection dropdown (Traditional ML - Random Forest, Traditional ML - SVM, CNN)
    - Add "Predict Disease" button
    - Show loading spinner during prediction

    - Display predicted disease class prominently with confidence percentage
    - Show probability distribution bar chart for all four classes
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 7.3, 7.4_

  - [ ] 6.3 Implement model performance dashboard
    - Create tabs for Traditional ML Metrics, CNN Metrics, and Model Comparison
    - Display confusion matrix images for both model types

    - Show accuracy, precision, recall, F1-score tables
    - Display training history plots for CNN (accuracy and loss curves)
    - Create side-by-side model comparison with recommendations
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 6.4 Add responsive design and error handling


    - Implement responsive layout for mobile, tablet, and desktop
    - Add loading indicators and progress feedback


    - Implement error handling with user-friendly messages
    - Add success notifications after predictions
    - Handle cases where models are not found with clear instructions
    - _Requirements: 7.2, 7.3, 7.5_



  - [ ] 6.5 Create About section with documentation
    - Add dataset information (4 classes, image counts)
    - Document model architectures and training details
    - Provide usage instructions and tips

    - Include information about prediction reliability
    - _Requirements: 4.5_

- [ ] 7. Create comprehensive documentation
  - Write detailed README.md with setup instructions, dataset preparation, training commands, and app usage
  - Document all functions with docstrings
  - Add inline comments for complex logic

  - Create example usage scripts
  - _Requirements: All requirements_

- [ ] 8. Testing and validation
  - [ ] 8.1 Test training scripts with sample data
    - Verify traditional ML training completes successfully
    - Verify CNN training completes successfully
    - Confirm models are saved correctly
    - Validate metrics are calculated accurately
    - _Requirements: 1.5, 2.1, 6.6_

  - [ ] 8.2 Test inference with various image sources
    - Test predictions with training dataset images
    - Test with external images downloaded from Google
    - Test with various image sizes and formats
    - Test with poor quality and rotated images
    - Verify preprocessing handles edge cases
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ] 8.3 Test web interface functionality
    - Test file upload with different formats
    - Test prediction with all three model options
    - Verify confusion matrices display correctly
    - Test responsive design on different screen sizes
    - Verify error handling works properly
    - _Requirements: 3.2, 4.1, 7.2, 7.5_
