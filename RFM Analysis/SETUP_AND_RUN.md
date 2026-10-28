# RFM Analysis Project - Complete Setup & Running Guide

This guide provides step-by-step instructions to set up and run the RFM Analysis project on Windows, macOS, and Linux.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Project Structure](#project-structure)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Running the Project](#running-the-project)
6. [API Endpoints](#api-endpoints)
7. [CSV Data Format](#csv-data-format)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **npm** (comes with Node.js)
- **Git** (optional, for version control)

### Verify Installation

```bash
# Check Python version
python --version

# Check Node.js version
node --version

# Check npm version
npm --version
```

---

## Project Structure

```
RFM-Analysis/
├── backend/                          # FastAPI backend
│   ├── main.py                       # Application entry point
│   ├── config.py                     # Configuration settings
│   ├── requirements.txt              # Python dependencies
│   ├── data/
│   │   ├── online_retail.csv         # Training dataset (100 transactions)
│   │   ├── test_dataset.csv          # Test dataset (40 transactions)
│   │   ├── ingestion.py              # Data loading & cleaning
│   │   └── generate_dataset.py       # Dataset generation utility
│   ├── rfm/
│   │   ├── computation.py            # RFM calculation logic
│   │   └── __init__.py
│   ├── api/
│   │   ├── router.py                 # API endpoints
│   │   └── __init__.py
│   ├── tests/                        # Unit tests
│   │   ├── test_api.py
│   │   ├── test_computation.py
│   │   ├── test_ingestion.py
│   │   └── conftest.py
│   ├── docs/                         # Documentation
│   │   ├── rfm_methodology.md
│   │   └── segment_mapping.md
│   └── README.md
│
├── frontend/                         # React frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js                    # Main React component
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css
│   │   └── components/
│   │       ├── TrainingDataTab.js    # Training data visualization
│   │       ├── UnseenDataTab.js      # Upload & analyze new data
│   │       ├── BarChart.js           # Segment distribution chart
│   │       ├── ScatterPlot.js        # Recency vs Monetary chart
│   │       ├── DataTable.js          # Customer data table
│   │       └── SummaryCards.js       # KPI cards
│   ├── package.json
│   ├── package-lock.json
│   └── node_modules/
│
└── SETUP_AND_RUN.md                  # This file
```

---

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.135.3 uvicorn-0.44.0 pandas-3.0.2 ...
```

### Step 4: Verify Backend Setup

```bash
python -c "import fastapi; import pandas; print('✓ Backend dependencies installed')"
```

---

## Frontend Setup

### Step 1: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 2: Install Dependencies

```bash
npm install
```

**Expected output:**
```
added 1234 packages in 45s
```

### Step 3: Verify Frontend Setup

```bash
npm --version
```

---

## Running the Project

### Option 1: Run Both Servers (Recommended)

#### Terminal 1 - Start Backend

```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
INFO:     Startup complete — 1482 customers loaded and segmented.
```

#### Terminal 2 - Start Frontend

```bash
cd frontend
npm start
```

**Expected output:**
```
Compiled successfully!

You can now view rfm-analysis-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

### Option 2: Run Backend Only (API Testing)

```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

Then test the API:
```bash
# Health check
curl http://localhost:8000/api/health

# Get RFM data
curl http://localhost:8000/api/rfm

# Get segment summary
curl http://localhost:8000/api/segments/summary

# Get top 10 customers
curl http://localhost:8000/api/rfm/top?n=10
```

### Option 3: Run Frontend Only (Static Testing)

```bash
cd frontend
npm start
```

**Note:** The frontend will show errors if the backend is not running.

---

## API Endpoints

### Base URL
```
http://localhost:8000
```

### 1. Health Check
```
GET /api/health
```

**Response:**
```json
{
  "status": "ok"
}
```

### 2. Get All RFM Data
```
GET /api/rfm
```

**Response:**
```json
[
  {
    "CustomerID": "C10001",
    "Recency": 14,
    "Frequency": 8,
    "Monetary": 1234.56,
    "R_Score": 4,
    "F_Score": 5,
    "M_Score": 4,
    "RFM_Score": "454",
    "Customer_Segment": "Loyal Customers"
  },
  ...
]
```

### 3. Get Segment Summary
```
GET /api/segments/summary
```

**Response:**
```json
[
  {
    "segment": "Champions",
    "count": 312,
    "percentage": 21.05
  },
  {
    "segment": "Loyal Customers",
    "count": 456,
    "percentage": 30.76
  },
  ...
]
```

### 4. Get Top-N Customers
```
GET /api/rfm/top?n=10
```

**Query Parameters:**
- `n` (optional, default=10): Number of top customers to return

**Response:** Same format as `/api/rfm`

### 5. Analyze Unseen Dataset
```
POST /api/rfm/analyze-unseen
```

**Request:**
- Content-Type: `multipart/form-data`
- File: CSV file with required columns

**Response:**
```json
{
  "rfm_data": [...],
  "segments_summary": [...],
  "stats": {
    "total_customers": 150,
    "total_transactions": 250,
    "avg_recency": 45.2,
    "avg_frequency": 3.5,
    "avg_monetary": 125.75,
    "rows_cleaned": 10
  },
  "message": "Successfully analyzed 150 customers from uploaded dataset"
}
```

---

## CSV Data Format

### Required Columns

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| InvoiceNo | string | Unique invoice identifier | INV001 |
| StockCode | string | Product code | SKU001 |
| Description | string | Product name | Ceramic Coffee Mug |
| Quantity | integer | Units purchased | 5 |
| InvoiceDate | datetime | Purchase date | 01/15/2024 10:30 |
| UnitPrice | float | Price per unit | 12.99 |
| CustomerID | string | Customer identifier | C10001 |
| Country | string | Customer country | United Kingdom |

### Example CSV

```csv
InvoiceNo,StockCode,Description,Quantity,InvoiceDate,UnitPrice,CustomerID,Country
INV001,SKU001,Ceramic Coffee Mug,5,01/15/2024 10:30,12.99,C10001,United Kingdom
INV001,SKU002,Stainless Steel Bottle,3,01/15/2024 10:30,24.99,C10001,United Kingdom
INV002,SKU003,Organic Cotton T-Shirt,2,01/16/2024 14:15,18.50,C10002,United States
```

### Data Validation Rules

✅ **Valid data:**
- All required columns present
- No null values in required columns
- Quantity and UnitPrice are positive numbers
- InvoiceDate is a valid date

❌ **Invalid data (will be removed):**
- Missing CustomerID, InvoiceDate, Quantity, or UnitPrice
- Quantity ≤ 0 (returns/cancellations)
- UnitPrice ≤ 0
- Amount (Quantity × UnitPrice) ≤ 0

### Sample Datasets

**Training Dataset:** `backend/data/online_retail.csv` (100 transactions)
**Test Dataset:** `backend/data/test_dataset.csv` (40 transactions)

---

## Running Tests

### Install Test Dependencies

```bash
cd backend
pip install pytest hypothesis httpx
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_ingestion.py -v
pytest tests/test_computation.py -v
pytest tests/test_api.py -v
```

### Run with Coverage

```bash
pip install pytest-cov
pytest tests/ --cov=. --cov-report=html
```

---

## Environment Variables

### Backend Configuration

Create a `.env` file in the `backend/` directory:

```bash
# Custom dataset path
DATASET_PATH=data/online_retail.csv

# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5500

# Server settings
HOST=0.0.0.0
PORT=8000
```

### Load Environment Variables

**Windows (PowerShell):**
```powershell
$env:DATASET_PATH="data/online_retail.csv"
$env:CORS_ORIGINS="http://localhost:3000"
```

**macOS/Linux:**
```bash
export DATASET_PATH="data/online_retail.csv"
export CORS_ORIGINS="http://localhost:3000"
```

---

## Troubleshooting

### Backend Issues

#### "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Ensure virtual environment is activated
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

# Then install dependencies
pip install -r requirements.txt
```

#### "Address already in use" (Port 8000)
```bash
# Use a different port
python -m uvicorn main:app --port 8001

# Or kill the process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :8000
kill -9 <PID>
```

#### "Dataset file not found"
```bash
# Ensure you're in the backend directory
cd backend

# Check if the CSV file exists
ls data/online_retail.csv

# Or set custom path
export DATASET_PATH=/path/to/your/dataset.csv
```

### Frontend Issues

#### "npm: command not found"
```bash
# Install Node.js from https://nodejs.org/
# Then verify installation
node --version
npm --version
```

#### "Port 3000 already in use"
```bash
# Use a different port
PORT=3001 npm start

# Or kill the process using port 3000
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :3000
kill -9 <PID>
```

#### "Cannot GET /" (Frontend not loading)
- Ensure backend is running on port 8000
- Check browser console for CORS errors
- Verify `apiBaseUrl` in frontend code points to correct backend

### CORS Errors

**Error:** "Access to XMLHttpRequest blocked by CORS policy"

**Solution:**
```bash
# Backend is already configured with CORS
# If still having issues, check config.py:
# CORS_ORIGINS = ["*"]  # Allow all origins

# Or specify allowed origins:
# CORS_ORIGINS = ["http://localhost:3000"]
```

### Data Upload Issues

#### "Missing required columns"
- Ensure CSV has all 8 required columns
- Check column names match exactly (case-sensitive)
- Verify no extra spaces in column names

#### "No valid records after cleaning"
- Check for null values in required columns
- Ensure Quantity and UnitPrice are positive
- Verify Amount (Quantity × UnitPrice) > 0

---

## Performance Tips

### Backend Optimization

1. **Increase worker processes:**
   ```bash
   python -m uvicorn main:app --workers 4
   ```

2. **Disable reload in production:**
   ```bash
   python -m uvicorn main:app --reload=false
   ```

3. **Use production server:**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```

### Frontend Optimization

1. **Build for production:**
   ```bash
   npm run build
   ```

2. **Serve production build:**
   ```bash
   npm install -g serve
   serve -s build
   ```

---

## Quick Start Commands

### Complete Setup (First Time)

```bash
# Backend
cd backend
python -m venv .venv
# Activate virtual environment (see above for your OS)
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install

# Done! Now run the project
```

### Run Project (After Setup)

**Terminal 1:**
```bash
cd backend
# Activate virtual environment
python -m uvicorn main:app --reload
```

**Terminal 2:**
```bash
cd frontend
npm start
```

### Access Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## Additional Resources

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **React Documentation:** https://react.dev/
- **Pandas Documentation:** https://pandas.pydata.org/
- **RFM Analysis Theory:** See `backend/docs/rfm_methodology.md`
- **Segment Definitions:** See `backend/docs/segment_mapping.md`

---

## Support

For issues or questions:

1. Check the **Troubleshooting** section above
2. Review backend logs in terminal
3. Check browser console (F12) for frontend errors
4. Verify all prerequisites are installed
5. Ensure ports 8000 and 3000 are available

---

**Last Updated:** April 2024
**Project Version:** 1.0.0
