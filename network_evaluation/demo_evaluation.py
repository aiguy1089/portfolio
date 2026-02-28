"""
Demo Script for CIFAR-10 Neural Network Evaluation Project
D802 STN1 Task 4: Evaluation of the Network Architecture Model

This is a shortened demo version that runs quickly to demonstrate functionality.
For the full evaluation, run cifar10_evaluation.py
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

def demo_evaluation():
    """
    Run a quick demo of the evaluation process.
    """
    print("="*60)
    print("CIFAR-10 Neural Network Evaluation - DEMO VERSION")
    print("="*60)
    
    # Load a small subset of CIFAR-10 data
    print("\n1. Loading CIFAR-10 dataset (subset for demo)...")
    (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
    
    # Use only a small subset for demo
    x_train = x_train[:1000].astype('float32') / 255.0
    y_train = keras.utils.to_categorical(y_train[:1000], 10)
    x_test = x_test[:200].astype('float32') / 255.0
    y_test = keras.utils.to_categorical(y_test[:200], 10)
    
    print(f"Demo training set: {x_train.shape}")
    print(f"Demo test set: {x_test.shape}")
    
    # Build a simple model for demo
    print("\n2. Building demo CNN model...")
    model = models.Sequential([
        layers.Conv2D(16, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    print("Model architecture:")
    model.summary()
    
    # Train for just a few epochs
    print("\n3. Training model (demo - 3 epochs only)...")
    history = model.fit(
        x_train, y_train,
        validation_split=0.2,
        epochs=3,
        batch_size=32,
        verbose=1
    )
    
    # Evaluate model
    print("\n4. Evaluating model...")
    test_loss, test_accuracy = model.evaluate(x_test, y_test, verbose=0)
    print(f"Demo Test Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    
    # Create simple visualization
    print("\n5. Creating demo visualization...")
    plt.figure(figsize=(12, 4))
    
    # Loss curve
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'], label='Training Loss', marker='o')
    plt.plot(history.history['val_loss'], label='Validation Loss', marker='s')
    plt.title('Demo: Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Accuracy curve
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'], label='Training Accuracy', marker='o')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy', marker='s')
    plt.title('Demo: Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_training_curves.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Show some predictions
    print("\n6. Demo predictions on test samples...")
    predictions = model.predict(x_test[:5])
    class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
                   'dog', 'frog', 'horse', 'ship', 'truck']
    
    for i in range(5):
        true_class = np.argmax(y_test[i])
        pred_class = np.argmax(predictions[i])
        confidence = predictions[i][pred_class]
        
        print(f"Sample {i+1}:")
        print(f"  True class: {class_names[true_class]}")
        print(f"  Predicted: {class_names[pred_class]} (confidence: {confidence:.3f})")
        print(f"  Correct: {'✓' if true_class == pred_class else '✗'}")
    
    print("\n" + "="*60)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("\nThis was a shortened demo version.")
    print("For the complete evaluation with all requirements:")
    print("python cifar10_evaluation.py")
    print("\nDemo generated file: demo_training_curves.png")
    print("="*60)

if __name__ == "__main__":
    demo_evaluation()