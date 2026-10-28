from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Dict, List


def parse_args():
    parser = argparse.ArgumentParser(description="Train clinical triage model (TF-IDF baseline or ClinicalBERT scaffold).")
    parser.add_argument("--dataset", default="ml/data/clinical_symptom_dataset_sample.jsonl", help="Path to MIMIC-style JSONL dataset")
    parser.add_argument("--output-dir", default="ml/artifacts", help="Directory for model artifacts")
    parser.add_argument("--model-type", choices=["tfidf", "clinicalbert"], default="tfidf")
    parser.add_argument("--clinicalbert-model", default="emilyalsentzer/Bio_ClinicalBERT", help="Hugging Face model id")
    parser.add_argument("--epochs", type=int, default=2)
    return parser.parse_args()


def load_jsonl(path: Path) -> List[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def build_training_text(row: dict) -> str:
    note = str(row.get("note") or "").strip()
    symptoms = str(row.get("symptoms") or "").strip()
    language = str(row.get("language") or "en").strip()
    return f"{note} symptoms: {symptoms} language: {language}".strip()


def train_tfidf(dataset_rows: List[dict], output_dir: Path):
    import joblib
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    labels = sorted({row["label"] for row in dataset_rows})
    label_to_index: Dict[str, int] = {label: idx for idx, label in enumerate(labels)}

    x_train = [build_training_text(row) for row in dataset_rows]
    y_train = [label_to_index[row["label"]] for row in dataset_rows]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    x_vec = vectorizer.fit_transform(x_train)

    model = LogisticRegression(max_iter=300)
    model.fit(x_vec, y_train)

    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = output_dir / "triage_tfidf.joblib"
    joblib.dump(
        {
            "model": model,
            "vectorizer": vectorizer,
            "labels": labels,
            "meta": {
                "model_type": "tfidf_logistic_regression",
                "dataset_size": len(dataset_rows),
            },
        },
        artifact_path,
    )
    print(f"Saved TF-IDF artifact: {artifact_path}")


def train_clinicalbert(dataset_rows: List[dict], output_dir: Path, model_name: str, epochs: int):
    try:
        from datasets import Dataset
        from transformers import (
            AutoModelForSequenceClassification,
            AutoTokenizer,
            Trainer,
            TrainingArguments,
        )
    except Exception as exc:
        raise RuntimeError(
            "ClinicalBERT training requires transformers, datasets, and torch packages. "
            "Install requirements and retry."
        ) from exc

    labels = sorted({row["label"] for row in dataset_rows})
    label_to_index = {label: idx for idx, label in enumerate(labels)}

    records = [
        {
            "text": build_training_text(row),
            "label": label_to_index[row["label"]],
        }
        for row in dataset_rows
    ]

    ds = Dataset.from_list(records)
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    def tokenize_fn(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=128)

    tokenized = ds.map(tokenize_fn, batched=True)
    tokenized = tokenized.train_test_split(test_size=0.2, seed=42)

    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=len(labels))

    output_dir.mkdir(parents=True, exist_ok=True)
    run_dir = output_dir / "clinicalbert"

    args = TrainingArguments(
        output_dir=str(run_dir),
        num_train_epochs=epochs,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        learning_rate=2e-5,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_steps=10,
        remove_unused_columns=False,
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized["train"],
        eval_dataset=tokenized["test"],
        tokenizer=tokenizer,
    )

    trainer.train()

    model.save_pretrained(run_dir)
    tokenizer.save_pretrained(run_dir)
    (run_dir / "labels.json").write_text(json.dumps(labels, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Saved ClinicalBERT fine-tuned model: {run_dir}")


def main():
    args = parse_args()
    dataset_path = Path(args.dataset)
    output_dir = Path(args.output_dir)

    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    rows = load_jsonl(dataset_path)
    rows = [row for row in rows if row.get("label")]
    if len(rows) < 4:
        raise ValueError("Dataset too small. Add more labeled records for training.")

    if args.model_type == "tfidf":
        train_tfidf(rows, output_dir)
        return

    try:
        train_clinicalbert(rows, output_dir, args.clinicalbert_model, args.epochs)
    except Exception as exc:
        print(f"ClinicalBERT training failed ({exc}). Falling back to TF-IDF baseline.")
        train_tfidf(rows, output_dir)


if __name__ == "__main__":
    main()
