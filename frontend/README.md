# Uterine Cancer Prediction System

## 🎯 Project Overview

An advanced **Uterine Cancer Risk Prediction System** designed to assess cancer risk using comprehensive clinical, molecular, and imaging data. This application serves as a unified platform for three distinct decision support modules.

**Live Demo**: [https://lovable.dev/projects/c6497165-f2a1-4a5d-831d-2413e4a4ed24](https://lovable.dev/projects/c6497165-f2a1-4a5d-831d-2413e4a4ed24)

---

## 🚀 Decision Support Modules

### 1. Clinical Risk Prediction (`/synthetic`)
*Status: Frontend Complete, Backend Mocked*
-   **Purpose**: Assessing general cancer risk using non-invasive clinical features.
-   **Features**:
    -   19-point comprehensive clinical form (Demographics, Symptoms, Medical History).
    -   Real-time validation.
    -   Risk stratification (Low/Medium/High).
    -   **AI Engine**: H2O.ai AutoML (Planned).

### 2. Molecular Prognostic Module (`/molecular`)
*Status: Fully Integrated*
-   **Purpose**: Predicting molecular subtypes (POLE, MSI, CN-Low, CN-High) and survival outcomes.
-   **Features**:
    -   Targeted input for TCGA-specific biomarkers (Mutation Count, MSI Scores, etc.).
    -   **Backend**: Flask API with XGBoost/RandomForest models.
    -   **Outputs**:
        -   Molecular Subtype Classification.
        -   Survival Probability & Risk Category.
        -   Confidence Scores.

### 3. Imaging Analysis Module (`/imaging`)
*Status: Initial Design*
-   **Purpose**: Deep learning analysis of ultrasound/MRI images.
-   **Features**:
    -   Image upload interface.
    -   **AI Engine**: Convolutional Neural Networks (CNN) (Planned).

---

## 🛠️ Technology Stack

### Frontend
-   **Framework**: React 18 + TypeScript + Vite
-   **Styling**: Tailwind CSS + shadcn/ui
-   **State/Routing**: React Router, React Hook Form
-   **Visuals**: Lucide Icons, Custom Medical Design System

### Backend Services
1.  **Molecular API** (Active):
    -   Python Flask
    -   scikit-learn, XGBoost
    -   RESTful Endpoints
2.  **Clinical API** (Planned):
    -   FastAPI
    -   H2O.ai MOJO
3.  **Database** (Planned):
    -   PostgreSQL

---

## 🏃 Getting Started

### Prerequisites
-   Node.js >= 18.0.0
-   Python 3.10+ (for Molecular backend)

### 1. Setup Frontend
```bash
cd frontend
npm install
npm run dev
```
The application will launch at `http://localhost:8080`.

### 2. Setup Molecular Backend
To enable predictions for the Molecular Module:
```bash
cd backend/tcga-ml
# Windows
.\start.bat
# Linux/Mac
./start.sh
```
The API serves at `http://localhost:5000`.

---

## 🔮 Future Roadmap

-   [ ] **Clinical Backend**: Integrate H2O.ai models with FastAPI.
-   [ ] **Imaging Backend**: Deploy CNN models for image analysis.
-   [ ] **Unified Database**: Patient history and longitudinal tracking.
-   [ ] **Report Generation**: PDF export for clinical records.

---

## 🤝 Contributing
This is a research prototype. Contributions are welcome for both UI enhancements and ML model improvements.

## 📄 License
Educational and Research Use Only.
