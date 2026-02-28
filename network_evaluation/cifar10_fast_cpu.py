"""
CIFAR-10 Neural Network Evaluation - CPU Optimized Version
Fast training optimized for CPU execution
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks, optimizers
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

# Set random seeds for reproducibility
np.random.seed(42)
tf.random.set_seed(42)

# CPU Optimizations
tf.config.threading.set_inter_op_parallelism_threads(4)
tf.config.threading.set_intra_op_parallelism_threads(4)

class FastCIFAR10Evaluator:
    """
    CPU-optimized CIFAR-10 evaluator for faster training
    """
    
    def __init__(self):
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
                           'dog', 'frog', 'horse', 'ship', 'truck']
        self.history = None
        self.model = None
        
    def load_and_preprocess_data(self):
        """Load and preprocess CIFAR-10 dataset"""
        print("Loading CIFAR-10 dataset...")
        
        # Load data
        (x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()
        
        # Normalize pixel values
        x_train = x_train.astype('float32') / 255.0
        x_test = x_test.astype('float32') / 255.0
        
        # Convert labels to categorical
        y_train = keras.utils.to_categorical(y_train, 10)
        y_test = keras.utils.to_categorical(y_test, 10)
        
        # Create validation split (smaller for faster training)
        val_size = 5000  # Reduced from 10000
        indices = np.random.permutation(len(x_train))
        train_indices = indices[val_size:]
        val_indices = indices[:val_size]
        
        self.x_train = x_train[train_indices]
        self.y_train = y_train[train_indices]
        self.x_val = x_train[val_indices]
        self.y_val = y_train[val_indices]
        self.x_test = x_test
        self.y_test = y_test
        
        print(f"Training samples: {len(self.x_train)}")
        print(f"Validation samples: {len(self.x_val)}")
        print(f"Test samples: {len(self.x_test)}")
        
    def create_optimized_model(self):
        """Create a smaller, faster model optimized for CPU training"""
        print("Creating optimized model...")
        
        model = models.Sequential([
            # Smaller convolutional layers
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            
            # Flatten and dense layers
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(10, activation='softmax')
        ])
        
        # Compile with efficient optimizer
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        print("Model created successfully!")
        model.summary()
        
    def train_model(self):
        """Train the model with optimized settings for CPU"""
        print("Starting optimized training...")
        
        # Callbacks for efficient training
        callbacks_list = [
            callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=5,  # Reduced patience
                restore_best_weights=True,
                verbose=1
            ),
            callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=3,
                min_lr=1e-7,
                verbose=1
            )
        ]
        
        # Train with larger batch size for CPU efficiency
        self.history = self.model.fit(
            self.x_train, self.y_train,
            batch_size=128,  # Larger batch size for CPU
            epochs=25,       # Reduced epochs
            validation_data=(self.x_val, self.y_val),
            callbacks=callbacks_list,
            verbose=1
        )
        
        print("Training completed!")
        
    def evaluate_model(self):
        """Evaluate the trained model"""
        print("Evaluating model...")
        
        # Test accuracy
        test_loss, test_accuracy = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print(f"Test Accuracy: {test_accuracy:.4f}")
        print(f"Test Loss: {test_loss:.4f}")
        
        # Predictions
        y_pred = self.model.predict(self.x_test, verbose=0)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true_classes = np.argmax(self.y_test, axis=1)
        
        # Classification report
        print("\nClassification Report:")
        print(classification_report(y_true_classes, y_pred_classes, 
                                   target_names=self.class_names))
        
        return test_accuracy, test_loss
        
    def plot_training_history(self):
        """Plot training history"""
        if self.history is None:
            print("No training history available!")
            return
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Accuracy plot
        ax1.plot(self.history.history['accuracy'], label='Training Accuracy')
        ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Loss plot
        ax2.plot(self.history.history['loss'], label='Training Loss')
        ax2.plot(self.history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('fast_training_history.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def plot_confusion_matrix(self):
        """Plot confusion matrix"""
        y_pred = self.model.predict(self.x_test, verbose=0)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true_classes = np.argmax(self.y_test, axis=1)
        
        cm = confusion_matrix(y_true_classes, y_pred_classes)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=self.class_names,
                   yticklabels=self.class_names)
        plt.title('Confusion Matrix - Fast CPU Training')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        plt.savefig('fast_confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.show()
        
    def run_complete_evaluation(self):
        """Run the complete evaluation pipeline"""
        print("="*60)
        print("CIFAR-10 Fast CPU Training - Starting Evaluation")
        print("="*60)
        
        # Load data
        self.load_and_preprocess_data()
        
        # Create model
        self.create_optimized_model()
        
        # Train model
        self.train_model()
        
        # Evaluate
        test_acc, test_loss = self.evaluate_model()
        
        # Create visualizations
        self.plot_training_history()
        self.plot_confusion_matrix()
        
        print("="*60)
        print("EVALUATION COMPLETE!")
        print(f"Final Test Accuracy: {test_acc:.4f}")
        print("="*60)
        
        return test_acc, test_loss

def main():
    """Main execution function"""
    evaluator = FastCIFAR10Evaluator()
    evaluator.run_complete_evaluation()

if __name__ == "__main__":
    main()