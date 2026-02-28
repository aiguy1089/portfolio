"""
Setup script for CIFAR-10 Neural Network Evaluation Project
D802 STN1 Task 4: Evaluation of the Network Architecture Model

This script installs required dependencies and verifies the environment.
"""

import subprocess
import sys
import importlib

def install_package(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed and importable."""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✓ {package_name} is available")
        return True
    except ImportError:
        print(f"✗ {package_name} is not available")
        return False

def main():
    """Main setup function."""
    print("="*60)
    print("CIFAR-10 Neural Network Evaluation Project Setup")
    print("="*60)
    
    # Required packages
    packages = [
        ("tensorflow", "tensorflow"),
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("scikit-learn", "sklearn"),
        ("pandas", "pandas"),
        ("Pillow", "PIL")
    ]
    
    print("\nChecking existing packages...")
    missing_packages = []
    
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\nInstalling {len(missing_packages)} missing packages...")
        for package in missing_packages:
            install_package(package)
    else:
        print("\n✓ All required packages are already installed!")
    
    print("\nVerifying TensorFlow GPU support...")
    try:
        import tensorflow as tf
        print(f"TensorFlow version: {tf.__version__}")
        
        # Check for GPU availability
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"✓ GPU support available: {len(gpus)} GPU(s) detected")
            for i, gpu in enumerate(gpus):
                print(f"  GPU {i}: {gpu.name}")
        else:
            print("⚠ No GPU detected. Training will use CPU (slower but functional)")
    except ImportError:
        print("✗ TensorFlow not available")
    
    print("\nEnvironment verification complete!")
    print("\nTo run the evaluation:")
    print("python cifar10_evaluation.py")
    print("="*60)

if __name__ == "__main__":
    main()