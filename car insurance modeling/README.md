# 🚗✨ Car Insurance Premium Prediction ✨🚗

A **stunning, AI-powered** machine learning web application with **crazy modern design** to predict car insurance premiums based on driver demographics, vehicle characteristics, and risk factors.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-83%25%20Accuracy-green.svg)
![Design](https://img.shields.io/badge/Design-Cyberpunk-ff006e.svg)
![UI](https://img.shields.io/badge/UI-Glassmorphism-8338ec.svg)
![Animations](https://img.shields.io/badge/Animations-10+-3a86ff.svg)

---

## ⚡ Quick Highlights

🎨 **Stunning Cyberpunk Design** • 💎 **Glassmorphism Effects** • ✨ **10+ CSS Animations**  
🌈 **Animated Gradients** • 🔮 **3D Transformations** • ⚡ **Neon Glow Effects**  
🤖 **83% AI Accuracy** • 📊 **Interactive Charts** • 🚀 **Real-time Predictions**

---

## 🎨 NEW! Crazy Modern Frontend Design

### ✨ Before & After Transformation

#### Before 😴
- Plain white background
- Basic buttons
- Simple cards
- Static text
- Minimal styling

#### After 🤩
- **Animated gradient background** with 4-color transitions
- **Neon glow buttons** with pulse effects
- **Glassmorphism cards** with frosted glass
- **3D floating premium display** with shine sweep
- **Color-shifting text** with gradient animations
- **Interactive hover effects** on everything
- **Custom scrollbar** with gradient design
- **Smooth transitions** throughout

### 🌟 Visual Features
- **🌈 Animated Gradient Background** - Continuously shifting colors (15s cycle)
- **💎 Glassmorphism Effects** - Frosted glass aesthetic throughout
- **✨ 3D Premium Display** - Floating animation with shine sweep effect
- **⚡ Neon Glow Buttons** - Triple gradient with pulsing shadows
- **🎯 Interactive Cards** - Hover effects with lift and scale
- **🔮 Animated Typography** - Color-shifting gradient text
- **🎨 Custom Scrollbar** - Gradient design matching theme
- **💫 10+ CSS Animations** - Smooth, eye-catching transitions

### 🎭 Design Aesthetic
**Cyberpunk meets Modern Minimalism**
- Vibrant neon colors (Pink, Purple, Blue, Green)
- Futuristic glassmorphism
- 3D transformations
- High-tech premium feel
- Immersive visual experience

### 📊 Feature Comparison

| Feature | Standard App | This App |
|---------|-------------|----------|
| Background | Plain white | 🌈 Animated gradient |
| Buttons | Basic | ⚡ Neon glow with pulse |
| Cards | Flat | 💎 Glassmorphism 3D |
| Text | Static | ✨ Gradient animations |
| Interactions | None | 🎯 Hover effects everywhere |
| Premium Display | Simple box | 🔮 3D floating with shine |
| Scrollbar | Default | 🎨 Custom gradient |
| Overall Feel | Boring | 🚀 Futuristic & Premium |

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train Models (First Time Only)
```bash
python main.py
```
This will train all three models and save them to the `models/` directory.

### 3. Launch Web Application 🎨
```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

### 🎉 What to Expect
When you launch the app, you'll be greeted with:
- 🌈 **Animated gradient background** that continuously shifts colors
- 💎 **Glassmorphism interface** with frosted glass effects
- ⚡ **Neon glow buttons** that pulse when you hover
- 🔮 **3D premium display** that floats and shines
- ✨ **Smooth animations** on every interaction
- 🎨 **Cyberpunk aesthetic** throughout

**Pro Tip:** Try hovering over different elements to see the interactive effects! 🖱️✨

---

## 🎨 Design System

### Color Palette
```css
Primary Colors:
- Hot Pink:      #ff006e  🔴
- Electric Purple: #8338ec  🟣
- Bright Blue:    #3a86ff  🔵
- Neon Green:     #06ffa5  🟢

Gradients:
- Background: Coral → Pink → Blue → Teal
- Buttons:    Pink → Purple → Blue
- Premium Box: Purple → Deep Purple → Light Purple
- Text:       Pink → Purple → Blue → Green
```

### Typography
- **Font Family:** Poppins (Google Fonts)
- **Weights:** 300 (Light), 400 (Regular), 600 (SemiBold), 700 (Bold), 900 (Black)
- **Effects:** Text shadows, gradient fills, glow animations

### Visual Effects
| Effect | Duration | Description |
|--------|----------|-------------|
| Gradient Background | 15s | Infinite color shifting animation |
| Float | 3s | Vertical up/down motion |
| Pulse | 1s | Pulsing glow on buttons |
| Shine | 3s | Diagonal light sweep |
| Glow | 2s | Text glow pulsing |
| Gradient Text | 5s | Color-shifting text |

### Animation Details

#### 1. **Gradient Background Animation**
```css
Colors: #ee7752 → #e73c7e → #23a6d5 → #23d5ab
Duration: 15 seconds
Loop: Infinite
Effect: Smooth color transitions across entire background
```

#### 2. **3D Premium Box**
```css
Transform: perspective(1000px) rotateX(5deg)
Animation: Float (3s) + Shine sweep (3s)
Hover: Scale(1.05) + Enhanced shadow
Effect: Floating card with light sweep
```

#### 3. **Neon Glow Button**
```css
Gradient: #ff006e → #8338ec → #3a86ff
Shadows: 3 layers (20px, 40px, 60px)
Animation: Pulse (1s infinite)
Hover: Scale(1.05) + translateY(-5px)
```

#### 4. **Glassmorphism Cards**
```css
Background: rgba(255, 255, 255, 0.15)
Backdrop-filter: blur(20px)
Border: 2px solid rgba(255, 255, 255, 0.3)
Hover: translateY(-10px) + scale(1.02)
```

#### 5. **Gradient Text Animation**
```css
Colors: #ff006e → #8338ec → #3a86ff → #06ffa5
Background-size: 300% 300%
Animation: 5s ease infinite
Effect: Continuous color shifting
```

### Design Principles
- **Glassmorphism:** Frosted glass with backdrop blur (10-20px)
- **3D Transforms:** Perspective effects and rotations
- **Neon Aesthetics:** Multi-layered glowing shadows
- **Smooth Transitions:** 0.3-0.5s ease on all interactions
- **Responsive:** Flexible layouts with columns
- **Accessibility:** High contrast ratios maintained

---

## 📁 Project Structure

```
car-insurance-ml/
├── app.py                      # Streamlit web app with CRAZY design! 🎨
├── main.py                     # Complete ML pipeline
├── config/
│   └── config.yaml            # Model & data configuration
├── data/
│   ├── raw/                   # Raw CSV dataset (10,000 records)
│   └── processed/             # Preprocessed train/test splits
├── models/                    # Trained model files (.pkl)
├── reports/                   # Model evaluation results
├── src/
│   ├── data/
│   │   └── preprocess.py     # Data preprocessing
│   ├── models/
│   │   ├── train.py          # Model training
│   │   ├── evaluate.py       # Model evaluation
│   │   └── predict.py        # Prediction logic
│   └── utils/
│       └── config_loader.py  # Configuration utilities
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── DESIGN_FEATURES.md        # Detailed design documentation
```

## 🎯 Features

### 💰 Premium Calculator
- **Stunning Visual Interface** - Cyberpunk-inspired design with glassmorphism
- **Real-time Predictions** - Instant premium calculations using XGBoost
- **3D Result Display** - Floating, glowing premium box with animations
- **Risk Analysis** - Detailed breakdown of factors affecting premium
- **Monthly/Annual Quotes** - View premiums in different formats
- **Interactive Inputs** - Modern sliders and selectors with hover effects

### 🎨 Design Highlights
- **Animated Gradient Background** - Never-ending color transitions
- **Neon Glow Effects** - Pulsing buttons and glowing text
- **Glassmorphism Cards** - Frosted glass effect with backdrop blur
- **Smooth Animations** - Float, pulse, shine, and glow effects
- **3D Transformations** - Perspective effects on premium display
- **Custom Styling** - Every element beautifully designed

### 📊 Data Insights
- **Interactive Visualizations** - Plotly charts with hover effects
- **Premium Distribution** - Histogram showing premium ranges
- **Age Group Analysis** - Box plots by driver age groups
- **Vehicle Type Comparison** - Premium variations by vehicle model
- **Regional Analysis** - Average premiums by location
- **Glassmorphism Dashboard** - Modern, transparent card designs

### 🤖 Machine Learning Models
- **Linear Regression** - Baseline model (R² = 0.51)
- **Random Forest** - Ensemble learning (R² = 0.77)
- **XGBoost** - Best performer (R² = 0.83)

## 📊 Dataset

**Size:** 10,000 insurance records  
**Features:** 13 input features + 1 target variable

### Input Features:

**Personal Information:**
- Age (18-80 years)
- Gender (Male/Female)
- Driving Experience (0-60 years)
- Education Level (High School, Bachelor, Master, PhD)
- Marital Status (Single, Married, Divorced, Widowed)

**Vehicle Information:**
- Vehicle Make (Toyota, Honda, Ford, BMW, Mercedes, Audi, Chevrolet, Nissan)
- Vehicle Model (Sedan, SUV, Truck, Coupe, Hatchback, Van)
- Vehicle Age (0-25 years)
- Engine Size (1.0-6.0L)
- Annual Mileage (1,000-50,000 miles)

**Financial & Risk:**
- Credit Score (300-850)
- Previous Claims (0-10)
- Region (Urban, Suburban, Rural)

**Target Variable:**
- Premium Amount ($706 - $5,000)

## 🎯 Model Performance

| Model | MAE | RMSE | R² Score |
|-------|-----|------|----------|
| Linear Regression | $224.16 | $290.97 | 0.5059 |
| Random Forest | $153.07 | $200.46 | 0.7655 |
| **XGBoost** | **$131.32** | **$170.11** | **0.8311** ✨ |

**Best Model:** XGBoost with 83.1% accuracy

## 🔧 Configuration

Edit `config/config.yaml` to customize:

```yaml
data:
  test_size: 0.2              # Train/test split ratio
  random_state: 42            # Random seed

models:
  xgboost:
    n_estimators: 100         # Number of trees
    max_depth: 6              # Tree depth
    learning_rate: 0.1        # Learning rate

evaluation:
  metrics:
    - mae                     # Mean Absolute Error
    - rmse                    # Root Mean Squared Error
    - r2_score                # R² Score
```

## 📝 Usage Examples

### Via Web Interface
```bash
streamlit run app.py
```
1. Fill in personal and vehicle information
2. Click "Calculate Premium"
3. View estimated premium and risk factors

### Via Python Script
```python
from src.models.predict import predict_single

premium = predict_single(
    age=35,
    gender='Male',
    driving_experience=15,
    vehicle_make='Toyota',
    vehicle_model='Sedan',
    vehicle_age=3,
    engine_size=2.0,
    annual_mileage=12000,
    credit_score=720,
    previous_claims=0,
    region='Suburban',
    education_level='Bachelor',
    marital_status='Married'
)

print(f"Predicted Premium: ${premium:.2f}")
```

### Retrain Models
```bash
python main.py
```

## 📦 Requirements

- **Python:** 3.8 or higher
- **Core ML Libraries:** pandas, numpy, scikit-learn, xgboost
- **Web Framework:** streamlit
- **Visualization:** plotly
- **Utilities:** joblib, pyyaml

See `requirements.txt` for complete list with versions.

## 🛠️ Tech Stack

### Backend & ML
- **Python 3.8+** - Core language
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - ML algorithms
- **XGBoost** - Gradient boosting
- **Joblib** - Model serialization

### Frontend & Visualization
- **Streamlit** - Web framework
- **Plotly** - Interactive charts
- **CSS3** - Custom styling & animations
- **Google Fonts** - Poppins typography

### Design Technologies
- **CSS Keyframes** - Custom animations
- **Backdrop Filter** - Glassmorphism effects
- **CSS Gradients** - Multi-color transitions
- **Transform 3D** - Perspective effects
- **Box Shadow** - Neon glow effects
- **Flexbox** - Responsive layouts

## 🛠️ Installation

### Option 1: Using pip
```bash
# Clone or download the repository
cd car-insurance-ml

# Install dependencies
pip install -r requirements.txt

# Train models
python main.py

# Run the app
streamlit run app.py
```

### Option 2: Using virtual environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Train models
python main.py

# Run the app
streamlit run app.py
```

## 📈 Model Training Pipeline

The `main.py` script runs the complete pipeline:

1. **Data Preprocessing**
   - Load raw CSV data
   - Clean and remove outliers
   - Encode categorical features
   - Scale numerical features
   - Split into train/test sets (80/20)

2. **Model Training**
   - Train Linear Regression
   - Train Random Forest (100 trees)
   - Train XGBoost (100 estimators)
   - Save models to `models/` directory

3. **Model Evaluation**
   - Calculate MAE, RMSE, R² for each model
   - Compare model performance
   - Save results to `reports/model_comparison.csv`

## 🎨 Web Interface Features

### 🌟 Visual Design
- **Cyberpunk Aesthetic** - Neon colors and futuristic design
- **Glassmorphism** - Frosted glass effects with backdrop blur
- **Animated Gradients** - Background and text color transitions
- **3D Effects** - Perspective transforms and floating animations
- **Neon Glow** - Pulsing shadows and glowing elements
- **Smooth Transitions** - All interactions beautifully animated

### 🎯 User Experience
- **Responsive Design** - Works on desktop and mobile
- **Modern UI** - Gradient colors, cards, and smooth animations
- **Interactive Charts** - Hover, zoom, and explore data
- **Risk Indicators** - Color-coded factors (🟢 Low, 🟡 Medium, 🔴 High)
- **Real-time Validation** - Input constraints and helpful tooltips
- **Visual Feedback** - Hover states on all interactive elements

### ✨ Special Effects
- **Floating Animation** - Premium box floats up and down
- **Shine Sweep** - Light sweep across premium display
- **Pulse Effect** - Buttons pulse with neon glow
- **Gradient Text** - Animated color-shifting titles
- **Card Hover** - Lift and scale transformations
- **Custom Scrollbar** - Gradient design matching theme

## 📊 Data Insights Dashboard

The Data Insights tab provides:
- **Summary Statistics** - Total records, average/min/max premiums
- **Premium Distribution** - Histogram showing frequency
- **Age Group Analysis** - Box plots comparing age ranges
- **Vehicle Type Comparison** - Premium variations by model
- **Regional Analysis** - Bar chart of average premiums by region

## ⚠️ Disclaimer

This is a predictive model for **educational and demonstration purposes**. Actual insurance premiums may vary based on:
- Additional risk factors not included in the model
- Insurance company policies and underwriting guidelines
- State/regional regulations
- Market conditions and competition
- Individual insurance history

**Not for commercial use without proper validation and compliance.**

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Add more features (vehicle safety ratings, driver history)
- Implement additional ML models (Neural Networks, LightGBM)
- Add model explainability (SHAP values)
- Create API endpoint for predictions
- Add unit tests and CI/CD pipeline
- Enhance animations and visual effects
- Add dark/light theme toggle
- Implement more interactive visualizations

## 🎨 Design Credits

**Frontend Design:**
- **Style**: Cyberpunk meets Modern Minimalism
- **Effects**: Glassmorphism, 3D transforms, Neon glow
- **Animations**: CSS keyframes (10+ custom animations)
- **Typography**: Google Fonts - Poppins
- **Color Palette**: Pink (#ff006e), Purple (#8338ec), Blue (#3a86ff), Green (#06ffa5)

## 📄 License

This project is for educational purposes. Feel free to use and modify for learning.

## 🙏 Acknowledgments

- **Dataset:** Synthetic data generated for demonstration
- **ML Libraries:** scikit-learn, XGBoost
- **Web Framework:** Streamlit
- **Visualization:** Plotly
- **Design Inspiration:** Cyberpunk aesthetics, Glassmorphism trends
- **Typography:** Google Fonts (Poppins)

---

**Built with ❤️ using Python, Streamlit, XGBoost & Crazy CSS Animations**

*Last Updated: May 2026*

---

## 📸 Screenshots

### 🎨 Design Features
- ✨ Animated gradient background with 4-color transitions
- 💎 Glassmorphism effects on all containers
- 🔮 3D floating premium display with shine effect
- ⚡ Neon glow buttons with pulse animation
- 🌈 Color-shifting gradient text
- 💫 Interactive hover effects on all elements
- 🎯 Custom gradient scrollbar
- 🚀 Smooth transitions and animations throughout

### 🎭 Visual Effects List
1. **gradientBG** - Background color shifting (15s)
2. **float** - Vertical floating motion (3s)
3. **pulse** - Pulsing glow effect (1s)
4. **shine** - Diagonal sweep effect (3s)
5. **glow** - Text glow pulsing (2s)
6. **gradientText** - Text color shifting (5s)
7. **Hover animations** - Scale, lift, and transform
8. **3D transforms** - Perspective and rotation
9. **Backdrop blur** - Glassmorphism effect
10. **Custom scrollbar** - Gradient styling

---

🚗 **Experience the future of insurance calculators!** ✨

---

## 🎯 What Makes This Special?

### 🎨 Design Innovation
Unlike typical boring calculators, this app features:
- **Cyberpunk aesthetic** with neon colors and futuristic vibes
- **Glassmorphism** - the hottest design trend of 2026
- **10+ custom animations** that bring the interface to life
- **3D effects** that make elements pop off the screen
- **Every pixel carefully crafted** for maximum visual impact

### 🤖 AI Power
- **83.1% accuracy** using XGBoost gradient boosting
- **Real-time predictions** in milliseconds
- **Trained on 10,000 records** with 13 features
- **Multiple models** compared for best performance

### 💡 User Experience
- **Intuitive interface** - anyone can use it
- **Visual feedback** on every interaction
- **Risk analysis** with color-coded indicators
- **Interactive charts** for data exploration
- **Responsive design** works everywhere

### 🚀 Technical Excellence
- **Modern Python stack** (Pandas, Scikit-learn, XGBoost)
- **Streamlit framework** for rapid development
- **Modular architecture** for easy maintenance
- **Configuration-driven** for flexibility
- **Production-ready** code structure

---

## 📞 Support

Found a bug? Want a feature? Have design suggestions?
- Open an issue on GitHub
- Contribute via pull request
- Share your feedback

---

**Made with 💜 and lots of CSS magic**

*Transform your boring apps into visual masterpieces!* ✨🎨🚀