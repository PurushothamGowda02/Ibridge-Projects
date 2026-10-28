#!/usr/bin/env python3
"""
Test script to verify all models are working correctly.
"""

import os
import sys
import numpy as np
from PIL import Image

# Add app directory to path
sys.path.append('app')
from inference import ModelInference

def test_models():
    """Test all models with a sample image."""
    print("🧪 Testing Plant Disease Detection Models")
    print("=" * 50)
    
    # Initialize inference
    try:
        print("📁 Initializing ModelInference...")
        inference = ModelInference(model_dir='models')
        print("✅ ModelInference initialized successfully!")
    except Exception as e:
        print(f"❌ Failed to initialize ModelInference: {e}")
        return False
    
    # Find a test image
    test_image_path = None
    for class_dir in ['HEALTHY_LEAF', 'FROG_EYE_LEAF_SPOT', 'POWDERY_MILDEW', 'TOBACCO_MOSAIC_VIRUS']:
        class_path = os.path.join('data', class_dir)
        if os.path.exists(class_path):
            image_files = [f for f in os.listdir(class_path) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            if image_files:
                test_image_path = os.path.join(class_path, image_files[0])
                break
    
    if not test_image_path:
        print("❌ No test images found!")
        return False
    
    print(f"🖼️  Using test image: {test_image_path}")
    
    # Load test image
    try:
        image = Image.open(test_image_path)
        print(f"✅ Image loaded successfully! Size: {image.size}")
    except Exception as e:
        print(f"❌ Failed to load image: {e}")
        return False
    
    # Test each model
    models_to_test = [
        ('Random Forest', 'rf'),
        ('SVM', 'svm'),
        ('CNN', 'cnn'),
        ('MobileNet', 'mobilenet')
    ]
    
    results = {}
    
    for model_name, model_type in models_to_test:
        print(f"\n🤖 Testing {model_name}...")
        try:
            result = inference.predict(image, model_type=model_type)
            results[model_name] = result
            
            print(f"✅ {model_name} prediction successful!")
            print(f"   Predicted: {result['predicted_class']}")
            print(f"   Confidence: {result['confidence']:.4f}")
            
        except Exception as e:
            print(f"❌ {model_name} failed: {e}")
            results[model_name] = None
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 RESULTS SUMMARY")
    print("=" * 50)
    
    successful_models = 0
    for model_name, result in results.items():
        if result:
            successful_models += 1
            print(f"✅ {model_name}: {result['predicted_class']} ({result['confidence']:.4f})")
        else:
            print(f"❌ {model_name}: FAILED")
    
    print(f"\n🎯 {successful_models}/{len(models_to_test)} models working correctly")
    
    if successful_models == len(models_to_test):
        print("🎉 All models are working perfectly!")
        return True
    elif successful_models > 0:
        print("⚠️  Some models are working, but there are issues with others.")
        return True
    else:
        print("💥 No models are working!")
        return False

if __name__ == "__main__":
    success = test_models()
    if success:
        print("\n🚀 You can now use the Streamlit app with confidence!")
        print("   Run: streamlit run app/streamlit_app.py")
    else:
        print("\n🔧 Please check the error messages above and fix the issues.")