# 🌿 Data Augmentation Guide for Plant Disease Detection

This guide provides two data augmentation scripts to enhance your plant disease detection dataset.

## 📁 Files Created

1. **`simple_augmentation.py`** - Uses only OpenCV and NumPy (already installed)
2. **`data_augmentation.py`** - Advanced version using Albumentations library
3. **`augmentation_requirements.txt`** - Additional dependencies for advanced version

## 🚀 Quick Start (Simple Version)

### Run with Default Settings
```bash
python simple_augmentation.py
```

This will:
- ✅ Generate 15 augmentations per original image
- ✅ Balance classes automatically
- ✅ Create preview examples
- ✅ Save results in `data_augmented/` folder

### Generate Preview Only
```bash
python simple_augmentation.py --preview "data/HEALTHY_LEAF/healthy-1.jpg"
```

### Custom Settings
```bash
python simple_augmentation.py \
    --input_dir "data" \
    --output_dir "my_augmented_data" \
    --augmentations_per_image 20 \
    --balance_classes \
    --target_size 224 224
```

## 🔧 Advanced Version (Requires Additional Libraries)

### Install Dependencies
```bash
pip install -r augmentation_requirements.txt
```

### Run Advanced Augmentation
```bash
python data_augmentation.py
```

## 📊 Augmentation Types Available

### Simple Version (OpenCV-based)
- **Rotation**: Random rotation (-30° to +30°)
- **Flipping**: Horizontal and vertical flips
- **Brightness**: Brightness adjustment (0.7x to 1.3x)
- **Contrast**: Contrast adjustment (0.8x to 1.2x)
- **Noise**: Gaussian noise addition
- **Blur**: Gaussian blur with different kernel sizes
- **Zoom**: Zoom in/out effect
- **Shift**: Translate image position
- **Combined**: Multiple augmentations applied together

### Advanced Version (Albumentations-based)
- **Geometric**: Rotation, scaling, perspective, elastic transforms
- **Color**: HSV adjustments, color jitter, gamma correction
- **Noise**: Gaussian noise, motion blur, optical distortion
- **Advanced**: Grid distortion, CLAHE, channel shuffle

## 📈 Expected Results

### Before Augmentation
```
Original class distribution:
   FROG_EYE_LEAF_SPOT: 150 images
   HEALTHY_LEAF: 120 images
   POWDERY_MILDEW: 80 images
   TOBACCO_MOSAIC_VIRUS: 60 images
```

### After Augmentation (Balanced)
```
Final dataset statistics:
   FROG_EYE_LEAF_SPOT: 2250 images
   HEALTHY_LEAF: 2250 images
   POWDERY_MILDEW: 2250 images
   TOBACCO_MOSAIC_VIRUS: 2250 images
```

## 🎯 Benefits of Data Augmentation

1. **Increased Dataset Size**: 10-20x more training data
2. **Class Balance**: Equal representation of all disease types
3. **Better Generalization**: Models perform better on new images
4. **Reduced Overfitting**: More diverse training examples
5. **Improved Accuracy**: Typically 5-15% accuracy improvement

## 📱 Integration with Your Project

### Update Training Scripts
After augmentation, update your training scripts to use the new dataset:

```python
# In your training scripts, change:
data_dir = "data"  # Original dataset

# To:
data_dir = "data_augmented"  # Augmented dataset
```

### Retrain Models
```bash
# Retrain with augmented data
python training/train_traditional_ml.py
python training/train_cnn.py
python training/train_mobilenet.py
```

## 🔍 Quality Check

### Preview Generated Images
Check the `augmentation_preview/` folder to see examples of each augmentation type applied to a sample image.

### Verify Class Balance
The script will print statistics showing the final number of images per class.

### Manual Inspection
Randomly check some augmented images to ensure they look realistic and maintain disease characteristics.

## ⚙️ Customization Options

### Adjust Augmentation Intensity
Edit the augmentation parameters in the script:

```python
# For more aggressive augmentations
angle = random.uniform(-45, 45)  # Increase rotation range
factor = random.uniform(0.5, 1.5)  # Increase brightness range

# For more conservative augmentations
angle = random.uniform(-15, 15)  # Decrease rotation range
factor = random.uniform(0.9, 1.1)  # Decrease brightness range
```

### Add Custom Augmentations
You can add your own augmentation functions:

```python
def custom_augmentation(self, image):
    # Your custom augmentation logic here
    return modified_image
```

## 🚨 Important Notes

1. **Backup Original Data**: Always keep your original dataset safe
2. **Storage Space**: Augmented datasets can be 10-20x larger
3. **Training Time**: More data means longer training times
4. **Quality Control**: Verify augmented images look realistic
5. **Class Characteristics**: Ensure disease features are preserved

## 🎉 Next Steps

1. **Run Augmentation**: Choose simple or advanced version
2. **Check Results**: Verify output in `data_augmented/` folder
3. **Retrain Models**: Use augmented data for training
4. **Compare Performance**: Test accuracy improvement
5. **Fine-tune**: Adjust augmentation parameters if needed

Happy augmenting! 🌿🔬