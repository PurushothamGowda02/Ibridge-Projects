# RFM Analysis - Customer Segmentation Platform

A full-stack web application for RFM (Recency, Frequency, Monetary) customer segmentation analysis. Analyze customer behavior, identify high-value customers, and segment your customer base for targeted marketing strategies.

![Project Status](https://img.shields.io/badge/status-active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Node.js](https://img.shields.io/badge/Node.js-16+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135+-red)
![React](https://img.shields.io/badge/React-18.2+-61dafb)

## 🎯 Features

- **RFM Analysis** - Compute Recency, Frequency, and Monetary metrics for all customers
- **Customer Segmentation** - Automatically segment customers into 7 meaningful categories
- **Interactive Dashboard** - Visualize customer segments with charts and data tables
- **Data Upload** - Analyze new datasets with the same RFM methodology
- **REST API** - Complete API for programmatic access to RFM data
- **Real-time Processing** - Fast computation and analysis of customer data
- **Responsive Design** - Works on desktop, tablet, and mobile devices

## 📊 Customer Segments

The system automatically classifies customers into:

1. **Champions** - Best customers, high recency & frequency
2. **Loyal Customers** - Frequent buyers with good recency
3. **Potential Loyalists** - Recent customers with moderate frequency
4. **New Customers** - Recent first-time or infrequent buyers
5. **At Risk** - Previously frequent but haven't purchased recently
6. **Lost** - Inactive customers with low recency and frequency
7. **Others** - Remaining customers

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 16+
- npm (comes with Node.js)

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
run-project.bat
```

**macOS/Linux:**
```bash
chmod +x run-project.sh
./run-project.sh
```

### Option 2: Manual Setup

**Backend:**
```bash
cd backend
python -m venv .venv

# Windows
.\.venv\Scripts\activate.bat

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python -m uvicorn main:app --reload
```

**Frontend (in new terminal):**
```bash
cd frontend
npm install
npm start
```

### Access the Application

- **Frontend Dashboard:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## 📁 Project Structure

```
RFM-Analysis/
├── backend/                    # FastAPI backend
│   ├── main.py                # Application entry point
│   ├── config.py              # Configuration
│   ├── requirements.txt        # Python dependencies
│   ├── data/
│   │   ├── online_retail.csv  # Training dataset (100 transactions)
│   │   ├── test_dataset.csv   # Test dataset (40 transactions)
│   │   └── ingestion.py       # Data loading & cleaning
│   ├── rfm/
│   │   └── computation.py     # RFM calculation logic
│   ├── api/
│   │   └── router.py          # API endpoints
│   ├── tests/                 # Unit tests
│   └── docs/                  # Documentation
│
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── App.js            # Main component
│   │   └── components/       # React components
│   ├── package.json
│   └── public/
│
├── SETUP_AND_RUN.md          # Detailed setup guide
├── run-project.sh            # Quick start script (Unix)
├── run-project.bat           # Quick start script (Windows)
└── README.md                 # This file
```

## 🔌 API Endpoints

### Health Check
```
GET /api/health
```

### Get All RFM Data
```
GET /api/rfm
```

### Get Segment Summary
```
GET /api/segments/summary
```

### Get Top-N Customers
```
GET /api/rfm/top?n=10
```

### Analyze Unseen Dataset
```
POST /api/rfm/analyze-unseen
Content-Type: multipart/form-data
```

See [SETUP_AND_RUN.md](SETUP_AND_RUN.md) for detailed API documentation.

## 📊 CSV Data Format

Required columns for data upload:

| Column | Type | Example |
|--------|------|---------|
| InvoiceNo | string | INV001 |
| StockCode | string | SKU001 |
| Description | string | Ceramic Coffee Mug |
| Quantity | integer | 5 |
| InvoiceDate | datetime | 01/15/2024 10:30 |
| UnitPrice | float | 12.99 |
| CustomerID | string | C10001 |
| Country | string | United Kingdom |

**Sample datasets included:**
- `backend/data/online_retail.csv` - 100 transactions
- `backend/data/test_dataset.csv` - 40 transactions

## 🧪 Running Tests

```bash
cd backend

# Install test dependencies
pip install pytest hypothesis httpx

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_computation.py -v

# Run with coverage
pip install pytest-cov
pytest tests/ --cov=. --cov-report=html
```

## 📚 Documentation

- **[SETUP_AND_RUN.md](SETUP_AND_RUN.md)** - Complete setup and running guide
- **[backend/README.md](backend/README.md)** - Backend documentation
- **[backend/docs/rfm_methodology.md](backend/docs/rfm_methodology.md)** - RFM theory
- **[backend/docs/segment_mapping.md](backend/docs/segment_mapping.md)** - Segment definitions

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pandas** - Data manipulation and analysis
- **Pydantic** - Data validation
- **Pytest** - Testing framework

### Frontend
- **React** - UI library
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **CSS3** - Styling

## 🔧 Configuration

### Environment Variables

Create `.env` in `backend/` directory:

```bash
DATASET_PATH=data/online_retail.csv
CORS_ORIGINS=http://localhost:3000
HOST=0.0.0.0
PORT=8000
```

### Backend Configuration

Edit `backend/config.py`:

```python
DATASET_PATH = "data/online_retail.csv"
CORS_ORIGINS = ["*"]  # or specific origins
```

## 🐛 Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'fastapi'"**
```bash
# Activate virtual environment and install dependencies
pip install -r requirements.txt
```

**"Address already in use" (Port 8000)**
```bash
# Use different port
python -m uvicorn main:app --port 8001
```

### Frontend Issues

**"npm: command not found"**
- Install Node.js from https://nodejs.org/

**"Port 3000 already in use"**
```bash
PORT=3001 npm start
```

See [SETUP_AND_RUN.md](SETUP_AND_RUN.md) for more troubleshooting tips.

## 📈 Performance

- Handles datasets with up to 100,000+ customers
- Fast RFM computation using pandas vectorization
- Efficient quantile-based scoring
- Responsive UI with real-time updates

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is provided as-is for educational and commercial purposes.

## 📞 Support

For issues or questions:

1. Check [SETUP_AND_RUN.md](SETUP_AND_RUN.md) troubleshooting section
2. Review backend logs in terminal
3. Check browser console (F12) for frontend errors
4. Verify all prerequisites are installed

## 🎓 Learning Resources

- **RFM Analysis:** https://en.wikipedia.org/wiki/RFM_(customer_value)
- **FastAPI:** https://fastapi.tiangolo.com/
- **React:** https://react.dev/
- **Pandas:** https://pandas.pydata.org/

## 📊 Sample Data

The project includes sample datasets:

**Training Data** (`backend/data/online_retail.csv`):
- 100 transactions
- 13 unique customers
- Multiple countries
- Date range: Jan-Apr 2024

**Test Data** (`backend/data/test_dataset.csv`):
- 40 transactions
- 13 unique customers
- Multiple countries
- Date range: Apr-Jun 2024

Use these to test the application or upload your own data.

## 🚀 Deployment

### Deploy Backend

**Using Gunicorn:**
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

**Using Docker:**
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deploy Frontend

**Build for production:**
```bash
npm run build
```

**Serve with static server:**
```bash
npm install -g serve
serve -s build
```

## 📅 Version History

- **v1.0.0** (April 2024) - Initial release
  - RFM analysis and segmentation
  - Interactive dashboard
  - REST API
  - Data upload functionality

## 🎯 Roadmap

- [ ] Advanced filtering and search
- [ ] Export reports (PDF, Excel)
- [ ] Customer journey visualization
- [ ] Predictive churn analysis
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Mobile app

---

**Last Updated:** April 2024  
**Maintainer:** RFM Analysis Team  
**Status:** Active Development
