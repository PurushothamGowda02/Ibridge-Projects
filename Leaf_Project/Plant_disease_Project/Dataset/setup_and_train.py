"""
Setup and training script to get started quickly.
This script will guide you through the setup process.

Usage:
    python setup_and_train.py          # Interactive mode with prompts
    python setup_and_train.py --auto   # Automatic mode without prompts
"""

import os
import sys
import subprocess
import argparse


def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(text.center(60))
    print("="*60 + "\n")


def check_dependencies():
    """Check if required packages are installed."""
    print_header("Checking Dependencies")
    
    required_packages = [
        'tensorflow',
        'sklearn',
        'cv2',
        'streamlit',
        'numpy',
        'pandas',
        'matplotlib',
        'seaborn',
        'plotly'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            elif package == 'cv2':
                __import__('cv2')
            else:
                __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        return False
    
    print("\n✅ All dependencies are installed!")
    return True


def check_dataset():
    """Check if dataset is properly organized."""
    print_header("Checking Dataset")
    
    data_dir = "data"
    required_folders = [
        'FROG_EYE_LEAF_SPOT',
        'HEALTHY_LEAF',
        'POWDERY_MILDEW',
        'TOBACCO_MOSAIC_VIRUS'
    ]
    
    if not os.path.exists(data_dir):
        print(f"❌ Data directory '{data_dir}' not found!")
        return False
    
    all_good = True
    for folder in required_folders:
        folder_path = os.path.join(data_dir, folder)
        if os.path.exists(folder_path):
            image_count = len([f for f in os.listdir(folder_path) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
            print(f"✅ {folder}: {image_count} images")
            
            if image_count < 10:
                print(f"   ⚠️  Warning: Only {image_count} images (recommended: 50+)")
        else:
            print(f"❌ {folder}: NOT FOUND")
            all_good = False
    
    if all_good:
        print("\n✅ Dataset is properly organized!")
    else:
        print("\n❌ Dataset is incomplete. Please organize your data.")
    
    return all_good


def train_traditional_ml(auto_mode=False):
    """Train traditional ML models."""
    print_header("Training Traditional ML Models")
    
    print("This will train Random Forest and SVM models.")
    print("Estimated time: 5-10 minutes\n")
    
    if auto_mode:
        response = 'y'
        print("Auto mode: Training traditional ML models automatically...")
    else:
        response = input("Do you want to train traditional ML models? (y/n): ")
    
    if response.lower() == 'y':
        print("\nStarting training...")
        try:
            result = subprocess.run(
                [sys.executable, "training/train_traditional_ml.py"],
                check=True
            )
            print("\n✅ Traditional ML models trained successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Training failed: {e}")
            return False
    else:
        print("Skipping traditional ML training.")
        return False


def train_cnn(auto_mode=False):
    """Train CNN model."""
    print_header("Training CNN Model")
    
    print("This will train the deep learning CNN model.")
    print("Estimated time: 30-60 minutes (faster with GPU)\n")
    
    if auto_mode:
        response = 'y'
        print("Auto mode: Training CNN model automatically...")
    else:
        response = input("Do you want to train the CNN model? (y/n): ")
    
    if response.lower() == 'y':
        print("\nStarting training...")
        print("⚠️  This may take a while. Please be patient...\n")
        try:
            result = subprocess.run(
                [sys.executable, "training/train_cnn.py"],
                check=True
            )
            print("\n✅ CNN model trained successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Training failed: {e}")
            return False
    else:
        print("Skipping CNN training.")
        return False


def train_mobilenet(auto_mode=False):
    """Train MobileNetV2 model."""
    print_header("Training MobileNetV2 Model")
    
    print("This will train the MobileNetV2 model with transfer learning.")
    print("Estimated time: 20-40 minutes (faster with GPU)\n")
    
    if auto_mode:
        response = 'y'
        print("Auto mode: Training MobileNetV2 model automatically...")
    else:
        response = input("Do you want to train the MobileNetV2 model? (y/n): ")
    
    if response.lower() == 'y':
        print("\nStarting training...")
        print("⚠️  This may take a while. Please be patient...\n")
        try:
            result = subprocess.run(
                [sys.executable, "training/train_mobilenet.py"],
                check=True
            )
            print("\n✅ MobileNetV2 model trained successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Training failed: {e}")
            return False
    else:
        print("Skipping MobileNetV2 training.")
        return False


def launch_app(auto_mode=False):
    """Launch the Streamlit app."""
    print_header("Launch Web Application")
    
    print("The web application will open in your browser.")
    print("You can upload images and make predictions.\n")
    
    if auto_mode:
        print("Auto mode: Skipping app launch. You can launch it later with:")
        print("  streamlit run app/streamlit_app.py")
        return
    
    response = input("Do you want to launch the app now? (y/n): ")
    
    if response.lower() == 'y':
        print("\nLaunching Streamlit app...")
        print("Press Ctrl+C to stop the server.\n")
        try:
            subprocess.run(
                ["streamlit", "run", "app/streamlit_app.py"],
                check=True
            )
        except KeyboardInterrupt:
            print("\n\nApp stopped.")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Failed to launch app: {e}")
    else:
        print("\nYou can launch the app later with:")
        print("  streamlit run app/streamlit_app.py")


def main():
    """Main setup and training workflow."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Setup and train tobacco disease detection models',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python setup_and_train.py          # Interactive mode with prompts
  python setup_and_train.py --auto   # Automatic mode without prompts
        """
    )
    parser.add_argument(
        '--auto',
        action='store_true',
        help='Run in automatic mode without prompts (trains all models)'
    )
    args = parser.parse_args()
    
    print_header("Tobacco Leaf Disease Detection - Setup")
    
    if args.auto:
        print("🤖 Running in AUTOMATIC mode - all models will be trained without prompts\n")
    else:
        print("Welcome! This script will help you set up and train the models.\n")
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Please install dependencies first and run this script again.")
        return
    
    # Step 2: Check dataset
    if not check_dataset():
        print("\n❌ Please organize your dataset first and run this script again.")
        print("\nDataset should be organized as:")
        print("  data/")
        print("    ├── FROG_EYE_LEAF_SPOT/")
        print("    ├── HEALTHY_LEAF/")
        print("    ├── POWDERY_MILDEW/")
        print("    └── TOBACCO_MOSAIC_VIRUS/")
        return
    
    # Step 3: Train models
    print("\n" + "="*60)
    print("Ready to train models!")
    print("="*60)
    
    trad_ml_trained = train_traditional_ml(auto_mode=args.auto)
    cnn_trained = train_cnn(auto_mode=args.auto)
    mobilenet_trained = train_mobilenet(auto_mode=args.auto)
    
    # Step 4: Summary
    print_header("Setup Complete!")
    
    if trad_ml_trained or cnn_trained or mobilenet_trained:
        print("✅ Models have been trained!")
        print("\nTrained models:")
        if trad_ml_trained:
            print("  - Random Forest")
            print("  - SVM")
        if cnn_trained:
            print("  - CNN")
        if mobilenet_trained:
            print("  - MobileNetV2")
        
        # Step 5: Launch app
        launch_app(auto_mode=args.auto)
    else:
        print("⚠️  No models were trained.")
        print("\nYou can train models later by running:")
        print("  python training/train_traditional_ml.py")
        print("  python training/train_cnn.py")
        print("  python training/train_mobilenet.py")
    
    print("\n" + "="*60)
    print("Thank you for using Tobacco Leaf Disease Detection!")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        main()` `
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        sys.exit(0)
