# Loan Approval Prediction - BCA Final Year Project

A complete machine learning mini-project to predict loan approval using applicant details.

## Features
- Data preprocessing with missing-value handling
- Model training using `RandomForestClassifier`
- Evaluation: Accuracy, Precision, Recall, F1, Confusion Matrix
- Saved model pipeline (`joblib`) for reuse
- Streamlit web app for real-time prediction

## Project Structure
- `src/train.py` - train and evaluate model
- `src/predict.py` - helper for single prediction
- `app.py` - Streamlit frontend
- `requirements.txt` - dependencies
- `data/loan_data.csv` - optional dataset (place your dataset here)

## Dataset
Use a CSV with columns like:
`Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History, Property_Area, Loan_Status`

`Loan_Status` should be `Y/N` (or `1/0`).

If your column names differ, update `FEATURE_COLUMNS` in `src/train.py`.

## Setup
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

## Train Model
```bash
python src/train.py --data data/loan_data.csv
```

This creates:
- `models/loan_pipeline.joblib`
- `models/metrics.json`

## Run App
```bash
streamlit run app.py
```

## Viva Tips (Short)
- Explain preprocessing (`SimpleImputer`, `OneHotEncoder`)
- Explain train-test split and why we evaluate on unseen data
- Explain confusion matrix and why `Credit_History` is influential

## Future Improvements
- Hyperparameter tuning (`GridSearchCV`)
- Try `XGBoost`/`LightGBM`
- Add user login + prediction history in DB
