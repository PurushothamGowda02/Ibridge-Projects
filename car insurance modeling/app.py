"""Streamlit web application for car insurance premium prediction."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

from src.models.predict import predict_premium
from src.utils.config_loader import load_config

# Page configuration
st.set_page_config(
    page_title="Car Insurance Premium Calculator",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for CRAZY modern styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Animated gradient background */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Glassmorphism container */
    .main {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Floating animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    /* Neon glow button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff);
        color: white;
        font-weight: 900;
        padding: 1.2rem;
        border-radius: 50px;
        border: none;
        font-size: 1.3rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        box-shadow: 0 0 20px rgba(255, 0, 110, 0.5),
                    0 0 40px rgba(131, 56, 236, 0.3),
                    0 0 60px rgba(58, 134, 255, 0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: scale(1.05) translateY(-5px);
        box-shadow: 0 0 30px rgba(255, 0, 110, 0.8),
                    0 0 60px rgba(131, 56, 236, 0.6),
                    0 0 90px rgba(58, 134, 255, 0.4);
        animation: pulse 1s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 0, 110, 0.5); }
        50% { box-shadow: 0 0 40px rgba(255, 0, 110, 1); }
    }
    
    /* Premium result box with 3D effect */
    .premium-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem;
        border-radius: 30px;
        text-align: center;
        color: white;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3),
                    inset 0 0 50px rgba(255,255,255,0.1);
        transform: perspective(1000px) rotateX(5deg);
        transition: all 0.5s ease;
        position: relative;
        overflow: hidden;
        animation: float 3s ease-in-out infinite;
    }
    
    .premium-box::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .premium-box:hover {
        transform: perspective(1000px) rotateX(0deg) scale(1.05);
        box-shadow: 0 30px 80px rgba(0,0,0,0.4);
    }
    
    .premium-amount {
        font-size: 4.5rem;
        font-weight: 900;
        margin: 1rem 0;
        text-shadow: 0 0 20px rgba(255,255,255,0.5),
                     0 0 40px rgba(255,255,255,0.3);
        animation: glow 2s ease-in-out infinite;
    }
    
    @keyframes glow {
        0%, 100% { text-shadow: 0 0 20px rgba(255,255,255,0.5); }
        50% { text-shadow: 0 0 40px rgba(255,255,255,1); }
    }
    
    /* Glassmorphism info cards */
    .info-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        padding: 2rem;
        border-radius: 20px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .info-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .info-card:hover::before {
        left: 100%;
    }
    
    .info-card:hover {
        transform: translateY(-10px) scale(1.02);
        border-color: rgba(255, 255, 255, 0.6);
        box-shadow: 0 15px 45px 0 rgba(31, 38, 135, 0.5);
    }
    
    .info-card h4 {
        color: #fff;
        font-weight: 700;
        font-size: 1.3rem;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .info-card p {
        color: rgba(255, 255, 255, 0.95);
        font-weight: 500;
        font-size: 1.05rem;
    }
    
    /* Animated title */
    h1 {
        background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientText 5s ease infinite;
        font-weight: 900;
        font-size: 3.5rem !important;
        text-align: center;
        text-shadow: 0 0 30px rgba(255,255,255,0.5);
        letter-spacing: 2px;
    }
    
    @keyframes gradientText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Subheader styling */
    h3 {
        color: white !important;
        font-weight: 700;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
        font-size: 1.8rem !important;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 50px;
        padding: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 30px;
        color: white;
        font-weight: 600;
        padding: 15px 30px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-3px);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #ff006e, #8338ec) !important;
        box-shadow: 0 5px 20px rgba(255, 0, 110, 0.5);
    }
    
    /* Input styling */
    .stSelectbox, .stSlider, .stNumberInput {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 5px;
    }
    
    /* Labels */
    label {
        color: white !important;
        font-weight: 600 !important;
        text-shadow: 0 2px 5px rgba(0,0,0,0.3);
        font-size: 1.1rem !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
        text-shadow: 0 0 20px rgba(255,255,255,0.5);
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600 !important;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.5), transparent);
        margin: 2rem 0;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: white;
    }
    
    /* Risk factor badges */
    .stMarkdown p {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 12px 20px;
        border-radius: 15px;
        border-left: 4px solid #06ffa5;
        margin: 10px 0;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stMarkdown p:hover {
        transform: translateX(10px);
        background: rgba(255, 255, 255, 0.2);
        border-left-width: 8px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #ff006e !important;
        border-right-color: #8338ec !important;
        border-bottom-color: #3a86ff !important;
        border-left-color: #06ffa5 !important;
    }
    
    /* Plotly charts background */
    .js-plotly-plot {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 10px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #ff006e, #8338ec);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #8338ec, #3a86ff);
    }
    
    /* Particle effect container */
    .particle {
        position: fixed;
        width: 10px;
        height: 10px;
        background: white;
        border-radius: 50%;
        pointer-events: none;
        opacity: 0.5;
        animation: float-particle 10s infinite;
    }
    
    @keyframes float-particle {
        0%, 100% { transform: translateY(0) translateX(0); opacity: 0; }
        10% { opacity: 0.5; }
        90% { opacity: 0.5; }
        100% { transform: translateY(-100vh) translateX(50px); opacity: 0; }
    }
    </style>
""", unsafe_allow_html=True)

# Load configuration
@st.cache_resource
def load_app_config():
    return load_config()

config = load_app_config()

# Title and description with emoji animations
st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <div style='font-size: 5rem; margin-bottom: 1rem; animation: float 3s ease-in-out infinite;'>
            🚗✨💎✨🚗
        </div>
        <h1 style='margin-bottom: 0;'>CAR INSURANCE PREMIUM CALCULATOR</h1>
        <p style='font-size: 1.5rem; color: white; font-weight: 700; text-shadow: 0 2px 10px rgba(0,0,0,0.3); 
                  margin-top: 1rem; letter-spacing: 2px;'>
            🔮 AI-POWERED • INSTANT QUOTES • STUNNING VISUALS 🔮
        </p>
        <div style='margin-top: 1.5rem; font-size: 2rem;'>
            ⚡ 🎯 🚀 💰 🏆 ⚡
        </div>
    </div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3 = st.tabs(["💰 Calculate Premium", "📊 Data Insights", "ℹ️ About"])

with tab1:
    st.markdown("---")
    
    # Add a cool header
    st.markdown("""
        <div style='text-align: center; padding: 1rem; background: rgba(255,255,255,0.1); 
                    backdrop-filter: blur(10px); border-radius: 20px; margin-bottom: 2rem;'>
            <h2 style='color: white; font-weight: 800; margin: 0;'>
                💎 PREMIUM CALCULATOR 💎
            </h2>
            <p style='color: rgba(255,255,255,0.9); margin-top: 0.5rem;'>
                Fill in your details below to get your personalized quote
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); 
                        padding: 1.5rem; border-radius: 20px; margin-bottom: 1rem;'>
                <h3 style='margin: 0; font-size: 1.5rem;'>👤 Personal Information</h3>
            </div>
        """, unsafe_allow_html=True)
        
        age = st.slider("Age", 18, 80, 35, help="Your current age")
        
        gender = st.selectbox(
            "Gender",
            options=["Male", "Female"],
            help="Select your gender"
        )
        
        driving_experience = st.slider(
            "Driving Experience (years)",
            0, min(age - 18, 60), min(15, age - 18),
            help="Years of driving experience"
        )
        
        education_level = st.selectbox(
            "Education Level",
            options=["High School", "Bachelor", "Master", "PhD"],
            index=1,
            help="Highest education level"
        )
        
        marital_status = st.selectbox(
            "Marital Status",
            options=["Single", "Married", "Divorced", "Widowed"],
            index=1,
            help="Current marital status"
        )
        
        region = st.selectbox(
            "Region",
            options=["Urban", "Suburban", "Rural"],
            index=1,
            help="Where you primarily drive"
        )
    
    with col2:
        st.markdown("""
            <div style='background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); 
                        padding: 1.5rem; border-radius: 20px; margin-bottom: 1rem;'>
                <h3 style='margin: 0; font-size: 1.5rem;'>🚙 Vehicle & Financial Information</h3>
            </div>
        """, unsafe_allow_html=True)
        
        vehicle_make = st.selectbox(
            "Vehicle Make",
            options=["Toyota", "Honda", "Ford", "BMW", "Mercedes", "Audi", "Chevrolet", "Nissan"],
            help="Manufacturer of your vehicle"
        )
        
        vehicle_model = st.selectbox(
            "Vehicle Type",
            options=["Sedan", "SUV", "Truck", "Coupe", "Hatchback", "Van"],
            help="Type of vehicle"
        )
        
        vehicle_age = st.slider(
            "Vehicle Age (years)",
            0, 25, 3,
            help="Age of your vehicle"
        )
        
        engine_size = st.slider(
            "Engine Size (L)",
            1.0, 6.0, 2.0, 0.1,
            help="Engine displacement in liters"
        )
        
        annual_mileage = st.number_input(
            "Annual Mileage",
            min_value=1000, max_value=50000, value=12000, step=1000,
            help="Estimated miles driven per year"
        )
        
        credit_score = st.slider(
            "Credit Score",
            300, 850, 720,
            help="Your credit score"
        )
        
        previous_claims = st.number_input(
            "Previous Claims",
            min_value=0, max_value=10, value=0,
            help="Number of insurance claims in the past"
        )
    
    st.markdown("---")
    
    # Calculate button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        calculate_btn = st.button("🔮 Calculate Premium", use_container_width=True)
    
    if calculate_btn:
        with st.spinner("Calculating your premium..."):
            # Create input DataFrame
            input_data = pd.DataFrame([{
                'age': age,
                'gender': gender,
                'driving_experience': driving_experience,
                'vehicle_make': vehicle_make,
                'vehicle_model': vehicle_model,
                'vehicle_age': vehicle_age,
                'engine_size': engine_size,
                'annual_mileage': annual_mileage,
                'credit_score': credit_score,
                'previous_claims': previous_claims,
                'region': region,
                'education_level': education_level,
                'marital_status': marital_status
            }])
            
            # Get prediction
            result = predict_premium(input_data, config)
            premium = result['predicted_premium'].iloc[0]
            
            # Display result in a beautiful box
            st.markdown("### 🎉 Your Estimated Premium")
            st.markdown(f"""
                <div class="premium-box">
                    <div style="font-size: 1.5rem; font-weight: 700; letter-spacing: 3px;">💰 ANNUAL PREMIUM 💰</div>
                    <div class="premium-amount">${premium:,.2f}</div>
                    <div style="font-size: 1.3rem; opacity: 0.95; font-weight: 600; margin-top: 1rem;">
                        📅 Monthly: ${premium/12:,.2f}
                    </div>
                    <div style="font-size: 0.9rem; opacity: 0.8; margin-top: 1rem;">
                        ⚡ Powered by XGBoost AI ⚡
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Risk factors analysis
            st.markdown("""
                <div style='text-align: center; margin: 2rem 0;'>
                    <h3 style='font-size: 2rem;'>📋 PREMIUM BREAKDOWN 📋</h3>
                </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                st.markdown("""
                    <div class="info-card">
                        <h4>👤 Driver Profile</h4>
                        <p><strong>Age:</strong> {}</p>
                        <p><strong>Experience:</strong> {} years</p>
                        <p><strong>Claims History:</strong> {}</p>
                    </div>
                """.format(age, driving_experience, previous_claims), unsafe_allow_html=True)
            
            with col_b:
                st.markdown("""
                    <div class="info-card">
                        <h4>🚗 Vehicle Details</h4>
                        <p><strong>Make/Model:</strong> {} {}</p>
                        <p><strong>Age:</strong> {} years</p>
                        <p><strong>Engine:</strong> {}L</p>
                    </div>
                """.format(vehicle_make, vehicle_model, vehicle_age, engine_size), unsafe_allow_html=True)
            
            with col_c:
                st.markdown("""
                    <div class="info-card">
                        <h4>💳 Financial Profile</h4>
                        <p><strong>Credit Score:</strong> {}</p>
                        <p><strong>Region:</strong> {}</p>
                        <p><strong>Annual Mileage:</strong> {:,}</p>
                    </div>
                """.format(credit_score, region, annual_mileage), unsafe_allow_html=True)
            
            # Risk factors
            st.markdown("""
                <div style='text-align: center; margin: 2rem 0;'>
                    <h3 style='font-size: 2rem;'>⚠️ FACTORS AFFECTING YOUR PREMIUM ⚠️</h3>
                </div>
            """, unsafe_allow_html=True)
            
            factors = []
            if age < 25:
                factors.append(("Young Driver", "Higher risk due to age under 25", "🔴"))
            elif age > 65:
                factors.append(("Senior Driver", "Slightly higher risk", "🟡"))
            else:
                factors.append(("Optimal Age", "Good driver age range", "🟢"))
            
            if previous_claims > 0:
                factors.append(("Previous Claims", f"{previous_claims} claim(s) on record", "🔴"))
            else:
                factors.append(("Clean Record", "No previous claims", "🟢"))
            
            if credit_score < 600:
                factors.append(("Low Credit Score", "Credit score below 600", "🔴"))
            elif credit_score < 700:
                factors.append(("Fair Credit Score", "Credit score 600-700", "🟡"))
            else:
                factors.append(("Good Credit Score", "Credit score above 700", "🟢"))
            
            if region == "Urban":
                factors.append(("Urban Area", "Higher accident rates in cities", "🟡"))
            else:
                factors.append(("Non-Urban Area", "Lower risk area", "🟢"))
            
            for factor, desc, icon in factors:
                st.markdown(f"{icon} **{factor}**: {desc}")

with tab2:
    st.markdown("""
        <div style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); 
                    backdrop-filter: blur(10px); border-radius: 20px; margin-bottom: 2rem;'>
            <h2 style='color: white; font-weight: 900; font-size: 2.5rem; margin: 0;'>
                📊 INSURANCE DATA INSIGHTS 📊
            </h2>
            <p style='color: rgba(255,255,255,0.9); margin-top: 1rem; font-size: 1.2rem;'>
                Explore trends and patterns in our insurance dataset
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load the dataset
    @st.cache_data
    def load_data():
        return pd.read_csv("data/raw/insurance_data.csv")
    
    df = load_data()
    
    # Display statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df):,}")
    with col2:
        st.metric("Avg Premium", f"${df['premium_amount'].mean():,.2f}")
    with col3:
        st.metric("Min Premium", f"${df['premium_amount'].min():,.2f}")
    with col4:
        st.metric("Max Premium", f"${df['premium_amount'].max():,.2f}")
    
    st.markdown("---")
    
    # Visualizations
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        # Premium distribution
        fig1 = px.histogram(
            df, x='premium_amount',
            title='Premium Distribution',
            labels={'premium_amount': 'Premium Amount ($)'},
            color_discrete_sequence=['#667eea']
        )
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Premium by vehicle type
        fig3 = px.box(
            df, x='vehicle_model', y='premium_amount',
            title='Premium by Vehicle Type',
            labels={'vehicle_model': 'Vehicle Type', 'premium_amount': 'Premium ($)'},
            color='vehicle_model'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col_v2:
        # Premium by age group
        df['age_group'] = pd.cut(df['age'], bins=[0, 25, 35, 50, 65, 100], 
                                  labels=['<25', '25-35', '35-50', '50-65', '65+'])
        fig2 = px.box(
            df, x='age_group', y='premium_amount',
            title='Premium by Age Group',
            labels={'age_group': 'Age Group', 'premium_amount': 'Premium ($)'},
            color='age_group'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Premium by region
        avg_by_region = df.groupby('region')['premium_amount'].mean().reset_index()
        fig4 = px.bar(
            avg_by_region, x='region', y='premium_amount',
            title='Average Premium by Region',
            labels={'region': 'Region', 'premium_amount': 'Avg Premium ($)'},
            color='premium_amount',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.markdown("""
        <div style='text-align: center; padding: 2rem; background: rgba(255,255,255,0.1); 
                    backdrop-filter: blur(10px); border-radius: 20px; margin-bottom: 2rem;'>
            <h2 style='color: white; font-weight: 900; font-size: 2.5rem; margin: 0;'>
                ℹ️ ABOUT THIS APPLICATION ℹ️
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ### Car Insurance Premium Prediction System
    
    This application uses advanced machine learning algorithms to predict car insurance premiums 
    based on various factors including driver demographics, vehicle characteristics, and risk factors.
    
    #### 🤖 Machine Learning Models
    
    The system uses three different models and selects the best performer:
    - **Linear Regression**: Baseline model
    - **Random Forest**: Ensemble learning approach
    - **XGBoost**: Gradient boosting (Best performer with 83% accuracy)
    
    #### 📊 Features Considered
    
    **Personal Factors:**
    - Age and driving experience
    - Gender and marital status
    - Education level
    - Credit score
    - Previous claims history
    
    **Vehicle Factors:**
    - Make and model
    - Vehicle age
    - Engine size
    - Annual mileage
    
    **Location:**
    - Region (Urban/Suburban/Rural)
    
    #### 🎯 Model Performance
    
    - **Accuracy (R²)**: 83.1%
    - **Mean Absolute Error**: $131.32
    - **RMSE**: $170.11
    
    #### 💡 How to Use
    
    1. Fill in your personal and vehicle information in the "Calculate Premium" tab
    2. Click the "Calculate Premium" button
    3. View your estimated annual and monthly premium
    4. Review the factors affecting your premium
    
    #### ⚠️ Disclaimer
    
    This is a predictive model for educational purposes. Actual insurance premiums may vary 
    based on additional factors and insurance company policies.
    
    ---
    
    **Built with:** Python, Scikit-learn, XGBoost, Streamlit, Plotly
    """)

# Footer with animation
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 3rem; background: rgba(255,255,255,0.05); 
                backdrop-filter: blur(20px); border-radius: 30px; margin-top: 2rem;'>
        <h2 style='background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
                   background-size: 300% 300%;
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   background-clip: text;
                   animation: gradientText 5s ease infinite;
                   font-weight: 900;
                   margin-bottom: 1rem;'>
            🚗 CAR INSURANCE PREMIUM CALCULATOR 🚗
        </h2>
        <p style='color: white; font-size: 1.2rem; font-weight: 600; margin: 1rem 0;'>
            ⚡ Powered by Machine Learning & AI ⚡
        </p>
        <p style='color: rgba(255,255,255,0.8); font-size: 1rem; margin-top: 1.5rem;'>
            © 2026 - Built with 💜 using Streamlit & XGBoost
        </p>
        <div style='margin-top: 2rem; font-size: 2rem;'>
            ✨ 🎯 🚀 💎 🔮 ✨
        </div>
    </div>
""", unsafe_allow_html=True)
