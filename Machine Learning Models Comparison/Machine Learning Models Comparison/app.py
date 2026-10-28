from io import BytesIO
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from src.compare_models import build_preprocessor, evaluate_models, get_models


st.set_page_config(page_title="ML Model Comparison", page_icon="??", layout="wide")
st.title("Machine Learning Model Comparison Dashboard")
st.caption("BCA Final Year Project: Compare classification models on real-world datasets")

with st.sidebar:
    st.header("Configuration")
    test_size = st.slider("Test size", min_value=0.1, max_value=0.4, value=0.2, step=0.05)
    cv_folds = st.slider("CV folds", min_value=3, max_value=10, value=5, step=1)
    random_state = st.number_input("Random state", min_value=0, value=42, step=1)

st.subheader("1) Select Dataset")
source = st.radio("Choose input source", ["Use built-in Telco Churn CSV", "Upload CSV"], horizontal=True)

df = None
dataset_name = "dataset"

if source == "Use built-in Telco Churn CSV":
    default_path = Path("data/telco_churn.csv")
    if default_path.exists():
        df = pd.read_csv(default_path)
        dataset_name = default_path.stem
        st.success(f"Loaded {default_path} with shape {df.shape}")
    else:
        st.warning("`data/telco_churn.csv` not found. Upload a CSV below.")
else:
    uploaded = st.file_uploader("Upload your dataset (.csv)", type=["csv"])
    if uploaded is not None:
        df = pd.read_csv(uploaded)
        dataset_name = Path(uploaded.name).stem
        st.success(f"✅ Loaded **{uploaded.name}** with shape **{df.shape}**")
        st.info("👇 **Next step:** Select target column below and click 'Run Model Comparison' to train models")

if df is not None:
    st.subheader("2) Dataset Preview")
    st.dataframe(df.head(20), use_container_width=True)
    
    # Show dataset info
    with st.expander("📊 Dataset Information", expanded=False):
        st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
        st.write(f"**Columns:** {', '.join(df.columns.tolist())}")
        st.write(f"**Missing values:** {df.isnull().sum().sum()} total")
        st.write("**Data types:**")
        st.dataframe(pd.DataFrame({
            'Column': df.dtypes.index,
            'Type': df.dtypes.values,
            'Missing': df.isnull().sum().values,
            'Unique': [df[col].nunique() for col in df.columns]
        }), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        target_col = st.selectbox("Target column", options=df.columns.tolist())
        
        # Show target column info
        if target_col:
            n_unique = df[target_col].nunique()
            st.info(f"**Target '{target_col}':** {n_unique} unique values")
            if n_unique <= 20:
                st.write("**Class distribution:**")
                st.write(df[target_col].value_counts().to_dict())
            
            # Warnings about target selection
            if n_unique == len(df):
                st.error("⚠️ Every row has a unique value - this looks like an ID column!")
            elif n_unique > 100:
                st.warning(f"⚠️ {n_unique} unique classes - this might be better for regression")
            elif n_unique < 2:
                st.error("⚠️ Only 1 unique value - cannot train classification model")
                
    with col2:
        available_options = [c for c in df.columns if c != target_col]
        default_drop_candidates = ["customerID", "PassengerId", "Name", "Ticket", "Cabin"]
        drop_cols = st.multiselect(
            "Columns to drop (optional)",
            options=available_options,
            default=[c for c in default_drop_candidates if c in available_options],
        )

    run_btn = st.button("🚀 Run Model Comparison", type="primary", use_container_width=True)

    if run_btn:
        st.divider()
        st.subheader("🔄 Training Models...")
        
        work_df = df.drop(columns=drop_cols, errors="ignore").copy()
        X = work_df.drop(columns=[target_col])
        y = work_df[target_col]
        
        # Data validation - just warnings, not blocking
        n_classes = y.nunique()
        n_samples = len(y)
        
        st.info(f"📊 Training on **{n_samples} samples** with **{n_classes} classes** using **{X.shape[1]} features**")
        
        # Show informational warnings but don't stop execution
        if n_classes == n_samples:
            st.warning(f"⚠️ Every row has a unique value in '{target_col}'. This might be an ID column. Results may not be meaningful for classification.")
        elif n_classes > n_samples * 0.5:
            st.warning(f"⚠️ Dataset has {n_classes} unique classes with {n_samples} samples. This might be better suited for regression.")
        
        if n_classes > 100:
            st.info(f"ℹ️ Large number of classes ({n_classes}). Training may take longer and use more memory.")

        try:
            # Try stratified split first
            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X,
                    y,
                    test_size=test_size,
                    random_state=int(random_state),
                    stratify=y,
                )
            except ValueError:
                # Fall back to non-stratified split if classes have too few samples
                st.warning("Using non-stratified split due to small class sizes.")
                X_train, X_test, y_train, y_test = train_test_split(
                    X,
                    y,
                    test_size=test_size,
                    random_state=int(random_state),
                )

            preprocessor = build_preprocessor(X)
            models = get_models(int(random_state))
            
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(current, total, model_name):
                progress = int((current - 1) / total * 100)
                progress_bar.progress(progress)
                status_text.text(f"🔄 Training model {current}/{total}: {model_name}...")
            
            status_text.text("🔄 Starting model training...")
            
            results_df, best = evaluate_models(
                X_train, X_test, y_train, y_test, preprocessor, models, cv_folds, update_progress
            )
            
            progress_bar.progress(100)
            status_text.text("✅ Training completed!")
            
            import time
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()

            st.subheader("3) Results")
            c1, c2, c3 = st.columns(3)
            c1.metric("Best Model", best["name"])
            c2.metric("Best Accuracy", f"{best['accuracy']:.4f}")
            c3.metric("Rows Used", f"{len(work_df)}")

            st.dataframe(results_df, use_container_width=True)

            st.subheader("4) Visualizations")
            left, right = st.columns(2)

            with left:
                fig1, ax1 = plt.subplots(figsize=(8, 5))
                sns.barplot(
                    data=results_df,
                    x="Accuracy",
                    y="Model",
                    hue="Model",
                    palette="viridis",
                    legend=False,
                    ax=ax1,
                )
                ax1.set_xlim(0, 1)
                ax1.set_title("Accuracy Comparison")
                st.pyplot(fig1)

            with right:
                fig2, ax2 = plt.subplots(figsize=(6, 5))
                cm = confusion_matrix(y_test, best["y_pred"])
                sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax2)
                ax2.set_title("Confusion Matrix (Best Model)")
                ax2.set_xlabel("Predicted")
                ax2.set_ylabel("Actual")
                st.pyplot(fig2)

            st.subheader("5) Download Outputs")
            csv_bytes = results_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download Results CSV",
                data=csv_bytes,
                file_name=f"model_comparison_{dataset_name}.csv",
                mime="text/csv",
            )

            model_buffer = BytesIO()
            joblib.dump(best["pipeline"], model_buffer)
            model_buffer.seek(0)
            st.download_button(
                "Download Best Model (.pkl)",
                data=model_buffer,
                file_name=f"best_model_{dataset_name}.pkl",
                mime="application/octet-stream",
            )

        except Exception as exc:
            st.error(f"❌ Error while training models: {exc}")
            
            # Show more helpful error information
            with st.expander("🔍 Troubleshooting Tips"):
                st.write("""
                **Common issues:**
                
                1. **Too many unique classes**: Your target column might be continuous (regression) rather than categorical (classification)
                   - Solution: Check if your target should be binned into categories
                
                2. **Too few samples per class**: Some classes have very few examples
                   - Solution: Remove rare classes or collect more data
                
                3. **Wrong target column**: You might have selected an ID column or continuous variable
                   - Solution: Select the correct categorical target column
                
                4. **Missing values**: Dataset contains too many missing values
                   - Solution: Clean your data before uploading
                """)
                
                st.write("**Dataset Info:**")
                st.write(f"- Total samples: {len(y)}")
                st.write(f"- Unique classes: {y.nunique()}")
                st.write(f"- Class distribution:\n{y.value_counts().to_dict()}")
            
            import traceback
            with st.expander("📋 Full Error Details"):
                st.code(traceback.format_exc())
else:
    st.info("Load a dataset to start the model comparison.")
