# Quick Start Guide

Get up and running with the Tobacco Leaf Disease Detection System in minutes!

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Verify Dataset

Make sure your dataset is organized like this:
```
data/
├── FROG_EYE_LEAF_SPOT/
├── HEALTHY_LEAF/
├── POWDERY_MILDEW/
└── TOBACCO_MOSAIC_VIRUS/
```

### 3. Train Models

#### Train Traditional ML Models (5-10 minutes)
```bash
cd training
python train_traditional_ml.py
```

This will train Random Forest and SVM models and save them to `models/traditional_ml/`.

#### Train CNN Model (30-60 minutes)
```bash
cd training
python train_cnn.py
```

This will train the deep learning model and save it to `models/cnn/`.

**Note**: CNN training is faster with a GPU. On CPU, it may take longer.

### 4. Run the Web App

```bash
cd app
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 📱 Using the App

1. **Upload Image**: Click "Browse files" and select a tobacco leaf image
2. **Select Model**: Choose CNN, Random Forest, or SVM
3. **Predict**: Click "Predict Disease" button
4. **View Results**: See the predicted disease with confidence scores

## 🎯 Testing with Sample Images

You can test the system with:
- Images from your training dataset
- Images downloaded from Google
- Photos taken with your camera

The system handles various image formats (JPG, PNG, WEBP) and sizes.

## 📊 View Model Performance

Navigate to the "Metrics" page in the app to see:
- Confusion matrices for all models
- Accuracy, precision, recall, F1-scores
- Training history plots (CNN)
- Model comparison

## 🔧 Troubleshooting

### Models not found
- Make sure you've run both training scripts
- Check that models are saved in `models/traditional_ml/` and `models/cnn/`

### Out of memory during training
- Reduce batch size in `train_cnn.py` (default is 32)
- Close other applications
- Use a machine with more RAM

### Slow predictions
- First prediction loads the models (may take a few seconds)
- Subsequent predictions are faster
- CNN is slower than traditional ML models

### Poor accuracy on external images
- Ensure images are clear and well-lit
- The leaf should fill most of the frame
- Try different models to compare results

## 💡 Tips for Best Results

1. **Image Quality**: Use high-resolution, well-lit images
2. **Framing**: Ensure the leaf fills most of the image
3. **Background**: Plain backgrounds work best
4. **Model Selection**: 
   - CNN: Best overall accuracy
   - Random Forest: Fast and reliable
   - SVM: Good for resource-constrained environments

## 📚 Next Steps

- Explore the metrics dashboard to understand model performance
- Try different models on the same image to compare results
- Read the full README.md for detailed information
- Check the About page in the app for more details

## 🆘 Need Help?

- Check the full README.md for detailed documentation
- Review the code comments in training scripts
- Ensure all dependencies are installed correctly

Happy detecting! 🌿
