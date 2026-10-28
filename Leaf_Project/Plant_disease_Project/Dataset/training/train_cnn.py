"""
Training script for CNN model.
"""

import os
import sys
import numpy as np
import json
import time
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Import utilities
from utils import (
    load_dataset, split_data, preprocess_for_cnn,
    encode_labels, CLASS_NAMES, RANDOM_SEED
)

# Set random seeds
tf.random.set_seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def build_cnn_model(input_shape=(224, 224, 3), num_classes=4):
    """
    Build improved CNN model architecture with data augmentation.
    
    Args:
        input_shape: Shape of input images
        num_classes: Number of output classes
        
    Returns:
        Compiled Keras model
    """
    # Data augmentation layers
    data_augmentation = keras.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
        layers.RandomTranslation(0.1, 0.1),
    ])
    
    model = models.Sequential([
        # Input layer
        layers.Input(shape=input_shape),
        
        # Data augmentation
        data_augmentation,
        
        # Block 1: 32 filters
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.2),
        
        # Block 2: 64 filters
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.2),
        
        # Block 3: 128 filters
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),
        
        # Block 4: 256 filters
        layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.Conv2D(256, (3, 3), activation='relu', padding='same'),
        layers.BatchNormalization(),
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.4),
        
        # Dense layers
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.4),
        
        # Output layer
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model


def plot_training_history(history, save_dir):
    """
    Plot and save training history (accuracy and loss curves).
    
    Args:
        history: Keras training history object
        save_dir: Directory to save plots
    """
    # Plot accuracy
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
    plt.title('Model Accuracy', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    
    # Plot loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss', linewidth=2)
    plt.plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
    plt.title('Model Loss', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_path = os.path.join(save_dir, 'cnn_training_history.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Training history plot saved to {save_path}")


def plot_confusion_matrix(cm, class_names, save_path):
    """
    Plot and save confusion matrix.
    
    Args:
        cm: Confusion matrix array
        class_names: List of class names
        save_path: Path to save the plot
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names,
                cbar_kws={'label': 'Count'})
    plt.title('Confusion Matrix - CNN Model', fontsize=16, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Confusion matrix saved to {save_path}")


def main():
    """Main training pipeline for CNN model."""
    
    print("="*60)
    print("CNN TRAINING PIPELINE")
    print("="*60)
    
    # Configuration
    DATA_DIR = "data"
    MODEL_DIR = "models/cnn"
    EVAL_DIR = "evaluation"
    CM_DIR = os.path.join(EVAL_DIR, "confusion_matrices")
    
    BATCH_SIZE = 16
    EPOCHS = 100
    LEARNING_RATE = 0.001
    
    # Create directories
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
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(
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
    
    # Convert to categorical
    y_train_cat = to_categorical(y_train_encoded, num_classes=len(CLASS_NAMES))
    y_val_cat = to_categorical(y_val_encoded, num_classes=len(CLASS_NAMES))
    y_test_cat = to_categorical(y_test_encoded, num_classes=len(CLASS_NAMES))
    
    # Step 3: Preprocess images
    print("\nStep 3: Preprocessing images...")
    X_train = preprocess_for_cnn(X_train, normalize=True)
    X_val = preprocess_for_cnn(X_val, normalize=True)
    X_test = preprocess_for_cnn(X_test, normalize=True)
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Validation data shape: {X_val.shape}")
    print(f"Test data shape: {X_test.shape}")
    
    # Step 4: Data augmentation will be done during training
    print("\nStep 4: Data augmentation will be applied during training...")
    
    # Step 5: Build model
    print("\nStep 5: Building CNN model...")
    model = build_cnn_model(
        input_shape=(224, 224, 3),
        num_classes=len(CLASS_NAMES)
    )
    
    # Print model summary
    model.summary()
    
    # Compile model
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Step 6: Setup callbacks
    print("\nStep 6: Setting up callbacks...")
    
    callbacks = [
        EarlyStopping(
            monitor='val_accuracy',
            patience=15,
            restore_best_weights=True,
            verbose=1,
            mode='max'
        ),
        ReduceLROnPlateau(
            monitor='val_accuracy',
            factor=0.5,
            patience=7,
            min_lr=1e-7,
            verbose=1,
            mode='max'
        ),
        ModelCheckpoint(
            filepath=os.path.join(MODEL_DIR, 'best_model.keras'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1,
            mode='max'
        )
    ]
    
    # Step 7: Train model
    print("\nStep 7: Training model...")
    print(f"Epochs: {EPOCHS}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Learning rate: {LEARNING_RATE}")
    
    start_time = time.time()
    
    # Train directly on data without generator to avoid data exhaustion issues
    history = model.fit(
        X_train, y_train_cat,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_val, y_val_cat),
        callbacks=callbacks,
        verbose=1,
        shuffle=True
    )
    
    training_time = time.time() - start_time
    print(f"\nTraining completed in {training_time:.2f} seconds ({training_time/60:.2f} minutes)")
    
    # Step 8: Save model
    print("\nStep 8: Saving model...")
    
    # Save in .keras format (recommended)
    keras_path = os.path.join(MODEL_DIR, 'cnn_model.keras')
    model.save(keras_path)
    print(f"Model saved to {keras_path}")
    
    # Save in .h5 format (for compatibility)
    h5_path = os.path.join(MODEL_DIR, 'cnn_model.h5')
    model.save(h5_path)
    print(f"Model saved to {h5_path}")
    
    # Save label mapping
    label_mapping_path = os.path.join(MODEL_DIR, "label_mapping.json")
    with open(label_mapping_path, 'w') as f:
        json.dump(label_to_idx, f, indent=2)
    print(f"Label mapping saved to {label_mapping_path}")
    
    # Step 9: Plot training history
    print("\nStep 9: Plotting training history...")
    plot_training_history(history, EVAL_DIR)
    
    # Step 10: Evaluate on test set
    print("\nStep 10: Evaluating on test set...")
    
    # Make predictions
    y_pred_probs = model.predict(X_test, verbose=1)
    y_pred = np.argmax(y_pred_probs, axis=1)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test_encoded, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_test_encoded, y_pred,
        average=None,
        labels=range(len(CLASS_NAMES))
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
    cm = confusion_matrix(y_test_encoded, y_pred, labels=range(len(CLASS_NAMES)))
    
    # Print results
    print(f"\nCNN Model Results:")
    print(f"Overall Accuracy: {accuracy:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test_encoded, y_pred, target_names=CLASS_NAMES))
    
    # Plot confusion matrix
    cm_path = os.path.join(CM_DIR, "cnn_cm.png")
    plot_confusion_matrix(cm, CLASS_NAMES, cm_path)
    
    # Step 11: Save metrics
    print("\nStep 11: Saving metrics...")
    
    metrics = {
        'model_name': 'CNN',
        'accuracy': float(accuracy),
        'per_class_metrics': per_class_metrics,
        'confusion_matrix': cm.tolist(),
        'training_time': training_time,
        'training_history': {
            'accuracy': [float(x) for x in history.history['accuracy']],
            'val_accuracy': [float(x) for x in history.history['val_accuracy']],
            'loss': [float(x) for x in history.history['loss']],
            'val_loss': [float(x) for x in history.history['val_loss']]
        },
        'dataset_info': {
            'total_samples': len(images),
            'train_samples': len(X_train),
            'val_samples': len(X_val),
            'test_samples': len(X_test),
            'num_classes': len(CLASS_NAMES),
            'class_names': CLASS_NAMES
        },
        'model_config': {
            'input_shape': [224, 224, 3],
            'batch_size': BATCH_SIZE,
            'epochs_trained': len(history.history['accuracy']),
            'learning_rate': LEARNING_RATE
        }
    }
    
    metrics_path = os.path.join(EVAL_DIR, "cnn_metrics.json")
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to {metrics_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"\nCNN Accuracy: {accuracy:.4f}")
    print(f"Training time: {training_time/60:.2f} minutes")
    print(f"\nModel saved in: {MODEL_DIR}")
    print(f"Confusion matrix saved in: {CM_DIR}")
    print(f"Metrics saved in: {metrics_path}")
    print("\nYou can now use this model for inference!")


if __name__ == "__main__":
    main()
