from pathlib import Path
from typing import Dict, Any

import joblib
import pandas as pd

MODEL_PATH = Path("models/loan_pipeline.joblib")


def predict_loan_approval(input_data: Dict[str, Any], model_path: Path = MODEL_PATH):
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at {model_path}. Train the model first.")

    model = joblib.load(model_path)
    input_df = pd.DataFrame([input_data])

    pred = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0][1] if hasattr(model, "predict_proba") else None

    result = {
        "prediction_label": "Approved" if int(pred) == 1 else "Rejected",
        "prediction_value": int(pred),
        "approval_probability": float(proba) if proba is not None else None,
    }
    return result
