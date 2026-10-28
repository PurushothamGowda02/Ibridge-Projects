"""
Training script for MobileNetV2 model with transfer learning.
"""

import os
import sys
import numpy as np
import json
import time
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import MobileNetV2
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


def build_mobilenet_model(input_shape=(224, 224, 3), num_classes=4):
    """
    Build MobileNetV2 model with transfer learning.
    
    Args:
        input_shape: Shape of input images
        num_classes: Number of output classes
        
    Returns:
        Compiled Keras model
    """
    # Load pre-trained MobileNetV2 (without top layers)
    base_model = MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    # Freeze base model layers
    base_model.trainable = False
    
    # Build model
    model = keras.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.BatchNormalization(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax')
    ])
    
    return model, base_model


def plot_training_history(history, save_dir):
    """
    Plot and save training history.
    """
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Training Accuracy', linewidth=2)
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
    plt.title('Model Accuracy', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Accuracy', fontsize=12)
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Training Loss', linewidth=2)
    plt.plot(history.history['val_loss'], label='Validation Loss', linewidth=2)
    plt.title('Model Loss', fontsize=14, fontweight='bold')
    plt.xlabel('Epoch', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_path = os.path.join(save_dir, 'mobilenet_training_history.png')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Training history plot saved to {save_path}")


def plot_confusion_matrix(cm, class_names, save_path):
    """
    Plot and save confusion matrix.
    """
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names,
                cbar_kws={'label': 'Count'})
    plt.title('Confusion Matrix - MobileNetV2', fontsize=16, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Confusion matrix saved to {save_path}")


def main():
    """Main training pipeline for MobileNetV2."""
    
    print("="*60)
    print("MOBILENETV2 TRAINING PIPELINE")
    print("="*60)
    
    # Configuration
    DATA_DIR = "data"
    MODEL_DIR = "models/mobilenet"
    EVAL_DIR = "evaluation"
    CM_DIR = os.path.join(EVAL_DIR, "confusion_matrices")
    
    BATCH_SIZE = 32
    EPOCHS = 30
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
    
    # MobileNetV2 expects values in [-1, 1]
    X_train = (X_train * 2) - 1
    X_val = (X_val * 2) - 1
    X_test = (X_test * 2) - 1
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Validation data shape: {X_val.shape}")
    print(f"Test data shape: {X_test.shape}")
    
    # Step 4: Data augmentation
    print("\nStep 4: Setting up data augmentation...")
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        fill_mode='nearest'
    )
    
    train_datagen.fit(X_train)
    
    # Step 5: Build model
    print("\nStep 5: Building MobileNetV2 model...")
    model, base_model = build_mobilenet_model(
        input_shape=(224, 224, 3),
        num_classes=len(CLASS_NAMES)
    )
    
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
            monitor='val_loss',
            patience=10,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=5,
            min_lr=1e-7,
            verbose=1
        ),
        ModelCheckpoint(
            filepath=os.path.join(MODEL_DIR, 'best_mobilenet.keras'),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Step 7: Train model
    print("\nStep 7: Training model...")
    print(f"Epochs: {EPOCHS}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Learning rate: {LEARNING_RATE}")
    
    start_time = time.time()
    
    history = model.fit(
        train_datagen.flow(X_train, y_train_cat, batch_size=BATCH_SIZE),
        steps_per_epoch=len(X_train) // BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_val, y_val_cat),
        callbacks=callbacks,
        verbose=1
    )
    
    training_time = time.time() - start_time
    print(f"\nTraining completed in {training_time:.2f} seconds ({training_time/60:.2f} minutes)")
    
    # Step 8: Fine-tune model
    print("\nStep 8: Fine-tuning model...")
    base_model.trainable = True
    
    # Freeze early layers
    for layer in base_model.layers[:100]:
        layer.trainable = False
    
    # Recompile with lower learning rate
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=LEARNING_RATE/10),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    # Fine-tune for a few more epochs
    fine_tune_epochs = 10
    print(f"Fine-tuning for {fine_tune_epochs} epochs...")
    
    history_fine = model.fit(
        train_datagen.flow(X_train, y_train_cat, batch_size=BATCH_SIZE),
        steps_per_epoch=len(X_train) // BATCH_SIZE,
        epochs=fine_tune_epochs,
        validation_data=(X_val, y_val_cat),
        callbacks=callbacks,
        verbose=1
    )
    
    fine_tune_time = time.time() - start_time - training_time
    total_time = time.time() - start_time
    
    # Step 9: Save model
    print("\nStep 9: Saving model...")
    keras_path = os.path.join(MODEL_DIR, 'mobilenet_model.keras')
    model.save(keras_path)
    print(f"Model saved to {keras_path}")
    
    h5_path = os.path.join(MODEL_DIR, 'mobilenet_model.h5')
    model.save(h5_path)
    print(f"Model saved to {h5_path}")
    
    # Save label mapping
    label_mapping_path = os.path.join(MODEL_DIR, "label_mapping.json")
    with open(label_mapping_path, 'w') as f:
        json.dump(label_to_idx, f, indent=2)
    print(f"Label mapping saved to {label_mapping_path}")
    
    # Step 10: Plot training history
    print("\nStep 10: Plotting training history...")
    plot_training_history(history, EVAL_DIR)
    
    # Step 11: Evaluate on test set
    print("\nStep 11: Evaluating on test set...")
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
    print(f"\nMobileNetV2 Results:")
    print(f"Overall Accuracy: {accuracy:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_test_encoded, y_pred, target_names=CLASS_NAMES))
    
    # Plot confusion matrix
    cm_path = os.path.join(CM_DIR, "mobilenet_cm.png")
    plot_confusion_matrix(cm, CLASS_NAMES, cm_path)
    
    # Step 12: Save metrics
    print("\nStep 12: Saving metrics...")
    metrics = {
        'model_name': 'MobileNetV2',
        'accuracy': float(accuracy),
        'per_class_metrics': per_class_metrics,
        'confusion_matrix': cm.tolist(),
        'training_time': total_time,
        'initial_training_time': training_time,
        'fine_tuning_time': fine_tune_time,
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
            'initial_epochs': len(history.history['accuracy']),
            'fine_tune_epochs': fine_tune_epochs,
            'learning_rate': LEARNING_RATE,
            'base_model': 'MobileNetV2',
            'pretrained_weights': 'imagenet'
        }
    }
    
    metrics_path = os.path.join(EVAL_DIR, "mobilenet_metrics.json")
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to {metrics_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("TRAINING COMPLETE!")
    print("="*60)
    print(f"\nMobileNetV2 Accuracy: {accuracy:.4f}")
    print(f"Total training time: {total_time/60:.2f} minutes")
    print(f"  - Initial training: {training_time/60:.2f} minutes")
    print(f"  - Fine-tuning: {fine_tune_time/60:.2f} minutes")
    print(f"\nModel saved in: {MODEL_DIR}")
    print(f"Confusion matrix saved in: {CM_DIR}")
    print(f"Metrics saved in: {metrics_path}")
    print("\nYou can now use this model for inference!")


if __name__ == "__main__":
    main()
