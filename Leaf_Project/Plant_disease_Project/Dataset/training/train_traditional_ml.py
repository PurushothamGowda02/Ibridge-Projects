"""
Training script for traditional ML models (Random Forest and SVM).
"""

import os
import sys
import numpy as np
import joblib
import json
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Import utilities
from utils import (
    load_dataset, split_data, extract_features_batch, 
    encode_labels, CLASS_NAMES, RANDOM_SEED
)


def train_and_evaluate_model(model, model_name, X_train, y_train, X_test, y_test):
    """
    Train and evaluate a model.
    
    Args:
        model: Sklearn model instance
        model_name: Name of the model
        X_train, y_train: Training data
        X_test, y_test: Test data
        
    Returns:
        Trained model and metrics dictionary
    """
    print(f"\n{'='*60}")
    print(f"Training {model_name}...")
    print(f"{'='*60}")
    
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time
    
    print(f"Training completed in {training_time:.2f} seconds")
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test, y_pred, average=None, labels=range(len(CLASS_NAMES))
    )
    
    # Per-class metrics
    per_class_metrics = {}
    for i, class_name in enumerate(CLASS_NAMES):
        per_class_metrics[class_name] = {
            'precision': float(precision[i]),
            'recall': float(recall[i]),
            'f1_score': float(f1[i]),
            'support': int(support[i])
        }
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred, labels=range(len(CLASS_NAMES)))
    
    # Print results
    print(f"\n{model_name} Results:")
    print(f"Overall Accuracy: {accuracy:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=CLASS_NAMES))
    
    metrics = {
        'model_name': model_name,
        'accuracy': float(accuracy),
        'per_class_metrics': per_class_metrics,
        'confusion_matrix': cm.tolist(),
        'training_time': training_time
    }
    
    return model, metrics


def plot_confusion_matrix(cm, class_names, model_name, save_path):
    """
    Plot and save confusion matrix.
    
    Args:
        cm: Confusion matrix array
        class_names: List of class names
        model_name: Name of the model
        save_path: Path to save the plot
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names,
                cbar_kws={'label': 'Count'})
    plt.title(f'Confusion Matrix - {model_name}', fontsize=16, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Confusion matrix saved to {save_path}")


def main():
    """Main training pipeline for traditional ML models."""
    
    print("="*60)
    print("TRADITIONAL ML TRAINING PIPELINE")
    print("="*60)
    
    # Configuration
    DATA_DIR = "data"
    MODEL_DIR = "models/traditional_ml"
    EVAL_DIR = "evaluation"
    CM_DIR = os.path.join(EVAL_DIR, "confusion_matrices")
    
    # Create directories if they don't exist
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(CM_DIR, exist_ok=True)
    
    # Step 1: Load dataset
    print("\nStep 1: Loading dataset...")
    images, labels, label_to_idx = load_dataset(DATA_DIR)
    
    if len(images) == 0:
        print("Error: No images loaded. Please check the data directory.")
        sys.exit(1)
    
    # Step 2: Split data
    print("\nStep 2: Splitting data...")
    X_train_img, X_val_img, X_test_img, y_train, y_val, y_test = split_data(
        images, labels, 
        train_size=0.7, 
        val_size=0.15, 
        test_size=0.15,
        random_state=RANDOM_SEED
    )
    
    # Encode labels
    y_train_encoded = encode_labels(y_train, label_to_idx)
    y_val_encoded = encode_labels(y_val, label_to_idx)
    y_test_encoded = encode_labels(y_test, label_to_idx)
    
    # Step 3: Extract features
    print("\nStep 3: Extracting features...")
    print("Extracting training features...")
    X_train_features = extract_features_batch(X_train_img, verbose=True)
    
    print("Extracting validation features...")
    X_val_features = extract_features_batch(X_val_img, verbose=True)
    
    print("Extracting test features...")
    X_test_features = extract_features_batch(X_test_img, verbose=True)
    
    # Step 4: Scale features
    print("\nStep 4: Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_features)
    X_val_scaled = scaler.transform(X_val_features)
    X_test_scaled = scaler.transform(X_test_features)
    
    # Save scaler
    scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")
    joblib.dump(scaler, scaler_path)
    print(f"Scaler saved to {scaler_path}")
    
    # Save label mapping
    label_mapping_path = os.path.join(MODEL_DIR, "label_mapping.json")
    with open(label_mapping_path, 'w') as f:
        json.dump(label_to_idx, f, indent=2)
    print(f"Label mapping saved to {label_mapping_path}")
    
    # Step 5: Train Random Forest
    print("\nStep 5: Training Random Forest...")
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        class_weight='balanced',
        random_state=RANDOM_SEED,
        n_jobs=-1,
        verbose=1
    )
    
    rf_model, rf_metrics = train_and_evaluate_model(
        rf_model, "Random Forest", 
        X_train_scaled, y_train_encoded,
        X_test_scaled, y_test_encoded
    )
    
    # Save Random Forest model
    rf_path = os.path.join(MODEL_DIR, "random_forest.pkl")
    joblib.dump(rf_model, rf_path)
    print(f"Random Forest model saved to {rf_path}")
    
    # Plot Random Forest confusion matrix
    rf_cm_path = os.path.join(CM_DIR, "random_forest_cm.png")
    plot_confusion_matrix(
        np.array(rf_metrics['confusion_matrix']),
        CLASS_NAMES,
        "Random Forest",
        rf_cm_path
    )
    
    # Step 6: Train SVM
    print("\nStep 6: Training SVM...")
    svm_model = SVC(
        kernel='rbf',
        C=10,
        gamma='auto',
        class_weight='balanced',
        random_state=RANDOM_SEED,
        verbose=True,
        probability=True  # Enable probability estimates
    )
    
    svm_model, svm_metrics = train_and_evaluate_model(
        svm_model, "SVM",
        X_train_scaled, y_train_encoded,
        X_test_scaled, y_test_encoded
    )
    
    # Save SVM model
    svm_path = os.path.join(MODEL_DIR, "svm.pkl")
    joblib.dump(svm_model, svm_path)
    print(f"SVM model saved to {svm_path}")
    
    # Plot SVM confusion matrix
    svm_cm_path = os.path.join(CM_DIR, "svm_cm.png")
    plot_confusion_matrix(
        np.array(svm_metrics['confusion_matrix']),
        CLASS_NAMES,
        "SVM",
        svm_cm_path
    )
    
    # Step 7: Save combined metrics
    print("\nStep 7: Saving metrics...")
    combined_metrics = {
        'random_forest': rf_metrics,
        'svm': svm_metrics,
        'dataset_info': {
            'total_samples': len(images),
            'train_samples': len(X_train_img),
            'val_samples': len(X_val_img),
            'test_samples': len(X_test_img),
            'num_classes': len(CLASS_NAMES),
            'class_names': CLASS_NAMES,
            'feature_vector_size': X_train_features.shape[1]
        }
    }
    
    metrics_path = os.path.join(EVAL_DIR, "traditional_ml_metrics.json")
    with open(metrics_path, 'w') as f:
        json.dump(combined_metrics, f, indent=2)
    print(f"Metrics saved to {metrics_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"\nRandom Forest Accuracy: {rf_metrics['accuracy']:.4f}")
    print(f"SVM Accuracy: {svm_metrics['accuracy']:.4f}")
    print(f"\nModels saved in: {MODEL_DIR}")
    print(f"Confusion matrices saved in: {CM_DIR}")
    print(f"Metrics saved in: {metrics_path}")
    print("\nYou can now use these models for inference!")


if __name__ == "__main__":
    main()
