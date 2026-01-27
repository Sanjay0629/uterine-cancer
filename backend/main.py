from pathlib import Path
import subprocess
from typing import List, Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"


class PredictRequest(BaseModel):
    Age: float
    BMI: float
    MenopauseStatus: str
    AbnormalBleeding: str
    PelvicPain: str
    ThickEndometrium: float
    Hypertension: str
    Diabetes: str
    FamilyHistoryCancer: str
    Smoking: str
    EstrogenTherapy: str
    CA125_Level: float
    HistologyType: str
    Parity: float
    Gravidity: float
    HormoneReceptorStatus: str
    VaginalDischarge: str
    UnexplainedWeightLoss: str


class PredictResponse(BaseModel):
    predict: str  # "0" or "1"
    p0: float  # Probability of class 0
    p1: float  # Probability of class 1
    raw_output: str | None = None


app = FastAPI(title="Uterine Cancer Prediction API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.options("/predict")
async def options_predict(request: Request):
    """Handle CORS preflight for /predict endpoint"""
    return JSONResponse(
        content={"status": "ok"},
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        },
    )


def _normalize_categoricals(payload: PredictRequest) -> PredictRequest:
    """
    Map UI-friendly categorical values to the *exact* domain values expected by the H2O MOJO.
    Domain values were extracted from the MOJO (see backend/mojo.json).
    """
    menopause_map = {
        # MOJO: Perimenopausal, Postmenopausal, Premenopausal
        "Pre-menopausal": "Premenopausal",
        "Pre menopausal": "Premenopausal",
        "Premenopausal": "Premenopausal",
        "Post-menopausal": "Postmenopausal",
        "Post menopausal": "Postmenopausal",
        "Postmenopausal": "Postmenopausal",
        "Peri-menopausal": "Perimenopausal",
        "Perimenopausal": "Perimenopausal",
    }

    histology_map = {
        # MOJO: Clear Cell, Endometrioid, Normal, Other, Serous
        "ClearCell": "Clear Cell",
        "Clear Cell": "Clear Cell",
        "Endometrioid": "Endometrioid",
        "Serous": "Serous",
        "Other": "Other",
        "None": "Normal",
        "Normal": "Normal",
    }

    hrs_map = {
        # MOJO: Negative, Positive, Unknown
        "Positive": "Positive",
        "Negative": "Negative",
        "NotApplicable": "Unknown",
        "Not Applicable": "Unknown",
        "Unknown": "Unknown",
    }

    data = payload.model_dump()
    data["MenopauseStatus"] = menopause_map.get(data["MenopauseStatus"], data["MenopauseStatus"])
    data["HistologyType"] = histology_map.get(data["HistologyType"], data["HistologyType"])
    data["HormoneReceptorStatus"] = hrs_map.get(
        data["HormoneReceptorStatus"], data["HormoneReceptorStatus"]
    )
    return PredictRequest(**data)


def run_java_scorer(features: List[Any]) -> PredictResponse:
    """
    Call the Java ModelScorer class which uses h2o-genmodel.jar to score the MOJO model.
    """
    jar_path = MODELS_DIR / "h2o-genmodel.jar"
    if not jar_path.exists():
        raise HTTPException(status_code=500, detail=f"h2o-genmodel.jar not found at {jar_path}")

    # Build the classpath for Windows (use ';' as separator)
    classpath = f".;{jar_path}"

    # Convert features to strings for command-line arguments
    feature_args = [str(f) for f in features]

    cmd = [
        "java",
        "-cp",
        classpath,
        "ModelScorer",
        *feature_args,
    ]

    try:
        result = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        # java not found on PATH
        raise HTTPException(status_code=500, detail="Java runtime (java) not found on PATH.")

    if result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail=f"Java scorer error: {result.stderr.strip() or 'Unknown error'}",
        )

    stdout = result.stdout.strip()
    try:
        # Parse output format: "p0,p1,predict"
        parts = stdout.split(",")
        if len(parts) != 3:
            raise ValueError(f"Expected 3 comma-separated values, got {len(parts)}")
        
        p0 = float(parts[0])
        p1 = float(parts[1])
        predict = parts[2].strip()
        
        # Validate predict is "0" or "1"
        if predict not in ["0", "1"]:
            raise ValueError(f"Expected predict to be '0' or '1', got '{predict}'")
            
    except ValueError as e:
        # If parsing fails, return raw output for debugging
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected scorer output: {stdout}. Error: {str(e)}",
        )

    return PredictResponse(predict=predict, p0=p0, p1=p1, raw_output=stdout)


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    req = _normalize_categoricals(req)
    # Map request fields to a list in the order expected by ModelScorer
    # Order must match the featureNames array in ModelScorer.java
    features = [
        req.Age,
        req.BMI,
        req.MenopauseStatus,
        req.AbnormalBleeding,
        req.PelvicPain,
        req.ThickEndometrium,
        req.Hypertension,
        req.Diabetes,
        req.FamilyHistoryCancer,
        req.Smoking,
        req.EstrogenTherapy,
        req.CA125_Level,
        req.HistologyType,
        req.Parity,
        req.Gravidity,
        req.HormoneReceptorStatus,
        req.VaginalDischarge,
        req.UnexplainedWeightLoss,
    ]
    return run_java_scorer(features)

