"""
Data Preprocessing Module for TCGA-UCEC Prognostic Module
This module contains functions for data cleaning, preprocessing, and preparation.

Author: TCGA-UCEC Project
Date: January 2026
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
import joblib
import os

class DataPreprocessor:
    """
    Main class for data preprocessing operations.
    Handles missing values, encoding, scaling, and train-test split.
    """
    
    def __init__(self, config=None):
        """
        Initialize the DataPreprocessor.
        
        Parameters:
        -----------
        config : dict, optional
            Configuration dictionary with preprocessing parameters
        """
        self.config = config or {}
        self.label_encoders = {}
        self.scaler = None
        self.imputer = None
        self.feature_names = None
        
    def load_data(self, filepath):
        """
        Load the dataset from CSV file.
        
        Parameters:
        -----------
        filepath : str
            Path to the CSV file
            
        Returns:
        --------
        pd.DataFrame
            Loaded dataframe
        """
        print(f"📂 Loading data from: {filepath}")
        df = pd.read_csv(filepath)
        print(f"✅ Data loaded successfully!")
        print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        return df
    
    def explore_data(self, df):
        """
        Print basic information about the dataset.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        """
        print("\n" + "="*70)
        print("📊 DATA EXPLORATION")
        print("="*70)
        
        print(f"\n1️⃣  Dataset Shape: {df.shape}")
        print(f"\n2️⃣  Column Names and Types:")
        print(df.dtypes)
        
        print(f"\n3️⃣  Missing Values:")
        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100).round(2)
        missing_df = pd.DataFrame({
            'Missing Count': missing,
            'Percentage': missing_pct
        })
        print(missing_df[missing_df['Missing Count'] > 0])
        
        print(f"\n4️⃣  Target Distribution (Subtype):")
        if 'Subtype' in df.columns:
            print(df['Subtype'].value_counts())
        
        print(f"\n5️⃣  Survival Status Distribution:")
        if 'Overall Survival Status' in df.columns:
            print(df['Overall Survival Status'].value_counts())
        
        print("\n" + "="*70)
    
    def remove_identifiers(self, df):
        """
        Remove patient and sample ID columns.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
            
        Returns:
        --------
        pd.DataFrame
            Dataframe without identifier columns
        """
        print("\n🔧 Removing identifier columns...")
        id_columns = ['Patient ID', 'Sample ID']
        columns_to_drop = [col for col in id_columns if col in df.columns]
        
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
            print(f"   ✓ Removed: {', '.join(columns_to_drop)}")
        else:
            print("   → No identifier columns found")
        
        return df
    
    def handle_missing_values(self, df, strategy='median'):
        """
        Handle missing values in the dataset.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        strategy : str, default='median'
            Imputation strategy ('mean', 'median', 'most_frequent')
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with imputed values
        """
        print(f"\n🔧 Handling missing values (strategy: {strategy})...")
        
        # Separate numeric and categorical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Impute numeric columns
        if numeric_cols:
            self.numeric_imputer = SimpleImputer(strategy=strategy)
            df[numeric_cols] = self.numeric_imputer.fit_transform(df[numeric_cols])
            print(f"   ✓ Imputed {len(numeric_cols)} numeric columns")
        
        # Impute categorical columns
        if categorical_cols:
            self.categorical_imputer = SimpleImputer(strategy='most_frequent')
            df[categorical_cols] = self.categorical_imputer.fit_transform(df[categorical_cols])
            print(f"   ✓ Imputed {len(categorical_cols)} categorical columns")
        
        print(f"   ✓ Missing values after imputation: {df.isnull().sum().sum()}")
        
        return df
    
    def encode_categorical_features(self, df, target_columns=None):
        """
        Encode categorical features using Label Encoding.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        target_columns : list, optional
            Columns to exclude from encoding (target variables)
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with encoded categorical features
        """
        print("\n🔧 Encoding categorical features...")
        
        target_columns = target_columns or []
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        # Remove target columns from encoding
        categorical_cols = [col for col in categorical_cols if col not in target_columns]
        
        for col in categorical_cols:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            self.label_encoders[col] = le
            print(f"   ✓ Encoded: {col} ({len(le.classes_)} classes)")
        
        return df
    
    def encode_target_variables(self, df):
        """
        Encode target variables (Subtype and Survival Status).
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with encoded target variables
        """
        print("\n🔧 Encoding target variables...")
        
        # Encode Subtype
        if 'Subtype' in df.columns:
            le_subtype = LabelEncoder()
            df['Subtype_Encoded'] = le_subtype.fit_transform(df['Subtype'])
            self.label_encoders['Subtype'] = le_subtype
            print(f"   ✓ Subtype: {len(le_subtype.classes_)} classes")
            print(f"      {dict(enumerate(le_subtype.classes_))}")
        
        # Encode Overall Survival Status
        if 'Overall Survival Status' in df.columns:
            # Convert to binary: 0 = Living, 1 = Deceased
            df['Survival_Binary'] = df['Overall Survival Status'].apply(
                lambda x: 1 if '1:DECEASED' in str(x) else 0
            )
            print(f"   ✓ Survival Status: Binary (0=Living, 1=Deceased)")
        
        # Encode Disease Free Status
        if 'Disease Free Status' in df.columns:
            df['Disease_Free_Binary'] = df['Disease Free Status'].apply(
                lambda x: 1 if '1:Recurred' in str(x) else 0
            )
            print(f"   ✓ Disease Free Status: Binary (0=Free, 1=Recurred)")
        
        return df
    
    def scale_features(self, X_train, X_test=None):
        """
        Scale numerical features using StandardScaler.
        
        Parameters:
        -----------
        X_train : pd.DataFrame
            Training features
        X_test : pd.DataFrame, optional
            Test features
            
        Returns:
        --------
        tuple
            (X_train_scaled, X_test_scaled) or X_train_scaled if X_test is None
        """
        print("\n🔧 Scaling features...")
        
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
        print(f"   ✓ Scaled training data: {X_train_scaled.shape}")
        
        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
            X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
            print(f"   ✓ Scaled test data: {X_test_scaled.shape}")
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled
    
    def prepare_features_and_targets(self, df):
        """
        Prepare feature matrix and target variables.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
            
        Returns:
        --------
        tuple
            (X, y_subtype, y_survival) feature matrix and target variables
        """
        print("\n🔧 Preparing features and targets...")
        
        # Define feature columns (exclude targets and identifiers)
        exclude_cols = [
            'Subtype', 'Subtype_Encoded',
            'Overall Survival Status', 'Survival_Binary',
            'Disease Free Status', 'Disease_Free_Binary',
            'Disease-specific Survival status',
            'Cancer Type Detailed', 'Tumor Type'  # These are redundant/categorical
        ]
        
        feature_cols = [col for col in df.columns if col not in exclude_cols]
        
        X = df[feature_cols]
        self.feature_names = feature_cols
        
        # Get targets
        y_subtype = df['Subtype_Encoded'] if 'Subtype_Encoded' in df.columns else None
        y_survival = df['Survival_Binary'] if 'Survival_Binary' in df.columns else None
        
        print(f"   ✓ Features: {X.shape[1]} columns")
        print(f"      {feature_cols}")
        if y_subtype is not None:
            print(f"   ✓ Subtype target: {len(y_subtype)} samples")
        if y_survival is not None:
            print(f"   ✓ Survival target: {len(y_survival)} samples")
        
        return X, y_subtype, y_survival
    
    def split_data(self, X, y, test_size=0.2, random_state=42, stratify=True):
        """
        Split data into training and testing sets.
        
        Parameters:
        -----------
        X : pd.DataFrame
            Feature matrix
        y : pd.Series
            Target variable
        test_size : float, default=0.2
        random_state : int, default=42
        stratify : bool, default=True
        
        Returns:
        --------
        tuple
            (X_train, X_test, y_train, y_test)
        """
        print(f"\n🔧 Splitting data (test_size={test_size})...")
        
        stratify_param = y if stratify else None
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=test_size,
            random_state=random_state,
            stratify=stratify_param
        )
        
        print(f"   ✓ Training set: {X_train.shape[0]} samples")
        print(f"   ✓ Test set: {X_test.shape[0]} samples")
        
        return X_train, X_test, y_train, y_test
    
    def save_processed_data(self, data_dict, output_dir='data/processed'):
        """
        Save processed data to CSV files.
        
        Parameters:
        -----------
        data_dict : dict
            Dictionary with dataframes to save
        output_dir : str
            Output directory path
        """
        print(f"\n💾 Saving processed data to {output_dir}...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        for name, df in data_dict.items():
            filepath = os.path.join(output_dir, f"{name}.csv")
            df.to_csv(filepath, index=False)
            print(f"   ✓ Saved: {name}.csv")
    
    def save_preprocessors(self, output_dir='models/preprocessors'):
        """
        Save preprocessing objects (encoders, scalers, imputers).
        
        Parameters:
        -----------
        output_dir : str
            Output directory path
        """
        print(f"\n💾 Saving preprocessors to {output_dir}...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save label encoders
        if self.label_encoders:
            joblib.dump(self.label_encoders, os.path.join(output_dir, 'label_encoders.pkl'))
            print(f"   ✓ Saved: label_encoders.pkl")
        
        # Save scaler
        if self.scaler:
            joblib.dump(self.scaler, os.path.join(output_dir, 'scaler.pkl'))
            print(f"   ✓ Saved: scaler.pkl")
        
        # Save imputers
        if hasattr(self, 'numeric_imputer'):
            joblib.dump(self.numeric_imputer, os.path.join(output_dir, 'numeric_imputer.pkl'))
            print(f"   ✓ Saved: numeric_imputer.pkl")
        
        if hasattr(self, 'categorical_imputer'):
            joblib.dump(self.categorical_imputer, os.path.join(output_dir, 'categorical_imputer.pkl'))
            print(f"   ✓ Saved: categorical_imputer.pkl")
        
        # Save feature names
        if self.feature_names:
            joblib.dump(self.feature_names, os.path.join(output_dir, 'feature_names.pkl'))
            print(f"   ✓ Saved: feature_names.pkl")
    
    def load_preprocessors(self, input_dir='models/preprocessors'):
        """
        Load preprocessing objects from saved files.
        
        Parameters:
        -----------
        input_dir : str
            Input directory path
        """
        print(f"\n📂 Loading preprocessors from {input_dir}...")
        
        # Load label encoders
        encoders_path = os.path.join(input_dir, 'label_encoders.pkl')
        if os.path.exists(encoders_path):
            self.label_encoders = joblib.load(encoders_path)
            print(f"   ✓ Loaded: label_encoders.pkl")
        
        # Load scaler
        scaler_path = os.path.join(input_dir, 'scaler.pkl')
        if os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path)
            print(f"   ✓ Loaded: scaler.pkl")
        
        # Load feature names
        features_path = os.path.join(input_dir, 'feature_names.pkl')
        if os.path.exists(features_path):
            self.feature_names = joblib.load(features_path)
            print(f"   ✓ Loaded: feature_names.pkl")


def preprocess_pipeline(data_path, output_dir='data/processed', save_preprocessors_dir='models/preprocessors'):
    """
    Complete preprocessing pipeline.
    
    Parameters:
    -----------
    data_path : str
        Path to raw data CSV file
    output_dir : str
        Directory to save processed data
    save_preprocessors_dir : str
        Directory to save preprocessing objects
        
    Returns:
    --------
    dict
        Dictionary containing all processed data and objects
    """
    print("\n" + "="*70)
    print("🚀 STARTING DATA PREPROCESSING PIPELINE")
    print("="*70)
    
    # Initialize preprocessor
    preprocessor = DataPreprocessor()
    
    # Load data
    df = preprocessor.load_data(data_path)
    
    # Explore data
    preprocessor.explore_data(df)
    
    # Preprocessing steps
    df = preprocessor.remove_identifiers(df)
    df = preprocessor.handle_missing_values(df, strategy='median')
    df = preprocessor.encode_target_variables(df)
    df = preprocessor.encode_categorical_features(df, target_columns=['Subtype', 'Overall Survival Status'])
    
    # Prepare features and targets
    X, y_subtype, y_survival = preprocessor.prepare_features_and_targets(df)
    
    # Split data for subtype classification
    X_train_sub, X_test_sub, y_train_sub, y_test_sub = preprocessor.split_data(
        X, y_subtype, test_size=0.2, random_state=42
    )
    
    # Split data for survival prediction
    X_train_surv, X_test_surv, y_train_surv, y_test_surv = preprocessor.split_data(
        X, y_survival, test_size=0.2, random_state=42
    )
    
    # Scale features
    X_train_sub_scaled, X_test_sub_scaled = preprocessor.scale_features(X_train_sub, X_test_sub)
    
    # Save processed data
    data_dict = {
        'X_train_subtype': X_train_sub_scaled,
        'X_test_subtype': X_test_sub_scaled,
        'y_train_subtype': y_train_sub,
        'y_test_subtype': y_test_sub,
        'X_train_survival': X_train_surv,
        'X_test_survival': X_test_surv,
        'y_train_survival': y_train_surv,
        'y_test_survival': y_test_surv,
    }
    
    preprocessor.save_processed_data(data_dict, output_dir)
    preprocessor.save_preprocessors(save_preprocessors_dir)
    
    print("\n" + "="*70)
    print("✅ PREPROCESSING PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*70)
    
    return {
        'preprocessor': preprocessor,
        'data': data_dict,
        'original_df': df
    }


if __name__ == "__main__":
    # Example usage
    data_path = 'data/raw/Uterine_Corpus_Endometrial_Carcinoma.csv'
    result = preprocess_pipeline(data_path)
    print("\n🎉 Data preprocessing complete! Ready for model training.")
