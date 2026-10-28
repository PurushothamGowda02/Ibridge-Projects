"""
Test script to verify training utilities work correctly.
"""

import os
import sys
import numpy as np

# Import utilities
from utils import (
    load_dataset, split_data, extract_features_traditional_ml,
    preprocess_for_cnn, augment_image, encode_labels, CLASS_NAMES
)


def test_data_loading():
    """Test data loading functionality."""
    print("\n" + "="*60)
    print("TEST 1: Data Loading")
    print("="*60)
    
    data_dir = "../data"
    
    try:
        images, labels, label_to_idx = load_dataset(data_dir, max_images_per_class=10)
        
        assert len(images) > 0, "No images loaded"
        assert len(images) == len(labels), "Mismatch between images and labels"
        assert images[0].shape == (224, 224, 3), f"Unexpected image shape: {images[0].shape}"
        
        print("✅ Data loading test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Data loading test FAILED: {e}")
        return False


def test_data_splitting():
    """Test data splitting functionality."""
    print("\n" + "="*60)
    print("TEST 2: Data Splitting")
    print("="*60)
    
    try:
        # Create dummy data
        images = np.random.rand(100, 224, 224, 3)
        labels = np.array([CLASS_NAMES[i % 4] for i in range(100)])
        
        X_train, X_val, X_test, y_train, y_val, y_test = split_data(
            images, labels,
            train_size=0.7,
            val_size=0.15,
            test_size=0.15
        )
        
        total = len(X_train) + len(X_val) + len(X_test)
        assert total == 100, f"Data split error: {total} != 100"
        assert len(X_train) == len(y_train), "Train set mismatch"
        assert len(X_val) == len(y_val), "Val set mismatch"
        assert len(X_test) == len(y_test), "Test set mismatch"
        
        print("✅ Data splitting test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Data splitting test FAILED: {e}")
        return False


def test_feature_extraction():
    """Test feature extraction for traditional ML."""
    print("\n" + "="*60)
    print("TEST 3: Feature Extraction")
    print("="*60)
    
    try:
        # Create dummy image
        image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        features = extract_features_traditional_ml(image)
        
        assert len(features) > 0, "No features extracted"
        assert isinstance(features, np.ndarray), "Features not numpy array"
        
        print(f"Feature vector size: {len(features)}")
        print("✅ Feature extraction test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Feature extraction test FAILED: {e}")
        return False


def test_cnn_preprocessing():
    """Test CNN preprocessing."""
    print("\n" + "="*60)
    print("TEST 4: CNN Preprocessing")
    print("="*60)
    
    try:
        # Create dummy images
        images = np.random.randint(0, 255, (10, 224, 224, 3), dtype=np.uint8)
        
        processed = preprocess_for_cnn(images, normalize=True)
        
        assert processed.shape == images.shape, "Shape mismatch"
        assert processed.dtype == np.float32, "Wrong dtype"
        assert processed.max() <= 1.0, "Not normalized"
        assert processed.min() >= 0.0, "Negative values"
        
        print("✅ CNN preprocessing test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ CNN preprocessing test FAILED: {e}")
        return False


def test_augmentation():
    """Test image augmentation."""
    print("\n" + "="*60)
    print("TEST 5: Image Augmentation")
    print("="*60)
    
    try:
        # Create dummy image
        image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        
        augmented = augment_image(image)
        
        assert augmented.shape == image.shape, "Shape changed"
        assert augmented.dtype == image.dtype, "Dtype changed"
        
        print("✅ Image augmentation test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Image augmentation test FAILED: {e}")
        return False


def test_label_encoding():
    """Test label encoding."""
    print("\n" + "="*60)
    print("TEST 6: Label Encoding")
    print("="*60)
    
    try:
        labels = np.array(['HEALTHY_LEAF', 'POWDERY_MILDEW', 'HEALTHY_LEAF'])
        label_to_idx = {name: idx for idx, name in enumerate(CLASS_NAMES)}
        
        encoded = encode_labels(labels, label_to_idx)
        
        assert len(encoded) == len(labels), "Length mismatch"
        assert all(isinstance(x, (int, np.integer)) for x in encoded), "Not integers"
        
        print("✅ Label encoding test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Label encoding test FAILED: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("RUNNING UTILITY TESTS")
    print("="*60)
    
    tests = [
        test_data_loading,
        test_data_splitting,
        test_feature_extraction,
        test_cnn_preprocessing,
        test_augmentation,
        test_label_encoding
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n❌ {total - passed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
