"""
Environment Test Script for CIFAR-10 Neural Network Evaluation Project
D802 STN1 Task 4: Evaluation of the Network Architecture Model

This script tests the environment and runs a quick validation.
"""

import sys
import os

def test_imports():
    """Test all required imports."""
    print("Testing imports...")
    
    try:
        import tensorflow as tf
        print(f"✓ TensorFlow {tf.__version__}")
    except ImportError as e:
        print(f"✗ TensorFlow import failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✓ NumPy {np.__version__}")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ Matplotlib")
    except ImportError as e:
        print(f"✗ Matplotlib import failed: {e}")
        return False
    
    try:
        import seaborn as sns
        print("✓ Seaborn")
    except ImportError as e:
        print(f"✗ Seaborn import failed: {e}")
        return False
    
    try:
        from sklearn.metrics import classification_report
        print("✓ Scikit-learn")
    except ImportError as e:
        print(f"✗ Scikit-learn import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ Pandas")
    except ImportError as e:
        print(f"✗ Pandas import failed: {e}")
        return False
    
    return True

def test_tensorflow():
    """Test TensorFlow functionality."""
    print("\nTesting TensorFlow functionality...")
    
    try:
        import tensorflow as tf
        
        # Test basic operations
        a = tf.constant([1, 2, 3])
        b = tf.constant([4, 5, 6])
        c = tf.add(a, b)
        print(f"✓ Basic operations: {c.numpy()}")
        
        # Test GPU availability
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✓ GPU available: {len(gpus)} device(s)")
        else:
            print("⚠ No GPU available (CPU will be used)")
        
        # Test CIFAR-10 dataset loading
        print("Testing CIFAR-10 dataset loading...")
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
        print(f"✓ CIFAR-10 loaded: Train {x_train.shape}, Test {x_test.shape}")
        
        return True
        
    except Exception as e:
        print(f"✗ TensorFlow test failed: {e}")
        return False

def test_visualization():
    """Test visualization capabilities."""
    print("\nTesting visualization...")
    
    try:
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Create a simple test plot
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        plt.figure(figsize=(6, 4))
        plt.plot(x, y)
        plt.title("Test Plot")
        plt.savefig("test_plot.png")
        plt.close()
        
        if os.path.exists("test_plot.png"):
            print("✓ Matplotlib plotting works")
            os.remove("test_plot.png")  # Clean up
            return True
        else:
            print("✗ Plot file not created")
            return False
            
    except Exception as e:
        print(f"✗ Visualization test failed: {e}")
        return False

def main():
    """Main test function."""
    print("="*60)
    print("CIFAR-10 Neural Network Evaluation - Environment Test")
    print("="*60)
    
    # Test imports
    if not test_imports():
        print("\n✗ Import tests failed. Please install missing packages.")
        print("Run: python setup.py")
        return False
    
    # Test TensorFlow
    if not test_tensorflow():
        print("\n✗ TensorFlow tests failed.")
        return False
    
    # Test visualization
    if not test_visualization():
        print("\n✗ Visualization tests failed.")
        return False
    
    print("\n" + "="*60)
    print("✓ All tests passed! Environment is ready.")
    print("\nYou can now run the main evaluation:")
    print("python cifar10_evaluation.py")
    print("="*60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)