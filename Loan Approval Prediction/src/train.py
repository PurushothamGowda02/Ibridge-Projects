import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Update here if your dataset uses different names
FEATURE_COLUMNS = [
    "Gender",
    "Married",
    "Dependents",
    "Education",
    "Self_Employed",
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History",
    "Property_Area",
]

TARGET_COLUMN = "Loan_Status"


def normalize_target(series: pd.Series) -> pd.Series:
    mapping = {"Y": 1, "N": 0, "y": 1, "n": 0, 1: 1, 0: 0, "1": 1, "0": 0}
    normalized = series.map(mapping)
    if normalized.isna().any():
        unknown_values = series[normalized.isna()].unique().tolist()
        raise ValueError(f"Unsupported target values found: {unknown_values}")
    return normalized.astype(int)


def build_pipeline(categorical_features, numerical_features):
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    numerical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", categorical_pipeline, categorical_features),
            ("num", numerical_pipeline, numerical_features),
        ]
    )

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42,
        class_weight="balanced",
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ]
    )
    return pipeline


def train(data_path: Path, model_path: Path, metrics_path: Path):
    df = pd.read_csv(data_path)

    missing_features = [col for col in FEATURE_COLUMNS if col not in df.columns]
    if missing_features:
        raise ValueError(f"Missing feature columns in CSV: {missing_features}")
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"Target column '{TARGET_COLUMN}' not found in CSV")

    X = df[FEATURE_COLUMNS].copy()
    y = normalize_target(df[TARGET_COLUMN])

    categorical_features = X.select_dtypes(include=["object", "category"]).columns.tolist()
    numerical_features = [col for col in FEATURE_COLUMNS if col not in categorical_features]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = build_pipeline(categorical_features, numerical_features)
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "classification_report": classification_report(y_test, y_pred, zero_division=0),
        "train_shape": list(X_train.shape),
        "test_shape": list(X_test.shape),
    }

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, model_path)

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    print("Training complete")
    print(f"Model saved to: {model_path}")
    print(f"Metrics saved to: {metrics_path}")
    print(f"Accuracy: {metrics['accuracy']:.4f}")


def parse_args():
    parser = argparse.ArgumentParser(description="Train loan approval prediction model")
    parser.add_argument("--data", required=True, help="Path to CSV dataset")
    parser.add_argument("--model-out", default="models/loan_pipeline.joblib", help="Output model file")
    parser.add_argument("--metrics-out", default="models/metrics.json", help="Output metrics JSON")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    train(Path(args.data), Path(args.model_out), Path(args.metrics_out))
