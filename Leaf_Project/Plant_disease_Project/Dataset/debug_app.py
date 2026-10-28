#!/usr/bin/env python3
"""
Debug version of the Streamlit app to identify issues.
"""

import streamlit as st
import os
import sys
from PIL import Image

# Add app directory to path
sys.path.append('app')
from inference import ModelInference

st.set_page_config(
    page_title="Debug - Plant Disease Detection",
    page_icon="🔧",
    layout="wide"
)

st.title("🔧 Debug - Plant Disease Detection")

# Debug information
st.subheader("🔍 Debug Information")

# Check if models exist
st.write("**Model Directory Check:**")
model_dirs = ['models/cnn', 'models/mobilenet', 'models/traditional_ml']
for model_dir in model_dirs:
    if os.path.exists(model_dir):
        files = os.listdir(model_dir)
        st.success(f"✅ {model_dir}: {len(files)} files found")
        st.write(f"   Files: {', '.join(files[:3])}{'...' if len(files) > 3 else ''}")
    else:
        st.error(f"❌ {model_dir}: Not found")

st.write("---")

# Initialize inference
st.subheader("🤖 Model Initialization")
try:
    with st.spinner("Initializing models..."):
        inference = ModelInference(model_dir='models')
    st.success("✅ ModelInference initialized successfully!")
except Exception as e:
    st.error(f"❌ Failed to initialize ModelInference: {e}")
    st.stop()

st.write("---")

# Test image upload and prediction
st.subheader("📤 Test Prediction")

uploaded_file = st.file_uploader(
    "Upload a test image",
    type=['jpg', 'jpeg', 'png', 'webp']
)

if uploaded_file is not None:
    try:
        # Load image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=300)
        
        # Test each model
        models_to_test = [
            ('MobileNet', 'mobilenet'),
            ('CNN', 'cnn'),
            ('Random Forest', 'rf'),
            ('SVM', 'svm')
        ]
        
        st.write("**Testing Models:**")
        
        for model_name, model_type in models_to_test:
            try:
                with st.spinner(f"Testing {model_name}..."):
                    result = inference.predict(image, model_type=model_type)
                
                st.success(f"✅ {model_name}: {result['predicted_class']} ({result['confidence']:.2%})")
                
                # Show probabilities
                with st.expander(f"View {model_name} probabilities"):
                    for class_name, prob in result['probabilities'].items():
                        st.write(f"  {class_name}: {prob:.4f}")
                        
            except Exception as e:
                st.error(f"❌ {model_name} failed: {e}")
                st.write(f"   Error details: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Error processing image: {e}")

st.write("---")
st.info("💡 If all tests pass here, the main app should work fine. Check your browser console for any JavaScript errors.")