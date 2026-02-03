# TCGA-UCEC Molecular Prognostic Module

This module provides a Flask API for predicting uterine cancer molecular subtypes and survival outcomes.

## Setup

1.  **Manual Step**: Copy the `models` folder from your original project to `backend/tcga-ml/models`.
    -   You should have `backend/tcga-ml/models/subtype_classification/best_model.pkl`
    -   You should have `backend/tcga-ml/models/survival_improved/xgboost_improved.pkl`
    -   You should have `backend/tcga-ml/models/preprocessors/scaler.pkl` etc.

2.  **Start the API**:
    -   **Windows**: Run `start.bat`
    -   **Linux/Mac**: Run `./start.sh`

    This will create a virtual environment, install dependencies, and start the server at `http://localhost:5000`.

## API Endpoints

### POST /predict
Accepts JSON data:
```json
{
  "diagnosisAge": 65,
  "mutationCount": 1250,
  "msiMantisScore": 0.45,
  "msiSensorScore": 0.35,
  "fractionGenomeAltered": 0.2,
  "raceCategory": "0" 
}
```

Returns:
```json
{
  "molecular_subtype": {
    "predicted_class": "POLE",
    "confidence": 0.95
  },
  "survival": {
    "prediction": "Living",
    "survival_probability": 0.9,
    "risk_category": "Low Risk"
  }
}
```
