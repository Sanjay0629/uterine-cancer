# Backend – Uterine Cancer Prediction API

This folder contains a **Python FastAPI** backend that calls a **Java scorer** built on top of `h2o-genmodel.jar` and your exported H2O MOJO model.

## Requirements

- Python 3.10+ installed and on `PATH`
- Java JDK (or JRE) installed and `java`/`javac` available on `PATH`
- The following files already exist (from your project):
  - `models/h2o-genmodel.jar`
  - `models/GBM_grid_1_AutoML_1_20251122_200215_model_3.zip`

## Python setup

From the project root:

```bash
cd backend
python -m venv .venv        # optional but recommended
.\.venv\Scripts\activate    # on Windows PowerShell

pip install --upgrade pip
pip install -r requirements.txt
```

## Compile the Java scorer

Still in the `backend` directory:

```bash
javac -cp .;models\h2o-genmodel.jar ModelScorer.java
```

This will produce `ModelScorer.class` in the same directory.

> **Note:** The Java class currently assumes:
> - A MOJO file at `models/GBM_grid_1_AutoML_1_20251122_200215_model_3.zip`
> - Three numeric features named `feature1`, `feature2`, `feature3`
>
> You MUST edit `ModelScorer.java` (feature names and count) and `PredictRequest` in `main.py`
> to match your real model schema.

## Run the FastAPI server

With the virtual environment activated:

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### Test endpoints

- Health check:

  ```bash
  curl http://localhost:8000/health
  ```

- Prediction (example body; update fields to your real ones):

  ```bash
  curl -X POST http://localhost:8000/predict ^
    -H "Content-Type: application/json" ^
    -d "{\"feature1\": 1.0, \"feature2\": 2.0, \"feature3\": 3.0}"
  ```

## How it works (high level)

- `main.py` defines:
  - `GET /health` – simple status endpoint
  - `POST /predict` – accepts JSON with feature values
  - Calls `java ModelScorer ...` via `subprocess.run`, passing the features as CLI arguments
- `ModelScorer.java`:
  - Loads the MOJO via `MojoModel.load(...)` using `h2o-genmodel.jar`
  - Maps CLI arguments to a `RowData`
  - Scores the row and prints the positive-class probability to stdout

