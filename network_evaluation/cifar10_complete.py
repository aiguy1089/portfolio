"""
CIFAR-10 Neural Network Evaluation - Complete Fixed Version
Optimized for CPU with no display issues
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, callbacks, optimizers
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
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

class CompleteCIFAR10Evaluator:
    """
    Complete CIFAR-10 evaluator with fixed display issues
    """
    
    def __init__(self):
        self.class_names = ['airplane', 'automobile', 'bird', 'cat', 'deer', 
                           'dog', 'frog', 'horse', 'ship', 'truck']
        self.history = None
        self.model = None
        self.results = {}
        
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
        
        # Create validation split
        val_size = 5000
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
        """Create optimized model"""
        print("Creating optimized model...")
        
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            
            layers.Flatten(),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(10, activation='softmax')
        ])
        
        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        print("Model created successfully!")
        model.summary()
        
    def train_model(self):
        """Train the model"""
        print("Starting training...")
        
        callbacks_list = [
            callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=5,
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
        
        self.history = self.model.fit(
            self.x_train, self.y_train,
            batch_size=128,
            epochs=25,
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
        
        # Store results
        self.results['test_accuracy'] = test_accuracy
        self.results['test_loss'] = test_loss
        
        # Predictions on smaller subset for speed
        print("Generating predictions...")
        test_subset = 1000  # Use subset for faster evaluation
        indices = np.random.choice(len(self.x_test), test_subset, replace=False)
        x_test_subset = self.x_test[indices]
        y_test_subset = self.y_test[indices]
        
        y_pred = self.model.predict(x_test_subset, verbose=0)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true_classes = np.argmax(y_test_subset, axis=1)
        
        # Classification report
        print("\nClassification Report (on subset):")
        report = classification_report(y_true_classes, y_pred_classes, 
                                     target_names=self.class_names, output_dict=True)
        print(classification_report(y_true_classes, y_pred_classes, 
                                   target_names=self.class_names))
        
        # Store for later use
        self.y_pred_classes = y_pred_classes
        self.y_true_classes = y_true_classes
        self.results['classification_report'] = report
        
        return test_accuracy, test_loss
        
    def create_visualizations(self):
        """Create all visualizations"""
        print("Creating visualizations...")
        
        # Training history plot
        if self.history is not None:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            
            # Accuracy plot
            ax1.plot(self.history.history['accuracy'], label='Training Accuracy', linewidth=2)
            ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy', linewidth=2)
            ax1.set_title('Model Accuracy', fontsize=14, fontweight='bold')
            ax1.set_xlabel('Epoch')
            ax1.set_ylabel('Accuracy')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # Loss plot
            ax2.plot(self.history.history['loss'], label='Training Loss', linewidth=2)
            ax2.plot(self.history.history['val_loss'], label='Validation Loss', linewidth=2)
            ax2.set_title('Model Loss', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Epoch')
            ax2.set_ylabel('Loss')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig('complete_training_history.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✅ Training history plot saved!")
        
        # Confusion matrix
        if hasattr(self, 'y_pred_classes'):
            cm = confusion_matrix(self.y_true_classes, self.y_pred_classes)
            
            plt.figure(figsize=(10, 8))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                       xticklabels=self.class_names,
                       yticklabels=self.class_names,
                       cbar_kws={'label': 'Count'})
            plt.title('Confusion Matrix - CIFAR-10 Classification', fontsize=16, fontweight='bold')
            plt.xlabel('Predicted Class', fontsize=12)
            plt.ylabel('True Class', fontsize=12)
            plt.tight_layout()
            plt.savefig('complete_confusion_matrix.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("✅ Confusion matrix saved!")
            
    def save_results_summary(self):
        """Save a comprehensive results summary"""
        print("Saving results summary...")
        
        summary = f"""
CIFAR-10 Neural Network Evaluation Results
==========================================

Model Architecture:
- Input: 32x32x3 RGB images
- Conv2D layers: 32, 64, 64 filters
- Dense layers: 64 units + 10 output classes
- Dropout: 0.5
- Optimizer: Adam (lr=0.001)

Training Configuration:
- Training samples: {len(self.x_train)}
- Validation samples: {len(self.x_val)}
- Test samples: {len(self.x_test)}
- Batch size: 128
- Max epochs: 25 (with early stopping)

Results:
- Test Accuracy: {self.results['test_accuracy']:.4f} ({self.results['test_accuracy']*100:.2f}%)
- Test Loss: {self.results['test_loss']:.4f}

Training History:
- Final training accuracy: {self.history.history['accuracy'][-1]:.4f}
- Final validation accuracy: {self.history.history['val_accuracy'][-1]:.4f}
- Total epochs trained: {len(self.history.history['accuracy'])}

Files Generated:
- complete_training_history.png: Training curves
- complete_confusion_matrix.png: Classification confusion matrix
- results_summary.txt: This summary file

Performance Analysis:
The model achieved {self.results['test_accuracy']*100:.1f}% accuracy on CIFAR-10, which is a solid result
for this optimized architecture. The training was completed efficiently on CPU
with proper regularization and early stopping.
"""
        
        with open('results_summary.txt', 'w') as f:
            f.write(summary)
        
        print("✅ Results summary saved!")
        
    def run_complete_evaluation(self):
        """Run the complete evaluation pipeline"""
        print("="*60)
        print("CIFAR-10 Complete Evaluation - Starting")
        print("="*60)
        
        try:
            # Load data
            self.load_and_preprocess_data()
            
            # Create model
            self.create_optimized_model()
            
            # Train model
            self.train_model()
            
            # Evaluate
            test_acc, test_loss = self.evaluate_model()
            
            # Create visualizations
            self.create_visualizations()
            
            # Save summary
            self.save_results_summary()
            
            print("="*60)
            print("🎉 EVALUATION COMPLETE!")
            print(f"📊 Final Test Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
            print(f"📈 Files generated: training_history.png, confusion_matrix.png, results_summary.txt")
            print("="*60)
            
            return test_acc, test_loss
            
        except Exception as e:
            print(f"❌ Error during evaluation: {str(e)}")
            return None, None

def main():
    """Main execution function"""
    evaluator = CompleteCIFAR10Evaluator()
    evaluator.run_complete_evaluation()

if __name__ == "__main__":
    main()