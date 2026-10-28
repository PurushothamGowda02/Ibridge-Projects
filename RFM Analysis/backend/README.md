# RFM Analysis Backend

A Python-based REST API for RFM (Recency, Frequency, Monetary) customer segmentation analysis. This project demonstrates how to build a full-stack data application with a clean architecture, comprehensive documentation, and property-based testing.

## Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Setup Instructions

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   
   **On Windows (PowerShell):**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   **On Windows (Command Prompt):**
   ```cmd
   .\.venv\Scripts\activate.bat
   ```
   
   **On macOS/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Start the development server:**
   ```bash
   python -m uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`

6. **Open the frontend:**
   - Navigate to the `frontend/` directory
   - Open `index.html` in your web browser
   - The dashboard will load data from the running backend API

## Project Structure

```
backend/
├── main.py                  # FastAPI application entry point
├── config.py                # Configuration settings (dataset path, CORS origins)
├── requirements.txt         # Python dependencies (pinned versions)
├── data/
│   ├── __init__.py
│   ├── ingestion.py         # load_dataset(), clean_dataset()
│   └── online_retail.csv    # Sample dataset (12,000+ rows)
├── rfm/
│   ├── __init__.py
│   └── computation.py       # compute_rfm(), assign_scores(), assign_segments()
├── api/
│   ├── __init__.py
│   └── router.py            # REST API endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared pytest fixtures
│   ├── test_ingestion.py    # Tests for data ingestion
│   ├── test_computation.py  # Tests for RFM computation
│   └── test_api.py          # Tests for API endpoints
├── docs/
│   ├── rfm_methodology.md   # Explanation of RFM theory
│   └── segment_mapping.md   # Segment label rules and descriptions
└── README.md                # This file
```

## API Endpoints

### Health Check
```
GET /api/health
```
Returns: `{"status": "ok"}`

### Full RFM Data
```
GET /api/rfm
```
Returns a JSON array of all customers with their RFM metrics and segment labels.

**Response Example:**
```json
[
  {
    "CustomerID": "C1001",
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

### Segment Summary
```
GET /api/segments/summary
```
Returns the distribution of customers across segments with counts and percentages.

**Response Example:**
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

### Top-N Customers
```
GET /api/rfm/top?n=10
```
Returns the top-n customers ranked by RFM_Score in descending order.

**Query Parameters:**
- `n` (optional, default=10): Number of top customers to return. Must be a positive integer.

**Response:** Same format as `/api/rfm`, but limited to top-n records.

## Running Tests

### Install Test Dependencies
```bash
pip install pytest hypothesis httpx
```

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_ingestion.py -v
```

### Run with Hypothesis Statistics
```bash
pytest tests/ -v --hypothesis-show-statistics
```

## Configuration

### Environment Variables

You can override default settings using environment variables:

```bash
# Set custom dataset path
export DATASET_PATH=/path/to/custom_dataset.csv

# Set custom CORS origins (comma-separated)
export CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:5500"
```

### Configuration File

Settings are defined in `config.py`:
- `DATASET_PATH`: Path to the CSV dataset (default: `data/online_retail.csv`)
- `CORS_ORIGINS`: Allowed CORS origins (default: `["*"]`)

## Dataset Format

The backend expects a CSV file with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| InvoiceNo | string | Unique invoice identifier |
| StockCode | string | Product code |
| Description | string | Product name |
| Quantity | integer | Units purchased (can be negative for returns) |
| InvoiceDate | datetime | Purchase date (format: MM/DD/YYYY HH:MM) |
| UnitPrice | float | Price per unit |
| CustomerID | string | Customer identifier (can be null) |
| Country | string | Customer country |

**Data Cleaning:**
- Rows with null `CustomerID`, `InvoiceDate`, `Quantity`, or `UnitPrice` are dropped.
- `Amount` is derived as `Quantity × UnitPrice`.
- Rows where `Amount ≤ 0` are dropped (returns, cancellations, free items).

## RFM Methodology

### Metrics

- **Recency (R):** Days since last purchase (lower is better)
- **Frequency (F):** Number of distinct transactions (higher is better)
- **Monetary (M):** Total amount spent (higher is better)

### Scoring

Each metric is scored 1–5 using quantile binning:
- **Score 5:** Top 20% (most favorable)
- **Score 1:** Bottom 20% (least favorable)

Recency is inverted: lower recency (more recent) gets a higher score.

### Segments

Customers are assigned to one of seven segments based on their R and F scores:
1. **Champions** – R ≥ 4, F ≥ 4
2. **Loyal Customers** – F ≥ 4, R ≥ 2
3. **Potential Loyalists** – R ≥ 3, F ≥ 2
4. **New Customers** – R ≥ 4, F = 1
5. **At Risk** – R ≤ 2, F ≥ 3
6. **Lost** – R ≤ 2, F ≤ 2
7. **Others** – All remaining

For detailed explanations, see:
- `docs/rfm_methodology.md` – RFM theory and scoring
- `docs/segment_mapping.md` – Segment definitions and strategies

## Development

### Code Structure

- **`data/ingestion.py`** – Data loading and cleaning
- **`rfm/computation.py`** – RFM metric computation and segmentation
- **`api/router.py`** – REST API endpoint definitions
- **`main.py`** – FastAPI application factory and startup logic

### Adding New Endpoints

1. Add a new route to `api/router.py`:
   ```python
   @router.get("/api/new-endpoint")
   def new_endpoint(request: Request):
       rfm_df = request.app.state.rfm_df
       # Your logic here
       return result
   ```

2. The endpoint will be automatically available at `http://localhost:8000/api/new-endpoint`

### Logging

The application uses Python's standard `logging` module. Logs are printed to the console with timestamps and log levels.

## Troubleshooting

### "Dataset file not found"
- Ensure `data/online_retail.csv` exists in the backend directory.
- Or set the `DATASET_PATH` environment variable to the correct path.

### "Address already in use"
- The default port 8000 is already in use.
- Change the port in `main.py` or use: `uvicorn main:app --port 8001`

### CORS errors in the frontend
- Ensure the backend is running at `http://localhost:8000`
- Check that `CORS_ORIGINS` includes the frontend origin (default is `["*"]` which allows all)

### Tests fail with import errors
- Ensure you're running pytest from the `backend/` directory or with `pytest backend/tests/`
- Verify all dependencies are installed: `pip install -r requirements.txt pytest hypothesis httpx`

## Performance Notes

- The entire RFM dataset is loaded into memory at startup and cached on `app.state.rfm_df`.
- For datasets with millions of rows, consider implementing pagination or streaming responses.
- The current implementation is suitable for datasets up to ~100,000 customers.

## License

This project is provided as-is for educational purposes.

## Support

For questions or issues, refer to the documentation in `docs/` or review the inline code comments.
