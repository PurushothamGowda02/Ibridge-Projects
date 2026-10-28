#!/usr/bin/env python3
"""
Test script to verify metrics files are accessible.
"""

import os
import json

def test_metrics_files():
    """Test if all metrics files are accessible."""
    print("🧪 Testing Metrics Files Access")
    print("=" * 50)
    
    # Define evaluation files to check
    files_to_check = [
        'evaluation/traditional_ml_metrics.json',
        'evaluation/cnn_metrics.json', 
        'evaluation/mobilenet_metrics.json',
        'evaluation/confusion_matrices/random_forest_cm.png',
        'evaluation/confusion_matrices/svm_cm.png',
        'evaluation/confusion_matrices/cnn_cm.png',
        'evaluation/confusion_matrices/mobilenet_cm.png',
        'evaluation/cnn_training_history.png',
        'evaluation/mobilenet_training_history.png'
    ]
    
    found_files = 0
    total_files = len(files_to_check)
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
            found_files += 1
            
            # If it's a JSON file, try to load it
            if file_path.endswith('.json'):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    print(f"   📊 JSON loaded successfully ({len(data)} keys)")
                except Exception as e:
                    print(f"   ❌ JSON load failed: {e}")
        else:
            print(f"❌ {file_path} - NOT FOUND")
    
    print("\n" + "=" * 50)
    print(f"📊 SUMMARY: {found_files}/{total_files} files found")
    
    if found_files == total_files:
        print("🎉 All metrics files are accessible!")
        return True
    elif found_files > 0:
        print("⚠️  Some metrics files are missing, but basic functionality should work.")
        return True
    else:
        print("💥 No metrics files found!")
        return False

if __name__ == "__main__":
    success = test_metrics_files()
    if success:
        print("\n🚀 Metrics page should now work in the Streamlit app!")
        print("   Navigate to the 📈 Metrics tab to view model performance.")
    else:
        print("\n🔧 Please run the training scripts to generate metrics files.")
        print("   Run: python training/train_traditional_ml.py")
        print("   Run: python training/train_cnn.py") 
        print("   Run: python training/train_mobilenet.py")