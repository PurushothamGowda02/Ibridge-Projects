# RFM Analysis - Quick Commands Reference

Quick reference for common commands to run and manage the RFM Analysis project.

## 🚀 Quick Start

### Windows
```bash
run-project.bat
```

### macOS/Linux
```bash
chmod +x run-project.sh
./run-project.sh
```

---

## 📦 Setup Commands

### First Time Setup

**Windows (PowerShell):**
```powershell
# Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

**macOS/Linux:**
```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### Activate Virtual Environment

**Windows (PowerShell):**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
cd backend
.\.venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
cd backend
source .venv/bin/activate
```

---

## ▶️ Running the Project

### Run Both Backend and Frontend

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Run Backend Only

```bash
cd backend
python -m uvicorn main:app --reload
```

### Run Frontend Only

```bash
cd frontend
npm start
```

### Run on Different Ports

**Backend on port 8001:**
```bash
cd backend
python -m uvicorn main:app --port 8001
```

**Frontend on port 3001:**
```bash
cd frontend
PORT=3001 npm start
```

---

## 🧪 Testing Commands

### Install Test Dependencies

```bash
cd backend
pip install pytest hypothesis httpx pytest-cov
```

### Run All Tests

```bash
cd backend
pytest tests/ -v
```

### Run Specific Test File

```bash
cd backend
pytest tests/test_ingestion.py -v
pytest tests/test_computation.py -v
pytest tests/test_api.py -v
```

### Run Tests with Coverage

```bash
cd backend
pytest tests/ --cov=. --cov-report=html
```

### Run Tests with Hypothesis Statistics

```bash
cd backend
pytest tests/ -v --hypothesis-show-statistics
```

---

## 🔌 API Testing Commands

### Health Check
```bash
curl http://localhost:8000/api/health
```

### Get All RFM Data
```bash
curl http://localhost:8000/api/rfm
```

### Get Segment Summary
```bash
curl http://localhost:8000/api/segments/summary
```

### Get Top 10 Customers
```bash
curl http://localhost:8000/api/rfm/top?n=10
```

### Get Top 20 Customers
```bash
curl http://localhost:8000/api/rfm/top?n=20
```

### Upload CSV File for Analysis
```bash
curl -X POST -F "file=@backend/data/test_dataset.csv" \
  http://localhost:8000/api/rfm/analyze-unseen
```

### Using Python Requests

```python
import requests

# Health check
response = requests.get('http://localhost:8000/api/health')
print(response.json())

# Get RFM data
response = requests.get('http://localhost:8000/api/rfm')
data = response.json()
print(f"Total customers: {len(data)}")

# Upload file
with open('backend/data/test_dataset.csv', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/api/rfm/analyze-unseen',
        files=files
    )
    print(response.json())
```

---

## 📊 Data Management Commands

### Generate New Dataset

```bash
cd backend
python data/generate_dataset.py
```

### Validate CSV Format

```bash
cd backend
python -c "
import pandas as pd
df = pd.read_csv('data/online_retail.csv')
print('Columns:', df.columns.tolist())
print('Rows:', len(df))
print('Missing values:', df.isnull().sum().sum())
"
```

### Check Data Statistics

```bash
cd backend
python -c "
import pandas as pd
df = pd.read_csv('data/online_retail.csv')
print(df.describe())
"
```

---

## 🔧 Dependency Management

### Update Dependencies

```bash
cd backend
pip install --upgrade -r requirements.txt
```

### Check Outdated Packages

```bash
cd backend
pip list --outdated
```

### Freeze Current Dependencies

```bash
cd backend
pip freeze > requirements.txt
```

### Frontend Dependencies

```bash
cd frontend
npm update
npm outdated
npm install
```

---

## 🧹 Cleanup Commands

### Remove Virtual Environment

**Windows:**
```powershell
cd backend
Remove-Item -Recurse -Force .venv
```

**macOS/Linux:**
```bash
cd backend
rm -rf .venv
```

### Remove Node Modules

```bash
cd frontend
rm -rf node_modules
npm install
```

### Clear Python Cache

```bash
cd backend
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Clean Build Artifacts

```bash
cd frontend
rm -rf build
npm run build
```

---

## 🐛 Debugging Commands

### Check Backend Logs

```bash
cd backend
python -m uvicorn main:app --reload --log-level debug
```

### Check Frontend Logs

```bash
cd frontend
npm start
# Check browser console (F12)
```

### Test Backend Connection

```bash
cd backend
python -c "
import requests
try:
    response = requests.get('http://localhost:8000/api/health')
    print('✓ Backend is running')
    print(response.json())
except:
    print('✗ Backend is not running')
"
```

### Check Port Usage

**Windows:**
```powershell
netstat -ano | findstr :8000
netstat -ano | findstr :3000
```

**macOS/Linux:**
```bash
lsof -i :8000
lsof -i :3000
```

### Kill Process on Port

**Windows:**
```powershell
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
kill -9 <PID>
```

---

## 📝 Environment Setup

### Create .env File

**Windows (PowerShell):**
```powershell
cd backend
@"
DATASET_PATH=data/online_retail.csv
CORS_ORIGINS=http://localhost:3000
HOST=0.0.0.0
PORT=8000
"@ | Out-File -Encoding UTF8 .env
```

**macOS/Linux:**
```bash
cd backend
cat > .env << EOF
DATASET_PATH=data/online_retail.csv
CORS_ORIGINS=http://localhost:3000
HOST=0.0.0.0
PORT=8000
EOF
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

## 🚀 Production Commands

### Build Frontend for Production

```bash
cd frontend
npm run build
```

### Run Backend with Gunicorn

```bash
cd backend
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Run Backend with Multiple Workers

```bash
cd backend
python -m uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
```

### Serve Frontend with Static Server

```bash
cd frontend
npm install -g serve
serve -s build
```

---

## 📚 Documentation Commands

### View API Documentation

Open in browser:
```
http://localhost:8000/docs
```

### View ReDoc Documentation

Open in browser:
```
http://localhost:8000/redoc
```

### Generate Test Coverage Report

```bash
cd backend
pytest tests/ --cov=. --cov-report=html
# Open htmlcov/index.html in browser
```

---

## 🔄 Common Workflows

### Complete Development Cycle

```bash
# 1. Setup (first time only)
cd backend
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt

cd ../frontend
npm install

# 2. Run tests
cd ../backend
pytest tests/ -v

# 3. Start development servers
# Terminal 1
cd backend
python -m uvicorn main:app --reload

# Terminal 2
cd frontend
npm start

# 4. Access application
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Add New Python Dependency

```bash
cd backend
pip install <package-name>
pip freeze > requirements.txt
```

### Add New Frontend Dependency

```bash
cd frontend
npm install <package-name>
```

### Deploy to Production

```bash
# Backend
cd backend
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Frontend
cd frontend
npm run build
serve -s build
```

---

## 💡 Tips & Tricks

### Quick API Test with Python

```bash
cd backend
python << 'EOF'
import requests
import json

# Test health
r = requests.get('http://localhost:8000/api/health')
print("Health:", r.json())

# Test RFM data
r = requests.get('http://localhost:8000/api/rfm')
print(f"Customers: {len(r.json())}")

# Test segments
r = requests.get('http://localhost:8000/api/segments/summary')
print("Segments:", json.dumps(r.json(), indent=2))
EOF
```

### Monitor Backend in Real-time

```bash
cd backend
python -m uvicorn main:app --reload --log-level debug
```

### Clear Browser Cache

- Chrome: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
- Firefox: Ctrl+Shift+Delete (or Cmd+Shift+Delete on Mac)
- Safari: Develop → Empty Web Storage

### Restart Services

```bash
# Kill all Python processes
# Windows
taskkill /F /IM python.exe

# macOS/Linux
pkill -f python

# Kill all Node processes
# Windows
taskkill /F /IM node.exe

# macOS/Linux
pkill -f node
```

---

## 🆘 Emergency Commands

### Reset Everything

```bash
# Backend
cd backend
rm -rf .venv __pycache__ .pytest_cache
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Frontend
cd ../frontend
rm -rf node_modules
npm install
```

### Force Kill All Processes

**Windows:**
```powershell
taskkill /F /IM python.exe
taskkill /F /IM node.exe
```

**macOS/Linux:**
```bash
pkill -9 python
pkill -9 node
```

### Clear All Cache

```bash
# Python
cd backend
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Node
cd ../frontend
rm -rf node_modules .cache
npm install
```

---

## 📞 Getting Help

### Check Logs

```bash
# Backend logs are printed to console
# Frontend logs are in browser console (F12)

# Check for errors
cd backend
python -m uvicorn main:app --reload --log-level debug
```

### Verify Installation

```bash
python --version
node --version
npm --version
pip list
npm list
```

### Test Connectivity

```bash
curl http://localhost:8000/api/health
curl http://localhost:3000
```

---

**Last Updated:** April 2024  
**Version:** 1.0.0
