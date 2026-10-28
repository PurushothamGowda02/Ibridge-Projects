#!/usr/bin/env python3
"""
Advanced Data Augmentation for Plant Disease Detection Dataset
Generates augmented images to improve model performance and handle class imbalance.
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import random
import argparse
from tqdm import tqdm
import albumentations as A
from datetime import datetime

# Set random seeds for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

class PlantDiseaseAugmenter:
    """Advanced data augmentation for plant disease images."""
    
    def __init__(self, output_dir="data_augmented", target_size=(224, 224)):
        """
        Initialize the augmenter.
        
        Args:
            output_dir: Directory to save augmented images
            target_size: Target size for images (height, width)
        """
        self.output_dir = output_dir
        self.target_size = target_size
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize augmentation pipelines
        self._init_augmentation_pipelines()
    
    def _init_augmentation_pipelines(self):
        """Initialize different augmentation pipelines."""
        
        # Basic augmentation pipeline
        self.basic_transform = A.Compose([
            A.Resize(self.target_size[0], self.target_size[1]),
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.3),
            A.Rotate(limit=30, p=0.7),
            A.RandomBrightnessContrast(
                brightness_limit=0.2, 
                contrast_limit=0.2, 
                p=0.6
            ),
        ])
        
        # Advanced augmentation pipeline
        self.advanced_transform = A.Compose([
            A.Resize(self.target_size[0], self.target_size[1]),
            A.OneOf([
                A.HorizontalFlip(p=1.0),
                A.VerticalFlip(p=1.0),
                A.Transpose(p=1.0),
            ], p=0.7),
            A.OneOf([
                A.Rotate(limit=45, p=1.0),
                A.ShiftScaleRotate(
                    shift_limit=0.1, 
                    scale_limit=0.2, 
                    rotate_limit=30, 
                    p=1.0
                ),
            ], p=0.8),
            A.OneOf([
                A.RandomBrightnessContrast(
                    brightness_limit=0.3, 
                    contrast_limit=0.3, 
                    p=1.0
                ),
                A.HueSaturationValue(
                    hue_shift_limit=20, 
                    sat_shift_limit=30, 
                    val_shift_limit=20, 
                    p=1.0
                ),
                A.CLAHE(clip_limit=2.0, p=1.0),
            ], p=0.9),
            A.OneOf([
                A.GaussNoise(var_limit=(10.0, 50.0), p=1.0),
                A.GaussianBlur(blur_limit=(3, 7), p=1.0),
                A.MotionBlur(blur_limit=7, p=1.0),
            ], p=0.4),
            A.OneOf([
                A.ElasticTransform(p=1.0),
                A.GridDistortion(p=1.0),
                A.OpticalDistortion(p=1.0),
            ], p=0.3),
        ])
        
        # Color-focused augmentation for disease detection
        self.color_transform = A.Compose([
            A.Resize(self.target_size[0], self.target_size[1]),
            A.HorizontalFlip(p=0.5),
            A.Rotate(limit=20, p=0.6),
            A.OneOf([
                A.ColorJitter(
                    brightness=0.2, 
                    contrast=0.2, 
                    saturation=0.2, 
                    hue=0.1, 
                    p=1.0
                ),
                A.HueSaturationValue(
                    hue_shift_limit=15, 
                    sat_shift_limit=25, 
                    val_shift_limit=15, 
                    p=1.0
                ),
                A.ChannelShuffle(p=1.0),
            ], p=0.8),
            A.RandomGamma(gamma_limit=(80, 120), p=0.5),
        ])
        
        # Geometric-focused augmentation
        self.geometric_transform = A.Compose([
            A.Resize(self.target_size[0], self.target_size[1]),
            A.OneOf([
                A.HorizontalFlip(p=1.0),
                A.VerticalFlip(p=1.0),
                A.RandomRotate90(p=1.0),
            ], p=0.8),
            A.OneOf([
                A.Rotate(limit=45, p=1.0),
                A.Affine(
                    scale=(0.8, 1.2), 
                    translate_percent=(-0.1, 0.1), 
                    rotate=(-30, 30), 
                    shear=(-10, 10), 
                    p=1.0
                ),
                A.Perspective(scale=(0.05, 0.1), p=1.0),
            ], p=0.7),
            A.RandomCrop(
                height=int(self.target_size[0] * 0.9), 
                width=int(self.target_size[1] * 0.9), 
                p=0.3
            ),
        ])
    
    def augment_single_image(self, image_path, num_augmentations=5, pipeline='basic'):
        """
        Augment a single image.
        
        Args:
            image_path: Path to the input image
            num_augmentations: Number of augmented versions to create
            pipeline: Augmentation pipeline ('basic', 'advanced', 'color', 'geometric')
            
        Returns:
            List of augmented images as numpy arrays
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert BGR to RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Select augmentation pipeline
        if pipeline == 'basic':
            transform = self.basic_transform
        elif pipeline == 'advanced':
            transform = self.advanced_transform
        elif pipeline == 'color':
            transform = self.color_transform
        elif pipeline == 'geometric':
            transform = self.geometric_transform
        else:
            raise ValueError(f"Unknown pipeline: {pipeline}")
        
        augmented_images = []
        
        for i in range(num_augmentations):
            # Apply augmentation
            augmented = transform(image=image)['image']
            augmented_images.append(augmented)
        
        return augmented_images
    
    def augment_dataset(self, data_dir, augmentations_per_image=10, 
                       balance_classes=True, max_images_per_class=None):
        """
        Augment entire dataset with class balancing.
        
        Args:
            data_dir: Directory containing class folders
            augmentations_per_image: Number of augmentations per original image
            balance_classes: Whether to balance classes by generating more augmentations for smaller classes
            max_images_per_class: Maximum images per class after augmentation
        """
        print(f"🚀 Starting dataset augmentation...")
        print(f"📁 Input directory: {data_dir}")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"🔄 Augmentations per image: {augmentations_per_image}")
        
        # Get class information
        classes = [d for d in os.listdir(data_dir) 
                  if os.path.isdir(os.path.join(data_dir, d))]
        
        class_counts = {}
        for class_name in classes:
            class_path = os.path.join(data_dir, class_name)
            image_files = [f for f in os.listdir(class_path) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            class_counts[class_name] = len(image_files)
        
        print(f"\n📊 Original class distribution:")
        for class_name, count in class_counts.items():
            print(f"   {class_name}: {count} images")
        
        # Calculate target counts for balancing
        if balance_classes:
            max_class_count = max(class_counts.values())
            target_counts = {class_name: max_class_count for class_name in classes}
        else:
            target_counts = {class_name: count * augmentations_per_image 
                           for class_name, count in class_counts.items()}
        
        if max_images_per_class:
            target_counts = {class_name: min(count, max_images_per_class) 
                           for class_name, count in target_counts.items()}
        
        print(f"\n🎯 Target class distribution:")
        for class_name, count in target_counts.items():
            print(f"   {class_name}: {count} images")
        
        # Process each class
        total_generated = 0
        
        for class_name in classes:
            print(f"\n🔄 Processing class: {class_name}")
            
            class_input_dir = os.path.join(data_dir, class_name)
            class_output_dir = os.path.join(self.output_dir, class_name)
            os.makedirs(class_output_dir, exist_ok=True)
            
            # Get original images
            image_files = [f for f in os.listdir(class_input_dir) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            
            original_count = len(image_files)
            target_count = target_counts[class_name]
            
            # Copy original images
            for img_file in image_files:
                src_path = os.path.join(class_input_dir, img_file)
                dst_path = os.path.join(class_output_dir, f"original_{img_file}")
                
                # Copy and resize original
                img = cv2.imread(src_path)
                img_resized = cv2.resize(img, self.target_size)
                cv2.imwrite(dst_path, img_resized)
            
            # Calculate how many augmentations needed
            augmentations_needed = target_count - original_count
            
            if augmentations_needed <= 0:
                print(f"   ✅ Class already has enough images")
                continue
            
            augmentations_per_original = augmentations_needed // original_count
            extra_augmentations = augmentations_needed % original_count
            
            print(f"   📈 Generating {augmentations_needed} augmented images...")
            
            # Generate augmentations
            generated_count = 0
            
            for i, img_file in enumerate(tqdm(image_files, desc=f"   Augmenting {class_name}")):
                img_path = os.path.join(class_input_dir, img_file)
                base_name = os.path.splitext(img_file)[0]
                
                # Determine number of augmentations for this image
                num_augs = augmentations_per_original
                if i < extra_augmentations:
                    num_augs += 1
                
                # Generate augmentations with different pipelines
                pipelines = ['basic', 'advanced', 'color', 'geometric']
                
                for aug_idx in range(num_augs):
                    pipeline = pipelines[aug_idx % len(pipelines)]
                    
                    try:
                        augmented_images = self.augment_single_image(
                            img_path, 
                            num_augmentations=1, 
                            pipeline=pipeline
                        )
                        
                        for j, aug_img in enumerate(augmented_images):
                            output_filename = f"{base_name}_aug_{self.timestamp}_{generated_count:04d}.jpg"
                            output_path = os.path.join(class_output_dir, output_filename)
                            
                            # Convert RGB to BGR for OpenCV
                            aug_img_bgr = cv2.cvtColor(aug_img, cv2.COLOR_RGB2BGR)
                            cv2.imwrite(output_path, aug_img_bgr)
                            
                            generated_count += 1
                            total_generated += 1
                    
                    except Exception as e:
                        print(f"   ⚠️ Error augmenting {img_file}: {e}")
                        continue
            
            print(f"   ✅ Generated {generated_count} augmented images for {class_name}")
        
        print(f"\n🎉 Augmentation complete!")
        print(f"📊 Total augmented images generated: {total_generated}")
        
        # Print final statistics
        print(f"\n📈 Final dataset statistics:")
        for class_name in classes:
            class_output_dir = os.path.join(self.output_dir, class_name)
            if os.path.exists(class_output_dir):
                final_count = len([f for f in os.listdir(class_output_dir) 
                                 if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
                print(f"   {class_name}: {final_count} images")
    
    def create_custom_augmentation(self, image_path, output_dir, 
                                 rotation_range=30, brightness_range=0.2, 
                                 zoom_range=0.2, num_augmentations=10):
        """
        Create custom augmentations with specific parameters.
        
        Args:
            image_path: Path to input image
            output_dir: Directory to save augmented images
            rotation_range: Range for rotation in degrees
            brightness_range: Range for brightness adjustment
            zoom_range: Range for zoom/scale
            num_augmentations: Number of augmentations to generate
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Custom transform
        custom_transform = A.Compose([
            A.Resize(self.target_size[0], self.target_size[1]),
            A.Rotate(limit=rotation_range, p=0.8),
            A.RandomBrightnessContrast(
                brightness_limit=brightness_range, 
                contrast_limit=brightness_range, 
                p=0.7
            ),
            A.RandomScale(scale_limit=zoom_range, p=0.6),
            A.HorizontalFlip(p=0.5),
        ])
        
        # Load image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        for i in range(num_augmentations):
            augmented = custom_transform(image=image)['image']
            
            output_filename = f"{base_name}_custom_aug_{i:03d}.jpg"
            output_path = os.path.join(output_dir, output_filename)
            
            # Convert RGB to BGR for OpenCV
            aug_img_bgr = cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR)
            cv2.imwrite(output_path, aug_img_bgr)
        
        print(f"✅ Generated {num_augmentations} custom augmentations in {output_dir}")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Plant Disease Dataset Augmentation")
    parser.add_argument("--input_dir", type=str, default="data", 
                       help="Input directory containing class folders")
    parser.add_argument("--output_dir", type=str, default="data_augmented", 
                       help="Output directory for augmented dataset")
    parser.add_argument("--augmentations_per_image", type=int, default=10, 
                       help="Number of augmentations per original image")
    parser.add_argument("--target_size", type=int, nargs=2, default=[224, 224], 
                       help="Target image size (height width)")
    parser.add_argument("--balance_classes", action="store_true", 
                       help="Balance classes by generating more augmentations for smaller classes")
    parser.add_argument("--max_images_per_class", type=int, default=None, 
                       help="Maximum images per class after augmentation")
    
    args = parser.parse_args()
    
    # Initialize augmenter
    augmenter = PlantDiseaseAugmenter(
        output_dir=args.output_dir,
        target_size=tuple(args.target_size)
    )
    
    # Augment dataset
    augmenter.augment_dataset(
        data_dir=args.input_dir,
        augmentations_per_image=args.augmentations_per_image,
        balance_classes=args.balance_classes,
        max_images_per_class=args.max_images_per_class
    )


if __name__ == "__main__":
    # Example usage
    print("🌿 Plant Disease Data Augmentation")
    print("=" * 50)
    
    # Initialize augmenter
    augmenter = PlantDiseaseAugmenter(
        output_dir="data_augmented",
        target_size=(224, 224)
    )
    
    # Augment the dataset
    augmenter.augment_dataset(
        data_dir="data",
        augmentations_per_image=15,  # Generate 15 augmentations per original image
        balance_classes=True,        # Balance classes
        max_images_per_class=1000    # Limit to 1000 images per class
    )
    
    print("\n✅ Data augmentation completed!")
    print("📁 Check the 'data_augmented' folder for results")