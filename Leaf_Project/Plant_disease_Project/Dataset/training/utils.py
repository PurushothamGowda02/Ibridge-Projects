"""
Utility functions for data loading, preprocessing, and feature extraction.
"""

import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from skimage.feature import graycomatrix, graycoprops
from scipy.stats import skew, kurtosis
import random

# Set random seeds for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# Disease class names
CLASS_NAMES = ['FROG_EYE_LEAF_SPOT', 'HEALTHY_LEAF', 'POWDERY_MILDEW', 'TOBACCO_MOSAIC_VIRUS']


def load_dataset(data_dir, img_size=(224, 224), max_images_per_class=None):
    """
    Load images from directory structure organized by class folders.
    
    Args:
        data_dir: Path to data directory containing class folders
        img_size: Target size for images (height, width)
        max_images_per_class: Optional limit on images per class
        
    Returns:
        images: List of image arrays
        labels: List of string labels
        label_to_idx: Dictionary mapping label names to indices
    """
    images = []
    labels = []
    label_to_idx = {name: idx for idx, name in enumerate(CLASS_NAMES)}
    
    print(f"Loading dataset from {data_dir}...")
    
    for class_name in CLASS_NAMES:
        class_path = os.path.join(data_dir, class_name)
        
        if not os.path.exists(class_path):
            print(f"Warning: Class folder {class_name} not found!")
            continue
            
        image_files = [f for f in os.listdir(class_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        
        if max_images_per_class:
            image_files = image_files[:max_images_per_class]
        
        print(f"Loading {len(image_files)} images from {class_name}...")
        
        for img_file in image_files:
            img_path = os.path.join(class_path, img_file)
            
            try:
                # Read image
                img = cv2.imread(img_path)
                
                if img is None:
                    print(f"Warning: Could not read {img_path}")
                    continue
                
                # Convert BGR to RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                
                # Resize
                img = cv2.resize(img, img_size)
                
                images.append(img)
                labels.append(class_name)
                
            except Exception as e:
                print(f"Error loading {img_path}: {e}")
                continue
    
    print(f"\nTotal images loaded: {len(images)}")
    print(f"Class distribution:")
    for class_name in CLASS_NAMES:
        count = labels.count(class_name)
        print(f"  {class_name}: {count}")
    
    return np.array(images), np.array(labels), label_to_idx


def split_data(images, labels, train_size=0.7, val_size=0.15, test_size=0.15, random_state=RANDOM_SEED):
    """
    Split data into train, validation, and test sets with stratification.
    
    Args:
        images: Array of images
        labels: Array of labels
        train_size: Proportion for training set
        val_size: Proportion for validation set
        test_size: Proportion for test set
        random_state: Random seed for reproducibility
        
    Returns:
        X_train, X_val, X_test, y_train, y_val, y_test
    """
    assert abs(train_size + val_size + test_size - 1.0) < 0.001, "Sizes must sum to 1.0"
    
    # First split: separate test set
    X_temp, X_test, y_temp, y_test = train_test_split(
        images, labels, 
        test_size=test_size, 
        stratify=labels,
        random_state=random_state
    )
    
    # Second split: separate train and validation
    val_ratio = val_size / (train_size + val_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp,
        test_size=val_ratio,
        stratify=y_temp,
        random_state=random_state
    )
    
    print(f"\nData split:")
    print(f"  Training: {len(X_train)} samples")
    print(f"  Validation: {len(X_val)} samples")
    print(f"  Test: {len(X_test)} samples")
    
    return X_train, X_val, X_test, y_train, y_val, y_test


def preprocess_for_cnn(images, normalize=True):
    """
    Preprocess images for CNN model.
    
    Args:
        images: Array of images
        normalize: Whether to normalize pixel values to [0, 1]
        
    Returns:
        Preprocessed images
    """
    images = images.astype('float32')
    
    if normalize:
        images = images / 255.0
    
    return images


def extract_color_histogram(image, bins=32):
    """
    Extract color histogram features from RGB and HSV color spaces.
    
    Args:
        image: RGB image array
        bins: Number of bins for histogram
        
    Returns:
        Concatenated histogram features
    """
    # RGB histograms
    hist_r = cv2.calcHist([image], [0], None, [bins], [0, 256]).flatten()
    hist_g = cv2.calcHist([image], [1], None, [bins], [0, 256]).flatten()
    hist_b = cv2.calcHist([image], [2], None, [bins], [0, 256]).flatten()
    
    # Convert to HSV and extract histograms
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    hist_h = cv2.calcHist([hsv], [0], None, [bins], [0, 180]).flatten()
    hist_s = cv2.calcHist([hsv], [1], None, [bins], [0, 256]).flatten()
    hist_v = cv2.calcHist([hsv], [2], None, [bins], [0, 256]).flatten()
    
    # Normalize histograms
    hist_r = hist_r / (hist_r.sum() + 1e-7)
    hist_g = hist_g / (hist_g.sum() + 1e-7)
    hist_b = hist_b / (hist_b.sum() + 1e-7)
    hist_h = hist_h / (hist_h.sum() + 1e-7)
    hist_s = hist_s / (hist_s.sum() + 1e-7)
    hist_v = hist_v / (hist_v.sum() + 1e-7)
    
    return np.concatenate([hist_r, hist_g, hist_b, hist_h, hist_s, hist_v])


def extract_texture_features(image):
    """
    Extract GLCM texture features.
    
    Args:
        image: RGB image array
        
    Returns:
        Texture feature vector
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Compute GLCM
    distances = [1]
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    glcm = graycomatrix(gray, distances=distances, angles=angles, 
                        levels=256, symmetric=True, normed=True)
    
    # Extract properties
    contrast = graycoprops(glcm, 'contrast').flatten()
    dissimilarity = graycoprops(glcm, 'dissimilarity').flatten()
    homogeneity = graycoprops(glcm, 'homogeneity').flatten()
    energy = graycoprops(glcm, 'energy').flatten()
    correlation = graycoprops(glcm, 'correlation').flatten()
    
    return np.concatenate([contrast, dissimilarity, homogeneity, energy, correlation])


def extract_shape_features(image):
    """
    Extract Hu moments for shape features.
    
    Args:
        image: RGB image array
        
    Returns:
        Hu moments feature vector
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Calculate moments
    moments = cv2.moments(gray)
    
    # Calculate Hu moments
    hu_moments = cv2.HuMoments(moments).flatten()
    
    # Log transform for better scale invariance
    hu_moments = -np.sign(hu_moments) * np.log10(np.abs(hu_moments) + 1e-10)
    
    return hu_moments


def extract_statistical_features(image):
    """
    Extract statistical features (mean, std, skewness, kurtosis) per channel.
    
    Args:
        image: RGB image array
        
    Returns:
        Statistical feature vector
    """
    features = []
    
    for channel in range(3):
        channel_data = image[:, :, channel].flatten()
        
        features.append(np.mean(channel_data))
        features.append(np.std(channel_data))
        features.append(skew(channel_data))
        features.append(kurtosis(channel_data))
    
    return np.array(features)


def extract_features_traditional_ml(image):
    """
    Extract all handcrafted features for traditional ML models.
    
    Args:
        image: RGB image array
        
    Returns:
        Combined feature vector
    """
    color_hist = extract_color_histogram(image)
    texture = extract_texture_features(image)
    shape = extract_shape_features(image)
    stats = extract_statistical_features(image)
    
    return np.concatenate([color_hist, texture, shape, stats])


def extract_features_batch(images, verbose=True):
    """
    Extract features from a batch of images.
    
    Args:
        images: Array of images
        verbose: Whether to print progress
        
    Returns:
        Array of feature vectors
    """
    features = []
    
    for i, img in enumerate(images):
        if verbose and (i + 1) % 100 == 0:
            print(f"Extracting features: {i + 1}/{len(images)}")
        
        feat = extract_features_traditional_ml(img)
        features.append(feat)
    
    if verbose:
        print(f"Feature extraction complete. Feature vector size: {len(features[0])}")
    
    return np.array(features)


def augment_image(image):
    """
    Apply random augmentation to an image.
    
    Args:
        image: RGB image array
        
    Returns:
        Augmented image
    """
    img = image.copy()
    
    # Random rotation (-20 to 20 degrees)
    if random.random() > 0.5:
        angle = random.uniform(-20, 20)
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1.0)
        img = cv2.warpAffine(img, M, (w, h))
    
    # Random horizontal flip
    if random.random() > 0.5:
        img = cv2.flip(img, 1)
    
    # Random brightness adjustment (-20% to +20%)
    if random.random() > 0.5:
        brightness_factor = random.uniform(0.8, 1.2)
        img = np.clip(img * brightness_factor, 0, 255).astype(np.uint8)
    
    # Random zoom (90% to 110%)
    if random.random() > 0.5:
        zoom_factor = random.uniform(0.9, 1.1)
        h, w = img.shape[:2]
        new_h, new_w = int(h * zoom_factor), int(w * zoom_factor)
        img = cv2.resize(img, (new_w, new_h))
        
        # Crop or pad to original size
        if zoom_factor > 1:
            # Crop center
            start_h = (new_h - h) // 2
            start_w = (new_w - w) // 2
            img = img[start_h:start_h+h, start_w:start_w+w]
        else:
            # Pad
            pad_h = (h - new_h) // 2
            pad_w = (w - new_w) // 2
            img = cv2.copyMakeBorder(img, pad_h, h-new_h-pad_h, 
                                    pad_w, w-new_w-pad_w, 
                                    cv2.BORDER_REFLECT)
    
    return img


def encode_labels(labels, label_to_idx):
    """
    Encode string labels to integers.
    
    Args:
        labels: Array of string labels
        label_to_idx: Dictionary mapping labels to indices
        
    Returns:
        Array of integer labels
    """
    return np.array([label_to_idx[label] for label in labels])


def decode_labels(encoded_labels, label_to_idx):
    """
    Decode integer labels to strings.
    
    Args:
        encoded_labels: Array of integer labels
        label_to_idx: Dictionary mapping labels to indices
        
    Returns:
        Array of string labels
    """
    idx_to_label = {idx: label for label, idx in label_to_idx.items()}
    return np.array([idx_to_label[idx] for idx in encoded_labels])


if __name__ == "__main__":
    # Test the utilities
    print("Testing data loading utilities...")
    
    data_dir = "../data"
    images, labels, label_to_idx = load_dataset(data_dir, max_images_per_class=10)
    
    print(f"\nLoaded {len(images)} images")
    print(f"Image shape: {images[0].shape}")
    print(f"Label mapping: {label_to_idx}")
    
    # Test feature extraction
    print("\nTesting feature extraction...")
    features = extract_features_traditional_ml(images[0])
    print(f"Feature vector size: {len(features)}")
    
    # Test augmentation
    print("\nTesting augmentation...")
    aug_img = augment_image(images[0])
    print(f"Augmented image shape: {aug_img.shape}")
    
    print("\nAll tests passed!")
