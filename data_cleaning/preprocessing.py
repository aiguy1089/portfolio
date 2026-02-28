"""
CIFAR-10 Preprocessing Utilities
D802 Deep Learning - STN1 Task 2 Data Cleaning

This module contains utility functions for preprocessing CIFAR-10 images
including normalization, augmentation, and data preparation for neural networks.
"""

import numpy as np
import cv2
from PIL import Image, ImageFilter
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split

def normalize_images(images):
    """
    Normalize pixel values from [0, 255] to [0, 1] range
    
    Args:
        images (numpy.ndarray): Array of images with pixel values 0-255
        
    Returns:
        numpy.ndarray: Normalized images with pixel values 0-1
    """
    return images.astype('float32') / 255.0

def pad_image_before_resize(image, target_size, mode='constant'):
    """
    Apply padding before resizing to preserve aspect ratio
    
    Args:
        image (numpy.ndarray): Input image
        target_size (tuple): Target size (height, width)
        mode (str): Padding mode ('constant', 'edge', 'reflect')
        
    Returns:
        numpy.ndarray: Padded image
    """
    h, w = image.shape[:2]
    target_h, target_w = target_size
    
    # Calculate required padding
    pad_h = max(0, target_h - h)
    pad_w = max(0, target_w - w)
    
    # Apply symmetric padding
    pad_top = pad_h // 2
    pad_bottom = pad_h - pad_top
    pad_left = pad_w // 2
    pad_right = pad_w - pad_left
    
    # Pad the image
    if len(image.shape) == 3:
        padded = np.pad(image, 
                       ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0)), 
                       mode=mode)
    else:
        padded = np.pad(image, 
                       ((pad_top, pad_bottom), (pad_left, pad_right)), 
                       mode=mode)
    
    return padded

def enhance_blurry_image(image):
    """
    Enhance blurry images using UnsharpMask filter
    
    Args:
        image (numpy.ndarray): Input image
        
    Returns:
        numpy.ndarray: Enhanced image
    """
    try:
        # Convert to PIL Image
        pil_image = Image.fromarray(image.astype(np.uint8))
        
        # Apply UnsharpMask filter
        enhanced = pil_image.filter(ImageFilter.UnsharpMask(
            radius=1, percent=150, threshold=3))
        
        # Convert back to numpy array
        return np.array(enhanced)
    except Exception as e:
        print(f"Enhancement failed: {e}")
        return image

def calculate_blur_level(image):
    """
    Calculate blur level using gradient variance
    
    Args:
        image (numpy.ndarray): Input image
        
    Returns:
        float: Blur level (higher = sharper)
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = np.mean(image, axis=2)
    else:
        gray = image
    
    # Calculate gradients
    grad_x = np.diff(gray, axis=1)
    grad_y = np.diff(gray, axis=0)
    
    # Return gradient variance
    return np.var(grad_x) + np.var(grad_y)

def detect_occlusion(image, threshold=0.3):
    """
    Detect potential occlusion using edge density analysis
    
    Args:
        image (numpy.ndarray): Input image
        threshold (float): Edge density threshold
        
    Returns:
        bool: True if potentially occluded
    """
    # Convert to grayscale
    if len(image.shape) == 3:
        gray = np.mean(image, axis=2)
    else:
        gray = image
    
    # Calculate edge density using gradients
    grad_x = np.abs(np.diff(gray, axis=1))
    grad_y = np.abs(np.diff(gray, axis=0))
    
    # Calculate edge density
    edge_density = (np.sum(grad_x > 10) + np.sum(grad_y > 10)) / (gray.shape[0] * gray.shape[1])
    
    return edge_density < threshold

def validate_image(image):
    """
    Comprehensive image validation
    
    Args:
        image: Input image to validate
        
    Returns:
        bool: True if image is valid
    """
    # Check if image is None
    if image is None:
        return False
    
    # Check if it's a numpy array
    if not isinstance(image, np.ndarray):
        return False
    
    # Check shape (should be 32x32x3 for CIFAR-10)
    if len(image.shape) != 3 or image.shape[2] != 3:
        return False
    
    # Check for NaN or infinity values
    if np.any(np.isnan(image)) or np.any(np.isinf(image)):
        return False
    
    # Check for completely black or white images
    if np.all(image == 0) or np.all(image == 255):
        return False
    
    # Check pixel value range
    if np.min(image) < 0 or np.max(image) > 255:
        return False
    
    return True

def prepare_labels(labels, num_classes=10):
    """
    Convert labels to one-hot encoding
    
    Args:
        labels (numpy.ndarray): Integer labels
        num_classes (int): Number of classes
        
    Returns:
        numpy.ndarray: One-hot encoded labels
    """
    return to_categorical(labels, num_classes)

def create_data_splits(X, y, test_size=0.2, random_state=42):
    """
    Create stratified train/validation splits
    
    Args:
        X (numpy.ndarray): Images
        y (numpy.ndarray): Labels
        test_size (float): Fraction for validation
        random_state (int): Random seed
        
    Returns:
        tuple: (X_train, X_val, y_train, y_val)
    """
    return train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

def create_data_augmentation():
    """
    Create data augmentation pipeline
    
    Returns:
        ImageDataGenerator: Configured data generator
    """
    return ImageDataGenerator(
        rotation_range=15,          # Random rotation ±15 degrees
        width_shift_range=0.1,      # Horizontal shift ±10%
        height_shift_range=0.1,     # Vertical shift ±10%
        horizontal_flip=True,       # Random horizontal flipping
        zoom_range=0.1,             # Random zoom ±10%
        shear_range=0.1,            # Shear transformation ±10%
        fill_mode='nearest'         # Fill mode for transformations
    )

def calculate_dataset_statistics(X, y, class_names):
    """
    Calculate comprehensive dataset statistics
    
    Args:
        X (numpy.ndarray): Images
        y (numpy.ndarray): Labels
        class_names (list): List of class names
        
    Returns:
        dict: Dictionary containing statistics
    """
    stats = {
        'total_samples': len(X),
        'image_shape': X.shape[1:],
        'num_classes': len(class_names),
        'class_names': class_names,
        'pixel_mean': np.mean(X),
        'pixel_std': np.std(X),
        'pixel_min': np.min(X),
        'pixel_max': np.max(X)
    }
    
    # Calculate class distribution
    unique, counts = np.unique(np.argmax(y, axis=1), return_counts=True)
    stats['class_distribution'] = dict(zip(unique, counts))
    
    return stats

def save_preprocessing_report(stats, filename='preprocessing_report.txt'):
    """
    Save preprocessing statistics to file
    
    Args:
        stats (dict): Statistics dictionary
        filename (str): Output filename
    """
    with open(filename, 'w') as f:
        f.write("CIFAR-10 Preprocessing Report\n")
        f.write("=" * 40 + "\n\n")
        
        f.write(f"Total Samples: {stats['total_samples']}\n")
        f.write(f"Image Shape: {stats['image_shape']}\n")
        f.write(f"Number of Classes: {stats['num_classes']}\n")
        f.write(f"Pixel Statistics:\n")
        f.write(f"  Mean: {stats['pixel_mean']:.4f}\n")
        f.write(f"  Std: {stats['pixel_std']:.4f}\n")
        f.write(f"  Min: {stats['pixel_min']:.4f}\n")
        f.write(f"  Max: {stats['pixel_max']:.4f}\n\n")
        
        f.write("Class Distribution:\n")
        for class_idx, count in stats['class_distribution'].items():
            class_name = stats['class_names'][class_idx]
            f.write(f"  {class_name}: {count} samples\n")

# Example usage and testing
if __name__ == "__main__":
    print("CIFAR-10 Preprocessing Utilities")
    print("This module provides utility functions for data preprocessing.")
    print("Import this module to use the preprocessing functions in your pipeline.")
    
    # Test basic functionality
    test_image = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
    
    print(f"\nTesting with sample image shape: {test_image.shape}")
    print(f"Image validation: {validate_image(test_image)}")
    print(f"Blur level: {calculate_blur_level(test_image):.2f}")
    print(f"Occlusion detected: {detect_occlusion(test_image)}")
    
    # Test normalization
    normalized = normalize_images(test_image)
    print(f"Normalized range: [{normalized.min():.3f}, {normalized.max():.3f}]")
    
    print("\nPreprocessing utilities ready for use!")