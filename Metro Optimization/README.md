# 🚇 Metro Optimization System

A comprehensive web-based metro management and passenger assistance platform built with Flask, featuring AI-powered chatbot, ML-based demand forecasting, and real-time route optimization for Bangalore Metro (Namma Metro).

## ✨ Features

### 🎯 Core Features
- **User Authentication** - Secure login/registration with role-based access (User/Admin)
- **Metro Card Management** - Link NCMC/CMC cards, check balance, recharge online
- **KYC Verification** - Digital document verification for metro cards
- **Route Planning** - Find optimal routes between stations with fare calculation
- **Interactive Metro Map** - Visual representation of all metro lines and stations
- **Real-time Schedules** - View train timings and availability

### 🤖 AI & ML Features
- **AI Chatbot** - Powered by Groq LLM (Llama 3.1) for intelligent passenger assistance
- **Demand Forecasting** - ML-based 24-hour passenger demand prediction
- **Smart Recommendations** - Personalized route suggestions based on travel history

### 📊 Analytics & Monitoring
- **Passenger Flow Analysis** - Real-time tracking of station occupancy
- **Journey Statistics** - Personal travel history and spending analytics
- **Admin Dashboard** - System-wide metrics and user management

### 📧 Notifications
- **Email Alerts** - Recharge confirmations and line status updates
- **Real-time Updates** - Live metro line status and delays

## 🏗️ Tech Stack

**Backend:**
- Flask 3.0+ (Python web framework)
- SQLAlchemy (ORM)
- SQLite (Database)
- Flask-Login (Authentication)

**AI/ML:**
- LangChain + Groq API (AI Chatbot)
- scikit-learn (Demand forecasting)
- pandas, numpy (Data processing)

**Frontend:**
- HTML5, CSS3, JavaScript
- Tailwind CSS (Styling)
- Font Awesome (Icons)

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Groq API Key (for AI chatbot - get free at [console.groq.com](https://console.groq.com))

## 🚀 Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd metro-optimization
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

**Get your Groq API Key:**
1. Visit https://console.groq.com
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy and paste it in the .env file

### 5. Initialize the database
The database will be automatically created on first run with seed data for Bangalore Metro (Purple & Green Lines).

### 6. Run the application
```bash
python app.py
```

The application will be available at: **http://127.0.0.1:5000**

## 📁 Project Structure

```
metro-optimization/
├── app.py                  # Main Flask application
├── database.py             # Database models and initialization
├── chatbot.py              # AI chatbot implementation
├── email_service.py        # Email notification service
├── route_recommender.py    # Route optimization logic
├── ml_training.py          # ML model training script
├── data_generation.py      # Test data generation utility
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── metro_db.sqlite         # SQLite database (auto-generated)
├── data/                   # Passenger data files
├── models/                 # Trained ML models
├── static/                 # CSS, JavaScript, images
│   ├── css/
│   └── js/
└── templates/              # HTML templates
    ├── base.html
    ├── index.html
    ├── chatbot.html
    ├── cards.html
    ├── routes.html
    └── ...
```

## 🎮 Usage

### For Passengers

1. **Register/Login**
   - Create an account or login with existing credentials
   - Demo card with ₹100 balance is automatically created

2. **Manage Metro Cards**
   - Link NCMC/CMC cards
   - Recharge cards online
   - Complete KYC verification

3. **Plan Your Journey**
   - Select source and destination stations
   - View route options and fare
   - Check train schedules

4. **Use AI Chatbot**
   - Ask questions about fares, routes, schedules
   - Get instant AI-powered responses
   - Access quick action buttons

5. **View Analytics**
   - Track your journey history
   - Monitor spending patterns
   - Get personalized route recommendations

### For Administrators

1. **Access Admin Dashboard**
   - Login with admin role
   - View system-wide statistics

2. **Manage System**
   - Monitor all users and journeys
   - Configure train capacity settings
   - View demand forecasts

3. **System Settings**
   - Adjust base train count
   - Set maximum capacity
   - Configure operational parameters

## 🔑 Default Credentials

After registration, you can create an admin account by setting `role='admin'` in the database or during registration.

## 🗺️ Metro Lines

The system includes real Bangalore Metro (Namma Metro) data:

**Purple Line (East-West):**
- 37 stations from Kadugodi to Challaghatta
- Operational status

**Green Line (North-South):**
- 24 stations from Nagasandra to Yelachenahalli
- Operational status

**Interchange Station:**
- Nadaprabhu Kempegowda (Majestic)

## 💰 Fare Structure

Station-count based fare slabs (Bangalore Metro standard):
- 0-2 stations: ₹10
- 3-4 stations: ₹20
- 5-6 stations: ₹30
- 7-9 stations: ₹40
- 10+ stations: ₹50

## 🤖 AI Chatbot

The chatbot uses Groq's Llama 3.1 model for intelligent responses:
- Natural language understanding
- Context-aware answers
- Metro-specific knowledge base
- Fallback to rule-based responses if API unavailable

**Sample Questions:**
- "What are the operating hours?"
- "How do I recharge my card?"
- "What is the fare from MG Road to Indiranagar?"
- "Tell me about KYC verification"

## 📊 ML Demand Forecasting

The system uses Random Forest Regressor to predict passenger demand:
- 24-hour forecasting window
- Considers time of day, day of week
- Suggests optimal train allocation
- Helps in resource optimization

## 🛠️ Development

### Generate Test Data
```bash
python data_generation.py
```

### Train ML Model
```bash
python ml_training.py
```

### Run in Debug Mode
```bash
# Already enabled in app.py
python app.py
```

## 🔒 Security Features

- Password hashing with Werkzeug
- Session management with Flask-Login
- CSRF protection
- Role-based access control
- Secure environment variable handling

## 📧 Email Configuration

Email notifications are configured but require SMTP setup in `email_service.py`. Currently uses console output for development.

## 🐛 Troubleshooting

**Issue: Chatbot not responding**
- Ensure GROQ_API_KEY is set in .env file
- Get a valid API key from https://console.groq.com/keys
- Check internet connection
- Verify API key is valid and not expired
- Restart the application after updating .env file

**Issue: Database errors**
- Delete `metro_db.sqlite` and restart app
- Database will be recreated with seed data

**Issue: ML model not found**
- Run `python ml_training.py` to generate model
- Model will be saved in `models/` directory

**Issue: Import errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Activate virtual environment before running
- Check Python version (3.8+ required)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is for educational purposes.

## 👥 Authors

Metro Optimization System Development Team

## 🙏 Acknowledgments

- Bangalore Metro Rail Corporation Limited (BMRCL) for metro data
- Groq for AI API access
- Flask and Python community

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact: support@metrooptimized.com (demo)
- Phone: +91-80-2363-2363 (demo)

---

**Made with ❤️ for Bangalore Metro Passengers**
