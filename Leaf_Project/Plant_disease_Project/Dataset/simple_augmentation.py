#!/usr/bin/env python3
"""
Simple Data Augmentation for Plant Disease Detection Dataset
Uses only OpenCV and NumPy (already installed dependencies).
"""

import os
import cv2
import numpy as np
import random
from datetime import datetime
import argparse

# Set random seeds for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

class SimpleAugmenter:
    """Simple data augmentation using OpenCV and NumPy."""
    
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
    
    def rotate_image(self, image, angle):
        """Rotate image by given angle."""
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        
        # Get rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        
        # Apply rotation
        rotated = cv2.warpAffine(image, rotation_matrix, (width, height))
        return rotated
    
    def flip_image(self, image, flip_code):
        """
        Flip image.
        flip_code: 0 = vertical flip, 1 = horizontal flip, -1 = both
        """
        return cv2.flip(image, flip_code)
    
    def adjust_brightness(self, image, factor):
        """Adjust image brightness."""
        # Convert to float to avoid overflow
        bright = image.astype(np.float32) * factor
        # Clip values to valid range
        bright = np.clip(bright, 0, 255)
        return bright.astype(np.uint8)
    
    def adjust_contrast(self, image, factor):
        """Adjust image contrast."""
        # Convert to float
        contrast = image.astype(np.float32)
        # Apply contrast adjustment
        contrast = (contrast - 127.5) * factor + 127.5
        # Clip values
        contrast = np.clip(contrast, 0, 255)
        return contrast.astype(np.uint8)
    
    def add_noise(self, image, noise_factor=25):
        """Add Gaussian noise to image."""
        noise = np.random.normal(0, noise_factor, image.shape).astype(np.float32)
        noisy = image.astype(np.float32) + noise
        noisy = np.clip(noisy, 0, 255)
        return noisy.astype(np.uint8)
    
    def blur_image(self, image, kernel_size=5):
        """Apply Gaussian blur to image."""
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    def zoom_image(self, image, zoom_factor):
        """Zoom into image (crop and resize)."""
        height, width = image.shape[:2]
        
        # Calculate crop dimensions
        crop_height = int(height / zoom_factor)
        crop_width = int(width / zoom_factor)
        
        # Calculate crop coordinates (center crop)
        start_y = (height - crop_height) // 2
        start_x = (width - crop_width) // 2
        
        # Crop image
        cropped = image[start_y:start_y + crop_height, start_x:start_x + crop_width]
        
        # Resize back to original size
        zoomed = cv2.resize(cropped, (width, height))
        return zoomed
    
    def shift_image(self, image, shift_x, shift_y):
        """Shift image by given pixels."""
        height, width = image.shape[:2]
        
        # Create translation matrix
        translation_matrix = np.float32([[1, 0, shift_x], [0, 1, shift_y]])
        
        # Apply translation
        shifted = cv2.warpAffine(image, translation_matrix, (width, height))
        return shifted
    
    def augment_image(self, image, augmentation_type="random"):
        """
        Apply augmentation to image.
        
        Args:
            image: Input image as numpy array
            augmentation_type: Type of augmentation to apply
            
        Returns:
            Augmented image
        """
        if augmentation_type == "rotation":
            angle = random.uniform(-30, 30)
            return self.rotate_image(image, angle)
        
        elif augmentation_type == "horizontal_flip":
            return self.flip_image(image, 1)
        
        elif augmentation_type == "vertical_flip":
            return self.flip_image(image, 0)
        
        elif augmentation_type == "brightness":
            factor = random.uniform(0.7, 1.3)
            return self.adjust_brightness(image, factor)
        
        elif augmentation_type == "contrast":
            factor = random.uniform(0.8, 1.2)
            return self.adjust_contrast(image, factor)
        
        elif augmentation_type == "noise":
            noise_factor = random.uniform(10, 30)
            return self.add_noise(image, noise_factor)
        
        elif augmentation_type == "blur":
            kernel_size = random.choice([3, 5, 7])
            return self.blur_image(image, kernel_size)
        
        elif augmentation_type == "zoom":
            zoom_factor = random.uniform(1.1, 1.3)
            return self.zoom_image(image, zoom_factor)
        
        elif augmentation_type == "shift":
            shift_x = random.randint(-20, 20)
            shift_y = random.randint(-20, 20)
            return self.shift_image(image, shift_x, shift_y)
        
        elif augmentation_type == "combined":
            # Apply multiple augmentations
            aug_image = image.copy()
            
            # Random rotation
            if random.random() > 0.5:
                angle = random.uniform(-20, 20)
                aug_image = self.rotate_image(aug_image, angle)
            
            # Random flip
            if random.random() > 0.5:
                flip_code = random.choice([0, 1])
                aug_image = self.flip_image(aug_image, flip_code)
            
            # Random brightness
            if random.random() > 0.5:
                factor = random.uniform(0.8, 1.2)
                aug_image = self.adjust_brightness(aug_image, factor)
            
            # Random contrast
            if random.random() > 0.5:
                factor = random.uniform(0.9, 1.1)
                aug_image = self.adjust_contrast(aug_image, factor)
            
            return aug_image
        
        else:  # random
            augmentation_types = [
                "rotation", "horizontal_flip", "vertical_flip", 
                "brightness", "contrast", "noise", "blur", 
                "zoom", "shift", "combined"
            ]
            selected_type = random.choice(augmentation_types)
            return self.augment_image(image, selected_type)
    
    def augment_single_image(self, image_path, num_augmentations=10):
        """
        Generate multiple augmentations for a single image.
        
        Args:
            image_path: Path to input image
            num_augmentations: Number of augmentations to generate
            
        Returns:
            List of augmented images
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Resize to target size
        image = cv2.resize(image, self.target_size)
        
        augmented_images = []
        
        for i in range(num_augmentations):
            aug_image = self.augment_image(image, "random")
            augmented_images.append(aug_image)
        
        return augmented_images
    
    def augment_dataset(self, data_dir, augmentations_per_image=10, balance_classes=True):
        """
        Augment entire dataset.
        
        Args:
            data_dir: Directory containing class folders
            augmentations_per_image: Number of augmentations per original image
            balance_classes: Whether to balance classes
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
            target_augmentations = {}
            for class_name, count in class_counts.items():
                needed = max_class_count - count
                target_augmentations[class_name] = max(needed, augmentations_per_image)
        else:
            target_augmentations = {class_name: augmentations_per_image 
                                  for class_name in classes}
        
        print(f"\n🎯 Target augmentations per class:")
        for class_name, count in target_augmentations.items():
            print(f"   {class_name}: {count} augmentations")
        
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
            
            # Copy original images
            for img_file in image_files:
                src_path = os.path.join(class_input_dir, img_file)
                dst_path = os.path.join(class_output_dir, f"original_{img_file}")
                
                # Load, resize and save original
                img = cv2.imread(src_path)
                img_resized = cv2.resize(img, self.target_size)
                cv2.imwrite(dst_path, img_resized)
            
            # Generate augmentations
            target_augs = target_augmentations[class_name]
            augs_per_image = target_augs // len(image_files)
            extra_augs = target_augs % len(image_files)
            
            generated_count = 0
            
            for i, img_file in enumerate(image_files):
                img_path = os.path.join(class_input_dir, img_file)
                base_name = os.path.splitext(img_file)[0]
                
                # Determine number of augmentations for this image
                num_augs = augs_per_image
                if i < extra_augs:
                    num_augs += 1
                
                print(f"   📸 Augmenting {img_file} ({num_augs} versions)...")
                
                try:
                    augmented_images = self.augment_single_image(img_path, num_augs)
                    
                    for j, aug_img in enumerate(augmented_images):
                        output_filename = f"{base_name}_aug_{self.timestamp}_{generated_count:04d}.jpg"
                        output_path = os.path.join(class_output_dir, output_filename)
                        
                        cv2.imwrite(output_path, aug_img)
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
    
    def preview_augmentations(self, image_path, output_dir="preview"):
        """
        Generate preview of different augmentation types.
        
        Args:
            image_path: Path to input image
            output_dir: Directory to save preview images
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Load image
        image = cv2.imread(image_path)
        image = cv2.resize(image, self.target_size)
        
        # Save original
        cv2.imwrite(os.path.join(output_dir, "00_original.jpg"), image)
        
        # Generate different augmentation types
        augmentation_types = [
            "rotation", "horizontal_flip", "vertical_flip", 
            "brightness", "contrast", "noise", "blur", 
            "zoom", "shift", "combined"
        ]
        
        for i, aug_type in enumerate(augmentation_types, 1):
            aug_image = self.augment_image(image, aug_type)
            filename = f"{i:02d}_{aug_type}.jpg"
            cv2.imwrite(os.path.join(output_dir, filename), aug_image)
        
        print(f"✅ Preview images saved in {output_dir}")


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Simple Plant Disease Dataset Augmentation")
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
    parser.add_argument("--preview", type=str, default=None,
                       help="Generate preview of augmentations for a single image")
    
    args = parser.parse_args()
    
    # Initialize augmenter
    augmenter = SimpleAugmenter(
        output_dir=args.output_dir,
        target_size=tuple(args.target_size)
    )
    
    if args.preview:
        # Generate preview
        augmenter.preview_augmentations(args.preview)
    else:
        # Augment dataset
        augmenter.augment_dataset(
            data_dir=args.input_dir,
            augmentations_per_image=args.augmentations_per_image,
            balance_classes=args.balance_classes
        )


if __name__ == "__main__":
    # Example usage
    print("🌿 Simple Plant Disease Data Augmentation")
    print("=" * 50)
    
    # Initialize augmenter
    augmenter = SimpleAugmenter(
        output_dir="data_augmented",
        target_size=(224, 224)
    )
    
    # Option 1: Generate preview of augmentations
    # Find a sample image to preview
    sample_image = None
    for class_dir in ['HEALTHY_LEAF', 'FROG_EYE_LEAF_SPOT', 'POWDERY_MILDEW', 'TOBACCO_MOSAIC_VIRUS']:
        class_path = os.path.join('data', class_dir)
        if os.path.exists(class_path):
            image_files = [f for f in os.listdir(class_path) 
                          if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
            if image_files:
                sample_image = os.path.join(class_path, image_files[0])
                break
    
    if sample_image:
        print(f"\n🖼️ Generating preview with: {sample_image}")
        augmenter.preview_augmentations(sample_image, "augmentation_preview")
    
    # Option 2: Augment the entire dataset
    print(f"\n🚀 Starting full dataset augmentation...")
    augmenter.augment_dataset(
        data_dir="data",
        augmentations_per_image=15,  # Generate 15 augmentations per original image
        balance_classes=True         # Balance classes
    )
    
    print("\n✅ Data augmentation completed!")
    print("📁 Check the 'data_augmented' folder for results")
    print("📁 Check the 'augmentation_preview' folder for preview examples")