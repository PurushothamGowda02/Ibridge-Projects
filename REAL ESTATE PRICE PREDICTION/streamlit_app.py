import json
import os
import pickle
import sqlite3
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

MODEL_PATH = "ml_model/artifacts/real_estate_model.pkl"
CONFIG_PATH = "ml_model/artifacts/columns.json"
DB_PATH = "database/houses.db"


def preprocess_sqft(value):
    tokens = str(value).split("-")
    if len(tokens) == 2:
        try:
            return (float(tokens[0]) + float(tokens[1])) / 2
        except ValueError:
            return None
    try:
        return float(value)
    except ValueError:
        return None


def extract_availability_year(value):
    text = str(value).strip()
    if "-" not in text:
        return None
    parts = text.split("-")
    if len(parts) != 2:
        return None
    yy = parts[0]
    if not yy.isdigit() or len(yy) != 2:
        return None
    year = 2000 + int(yy)
    current_year = datetime.now().year
    if year < 2000 or year > current_year + 1:
        return None
    return year


def build_analytics(df):
    top_locations = (
        df["location"]
        .value_counts()
        .head(10)
        .rename_axis("location")
        .reset_index(name="count")
    )
    bhk_distribution = (
        df.groupby(df["bhk"].astype(int))["price"]
        .mean()
        .round(2)
        .rename_axis("bhk")
        .reset_index(name="avg_price")
    )
    price_distribution = (
        pd.cut(
            df["price"],
            bins=[0, 50, 100, 150, 200, 300, float("inf")],
            labels=["0-50", "50-100", "100-150", "150-200", "200-300", "300+"],
            include_lowest=True,
        )
        .value_counts()
        .sort_index()
        .rename_axis("bucket")
        .reset_index(name="count")
    )

    trend_df = df.dropna(subset=["availability"]).copy()
    trend_df["year"] = trend_df["availability"].apply(extract_availability_year)
    trend_df = trend_df.dropna(subset=["year"])
    trend_df["year"] = trend_df["year"].astype(int)
    yearly_prices = trend_df.groupby("year")["price"].mean().round(2).sort_index()

    ten_year_trend = []
    ten_year_change = None
    yearly_index = []
    if not yearly_prices.empty:
        latest_year = int(yearly_prices.index.max())
        latest_avg = float(yearly_prices.loc[latest_year])
        if latest_avg:
            yearly_index = [
                {"year": int(year), "index_vs_latest": round(float(price) / latest_avg, 6)}
                for year, price in yearly_prices.items()
            ]
        window = yearly_prices.tail(10)
        ten_year_trend = [
            {"year": int(year), "avg_price_lakhs": float(price)}
            for year, price in window.items()
        ]
        start_price = float(window.iloc[0])
        end_price = float(window.iloc[-1])
        pct_change = ((end_price - start_price) / start_price * 100.0) if start_price else 0.0
        ten_year_change = {
            "from_year": int(window.index[0]),
            "to_year": int(window.index[-1]),
            "from_price_lakhs": round(start_price, 2),
            "to_price_lakhs": round(end_price, 2),
            "absolute_change_lakhs": round(end_price - start_price, 2),
            "percent_change": round(pct_change, 2),
            "note": "Computed from records with month-year availability values.",
        }

    return {
        "dataset_size": int(len(df)),
        "avg_price_lakhs": round(float(df["price"].mean()), 2),
        "median_price_lakhs": round(float(df["price"].median()), 2),
        "bhk_distribution": bhk_distribution.to_dict(orient="records"),
        "top_locations": top_locations.to_dict(orient="records"),
        "price_distribution": price_distribution.to_dict(orient="records"),
        "ten_year_trend": ten_year_trend,
        "ten_year_change": ten_year_change,
        "available_years": [int(y["year"]) for y in yearly_index],
        "yearly_index": yearly_index,
    }


@st.cache_resource
def load_model_and_config():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(CONFIG_PATH):
        return None, None
    with open(MODEL_PATH, "rb") as model_file:
        model = pickle.load(model_file)
    with open(CONFIG_PATH, "r") as config_file:
        config = json.load(config_file)
    return model, config


@st.cache_data
def load_analytics():
    if not os.path.exists(DB_PATH):
        return None
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM houses", conn)
    conn.close()
    if df.empty:
        return None
    df = df.dropna(subset=["location", "size", "total_sqft", "price"]).copy()
    df["location"] = df["location"].astype(str).str.strip()
    df["bhk"] = df["size"].astype(str).str.extract(r"(\d+)").astype(float)
    df["total_sqft"] = df["total_sqft"].apply(preprocess_sqft)
    df = df.dropna(subset=["bhk", "total_sqft"])
    if df.empty:
        return None
    return build_analytics(df)


st.set_page_config(
    page_title="Bengaluru Real Estate Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern design
st.markdown("""
<style>
    /* Main background gradient */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card styling */
    .css-1r6slb0 {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Header styling */
    h1 {
        color: white !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        text-align: center;
        margin-bottom: 10px !important;
        text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.5);
    }
    
    h2 {
        color: #2d3748 !important;
        font-weight: 700 !important;
        margin-top: 20px !important;
    }
    
    h3 {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    
    h4 {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: white;
        font-size: 1.3rem;
        margin-bottom: 40px;
        font-weight: 400;
        text-shadow: 1px 1px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #2d3748 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 600 !important;
        color: #2d3748 !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    /* Form styling */
    .stForm {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 15px 30px;
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Input fields */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 10px;
        font-size: 1rem;
        color: #2d3748;
        font-weight: 500;
    }
    
    /* Labels */
    label {
        color: #2d3748 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    /* Success message */
    .stSuccess {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        font-size: 1.2rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Info box */
    .stInfo {
        background: rgba(102, 126, 234, 0.1);
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 15px;
    }
    
    /* Dataframe styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Chart container */
    .stPlotlyChart, .stVegaLiteChart {
        background: white;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* Divider */
    hr {
        margin: 40px 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
    }
    
    /* Caption */
    .caption {
        text-align: center;
        color: white;
        font-size: 0.95rem;
        margin-top: -30px;
        margin-bottom: 30px;
        text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
    }
    
    /* General text */
    p {
        color: #2d3748 !important;
    }
    
    /* Markdown text in white containers */
    .element-container p {
        color: #2d3748 !important;
    }
    
    /* Make all text in forms more visible */
    .stForm p, .stForm label, .stForm span {
        color: #2d3748 !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🏠 Bengaluru Real Estate Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-Powered Property Price Predictions & Market Analytics</p>", unsafe_allow_html=True)

model, config = load_model_and_config()
analytics = load_analytics()

if model is None or config is None:
    st.markdown("""
    <div style='background: rgba(255, 59, 48, 0.1); padding: 20px; border-radius: 12px; border-left: 4px solid #ff3b30;'>
        <h3 style='color: #ff3b30; margin: 0;'>⚠️ Model Artifacts Missing</h3>
        <p style='color: #666; margin-top: 10px;'>Please run: <code>python ml_model/train_model.py</code></p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()
if analytics is None:
    st.markdown("""
    <div style='background: rgba(255, 59, 48, 0.1); padding: 20px; border-radius: 12px; border-left: 4px solid #ff3b30;'>
        <h3 style='color: #ff3b30; margin: 0;'>⚠️ Database Missing</h3>
        <p style='color: #666; margin-top: 10px;'>Please run: <code>python database/load_to_db.py</code></p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

locations = sorted(config["data_columns"][3:])

# Create container with custom styling
st.markdown("<br>", unsafe_allow_html=True)
left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown("<h3 style='color: white; text-shadow: 2px 2px 6px rgba(0,0,0,0.4);'>🎯 Price Prediction</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    year_options = analytics.get("available_years", [])
    default_year = max(year_options) if year_options else datetime.now().year
    with st.form("prediction_form"):
        location = st.selectbox("📍 Location", locations, index=0)
        total_sqft = st.number_input("📐 Total Square Feet", min_value=300.0, value=1200.0, step=50.0)
        bath = st.number_input("🚿 Bathrooms", min_value=1.0, max_value=10.0, value=2.0, step=1.0)
        bhk = st.number_input("🛏️ BHK (Bedrooms)", min_value=1, max_value=10, value=2, step=1)
        if year_options:
            year = st.selectbox(
                "📅 Year",
                options=year_options,
                index=year_options.index(default_year) if default_year in year_options else 0,
            )
        else:
            year = st.number_input("📅 Year", min_value=2000, max_value=2100, value=default_year, step=1)
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🔮 Predict Price")

    if submitted:
        input_vector = np.zeros(len(config["data_columns"]))
        input_vector[0] = float(total_sqft)
        input_vector[1] = float(bath)
        input_vector[2] = int(bhk)
        input_vector[config["data_columns"].index(location.strip().lower())] = 1
        current_prediction = float(model.predict([input_vector])[0])

        yearly_index = analytics.get("yearly_index", [])
        idx_map = {int(item["year"]): float(item["index_vs_latest"]) for item in yearly_index}
        latest_year = max(idx_map.keys()) if idx_map else int(year)
        selected_prediction = current_prediction * idx_map.get(int(year), 1.0)
        diff = current_prediction - selected_prediction
        diff_pct = (diff / selected_prediction * 100.0) if selected_prediction else 0.0

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 15px; text-align: center; 
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);'>
            <h2 style='color: white; margin: 0; font-size: 2.5rem;'>
                ₹ {round(selected_prediction, 2)} Lakhs
            </h2>
            <p style='color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 1.2rem;'>
                ≈ ₹ {round(selected_prediction / 100.0, 2)} Crores
            </p>
            <p style='color: rgba(255,255,255,0.8); margin: 15px 0 0 0; font-size: 0.9rem;'>
                Estimated price for {int(year)}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                label=f"Current Value ({latest_year})",
                value=f"₹ {round(current_prediction, 2)}L"
            )
        with col2:
            st.metric(
                label="Difference",
                value=f"₹ {abs(round(diff, 2))}L",
                delta=f"{round(diff_pct, 2)}%"
            )

with right:
    st.markdown("<h3 style='color: white; text-shadow: 2px 2px 6px rgba(0,0,0,0.4);'>📊 Market Snapshot</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("📈 Dataset Size", f"{analytics['dataset_size']:,}")
    c2.metric("💰 Avg Price", f"₹{analytics['avg_price_lakhs']}L")
    c3.metric("📍 Median", f"₹{analytics['median_price_lakhs']}L")
    
    st.markdown("<br><br>", unsafe_allow_html=True)

if analytics.get("ten_year_change"):
    change = analytics["ten_year_change"]
    trend_emoji = "📈" if change['percent_change'] > 0 else "📉"
    st.markdown(f"""
    <div style='background: white; padding: 25px; border-radius: 12px; 
                border-left: 5px solid #667eea; margin: 20px 0;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);'>
        <h4 style='color: #667eea; margin: 0; font-size: 1.3rem;'>{trend_emoji} 10-Year Market Trend</h4>
        <p style='color: #2d3748; margin: 15px 0 0 0; font-size: 1.15rem; font-weight: 500;'>
            <strong>{change['from_year']} → {change['to_year']}:</strong> 
            ₹{change['from_price_lakhs']}L → ₹{change['to_price_lakhs']}L 
            <span style='color: {"#34c759" if change["percent_change"] > 0 else "#ff3b30"}; font-weight: 700;'>
                ({change['percent_change']:+.2f}%)
            </span>
        </p>
        <p style='color: #4a5568; margin: 10px 0 0 0; font-size: 0.9rem;'>{change['note']}</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown("<h3 style='color: white; text-align: center; text-shadow: 2px 2px 6px rgba(0,0,0,0.4);'>📈 Market Analytics Dashboard</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<h4 style='color: #2d3748;'>💵 Price Distribution by Range</h4>", unsafe_allow_html=True)
    price_df = pd.DataFrame(analytics["price_distribution"])
    st.bar_chart(price_df.set_index("bucket")["count"], color="#667eea")

with col2:
    st.markdown("<h4 style='color: #2d3748;'>🏘️ Average Price by BHK</h4>", unsafe_allow_html=True)
    bhk_df = pd.DataFrame(analytics["bhk_distribution"]).sort_values("bhk")
    bhk_df["bhk"] = bhk_df["bhk"].astype(str) + " BHK"
    st.bar_chart(bhk_df.set_index("bhk")["avg_price"], color="#764ba2")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h4 style='color: #2d3748;'>🌆 Top 10 Locations by Listings</h4>", unsafe_allow_html=True)
top_df = pd.DataFrame(analytics["top_locations"])
st.dataframe(
    top_df,
    width='stretch',
    hide_index=True,
    column_config={
        "location": st.column_config.TextColumn("Location", width="large"),
        "count": st.column_config.NumberColumn("Listings", format="%d")
    }
)

if analytics.get("ten_year_trend"):
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: #2d3748;'>📊 10-Year Price Trend Analysis</h4>", unsafe_allow_html=True)
    trend_df = pd.DataFrame(analytics["ten_year_trend"]).sort_values("year")
    st.line_chart(trend_df.set_index("year")["avg_price_lakhs"], color="#667eea")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: white; padding: 20px;'>
    <p style='margin: 0; font-size: 1rem; font-weight: 500; text-shadow: 1px 1px 4px rgba(0,0,0,0.4);'>
        🏠 Bengaluru Real Estate Intelligence | Powered by Machine Learning
    </p>
    <p style='margin: 8px 0 0 0; font-size: 0.9rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);'>
        Built with Streamlit, FastAPI & scikit-learn
    </p>
</div>
""", unsafe_allow_html=True)
