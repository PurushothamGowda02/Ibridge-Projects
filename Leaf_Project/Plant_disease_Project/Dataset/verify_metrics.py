#!/usr/bin/env python3
"""
Verify that all metrics and evaluation files are accessible.
"""

import os
import json

def verify_metrics():
    """Verify all metrics files exist and are readable."""
    print("🔍 Verifying Metrics Files")
    print("=" * 50)
    
    # Check from app directory perspective (where Streamlit runs)
    os.chdir('app')
    
    files_to_check = [
        '../evaluation/traditional_ml_metrics.json',
        '../evaluation/cnn_metrics.json', 
        '../evaluation/mobilenet_metrics.json',
        '../evaluation/confusion_matrices/random_forest_cm.png',
        '../evaluation/confusion_matrices/svm_cm.png',
        '../evaluation/confusion_matrices/cnn_cm.png',
        '../evaluation/confusion_matrices/mobilenet_cm.png',
        '../evaluation/cnn_training_history.png',
        '../evaluation/mobilenet_training_history.png'
    ]
    
    all_good = True
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
            
            # If it's a JSON file, try to load it
            if file_path.endswith('.json'):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    print(f"   📄 JSON loaded successfully ({len(data)} keys)")
                except Exception as e:
                    print(f"   ❌ JSON load failed: {e}")
                    all_good = False
        else:
            print(f"❌ {file_path} - NOT FOUND")
            all_good = False
    
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 All metrics files are accessible!")
        print("✅ The Streamlit app should now display all metrics correctly.")
    else:
        print("⚠️  Some files are missing. Check the errors above.")
    
    return all_good

if __name__ == "__main__":
    verify_metrics()