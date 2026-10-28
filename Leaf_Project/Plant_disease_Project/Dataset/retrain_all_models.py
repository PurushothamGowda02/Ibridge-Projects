"""
Automated script to retrain all models (Traditional ML, CNN, and MobileNetV2).
This script runs all training scripts sequentially without user prompts.
"""

import subprocess
import sys
import time

def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70 + "\n")

def run_training(script_name, model_name):
    """Run a training script and handle errors."""
    print_header(f"Training {model_name}")
    print(f"Running: python {script_name}")
    print(f"Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            check=True,
            capture_output=False
        )
        
        elapsed_time = time.time() - start_time
        print(f"\n✅ {model_name} training completed successfully!")
        print(f"Time taken: {elapsed_time/60:.2f} minutes")
        return True
        
    except subprocess.CalledProcessError as e:
        elapsed_time = time.time() - start_time
        print(f"\n❌ {model_name} training failed!")
        print(f"Error code: {e.returncode}")
        print(f"Time taken: {elapsed_time/60:.2f} minutes")
        return False
    except Exception as e:
        elapsed_time = time.time() - start_time
        print(f"\n❌ {model_name} training failed with exception!")
        print(f"Error: {str(e)}")
        print(f"Time taken: {elapsed_time/60:.2f} minutes")
        return False

def main():
    """Main function to retrain all models."""
    print_header("AUTOMATED MODEL RETRAINING")
    print("This script will retrain all three models:")
    print("  1. Traditional ML (Random Forest & SVM)")
    print("  2. CNN (Convolutional Neural Network)")
    print("  3. MobileNetV2 (Transfer Learning)")
    print("\nThis may take 30-90 minutes depending on your hardware.")
    print("GPU acceleration will significantly speed up deep learning models.\n")
    
    overall_start = time.time()
    results = {}
    
    # Train Traditional ML
    results['Traditional ML'] = run_training(
        "training/train_traditional_ml.py",
        "Traditional ML (Random Forest & SVM)"
    )
    
    # Train CNN
    results['CNN'] = run_training(
        "training/train_cnn.py",
        "CNN Model"
    )
    
    # Train MobileNetV2
    results['MobileNetV2'] = run_training(
        "training/train_mobilenet.py",
        "MobileNetV2 Model"
    )
    
    # Print summary
    overall_time = time.time() - overall_start
    
    print_header("TRAINING SUMMARY")
    print(f"Total time: {overall_time/60:.2f} minutes ({overall_time/3600:.2f} hours)\n")
    
    print("Results:")
    for model_name, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {model_name}: {status}")
    
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    
    print(f"\nSuccessfully trained: {successful}/{total} models")
    
    if successful == total:
        print("\n🎉 All models trained successfully!")
        print("\nYou can now:")
        print("  - View metrics: streamlit run app/streamlit_app.py")
        print("  - Make predictions using the web interface")
    elif successful > 0:
        print("\n⚠️  Some models trained successfully, but others failed.")
        print("Check the output above for error details.")
    else:
        print("\n❌ All models failed to train.")
        print("Please check the error messages above.")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user.")
        sys.exit(1)
