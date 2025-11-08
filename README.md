# Uterine Cancer Prediction System

## 🎯 Project Overview

An advanced **Uterine Cancer Risk Prediction System** designed to assess cancer risk using comprehensive clinical and pathological features. This application currently features a complete **frontend interface** (Design Phase) with planned integration of **H2O.ai AutoML** for real-time machine learning predictions.

**Live Demo**: [https://lovable.dev/projects/c6497165-f2a1-4a5d-831d-2413e4a4ed24](https://lovable.dev/projects/c6497165-f2a1-4a5d-831d-2413e4a4ed24)

---

## 🚀 Current Features (Frontend - v1.0)

### Pages & Functionality

1. **Home Page** (`/`)
   - Project overview with clear call-to-action
   - Feature highlights (AI-powered, clinical-grade, comprehensive)
   - How it works section (3-step process)
   - Responsive hero section with medical-themed design

2. **Prediction Form** (`/predict`)
   - Comprehensive input form with 19 clinical features:
     - **Demographics**: PatientID, Age, BMI, Menopause Status
     - **Symptoms**: Abnormal Bleeding, Pelvic Pain, Vaginal Discharge, Weight Loss
     - **Medical History**: Hypertension, Diabetes, Family History, Smoking, Estrogen Therapy
     - **Clinical Measurements**: Endometrium Thickness, CA125 Level, Parity, Gravidity
     - **Pathology**: Histology Type, Hormone Receptor Status
   - Form validation with React Hook Form
   - Loading animation during prediction
   - Color-coded results display (Green/Orange/Red risk levels)
   - Clinical recommendations

3. **About Page** (`/about`)
   - System overview and technology stack
   - Model performance metrics (PR-AUC focus)
   - Planned visualizations (ROC curves, feature importance, confusion matrix)
   - Input features breakdown
   - Future enhancement roadmap

### Design System

- **Medical-Grade UI**: Professional healthcare aesthetic
- **Color Palette**:
  - Primary: Soft medical blue (`hsl(210 85% 45%)`)
  - Risk levels: Green (low), Orange (moderate), Red (high)
  - Clean backgrounds with subtle gradients
- **Typography**: Clear, readable fonts optimized for clinical use
- **Responsive**: Mobile-first design, works on all devices
- **Accessibility**: High contrast, semantic HTML

---

## 🛠️ Technology Stack

### Frontend (Current)
- **React 18** - Modern UI library
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - High-quality component library
- **React Hook Form** - Form validation
- **React Router** - Client-side routing
- **Vite** - Fast build tool

### Backend (Planned)
- **H2O.ai AutoML** - Machine learning engine
- **FastAPI** - Python web framework
- **MOJO** - Model deployment format
- **SHAP** - Model explainability
- **PostgreSQL** - Database

---

## 📊 Machine Learning Details

### Target Variable
- **HasCancer** (Yes/No) - Binary classification target

### Input Features (19 total)
All features listed in the prediction form are used for model training.

### Evaluation Metrics
- **Primary**: PR-AUC (Precision-Recall Area Under Curve)
  - Optimal for imbalanced medical datasets
  - Focuses on positive class performance
- **Secondary**: Sensitivity (Recall), Specificity, ROC-AUC, Accuracy

### Model Explainability
- SHAP values for feature importance
- ROC and PR curves
- Confusion matrix analysis

---

## 🏃 Getting Started

### Prerequisites
- Node.js >= 18.0.0
- npm or yarn

### Installation

```bash
# Clone the repository
git clone <YOUR_GIT_URL>

# Navigate to project directory
cd uterine-cancer-predictor

# Install dependencies
npm install

# Start development server
npm run dev
```

The application will be available at `http://localhost:8080`

### Build for Production

```bash
npm run build
```

---

## 📁 Project Structure

```
src/
├── components/
│   ├── ui/                 # shadcn/ui components
│   └── Navigation.tsx      # Main navigation component
├── pages/
│   ├── Index.tsx          # Home page
│   ├── Predict.tsx        # Prediction form & results
│   ├── About.tsx          # About/methodology page
│   └── NotFound.tsx       # 404 page
├── hooks/                 # Custom React hooks
├── lib/                   # Utility functions
├── index.css             # Global styles & design system
└── App.tsx               # Main app component with routing
```

---

## 🔮 Future Development

### Phase 2: Backend Integration
- [ ] FastAPI server setup
- [ ] H2O.ai AutoML model training
- [ ] MOJO model deployment
- [ ] REST API endpoints (`/predict`, `/upload-model`, `/metrics`)
- [ ] Database integration (patient history)

### Phase 3: Advanced Features
- [ ] Real-time predictions with confidence scores
- [ ] Interactive model explainability dashboards
- [ ] Custom model upload (MOJO/H2O format)
- [ ] PDF report generation
- [ ] Historical prediction tracking
- [ ] User authentication & role management
- [ ] Multi-language support

---

## 🔒 API Design (Backend - Coming Soon)

### POST /predict
**Request:**
```json
{
  "PatientID": "P001",
  "Age": 55,
  "BMI": 26.8,
  "MenopauseStatus": "Post-menopausal",
  "AbnormalBleeding": "Yes",
  "PelvicPain": "No",
  "ThickEndometrium": 14.5,
  "Hypertension": "Yes",
  "Diabetes": "No",
  "FamilyHistoryCancer": "Yes",
  "Smoking": "No",
  "EstrogenTherapy": "Yes",
  "CA125_Level": 38.2,
  "HistologyType": "Endometrioid",
  "Parity": 2,
  "Gravidity": 3,
  "HormoneReceptorStatus": "Positive",
  "VaginalDischarge": "Yes",
  "UnexplainedWeightLoss": "No"
}
```

**Response:**
```json
{
  "cancer_presence": "Yes",
  "risk_level": "High",
  "one_year_recurrence": "Likely",
  "confidence": 0.87,
  "feature_importance": {...},
  "recommendations": [...]
}
```

---

## 📖 Design Decisions

### Why PR-AUC over ROC-AUC?
In medical diagnostics with imbalanced datasets (cancer is rare), PR-AUC provides more meaningful performance metrics by focusing on the precision-recall trade-off for positive cases.

### Static Results (Current Version)
The frontend currently displays **mock prediction results** to demonstrate the user experience. This will be replaced with real H2O.ai model predictions once the backend is integrated.

### Medical Design Theme
The UI uses soft blues, clean typography, and generous whitespace to create a professional, trustworthy interface appropriate for clinical settings.

---

## 🤝 Contributing

This is a design phase prototype. Contributions for UI improvements, bug fixes, and documentation are welcome.

---

## 📄 License

This project is for educational and research purposes.

---

## 📞 Support

For questions or issues, please open an issue on the repository.

---

**Note**: This application is in the **Design Phase**. The backend with H2O.ai AutoML integration will be implemented in future versions. Current predictions are simulated for demonstration purposes only.
