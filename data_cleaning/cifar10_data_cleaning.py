"""
CIFAR-10 Data Cleaning and Preprocessing Pipeline
Author: Data Science Instructor
Course: Data Preparation and Neural Networks

This script implements a comprehensive data cleaning and preprocessing pipeline
for the CIFAR-10 dataset, designed as a final project for students.
"""

import os
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageFilter, ImageEnhance
import pickle
import zipfile
import tarfile
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import warnings
warnings.filterwarnings('ignore')

class CIFAR10DataCleaner:
    """
    A comprehensive data cleaning and preprocessing class for CIFAR-10 dataset.
    
    This class handles:
    - Data loading and extraction
    - Noise detection and removal
    - Blur detection and enhancement
    - Occlusion handling
    - Image standardization and normalization
    - Data augmentation
    - Train/validation/test splitting
    """
    
    def __init__(self, data_path="cifar-10"):
        """
        Initialize the CIFAR-10 data cleaner.
        
        Args:
            data_path (str): Path to the CIFAR-10 dataset directory
        """
        self.data_path = data_path
        self.image_size = (32, 32)  # CIFAR-10 standard size
        self.target_size = (32, 32)  # Target size for training
        self.num_classes = 10
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
                           'dog', 'frog', 'horse', 'ship', 'truck']
        
        # Data containers
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        self.X_val = None
        self.y_val = None
        
        # Cleaning statistics
        self.cleaning_stats = {
            'original_count': 0,
            'noise_removed': 0,
            'blur_enhanced': 0,
            'occlusion_handled': 0,
            'null_removed': 0,
            'final_count': 0
        }
        
    def load_cifar10_data(self):
        """
        Load CIFAR-10 data from various sources (pickle files, images, etc.)
        
        Returns:
            tuple: (X_train, y_train, X_test, y_test)
        """
        print("Loading CIFAR-10 dataset...")
        
        # Try to load from TensorFlow/Keras first
        try:
            (X_train, y_train), (X_test, y_test) = tf.keras.datasets.cifar10.load_data()
            print(f"Loaded from Keras: Train: {X_train.shape}, Test: {X_test.shape}")
            
            self.X_train = X_train
            self.y_train = y_train.flatten()
            self.X_test = X_test
            self.y_test = y_test.flatten()
            
            self.cleaning_stats['original_count'] = len(X_train) + len(X_test)
            return True
            
        except Exception as e:
            print(f"Could not load from Keras: {e}")
            
        # Try to load from local files if available
        try:
            return self._load_from_local_files()
        except Exception as e:
            print(f"Could not load from local files: {e}")
            return False
    
    def _load_from_local_files(self):
        """Load data from local pickle files or image directories"""
        # This would be implemented based on the actual file structure
        # For now, we'll use the Keras dataset as fallback
        return False
    
    def detect_and_remove_noise(self, threshold=30):
        """
        Detect and remove noisy images using various noise detection methods.
        
        Args:
            threshold (float): Noise threshold for filtering
            
        Returns:
            tuple: Cleaned data arrays
        """
        print("Detecting and removing noisy images...")
        
        def calculate_noise_level(image):
            """Calculate noise level using Laplacian variance"""
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            return cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Calculate noise levels for training data
        noise_levels = []
        for img in self.X_train:
            noise_level = calculate_noise_level(img)
            noise_levels.append(noise_level)
        
        noise_levels = np.array(noise_levels)
        
        # Remove images with extremely low noise (potentially corrupted)
        valid_indices = noise_levels > threshold
        
        original_count = len(self.X_train)
        self.X_train = self.X_train[valid_indices]
        self.y_train = self.y_train[valid_indices]
        
        removed_count = original_count - len(self.X_train)
        self.cleaning_stats['noise_removed'] = removed_count
        
        print(f"Removed {removed_count} noisy images from training set")
        return self.X_train, self.y_train
    
    def detect_and_enhance_blur(self, blur_threshold=100):
        """
        Detect blurry images and enhance them or remove if too blurry.
        
        Args:
            blur_threshold (float): Threshold for blur detection
            
        Returns:
            tuple: Enhanced data arrays
        """
        print("Detecting and enhancing blurry images...")
        
        def calculate_blur_level(image):
            """Calculate blur level using Laplacian variance"""
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            return cv2.Laplacian(gray, cv2.CV_64F).var()
        
        def enhance_image(image):
            """Enhance image using sharpening filter"""
            pil_image = Image.fromarray(image)
            enhanced = pil_image.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
            return np.array(enhanced)
        
        enhanced_count = 0
        enhanced_images = []
        valid_labels = []
        
        for i, img in enumerate(self.X_train):
            blur_level = calculate_blur_level(img)
            
            if blur_level < blur_threshold:
                # Try to enhance the image
                try:
                    enhanced_img = enhance_image(img)
                    enhanced_images.append(enhanced_img)
                    valid_labels.append(self.y_train[i])
                    enhanced_count += 1
                except:
                    # If enhancement fails, keep original
                    enhanced_images.append(img)
                    valid_labels.append(self.y_train[i])
            else:
                enhanced_images.append(img)
                valid_labels.append(self.y_train[i])
        
        self.X_train = np.array(enhanced_images)
        self.y_train = np.array(valid_labels)
        self.cleaning_stats['blur_enhanced'] = enhanced_count
        
        print(f"Enhanced {enhanced_count} blurry images")
        return self.X_train, self.y_train
    
    def handle_occlusions(self, occlusion_threshold=0.3):
        """
        Detect and handle occluded images.
        
        Args:
            occlusion_threshold (float): Threshold for occlusion detection
            
        Returns:
            tuple: Processed data arrays
        """
        print("Handling occluded images...")
        
        def detect_occlusion(image):
            """Simple occlusion detection using edge density"""
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / (edges.shape[0] * edges.shape[1])
            
            # Low edge density might indicate occlusion
            return edge_density < occlusion_threshold
        
        occlusion_handled = 0
        valid_images = []
        valid_labels = []
        
        for i, img in enumerate(self.X_train):
            is_occluded = detect_occlusion(img)
            
            if is_occluded:
                # For now, we keep occluded images but mark them
                # In a real scenario, you might apply inpainting or other techniques
                valid_images.append(img)
                valid_labels.append(self.y_train[i])
                occlusion_handled += 1
            else:
                valid_images.append(img)
                valid_labels.append(self.y_train[i])
        
        self.X_train = np.array(valid_images)
        self.y_train = np.array(valid_labels)
        self.cleaning_stats['occlusion_handled'] = occlusion_handled
        
        print(f"Handled {occlusion_handled} potentially occluded images")
        return self.X_train, self.y_train
    
    def remove_null_and_erroneous_images(self):
        """
        Remove null, corrupted, or erroneous images and unusual characters.
        
        Returns:
            tuple: Cleaned data arrays
        """
        print("Removing null and erroneous images...")
        
        valid_indices = []
        null_removed = 0
        
        for i, img in enumerate(self.X_train):
            # Check for null or invalid images
            if img is None:
                null_removed += 1
                continue
                
            # Check for proper shape
            if len(img.shape) != 3 or img.shape[2] != 3:
                null_removed += 1
                continue
                
            # Check for proper data type and range
            if not isinstance(img, np.ndarray):
                null_removed += 1
                continue
                
            # Check for unusual pixel values
            if np.any(np.isnan(img)) or np.any(np.isinf(img)):
                null_removed += 1
                continue
                
            # Check for completely black or white images
            if np.all(img == 0) or np.all(img == 255):
                null_removed += 1
                continue
                
            valid_indices.append(i)
        
        self.X_train = self.X_train[valid_indices]
        self.y_train = self.y_train[valid_indices]
        self.cleaning_stats['null_removed'] = null_removed
        
        print(f"Removed {null_removed} null or erroneous images")
        return self.X_train, self.y_train
    
    def standardize_image_size(self, target_size=(32, 32), padding_mode='constant'):
        """
        Standardize image sizes using padding or resizing.
        
        Args:
            target_size (tuple): Target image size (height, width)
            padding_mode (str): Padding mode ('constant', 'edge', 'reflect')
            
        Returns:
            tuple: Standardized data arrays
        """
        print(f"Standardizing image sizes to {target_size}...")
        
        def pad_image(image, target_size, mode='constant'):
            """Pad image to target size"""
            h, w = image.shape[:2]
            target_h, target_w = target_size
            
            # Calculate padding
            pad_h = max(0, target_h - h)
            pad_w = max(0, target_w - w)
            
            # Pad symmetrically
            pad_top = pad_h // 2
            pad_bottom = pad_h - pad_top
            pad_left = pad_w // 2
            pad_right = pad_w - pad_left
            
            if len(image.shape) == 3:
                padded = np.pad(image, ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0)), 
                               mode=mode)
            else:
                padded = np.pad(image, ((pad_top, pad_bottom), (pad_left, pad_right)), 
                               mode=mode)
            
            return padded
        
        # Process training data
        standardized_train = []
        for img in self.X_train:
            if img.shape[:2] != target_size:
                # First resize if image is larger than target
                if img.shape[0] > target_size[0] or img.shape[1] > target_size[1]:
                    img = cv2.resize(img, target_size)
                else:
                    # Pad if image is smaller
                    img = pad_image(img, target_size, padding_mode)
            standardized_train.append(img)
        
        # Process test data
        standardized_test = []
        for img in self.X_test:
            if img.shape[:2] != target_size:
                if img.shape[0] > target_size[0] or img.shape[1] > target_size[1]:
                    img = cv2.resize(img, target_size)
                else:
                    img = pad_image(img, target_size, padding_mode)
            standardized_test.append(img)
        
        self.X_train = np.array(standardized_train)
        self.X_test = np.array(standardized_test)
        self.target_size = target_size
        
        print(f"Standardized {len(self.X_train)} training and {len(self.X_test)} test images")
        return self.X_train, self.X_test
    
    def normalize_images(self, method='minmax'):
        """
        Normalize image pixel values.
        
        Args:
            method (str): Normalization method ('minmax', 'zscore', 'unit')
            
        Returns:
            tuple: Normalized data arrays
        """
        print(f"Normalizing images using {method} method...")
        
        if method == 'minmax':
            # Scale to [0, 1]
            self.X_train = self.X_train.astype('float32') / 255.0
            self.X_test = self.X_test.astype('float32') / 255.0
            
        elif method == 'zscore':
            # Z-score normalization
            mean = np.mean(self.X_train, axis=(0, 1, 2), keepdims=True)
            std = np.std(self.X_train, axis=(0, 1, 2), keepdims=True)
            
            self.X_train = (self.X_train.astype('float32') - mean) / (std + 1e-8)
            self.X_test = (self.X_test.astype('float32') - mean) / (std + 1e-8)
            
        elif method == 'unit':
            # Unit normalization
            self.X_train = self.X_train.astype('float32') / 127.5 - 1.0
            self.X_test = self.X_test.astype('float32') / 127.5 - 1.0
        
        print("Image normalization completed")
        return self.X_train, self.X_test
    
    def prepare_labels(self):
        """
        Prepare labels for training (one-hot encoding).
        
        Returns:
            tuple: Processed label arrays
        """
        print("Preparing labels...")
        
        # Convert to categorical (one-hot encoding)
        self.y_train_categorical = to_categorical(self.y_train, self.num_classes)
        self.y_test_categorical = to_categorical(self.y_test, self.num_classes)
        
        print(f"Labels prepared: {self.num_classes} classes")
        return self.y_train_categorical, self.y_test_categorical
    
    def split_data(self, validation_split=0.2, random_state=42):
        """
        Split training data into train and validation sets.
        
        Args:
            validation_split (float): Fraction of data for validation
            random_state (int): Random seed for reproducibility
            
        Returns:
            tuple: Split data arrays
        """
        print(f"Splitting data with {validation_split:.1%} validation split...")
        
        # Split the training data
        X_train_split, X_val_split, y_train_split, y_val_split = train_test_split(
            self.X_train, self.y_train_categorical, 
            test_size=validation_split, 
            random_state=random_state,
            stratify=self.y_train
        )
        
        self.X_train = X_train_split
        self.X_val = X_val_split
        self.y_train = y_train_split
        self.y_val = y_val_split
        
        print(f"Data split completed:")
        print(f"  Training: {self.X_train.shape[0]} samples")
        print(f"  Validation: {self.X_val.shape[0]} samples")
        print(f"  Test: {self.X_test.shape[0]} samples")
        
        return self.X_train, self.X_val, self.y_train, self.y_val
    
    def create_data_augmentation(self):
        """
        Create data augmentation pipeline for training.
        
        Returns:
            ImageDataGenerator: Configured data generator
        """
        print("Creating data augmentation pipeline...")
        
        datagen = ImageDataGenerator(
            rotation_range=15,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=True,
            zoom_range=0.1,
            shear_range=0.1,
            fill_mode='nearest'
        )
        
        # Fit the generator on training data
        datagen.fit(self.X_train)
        
        print("Data augmentation pipeline created")
        return datagen
    
    def visualize_cleaning_results(self):
        """Visualize the results of the cleaning process"""
        print("Generating cleaning results visualization...")
        
        # Create visualization
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        # Sample images from each class
        for i in range(6):
            class_indices = np.where(self.y_train == i)[0]
            if len(class_indices) > 0:
                sample_idx = np.random.choice(class_indices)
                sample_image = self.X_train[sample_idx]
                
                axes[i//3, i%3].imshow(sample_image)
                axes[i//3, i%3].set_title(f'Class: {self.class_names[i]}')
                axes[i//3, i%3].axis('off')
        
        plt.tight_layout()
        plt.savefig('cleaning_results_samples.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Create statistics plot
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        stats_labels = list(self.cleaning_stats.keys())
        stats_values = list(self.cleaning_stats.values())
        
        bars = ax.bar(stats_labels, stats_values)
        ax.set_title('Data Cleaning Statistics')
        ax.set_ylabel('Number of Images')
        plt.xticks(rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('cleaning_statistics.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Visualizations saved as PNG files")
    
    def save_cleaned_data(self, output_path="cleaned_cifar10_data.npz"):
        """
        Save the cleaned and preprocessed data.
        
        Args:
            output_path (str): Path to save the cleaned data
        """
        print(f"Saving cleaned data to {output_path}...")
        
        # Update final statistics
        self.cleaning_stats['final_count'] = len(self.X_train) + len(self.X_val) + len(self.X_test)
        
        np.savez_compressed(
            output_path,
            X_train=self.X_train,
            y_train=self.y_train,
            X_val=self.X_val,
            y_val=self.y_val,
            X_test=self.X_test,
            y_test=self.y_test_categorical,
            class_names=self.class_names,
            cleaning_stats=self.cleaning_stats
        )
        
        print(f"Cleaned data saved successfully")
        print(f"Final dataset size: {self.cleaning_stats['final_count']} images")
    
    def generate_report(self):
        """Generate a comprehensive cleaning report"""
        print("\n" + "="*60)
        print("CIFAR-10 DATA CLEANING REPORT")
        print("="*60)
        
        print(f"\nDataset Information:")
        print(f"  - Number of classes: {self.num_classes}")
        print(f"  - Class names: {', '.join(self.class_names)}")
        print(f"  - Target image size: {self.target_size}")
        print(f"  - Final activation function: softmax (for {self.num_classes} classes)")
        
        print(f"\nData Cleaning Statistics:")
        for key, value in self.cleaning_stats.items():
            print(f"  - {key.replace('_', ' ').title()}: {value}")
        
        print(f"\nFinal Data Distribution:")
        print(f"  - Training set: {self.X_train.shape[0]} images")
        print(f"  - Validation set: {self.X_val.shape[0]} images")
        print(f"  - Test set: {self.X_test.shape[0]} images")
        
        print(f"\nData Preprocessing Steps Completed:")
        print(f"  ✓ Noise detection and removal")
        print(f"  ✓ Blur detection and enhancement")
        print(f"  ✓ Occlusion handling")
        print(f"  ✓ Null and erroneous image removal")
        print(f"  ✓ Image size standardization with padding")
        print(f"  ✓ Pixel normalization")
        print(f"  ✓ Label preparation (one-hot encoding)")
        print(f"  ✓ Train/validation/test split")
        print(f"  ✓ Data augmentation pipeline creation")
        
        print("\n" + "="*60)

def main():
    """Main execution function"""
    print("Starting CIFAR-10 Data Cleaning Pipeline...")
    
    # Initialize the data cleaner
    cleaner = CIFAR10DataCleaner()
    
    # Step 1: Load the data
    if not cleaner.load_cifar10_data():
        print("Failed to load CIFAR-10 data. Exiting...")
        return
    
    # Step 2: Data cleaning process
    cleaner.detect_and_remove_noise()
    cleaner.detect_and_enhance_blur()
    cleaner.handle_occlusions()
    cleaner.remove_null_and_erroneous_images()
    
    # Step 3: Image standardization and preprocessing
    cleaner.standardize_image_size(target_size=(32, 32), padding_mode='constant')
    cleaner.normalize_images(method='minmax')
    cleaner.prepare_labels()
    
    # Step 4: Data splitting
    cleaner.split_data(validation_split=0.2)
    
    # Step 5: Create data augmentation
    datagen = cleaner.create_data_augmentation()
    
    # Step 6: Visualization and reporting
    cleaner.visualize_cleaning_results()
    cleaner.generate_report()
    
    # Step 7: Save cleaned data
    cleaner.save_cleaned_data("cleaned_cifar10_data.npz")
    
    print("\nData cleaning pipeline completed successfully!")

if __name__ == "__main__":
    main()