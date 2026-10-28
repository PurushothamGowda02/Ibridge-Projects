# Tobacco Leaf Disease Detection System

A comprehensive machine learning system for detecting diseases in tobacco leaves using both traditional ML (Random Forest, SVM) and deep learning (CNN) approaches.

## Features

- **Dual Model Approach**: Compare traditional ML and CNN performance
- **Four Disease Classes**: 
  - Frog Eye Leaf Spot
  - Healthy Leaf
  - Powdery Mildew
  - Tobacco Mosaic Virus
- **Interactive Web Interface**: User-friendly Streamlit app for predictions
- **Comprehensive Metrics**: Confusion matrices, accuracy, precision, recall, F1-score
- **External Image Support**: Works with images from any source (Google, camera, etc.)

## Project Structure

```
tobacco-disease-detection/
├── data/                          # Dataset (organized by class)
│   ├── FROG_EYE_LEAF_SPOT/
│   ├── HEALTHY_LEAF/
│   ├── POWDERY_MILDEW/
│   └── TOBACCO_MOSAIC_VIRUS/
├── models/                        # Trained models
│   ├── traditional_ml/
│   │   ├── random_forest.pkl
│   │   ├── svm.pkl
│   │   └── scaler.pkl
│   └── cnn/
│       ├── cnn_model.h5
│       └── cnn_model.keras
├── training/                      # Training scripts
│   ├── train_traditional_ml.py
│   ├── train_cnn.py
│   └── utils.py
├── evaluation/                    # Evaluation results
│   ├── confusion_matrices/
│   └── metrics.json
├── app/                          # Web application
│   ├── streamlit_app.py
│   ├── inference.py
│   └── preprocessing.py
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) CUDA-enabled GPU for faster CNN training

### 2. Installation

```bash
# Clone or download the project
cd tobacco-disease-detection

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Dataset Preparation

Ensure your dataset is organized in the following structure:
```
data/
├── FROG_EYE_LEAF_SPOT/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── HEALTHY_LEAF/
├── POWDERY_MILDEW/
└── TOBACCO_MOSAIC_VIRUS/
```

Each folder should contain images of the respective disease class.

## Usage

### Training Models

#### Train Traditional ML Models (Random Forest & SVM)
```bash
python training/train_traditional_ml.py
```

This will:
- Extract handcrafted features from images
- Train Random Forest and SVM classifiers
- Generate confusion matrices
- Save models to `models/traditional_ml/`

#### Train CNN Model
```bash
python training/train_cnn.py
```

This will:
- Train a deep CNN with data augmentation
- Generate training history plots
- Save model to `models/cnn/`

Training time: ~30-60 minutes depending on dataset size and hardware.

### Running the Web Application

```bash
streamlit run app/streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Web Interface

1. **Upload Image**: Click "Browse files" and select a tobacco leaf image
2. **Select Model**: Choose between Random Forest, SVM, or CNN
3. **Predict**: Click the "Predict Disease" button
4. **View Results**: See the predicted disease class with confidence scores
5. **Explore Metrics**: Navigate to the dashboard to view model performance

## Model Details

### Traditional ML Models

**Features Extracted:**
- Color histograms (RGB and HSV)
- Texture features (GLCM: contrast, dissimilarity, homogeneity, energy, correlation)
- Shape features (Hu moments)
- Statistical features (mean, std, skewness, kurtosis)

**Random Forest:**
- 200 estimators
- Max depth: 20
- Balanced class weights

**SVM:**
- RBF kernel
- C=10
- Balanced class weights

### CNN Model

**Architecture:**
- 4 Convolutional blocks (32, 64, 128, 256 filters)
- Batch Normalization after each Conv layer
- MaxPooling after each block
- Global Average Pooling
- Dense layers: 256 → 128 → 4
- Dropout: 0.5, 0.3

**Training Configuration:**
- Optimizer: Adam (lr=0.0001)
- Loss: Categorical Crossentropy
- Data Augmentation: rotation, flip, zoom, brightness
- Early stopping with patience=10

## Performance Metrics

After training, you can find:
- Confusion matrices in `evaluation/confusion_matrices/`
- Detailed metrics in `evaluation/metrics.json`
- Training history plots (CNN) in `evaluation/`

## Troubleshooting

### Common Issues

**Issue**: Out of memory during training
- **Solution**: Reduce batch size in training scripts or use a smaller image size

**Issue**: Models not found when running web app
- **Solution**: Ensure you've run the training scripts first

**Issue**: Slow predictions
- **Solution**: Models are loaded once at startup. First prediction may be slower.

**Issue**: Poor prediction accuracy on external images
- **Solution**: Ensure images are clear and well-lit. The model works best with images similar to training data.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is for educational and research purposes.

## Acknowledgments

- Dataset: Tobacco leaf disease images
- Built with TensorFlow, scikit-learn, and Streamlit
