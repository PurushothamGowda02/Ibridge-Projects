"""Main pipeline for car insurance premium prediction."""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.data.preprocess import preprocess_data
from src.models.train import train_all_models
from src.models.evaluate import evaluate_all_models
from src.utils.config_loader import load_config

def run_pipeline():
    """Run the complete ML pipeline."""
    print("="*60)
    print("CAR INSURANCE PREMIUM PREDICTION PIPELINE")
    print("="*60)
    
    # Load configuration
    config = load_config()
    
    # Step 1: Preprocess data
    print("\n[1/3] Preprocessing data...")
    preprocess_data(config)
    
    # Step 2: Train models
    print("\n[2/3] Training models...")
    train_all_models(config)
    
    # Step 3: Evaluate models
    print("\n[3/3] Evaluating models...")
    evaluate_all_models(config)
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext steps:")
    print("  - Check reports/model_comparison.csv for detailed results")
    print("  - Run 'streamlit run app.py' to use the web interface")
    print("  - Use src/models/predict.py to make predictions")

if __name__ == "__main__":
    run_pipeline()
