from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
import os
import sys

# Add src to the system path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper mappings
SUBTYPE_MAPPING = {
    0: "POLE",
    1: "MSI",
    2: "CN_LOW",
    3: "CN_HIGH"
}

RISK_MAPPING = {
    0: "Low Risk",
    1: "High Risk"
}

SURVIVAL_MAPPING = {
    0: "Living",
    1: "Deceased" 
}

# --- Load Models and Preprocessors ---
# Paths are relative to this script
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

# Placeholders for models
subtype_model = None
survival_model = None
scaler = None
label_encoders = {}
feature_names = []

def load_resources():
    global subtype_model, survival_model, scaler, label_encoders, feature_names
    
    try:
        print("Loading resources...")
        
        # Load Subtype Model
        subtype_path = os.path.join(MODELS_DIR, 'subtype_classification', 'best_model.pkl')
        if os.path.exists(subtype_path):
            subtype_model = joblib.load(subtype_path)
            print("✅ Subtype model loaded.")
        else:
            print(f"⚠️ Subtype model not found at {subtype_path}")

        # Load Survival Model
        survival_path = os.path.join(MODELS_DIR, 'survival_improved', 'xgboost_improved.pkl')
        if os.path.exists(survival_path):
            survival_model = joblib.load(survival_path)
            print("✅ Survival model loaded.")
        else:
            print(f"⚠️ Survival model not found at {survival_path}")

        # Load Preprocessors
        scaler_path = os.path.join(MODELS_DIR, 'preprocessors', 'scaler.pkl')
        if os.path.exists(scaler_path):
            scaler = joblib.load(scaler_path)
            print("✅ Scaler loaded.")
            
        feature_names_path = os.path.join(MODELS_DIR, 'preprocessors', 'feature_names.pkl')
        if os.path.exists(feature_names_path):
            feature_names = joblib.load(feature_names_path)
            print("✅ Feature names loaded.")
            
    except Exception as e:
        print(f"❌ Error loading resources: {e}")

# Initial load
load_resources()

def prepare_input_data(data):
    """
    Prepare input data for prediction.
    Matches the feature names expected by the model.
    """
    # Create DataFrame from input
    # Note: You need to map the frontend field names to the model's expected feature names
    # This is an approximation based on standard TCGA feature names.
    # YOU MAY NEED TO ADJUST THESE MAPPINGS BASED ON YOUR ACTUAL TRAINING DATA
    
    # Mapped exactly to model expectations
    input_dict = {
        'Mutation Count': [data.get('mutationCount')],
        'Fraction Genome Altered': [data.get('fractionGenomeAltered')],
        'Diagnosis Age': [data.get('diagnosisAge')],
        'MSI MANTIS Score': [data.get('msiMantisScore')],
        'MSIsensor Score': [data.get('msiSensorScore')],
        'Race Category': [int(data.get('raceCategory', 3))]
    }
    
    df = pd.DataFrame(input_dict)
    
    # Force column order to match model expectations exactly
    # Confirmed via inspection: ['Mutation Count', 'Fraction Genome Altered', 'Diagnosis Age', 'MSI MANTIS Score', 'MSIsensor Score', 'Race Category']
    expected_order = ['Mutation Count', 'Fraction Genome Altered', 'Diagnosis Age', 'MSI MANTIS Score', 'MSIsensor Score', 'Race Category']
    
    # Add any missing columns with default 0 if feature_names loaded has more
    if feature_names:
        for feature in feature_names:
            if feature not in df.columns:
                df[feature] = 0
        # Reorder to match loaded feature_names if available, otherwise use hardcoded expected_order
        df = df[feature_names] if feature_names else df[expected_order]
    else:
        df = df[expected_order] # Fallback if feature_names.pkl fails to load
        
    return df
    
    # Ensure all features expected by the model are present (fill with 0 or default if missing)
    if feature_names:
        for feature in feature_names:
            if feature not in df.columns:
                df[feature] = 0 # Default value for missing features
        
        # reorder columns
        df = df[feature_names]
        
    return df

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "models_loaded": subtype_model is not None}), 200

@app.route('/predict', methods=['POST'])
def predict():
    if not subtype_model and not survival_model:
        return jsonify({"error": "Models not loaded. Please ensure model files are in backend/tcga-ml/models/"}), 503

    try:
        data = request.json
        print(f"Received prediction request: {data}")
        
        # Prepare data
        df = prepare_input_data(data)
        
        # Scale data if scaler exists
        if scaler:
            df_scaled = pd.DataFrame(scaler.transform(df), columns=df.columns)
        else:
            df_scaled = df

        response_data = {
            "molecular_subtype": {},
            "survival": {}
        }

        # Subtype Prediction
        if subtype_model:
            subtype_pred = subtype_model.predict(df_scaled)[0]
            subtype_proba = subtype_model.predict_proba(df_scaled)[0]
            max_proba = float(max(subtype_proba))
            
            response_data["molecular_subtype"] = {
                "predicted_class": SUBTYPE_MAPPING.get(subtype_pred, str(subtype_pred)),
                "confidence": max_proba
            }
        else:
            response_data["molecular_subtype"] = {"error": "Subtype model not loaded"}

        # Survival Prediction
        if survival_model:
            survival_pred = survival_model.predict(df_scaled)[0]
            # XGBoost might return probability directly or class
            if hasattr(survival_model, "predict_proba"):
                survival_proba = survival_model.predict_proba(df_scaled)[0]
                # Assuming index 1 is positive class/deceased event depending on training
                # This needs validation against your specific model training
                prob_value = float(survival_proba[1]) 
            else:
                prob_value = 0.5 # Fallback
                
            prediction_label = SURVIVAL_MAPPING.get(survival_pred, "Unknown")
            
            # Risk Category logic (Simplified)
            risk = "Low Risk"
            if prob_value > 0.5:
                risk = "High Risk"

            response_data["survival"] = {
                "prediction": prediction_label,
                "survival_probability": 1.0 - prob_value, # Probability of surviving
                "risk_category": risk
            }
        else:
            response_data["survival"] = {"error": "Survival model not loaded"}

        return jsonify(response_data)

    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run on port 5000
    print("Starting TCGA ML API on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
