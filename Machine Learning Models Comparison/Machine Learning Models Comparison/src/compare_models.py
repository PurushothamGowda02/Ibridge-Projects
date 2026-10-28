import argparse
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def parse_args():
    parser = argparse.ArgumentParser(description="Compare ML classification models on a dataset")
    parser.add_argument("--data", type=str, default="", help="Path to CSV dataset file")
    parser.add_argument("--target", type=str, default="", help="Target column name (required for CSV)")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test split ratio")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed")
    parser.add_argument("--cv", type=int, default=5, help="Cross-validation folds")
    parser.add_argument("--outdir", type=str, default="outputs", help="Output directory")
    parser.add_argument(
        "--drop-cols",
        type=str,
        default="",
        help="Comma-separated columns to drop before training (for CSV datasets)",
    )
    return parser.parse_args()


def load_dataset(data_path: str, target_col: str, drop_cols_csv: str):
    if data_path:
        df = pd.read_csv(data_path)
        if not target_col:
            raise ValueError("Please provide --target when using a CSV dataset.")
        if target_col not in df.columns:
            raise ValueError(f"Target column '{target_col}' not found in dataset.")

        if drop_cols_csv.strip():
            drop_cols = [c.strip() for c in drop_cols_csv.split(",") if c.strip()]
            present_drop_cols = [c for c in drop_cols if c in df.columns and c != target_col]
            if present_drop_cols:
                df = df.drop(columns=present_drop_cols)

        X = df.drop(columns=[target_col])
        y = df[target_col]
        dataset_name = Path(data_path).stem
        return X, y, dataset_name

    # Default dataset for quick demo/presentation
    dataset = load_breast_cancer(as_frame=True)
    X = dataset.data
    y = dataset.target
    return X, y, "breast_cancer"


def build_preprocessor(X: pd.DataFrame):
    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = X.select_dtypes(exclude=["number"]).columns.tolist()

    numeric_transformer = Pipeline(
        steps=[("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols),
        ]
    )


def get_models(random_state: int):
    return {
        "Logistic Regression": LogisticRegression(max_iter=300, random_state=random_state, solver='lbfgs'),
        "Decision Tree": DecisionTreeClassifier(random_state=random_state, max_depth=10),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=random_state, max_depth=10, n_jobs=-1),
        "SVM": SVC(kernel="rbf", probability=True, random_state=random_state, cache_size=500),
        "KNN": KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
    }


def evaluate_models(X_train, X_test, y_train, y_test, preprocessor, models, cv_folds, progress_callback=None):
    results = []
    best = None

    # Check if we have enough samples for cross-validation
    n_classes = y_train.nunique()
    n_samples = len(y_train)
    
    # Determine if we can do CV
    can_do_cv = True
    effective_cv_folds = cv_folds
    
    if n_classes > n_samples * 0.8:
        # Too many unique classes, skip CV
        can_do_cv = False
        print(f"Warning: Skipping cross-validation due to high number of unique classes ({n_classes}).")
    else:
        min_samples_per_class = y_train.value_counts().min()
        effective_cv_folds = min(cv_folds, min_samples_per_class)
        
        if effective_cv_folds < 2:
            can_do_cv = False
            print(f"Warning: Skipping cross-validation due to insufficient samples per class.")
        elif effective_cv_folds < cv_folds:
            print(f"Warning: Reducing CV folds from {cv_folds} to {effective_cv_folds} due to small class sizes.")

    total_models = len(models)
    for idx, (model_name, model) in enumerate(models.items(), 1):
        try:
            if progress_callback:
                progress_callback(idx, total_models, model_name)
            
            pipeline = Pipeline(
                steps=[
                    ("preprocessor", preprocessor),
                    ("model", model),
                ]
            )

            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)

            acc = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average="weighted", zero_division=0)
            recall = recall_score(y_test, y_pred, average="weighted", zero_division=0)
            f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

            # Try cross-validation with error handling
            cv_mean = "N/A"
            cv_std = "N/A"
            
            if can_do_cv:
                try:
                    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=effective_cv_folds, scoring="accuracy")
                    cv_mean = round(cv_scores.mean(), 4)
                    cv_std = round(cv_scores.std(), 4)
                except Exception as e:
                    print(f"Warning: Cross-validation failed for {model_name}: {str(e)[:100]}")

            results.append(
                {
                    "Model": model_name,
                    "Accuracy": round(acc, 4),
                    "Precision": round(precision, 4),
                    "Recall": round(recall, 4),
                    "F1 Score": round(f1, 4),
                    "CV Mean Accuracy": cv_mean,
                    "CV Std": cv_std,
                }
            )

            if best is None or acc > best["accuracy"]:
                best = {
                    "name": model_name,
                    "accuracy": acc,
                    "pipeline": pipeline,
                    "y_pred": y_pred,
                }
        except Exception as e:
            print(f"Error training {model_name}: {str(e)[:100]}")
            # Continue with other models even if one fails
            continue

    return pd.DataFrame(results).sort_values(by="Accuracy", ascending=False), best


def save_visuals(results_df: pd.DataFrame, y_test, y_pred, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=results_df,
        x="Accuracy",
        y="Model",
        hue="Model",
        palette="viridis",
        legend=False,
    )
    plt.title("Model Accuracy Comparison")
    plt.xlim(0, 1)
    plt.tight_layout()
    plt.savefig(outdir / "accuracy_comparison.png", dpi=200)
    plt.close()

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.title("Confusion Matrix (Best Model)")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(outdir / "best_model_confusion_matrix.png", dpi=200)
    plt.close()


def main():
    args = parse_args()
    outdir = Path(args.outdir)

    X, y, dataset_name = load_dataset(args.data, args.target, args.drop_cols)

    try:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=args.test_size, random_state=args.random_state, stratify=y
        )
    except ValueError:
        print("Warning: Using non-stratified split due to small class sizes.")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=args.test_size, random_state=args.random_state
        )

    preprocessor = build_preprocessor(X)
    models = get_models(args.random_state)

    results_df, best = evaluate_models(
        X_train, X_test, y_train, y_test, preprocessor, models, args.cv
    )

    outdir.mkdir(parents=True, exist_ok=True)

    results_path = outdir / f"model_comparison_{dataset_name}.csv"
    results_df.to_csv(results_path, index=False)

    best_model_path = outdir / f"best_model_{dataset_name}.pkl"
    joblib.dump(best["pipeline"], best_model_path)

    save_visuals(results_df, y_test, best["y_pred"], outdir)

    print("\nModel comparison completed.")
    print(f"Dataset: {dataset_name}")
    print(f"Best model: {best['name']} (Accuracy: {best['accuracy']:.4f})")
    print(f"Results saved to: {results_path}")
    print(f"Best model saved to: {best_model_path}")
    print(f"Charts saved to: {outdir}")


if __name__ == "__main__":
    main()
