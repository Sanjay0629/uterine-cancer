"""
Model Training Module for TCGA-UCEC Prognostic Module
This module contains functions for training machine learning models.

Author: TCGA-UCEC Project
Date: January 2026
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
from imblearn.over_sampling import SMOTE
import joblib
import os
import json
from datetime import datetime


class ModelTrainer:
    """
    Main class for training machine learning models.
    Supports multiple algorithms and hyperparameter tuning.
    """
    
    def __init__(self, task='classification', random_state=42):
        """
        Initialize the ModelTrainer.
        
        Parameters:
        -----------
        task : str, default='classification'
            Task type ('classification' or 'regression')
        random_state : int, default=42
            Random state for reproducibility
        """
        self.task = task
        self.random_state = random_state
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.training_history = {}
        
    def get_models(self, n_classes=2):
        """
        Get dictionary of models to train.
        
        Parameters:
        -----------
        n_classes : int, default=2
            Number of classes (for multiclass classification)
            
        Returns:
        --------
        dict
            Dictionary of model name: model object
        """
        models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.random_state,
                n_jobs=-1
            ),
            'XGBoost': XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=self.random_state,
                n_jobs=-1,
                eval_metric='mlogloss' if n_classes > 2 else 'logloss'
            ),
            'Logistic Regression': LogisticRegression(
                max_iter=1000,
                random_state=self.random_state,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                max_depth=5,
                learning_rate=0.1,
                random_state=self.random_state
            ),
            'LightGBM': LGBMClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=self.random_state,
                n_jobs=-1,
                verbose=-1
            ),
            'SVM': SVC(
                kernel='rbf',
                C=1.0,
                probability=True,
                random_state=self.random_state
            )
        }
        
        return models
    
    def handle_class_imbalance(self, X_train, y_train, method='smote'):
        """
        Handle class imbalance using oversampling techniques.
        
        Parameters:
        -----------
        X_train : pd.DataFrame or np.ndarray
            Training features
        y_train : pd.Series or np.ndarray
            Training labels
        method : str, default='smote'
            Method to handle imbalance ('smote', 'none')
            
        Returns:
        --------
        tuple
            (X_train_resampled, y_train_resampled)
        """
        if method == 'smote':
            print("\n🔧 Handling class imbalance with SMOTE...")
            
            # Check class distribution
            unique, counts = np.unique(y_train, return_counts=True)
            print(f"   Original distribution: {dict(zip(unique, counts))}")
            
            # Apply SMOTE
            smote = SMOTE(random_state=self.random_state)
            X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
            
            # Check new distribution
            unique, counts = np.unique(y_resampled, return_counts=True)
            print(f"   After SMOTE: {dict(zip(unique, counts))}")
            
            return X_resampled, y_resampled
        
        return X_train, y_train
    
    def train_single_model(self, model, model_name, X_train, y_train, X_test, y_test, cv=5):
        """
        Train a single model and evaluate it.
        
        Parameters:
        -----------
        model : sklearn model
            Model object to train
        model_name : str
            Name of the model
        X_train : pd.DataFrame
            Training features
        y_train : pd.Series
            Training labels
        X_test : pd.DataFrame
            Test features
        y_test : pd.Series
            Test labels
        cv : int, default=5
            Number of cross-validation folds
            
        Returns:
        --------
        dict
            Dictionary containing trained model and metrics
        """
        print(f"\n{'='*70}")
        print(f"🎯 Training: {model_name}")
        print(f"{'='*70}")
        
        # Train model
        start_time = datetime.now()
        model.fit(X_train, y_train)
        training_time = (datetime.now() - start_time).total_seconds()
        
        print(f"✅ Training completed in {training_time:.2f} seconds")
        
        # Evaluate on training set
        train_score = model.score(X_train, y_train)
        print(f"   Training Accuracy: {train_score:.4f}")
        
        # Evaluate on test set
        test_score = model.score(X_test, y_test)
        print(f"   Test Accuracy: {test_score:.4f}")
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='accuracy')
        print(f"   CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        # Store results
        results = {
            'model': model,
            'model_name': model_name,
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'cv_scores': cv_scores,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'training_time': training_time
        }
        
        return results
    
    def train_all_models(self, X_train, y_train, X_test, y_test, 
                        handle_imbalance=True, cv=5):
        """
        Train all available models.
        
        Parameters:
        -----------
        X_train : pd.DataFrame
            Training features
        y_train : pd.Series
            Training labels
        X_test : pd.DataFrame
            Test features
        y_test : pd.Series
            Test labels
        handle_imbalance : bool, default=True
            Whether to handle class imbalance
        cv : int, default=5
            Number of cross-validation folds
            
        Returns:
        --------
        dict
            Dictionary containing all trained models and results
        """
        print("\n" + "="*70)
        print("🚀 STARTING MODEL TRAINING")
        print("="*70)
        
        # Handle class imbalance if requested
        if handle_imbalance:
            X_train_balanced, y_train_balanced = self.handle_class_imbalance(
                X_train, y_train, method='smote'
            )
        else:
            X_train_balanced, y_train_balanced = X_train, y_train
        
        # Get models
        n_classes = len(np.unique(y_train))
        models_dict = self.get_models(n_classes=n_classes)
        
        # Train each model
        results = {}
        for model_name, model in models_dict.items():
            result = self.train_single_model(
                model, model_name,
                X_train_balanced, y_train_balanced,
                X_test, y_test,
                cv=cv
            )
            results[model_name] = result
        
        # Find best model
        best_model_name = max(results, key=lambda x: results[x]['test_accuracy'])
        self.best_model_name = best_model_name
        self.best_model = results[best_model_name]['model']
        
        print("\n" + "="*70)
        print(f"🏆 BEST MODEL: {best_model_name}")
        print(f"   Test Accuracy: {results[best_model_name]['test_accuracy']:.4f}")
        print("="*70)
        
        self.models = results
        return results
    
    def hyperparameter_tuning(self, model_name, X_train, y_train, param_grid, cv=5):
        """
        Perform hyperparameter tuning using GridSearchCV.
        
        Parameters:
        -----------
        model_name : str
            Name of the model to tune
        X_train : pd.DataFrame
            Training features
        y_train : pd.Series
            Training labels
        param_grid : dict
            Parameter grid for GridSearchCV
        cv : int, default=5
            Number of cross-validation folds
            
        Returns:
        --------
        sklearn model
            Best model after tuning
        """
        print(f"\n🔧 Hyperparameter tuning for {model_name}...")
        
        # Get base model
        n_classes = len(np.unique(y_train))
        models_dict = self.get_models(n_classes=n_classes)
        base_model = models_dict[model_name]
        
        # Grid search
        grid_search = GridSearchCV(
            base_model,
            param_grid,
            cv=cv,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        print(f"   ✅ Best parameters: {grid_search.best_params_}")
        print(f"   ✅ Best CV score: {grid_search.best_score_:.4f}")
        
        return grid_search.best_estimator_
    
    def save_model(self, model, model_name, output_dir='models'):
        """
        Save trained model to disk.
        
        Parameters:
        -----------
        model : sklearn model
            Trained model to save
        model_name : str
            Name of the model
        output_dir : str
            Output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Create safe filename
        safe_name = model_name.lower().replace(' ', '_')
        filepath = os.path.join(output_dir, f"{safe_name}.pkl")
        
        joblib.dump(model, filepath)
        print(f"💾 Saved model: {filepath}")
    
    def save_all_models(self, output_dir='models', task_name=''):
        """
        Save all trained models.
        
        Parameters:
        -----------
        output_dir : str
            Output directory
        task_name : str
            Task name for organizing models (e.g., 'subtype_classification')
        """
        if not self.models:
            print("⚠️  No models to save. Train models first.")
            return
        
        if task_name:
            output_dir = os.path.join(output_dir, task_name)
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\n💾 Saving all models to {output_dir}...")
        
        for model_name, result in self.models.items():
            self.save_model(result['model'], model_name, output_dir)
        
        # Save best model separately
        if self.best_model:
            best_model_path = os.path.join(output_dir, 'best_model.pkl')
            joblib.dump(self.best_model, best_model_path)
            print(f"💾 Saved best model: {best_model_path}")
        
        print("✅ All models saved successfully!")
    
    def save_training_summary(self, output_dir='results/metrics', task_name=''):
        """
        Save training summary as JSON.
        
        Parameters:
        -----------
        output_dir : str
            Output directory
        task_name : str
            Task name for file naming
        """
        if not self.models:
            print("⚠️  No training results to save.")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Prepare summary
        summary = {}
        for model_name, result in self.models.items():
            summary[model_name] = {
                'train_accuracy': float(result['train_accuracy']),
                'test_accuracy': float(result['test_accuracy']),
                'cv_mean': float(result['cv_mean']),
                'cv_std': float(result['cv_std']),
                'training_time': float(result['training_time'])
            }
        
        summary['best_model'] = self.best_model_name
        
        # Save to JSON
        filename = f"{task_name}_training_summary.json" if task_name else "training_summary.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(summary, f, indent=4)
        
        print(f"💾 Saved training summary: {filepath}")
    
    def load_model(self, filepath):
        """
        Load a saved model.
        
        Parameters:
        -----------
        filepath : str
            Path to saved model
            
        Returns:
        --------
        sklearn model
            Loaded model
        """
        model = joblib.load(filepath)
        print(f"📂 Loaded model from: {filepath}")
        return model
    
    def get_comparison_dataframe(self):
        """
        Get a comparison dataframe of all models.
        
        Returns:
        --------
        pd.DataFrame
            Comparison dataframe
        """
        if not self.models:
            print("⚠️  No models to compare. Train models first.")
            return None
        
        data = []
        for model_name, result in self.models.items():
            data.append({
                'Model': model_name,
                'Train Accuracy': result['train_accuracy'],
                'Test Accuracy': result['test_accuracy'],
                'CV Mean': result['cv_mean'],
                'CV Std': result['cv_std'],
                'Training Time (s)': result['training_time']
            })
        
        df = pd.DataFrame(data)
        df = df.sort_values('Test Accuracy', ascending=False)
        
        return df


def train_subtype_classification_models(X_train, y_train, X_test, y_test):
    """
    Train models for molecular subtype classification.
    
    Parameters:
    -----------
    X_train : pd.DataFrame
        Training features
    y_train : pd.Series
        Training labels (subtype)
    X_test : pd.DataFrame
        Test features
    y_test : pd.Series
        Test labels (subtype)
        
    Returns:
    --------
    ModelTrainer
        Trained ModelTrainer object
    """
    print("\n" + "="*70)
    print("🧬 MOLECULAR SUBTYPE CLASSIFICATION")
    print("="*70)
    
    trainer = ModelTrainer(task='classification', random_state=42)
    results = trainer.train_all_models(
        X_train, y_train, X_test, y_test,
        handle_imbalance=True,
        cv=5
    )
    
    # Save models
    trainer.save_all_models(output_dir='models', task_name='subtype_classification')
    trainer.save_training_summary(output_dir='results/metrics', task_name='subtype_classification')
    
    return trainer


def train_survival_prediction_models(X_train, y_train, X_test, y_test):
    """
    Train models for survival prediction.
    
    Parameters:
    -----------
    X_train : pd.DataFrame
        Training features
    y_train : pd.Series
        Training labels (survival)
    X_test : pd.DataFrame
        Test features
    y_test : pd.Series
        Test labels (survival)
        
    Returns:
    --------
    ModelTrainer
        Trained ModelTrainer object
    """
    print("\n" + "="*70)
    print("💊 SURVIVAL PREDICTION")
    print("="*70)
    
    trainer = ModelTrainer(task='classification', random_state=42)
    results = trainer.train_all_models(
        X_train, y_train, X_test, y_test,
        handle_imbalance=True,
        cv=5
    )
    
    # Save models
    trainer.save_all_models(output_dir='models', task_name='survival_prediction')
    trainer.save_training_summary(output_dir='results/metrics', task_name='survival_prediction')
    
    return trainer


if __name__ == "__main__":
    print("Model Training Module")
    print("Use this module by importing it in your training scripts.")
