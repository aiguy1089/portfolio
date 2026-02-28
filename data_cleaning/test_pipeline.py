"""
Test script to verify the CIFAR-10 data cleaning pipeline
"""

import sys
import os

def test_imports():
    """Test if all required packages are available"""
    print("Testing package imports...")
    
    try:
        import numpy as np
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ Pandas imported successfully")
    except ImportError as e:
        print(f"✗ Pandas import failed: {e}")
        return False
    
    try:
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ Matplotlib imported successfully")
    except ImportError as e:
        print(f"✗ Matplotlib import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✓ PIL imported successfully")
    except ImportError as e:
        print(f"✗ PIL import failed: {e}")
        return False
    
    try:
        import tensorflow as tf
        print("✓ TensorFlow imported successfully")
        print(f"  TensorFlow version: {tf.__version__}")
    except ImportError as e:
        print(f"✗ TensorFlow import failed: {e}")
        return False
    
    try:
        from sklearn.model_selection import train_test_split
        print("✓ Scikit-learn imported successfully")
    except ImportError as e:
        print(f"✗ Scikit-learn import failed: {e}")
        return False
    
    return True

def test_cifar10_loading():
    """Test CIFAR-10 dataset loading"""
    print("\nTesting CIFAR-10 dataset loading...")
    
    try:
        import tensorflow as tf
        (X_train, y_train), (X_test, y_test) = tf.keras.datasets.cifar10.load_data()
        
        print(f"✓ CIFAR-10 loaded successfully")
        print(f"  Training data shape: {X_train.shape}")
        print(f"  Training labels shape: {y_train.shape}")
        print(f"  Test data shape: {X_test.shape}")
        print(f"  Test labels shape: {y_test.shape}")
        print(f"  Data type: {X_train.dtype}")
        print(f"  Pixel value range: {X_train.min()} - {X_train.max()}")
        
        return True
        
    except Exception as e:
        print(f"✗ CIFAR-10 loading failed: {e}")
        return False

def main():
    """Main test function"""
    print("="*60)
    print("CIFAR-10 Data Cleaning Pipeline Test")
    print("="*60)
    
    # Test imports
    if not test_imports():
        print("\n✗ Some required packages are missing. Please install them using:")
        print("pip install -r requirements.txt")
        return False
    
    # Test CIFAR-10 loading
    if not test_cifar10_loading():
        print("\n✗ CIFAR-10 dataset loading failed.")
        return False
    
    print("\n" + "="*60)
    print("✓ All tests passed! Ready to run the data cleaning pipeline.")
    print("Run: python cifar10_data_cleaning.py")
    print("="*60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)