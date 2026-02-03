"""
Model Evaluation Module for TCGA-UCEC Prognostic Module
This module contains functions for evaluating models and generating visualizations.

Author: TCGA-UCEC Project
Date: January 2026
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report,
    roc_curve, auc, roc_auc_score,
    precision_recall_curve, average_precision_score
)
from sklearn.preprocessing import label_binarize
import os
import json


class ModelEvaluator:
    """
    Main class for model evaluation and visualization.
    """
    
    def __init__(self, output_dir='results'):
        """
        Initialize the ModelEvaluator.
        
        Parameters:
        -----------
        output_dir : str
            Output directory for saving figures and metrics
        """
        self.output_dir = output_dir
        self.metrics = {}
        
        # Set plotting style
        sns.set_style('whitegrid')
        plt.rcParams['figure.figsize'] = (10, 6)
        plt.rcParams['font.size'] = 10
    
    def calculate_metrics(self, y_true, y_pred, y_pred_proba=None, task_name=''):
        """
        Calculate comprehensive evaluation metrics.
        
        Parameters:
        -----------
        y_true : array-like
            True labels
        y_pred : array-like
            Predicted labels
        y_pred_proba : array-like, optional
            Prediction probabilities
        task_name : str
            Name of the task for organizing results
            
        Returns:
        --------
        dict
            Dictionary containing all metrics
        """
        print(f"\n📊 Calculating metrics for {task_name}...")
        
        # Basic metrics
        accuracy = accuracy_score(y_true, y_pred)
        
        # Handle multiclass vs binary
        n_classes = len(np.unique(y_true))
        average_method = 'weighted' if n_classes > 2 else 'binary'
        
        precision = precision_score(y_true, y_pred, average=average_method, zero_division=0)
        recall = recall_score(y_true, y_pred, average=average_method, zero_division=0)
        f1 = f1_score(y_true, y_pred, average=average_method, zero_division=0)
        
        metrics = {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'n_classes': int(n_classes)
        }
        
        # ROC-AUC for binary or multiclass
        if y_pred_proba is not None:
            try:
                if n_classes == 2:
                    # Binary classification
                    if y_pred_proba.ndim > 1:
                        y_pred_proba_pos = y_pred_proba[:, 1]
                    else:
                        y_pred_proba_pos = y_pred_proba
                    
                    roc_auc = roc_auc_score(y_true, y_pred_proba_pos)
                    avg_precision = average_precision_score(y_true, y_pred_proba_pos)
                else:
                    # Multiclass
                    roc_auc = roc_auc_score(y_true, y_pred_proba, 
                                           multi_class='ovr', average='weighted')
                    avg_precision = None
                
                metrics['roc_auc'] = float(roc_auc)
                if avg_precision:
                    metrics['avg_precision'] = float(avg_precision)
            except Exception as e:
                print(f"   ⚠️  Could not calculate ROC-AUC: {e}")
        
        # Print metrics
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"   Precision: {precision:.4f}")
        print(f"   Recall: {recall:.4f}")
        print(f"   F1-Score: {f1:.4f}")
        if 'roc_auc' in metrics:
            print(f"   ROC-AUC: {metrics['roc_auc']:.4f}")
        
        self.metrics[task_name] = metrics
        return metrics
    
    def plot_confusion_matrix(self, y_true, y_pred, class_names=None, 
                             task_name='', save=True):
        """
        Plot confusion matrix.
        
        Parameters:
        -----------
        y_true : array-like
            True labels
        y_pred : array-like
            Predicted labels
        class_names : list, optional
            Names of classes
        task_name : str
            Name of the task
        save : bool, default=True
            Whether to save the figure
        """
        print(f"\n📈 Plotting confusion matrix for {task_name}...")
        
        # Calculate confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # Create figure
        plt.figure(figsize=(10, 8))
        
        # Plot heatmap
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=class_names, yticklabels=class_names,
                   cbar_kws={'label': 'Count'})
        
        plt.title(f'Confusion Matrix - {task_name}', fontsize=14, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.tight_layout()
        
        if save:
            output_path = os.path.join(self.output_dir, 'figures', 
                                      task_name.lower().replace(' ', '_'))
            os.makedirs(output_path, exist_ok=True)
            filepath = os.path.join(output_path, 'confusion_matrix.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"   ✓ Saved: {filepath}")
        
        plt.show()
        plt.close()
    
    def plot_roc_curve(self, y_true, y_pred_proba, class_names=None,
                      task_name='', save=True):
        """
        Plot ROC curve.
        
        Parameters:
        -----------
        y_true : array-like
            True labels
        y_pred_proba : array-like
            Prediction probabilities
        class_names : list, optional
            Names of classes
        task_name : str
            Name of the task
        save : bool, default=True
            Whether to save the figure
        """
        print(f"\n📈 Plotting ROC curve for {task_name}...")
        
        n_classes = len(np.unique(y_true))
        
        plt.figure(figsize=(10, 8))
        
        if n_classes == 2:
            # Binary classification
            if y_pred_proba.ndim > 1:
                y_pred_proba_pos = y_pred_proba[:, 1]
            else:
                y_pred_proba_pos = y_pred_proba
            
            fpr, tpr, _ = roc_curve(y_true, y_pred_proba_pos)
            roc_auc = auc(fpr, tpr)
            
            plt.plot(fpr, tpr, color='darkorange', lw=2, 
                    label=f'ROC curve (AUC = {roc_auc:.3f})')
            plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
        else:
            # Multiclass - One vs Rest
            y_true_bin = label_binarize(y_true, classes=np.unique(y_true))
            
            for i in range(n_classes):
                fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_pred_proba[:, i])
                roc_auc = auc(fpr, tpr)
                
                class_label = class_names[i] if class_names else f'Class {i}'
                plt.plot(fpr, tpr, lw=2, 
                        label=f'{class_label} (AUC = {roc_auc:.3f})')
            
            plt.plot([0, 1], [0, 1], color='black', lw=2, linestyle='--', label='Random')
        
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontsize=12)
        plt.ylabel('True Positive Rate', fontsize=12)
        plt.title(f'ROC Curve - {task_name}', fontsize=14, fontweight='bold')
        plt.legend(loc='lower right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save:
            output_path = os.path.join(self.output_dir, 'figures', 
                                      task_name.lower().replace(' ', '_'))
            os.makedirs(output_path, exist_ok=True)
            filepath = os.path.join(output_path, 'roc_curve.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"   ✓ Saved: {filepath}")
        
        plt.show()
        plt.close()
    
    def plot_precision_recall_curve(self, y_true, y_pred_proba, 
                                    task_name='', save=True):
        """
        Plot precision-recall curve (for binary classification).
        
        Parameters:
        -----------
        y_true : array-like
            True labels
        y_pred_proba : array-like
            Prediction probabilities
        task_name : str
            Name of the task
        save : bool, default=True
            Whether to save the figure
        """
        print(f"\n📈 Plotting precision-recall curve for {task_name}...")
        
        # Only for binary classification
        if y_pred_proba.ndim > 1:
            y_pred_proba_pos = y_pred_proba[:, 1]
        else:
            y_pred_proba_pos = y_pred_proba
        
        precision, recall, _ = precision_recall_curve(y_true, y_pred_proba_pos)
        avg_precision = average_precision_score(y_true, y_pred_proba_pos)
        
        plt.figure(figsize=(10, 8))
        plt.plot(recall, precision, color='blue', lw=2,
                label=f'PR curve (AP = {avg_precision:.3f})')
        plt.xlabel('Recall', fontsize=12)
        plt.ylabel('Precision', fontsize=12)
        plt.title(f'Precision-Recall Curve - {task_name}', fontsize=14, fontweight='bold')
        plt.legend(loc='lower left')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save:
            output_path = os.path.join(self.output_dir, 'figures', 
                                      task_name.lower().replace(' ', '_'))
            os.makedirs(output_path, exist_ok=True)
            filepath = os.path.join(output_path, 'precision_recall_curve.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"   ✓ Saved: {filepath}")
        
        plt.show()
        plt.close()
    
    def plot_feature_importance(self, model, feature_names, top_n=20,
                               task_name='', save=True):
        """
        Plot feature importance.
        
        Parameters:
        -----------
        model : sklearn model
            Trained model with feature_importances_ attribute
        feature_names : list
            Names of features
        top_n : int, default=20
            Number of top features to display
        task_name : str
            Name of the task
        save : bool, default=True
            Whether to save the figure
        """
        print(f"\n📈 Plotting feature importance for {task_name}...")
        
        if not hasattr(model, 'feature_importances_'):
            print("   ⚠️  Model does not have feature_importances_ attribute")
            return
        
        # Get feature importances
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]
        
        # Create dataframe
        importance_df = pd.DataFrame({
            'Feature': [feature_names[i] for i in indices],
            'Importance': importances[indices]
        })
        
        # Plot
        plt.figure(figsize=(10, 8))
        sns.barplot(data=importance_df, x='Importance', y='Feature', palette='viridis')
        plt.title(f'Top {top_n} Feature Importance - {task_name}', 
                 fontsize=14, fontweight='bold')
        plt.xlabel('Importance', fontsize=12)
        plt.ylabel('Feature', fontsize=12)
        plt.tight_layout()
        
        if save:
            output_path = os.path.join(self.output_dir, 'figures', 
                                      task_name.lower().replace(' ', '_'))
            os.makedirs(output_path, exist_ok=True)
            filepath = os.path.join(output_path, 'feature_importance.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"   ✓ Saved: {filepath}")
        
        plt.show()
        plt.close()
        
        return importance_df
    
    def plot_model_comparison(self, comparison_df, metric='Test Accuracy',
                             task_name='', save=True):
        """
        Plot model comparison bar chart.
        
        Parameters:
        -----------
        comparison_df : pd.DataFrame
            Dataframe with model comparison results
        metric : str, default='Test Accuracy'
            Metric to compare
        task_name : str
            Name of the task
        save : bool, default=True
            Whether to save the figure
        """
        print(f"\n📈 Plotting model comparison for {task_name}...")
        
        plt.figure(figsize=(12, 6))
        
        # Sort by metric
        comparison_df_sorted = comparison_df.sort_values(metric, ascending=True)
        
        # Create horizontal bar plot
        plt.barh(comparison_df_sorted['Model'], comparison_df_sorted[metric], 
                color='steelblue')
        
        # Add value labels
        for i, v in enumerate(comparison_df_sorted[metric]):
            plt.text(v + 0.001, i, f'{v:.4f}', va='center')
        
        plt.xlabel(metric, fontsize=12)
        plt.ylabel('Model', fontsize=12)
        plt.title(f'Model Comparison - {task_name}', fontsize=14, fontweight='bold')
        plt.xlim([0, 1.05])
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        
        if save:
            output_path = os.path.join(self.output_dir, 'figures', 
                                      task_name.lower().replace(' ', '_'))
            os.makedirs(output_path, exist_ok=True)
            filepath = os.path.join(output_path, 'model_comparison.png')
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"   ✓ Saved: {filepath}")
        
        plt.show()
        plt.close()
    
    def print_classification_report(self, y_true, y_pred, class_names=None, task_name=''):
        """
        Print detailed classification report.
        
        Parameters:
        -----------
        y_true : array-like
            True labels
        y_pred : array-like
            Predicted labels
        class_names : list, optional
            Names of classes
        task_name : str
            Name of the task
        """
        print(f"\n" + "="*70)
        print(f"📊 Classification Report - {task_name}")
        print("="*70)
        
        report = classification_report(y_true, y_pred, target_names=class_names)
        print(report)
    
    def save_metrics(self, metrics, task_name='', filename=None):
        """
        Save metrics to JSON file.
        
        Parameters:
        -----------
        metrics : dict
            Dictionary of metrics
        task_name : str
            Name of the task
        filename : str, optional
            Custom filename
        """
        output_path = os.path.join(self.output_dir, 'metrics')
        os.makedirs(output_path, exist_ok=True)
        
        if filename is None:
            filename = f"{task_name.lower().replace(' ', '_')}_metrics.json"
        
        filepath = os.path.join(output_path, filename)
        
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=4)
        
        print(f"💾 Saved metrics: {filepath}")
    
    def evaluate_model(self, model, X_test, y_test, class_names=None,
                      feature_names=None, task_name='', save_all=True):
        """
        Complete evaluation pipeline for a model.
        
        Parameters:
        -----------
        model : sklearn model
            Trained model
        X_test : pd.DataFrame
            Test features
        y_test : pd.Series
            Test labels
        class_names : list, optional
            Names of classes
        feature_names : list, optional
            Names of features
        task_name : str
            Name of the task
        save_all : bool, default=True
            Whether to save all outputs
            
        Returns:
        --------
        dict
            Dictionary containing all metrics
        """
        print("\n" + "="*70)
        print(f"🔍 EVALUATING MODEL - {task_name}")
        print("="*70)
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
        
        # Calculate metrics
        metrics = self.calculate_metrics(y_true=y_test, y_pred=y_pred, 
                                        y_pred_proba=y_pred_proba, task_name=task_name)
        
        # Print classification report
        self.print_classification_report(y_test, y_pred, class_names, task_name)
        
        # Generate visualizations
        self.plot_confusion_matrix(y_test, y_pred, class_names, task_name, save=save_all)
        
        if y_pred_proba is not None:
            self.plot_roc_curve(y_test, y_pred_proba, class_names, task_name, save=save_all)
            
            if len(np.unique(y_test)) == 2:
                self.plot_precision_recall_curve(y_test, y_pred_proba, task_name, save=save_all)
        
        # Feature importance
        if feature_names and hasattr(model, 'feature_importances_'):
            importance_df = self.plot_feature_importance(model, feature_names, 
                                                        top_n=15, task_name=task_name, 
                                                        save=save_all)
        
        # Save metrics
        if save_all:
            self.save_metrics(metrics, task_name)
        
        print("\n✅ Evaluation complete!")
        
        return metrics


if __name__ == "__main__":
    print("Model Evaluation Module")
    print("Use this module by importing it in your evaluation scripts.")
