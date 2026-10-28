from pathlib import Path

import streamlit as st

from src.predict import predict_loan_approval

st.set_page_config(page_title="Loan Approval Predictor", layout="centered")
st.title("Loan Approval Prediction")
st.caption("BCA Final Year ML Project")

with st.form("loan_form"):
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Married", ["Yes", "No"])
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["No", "Yes"])
    applicant_income = st.number_input("Applicant Income", min_value=0.0, value=5000.0)
    coapplicant_income = st.number_input("Coapplicant Income", min_value=0.0, value=0.0)
    loan_amount = st.number_input("Loan Amount (in thousands)", min_value=0.0, value=120.0)
    loan_term = st.number_input("Loan Amount Term (days)", min_value=0.0, value=360.0)
    credit_history = st.selectbox("Credit History", [1.0, 0.0])
    property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

    submitted = st.form_submit_button("Predict")

if submitted:
    input_data = {
        "Gender": gender,
        "Married": married,
        "Dependents": dependents,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_term,
        "Credit_History": credit_history,
        "Property_Area": property_area,
    }

    try:
        result = predict_loan_approval(input_data, Path("models/loan_pipeline.joblib"))
        st.success(f"Prediction: {result['prediction_label']}")
        if result["approval_probability"] is not None:
            st.info(f"Approval Probability: {result['approval_probability']:.2%}")
    except FileNotFoundError:
        st.error("Model not found. Please train first: python src/train.py --data data/loan_data.csv")
    except Exception as exc:
        st.error(f"Error: {exc}")
