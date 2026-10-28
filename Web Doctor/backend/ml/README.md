# Clinical Model Pipeline

This folder contains retraining tools for medical triage NLP.

## Dataset format (MIMIC-style JSONL)
Each line should be a JSON object:
- note: clinical or patient note text
- symptoms: extracted symptom text
- label: target condition label (must match a known condition profile)
- severity: target severity
- language: en/hi

Example file:
- data/clinical_symptom_dataset_sample.jsonl

## Train TF-IDF baseline
python ml/train_triage_model.py --model-type tfidf --dataset ml/data/clinical_symptom_dataset_sample.jsonl --output-dir ml/artifacts

This creates:
- ml/artifacts/triage_tfidf.joblib

## Train ClinicalBERT (when environment is ready)
python ml/train_triage_model.py --model-type clinicalbert --clinicalbert-model emilyalsentzer/Bio_ClinicalBERT --epochs 2

Note: ClinicalBERT training needs transformers + torch + datasets and a larger real clinical dataset.
If ClinicalBERT download/training fails (restricted network/SSL), the trainer automatically falls back to TF-IDF and still creates `ml/artifacts/triage_tfidf.joblib`.

## Convert raw input files
python ml/prepare_mimic_style_dataset.py --input your_records.json --output ml/data/converted.jsonl
