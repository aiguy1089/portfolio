# Minimal FastAPI stub to demonstrate deployment approach
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
from pathlib import Path
from typing import Dict, Any

app = FastAPI(title="D804_PA_Model_AdultIncome_XGB API")

MODEL_PATH = Path(__file__).resolve().parents[2] / "artifacts" / "adult" / "model" / "adult_xgb_pipeline.joblib"
_model = None

class PredictRequest(BaseModel):
    # Provide a simple schema example; real schema should match features after preprocessing
    features: Dict[str, Any]

@app.on_event("startup")
def load_model():
    global _model
    if MODEL_PATH.exists():
        _model = joblib.load(MODEL_PATH)

@app.post("/predict")
async def predict(req: PredictRequest):
    if _model is None:
        return {"error": "Model not loaded"}
    import pandas as pd
    X = pd.DataFrame([req.features])
    proba = _model.predict_proba(X)[:, 1][0]
    pred = int(proba >= 0.5)
    return {"probability": float(proba), "prediction": pred}

# Run: uvicorn scripts.deploy.fastapi_stub:app --reload --port 8000