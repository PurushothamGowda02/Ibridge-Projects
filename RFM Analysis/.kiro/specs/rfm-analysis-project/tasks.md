# Implementation Plan: RFM Analysis Full-Stack Project

## Overview

Incremental build of the full-stack RFM application: project scaffold → dataset → backend pipeline → REST API → frontend → docs → tests. Each task wires into the previous so there is no orphaned code.

## Tasks

- [x] 1. Scaffold project structure and virtual environment
  - Create the top-level `backend/` and `frontend/` directory trees exactly as specified in the design
  - Create `backend/data/__init__.py`, `backend/rfm/__init__.py`, `backend/api/__init__.py`
  - Initialise a `uv` virtual environment inside `backend/` (`uv venv .venv`)
  - Install runtime dependencies: `fastapi`, `uvicorn[standard]`, `pandas`, `python-dotenv`
  - Generate `backend/requirements.txt` via `uv pip freeze > requirements.txt`
  - _Requirements: 1.1, 1.2_

- [x] 2. Generate sample dataset
  - Write a one-off Python script `backend/data/generate_dataset.py` that produces `backend/data/online_retail.csv` with 10,000+ rows and columns: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, `Country`
  - Ensure the generated data includes realistic variation: some null `CustomerID` rows, some negative `Quantity` rows, multiple invoices per customer, date range spanning at least 12 months
  - Run the script once to produce the CSV; commit the CSV (not the generator) as the project artifact
  - _Requirements: 2.1_

- [x] 3. Implement `config.py`
  - Create `backend/config.py` with a `Settings` class (or module-level constants) exposing `DATASET_PATH` (default `data/online_retail.csv`) and `CORS_ORIGINS` (default `["*"]`)
  - `DATASET_PATH` must be overridable via an environment variable
  - Add a module-level docstring explaining each setting
  - _Requirements: 2.3_

- [x] 4. Implement data ingestion (`data/ingestion.py`)
  - [x] 4.1 Implement `load_dataset(filepath: str) -> pd.DataFrame`
    - Read CSV with `pd.read_csv`; raise `FileNotFoundError` with a descriptive message if the path does not exist
    - Log at `INFO` level: filepath and row count after loading
    - Add full docstring (parameters, returns, raises)
    - _Requirements: 2.3, 2.4_

  - [x] 4.2 Implement `clean_dataset(df: pd.DataFrame) -> pd.DataFrame`
    - Step 1: drop rows with null `CustomerID`, `InvoiceDate`, `Quantity`, or `UnitPrice`; log count dropped at `WARNING`
    - Step 2: derive `Amount = Quantity × UnitPrice`
    - Step 3: drop rows where `Amount <= 0`; log count dropped at `WARNING`
    - Return cleaned dataframe with `Amount` column
    - Add full docstring
    - _Requirements: 2.2, 2.5, 2.6_

  - [ ]* 4.3 Write property test for `clean_dataset` — Property 1: Amount Derivation
    - **Property 1: For any row with given Quantity and UnitPrice, derived Amount equals exactly `Quantity × UnitPrice`**
    - **Validates: Requirements 2.2**
    - File: `backend/tests/test_ingestion.py`
    - Strategy: `st.integers()` × `st.floats(allow_nan=False, allow_infinity=False)` for Quantity/UnitPrice
    - Tag comment: `# Feature: rfm-analysis-project, Property 1: Amount Derivation`
    - `@settings(max_examples=100)`

  - [ ]* 4.4 Write property test for `clean_dataset` — Property 2: Dataset Cleaning Removes All Invalid Rows
    - **Property 2: After `clean_dataset()`, no rows have null CustomerID/InvoiceDate/Quantity/UnitPrice, and no rows have Amount ≤ 0**
    - **Validates: Requirements 2.5, 2.6**
    - Strategy: build dataframes with random null patterns and negative amounts using `hypothesis.extra.pandas`
    - Tag comment: `# Feature: rfm-analysis-project, Property 2: Dataset Cleaning Removes All Invalid Rows`
    - `@settings(max_examples=100)`

  - [ ]* 4.5 Write unit test for `load_dataset` — file not found
    - Test that `load_dataset("nonexistent.csv")` raises `FileNotFoundError`
    - _Requirements: 2.4_

- [x] 5. Implement RFM computation (`rfm/computation.py`)
  - [x] 5.1 Implement `compute_rfm(df, reference_date) -> pd.DataFrame`
    - Group by `CustomerID`; compute `Recency = (reference_date - max(InvoiceDate)).days`, `Frequency = nunique(InvoiceNo)`, `Monetary = sum(Amount)`
    - Return one-row-per-customer dataframe with columns `CustomerID`, `Recency`, `Frequency`, `Monetary`
    - Add full docstring
    - _Requirements: 3.1, 3.2, 3.3_

  - [ ]* 5.2 Write property test for `compute_rfm` — Property 3: RFM Aggregation Correctness
    - **Property 3: For any cleaned dataframe, computed Recency/Frequency/Monetary match the manual aggregation formulas for every customer**
    - **Validates: Requirements 3.1, 3.2, 3.3**
    - Strategy: `hypothesis.extra.pandas` dataframes with random CustomerID/InvoiceDate/Amount combos
    - Tag comment: `# Feature: rfm-analysis-project, Property 3: RFM Aggregation Correctness`
    - `@settings(max_examples=100)`

  - [x] 5.3 Implement `assign_scores(rfm: pd.DataFrame) -> pd.DataFrame`
    - Use `pd.qcut` with 5 bins to assign `R_Score` (inverted — lower Recency → higher score), `F_Score`, `M_Score`
    - Compute `RFM_Score = str(R_Score) + str(F_Score) + str(M_Score)` for each customer
    - Handle duplicate bin edges with `duplicates="drop"` and fill any resulting NaN scores with 1
    - Add full docstring
    - _Requirements: 3.4, 3.5_

  - [ ]* 5.4 Write property test for `assign_scores` — Property 4: Score Assignment Invariants
    - **Property 4: Every R/F/M score is in [1,5]; RFM_Score equals concatenation of the three scores; score ordering is monotone with respect to raw metric values**
    - **Validates: Requirements 3.4, 3.5**
    - Strategy: `hypothesis.extra.pandas` dataframes with random positive Recency/Frequency/Monetary values
    - Tag comment: `# Feature: rfm-analysis-project, Property 4: Score Assignment Invariants`
    - `@settings(max_examples=100)`

  - [x] 5.5 Implement `assign_segments(rfm: pd.DataFrame) -> pd.DataFrame`
    - Implement a priority-ordered rule list mapping R_Score/F_Score combinations to segment labels: Champions, Loyal Customers, Potential Loyalists, New Customers, At Risk, Lost, Others
    - Every customer must receive a non-null segment from the defined set
    - Add full docstring
    - _Requirements: 3.6_

  - [ ]* 5.6 Write property test for `assign_segments` — Property 5: Segment Assignment Completeness
    - **Property 5: For all 125 possible RFM_Score combinations ("111"–"555"), every customer receives a non-null segment from the defined set**
    - **Validates: Requirements 3.6**
    - Strategy: `st.sampled_from()` over all 125 RFM_Score strings; build minimal dataframe and call `assign_segments`
    - Tag comment: `# Feature: rfm-analysis-project, Property 5: Segment Assignment Completeness`
    - `@settings(max_examples=125)`

- [x] 6. Checkpoint — backend pipeline
  - Run `uv run pytest backend/tests/test_ingestion.py backend/tests/test_computation.py -v` and ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 7. Implement REST API (`api/router.py` and `main.py`)
  - [x] 7.1 Create `backend/api/router.py` with a FastAPI `APIRouter`
    - `GET /api/health` → `{"status": "ok"}` (HTTP 200)
    - `GET /api/rfm` → full RFM records array (JSON); each record contains all 9 fields from the RFM schema
    - `GET /api/segments/summary` → segment distribution array; each element has `segment`, `count`, `percentage`
    - `GET /api/rfm/top?n=10` → top-n records by `RFM_Score` descending; validate `n` is a positive integer, return HTTP 400 with `{"detail": "..."}` otherwise
    - All handlers call the ingestion and computation functions; results are computed once at startup and cached on the app state
    - Add docstrings and inline comments for each endpoint
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 6.5_

  - [x] 7.2 Create `backend/main.py`
    - Define `create_app()` factory that instantiates `FastAPI`, registers the router, and adds `CORSMiddleware` using `CORS_ORIGINS` from `config.py`
    - On startup event: call `load_dataset` → `clean_dataset` → `compute_rfm` → `assign_scores` → `assign_segments`; store result on `app.state.rfm_df`
    - Log startup completion at `INFO` level
    - Guard with `if __name__ == "__main__": uvicorn.run(...)` for direct execution
    - _Requirements: 1.4, 2.3, 4.6_

  - [ ]* 7.3 Write property test for `/api/rfm` — Property 6: API /api/rfm Response Schema
    - **Property 6: For any valid dataset, GET /api/rfm returns a JSON array where every element has exactly the 9 required fields with correct types**
    - **Validates: Requirements 4.1**
    - Use `httpx.AsyncClient` / `TestClient` with a test app fixture; inject random RFM dataframes via `app.state`
    - Tag comment: `# Feature: rfm-analysis-project, Property 6: API /api/rfm Response Schema`
    - `@settings(max_examples=50)`

  - [ ]* 7.4 Write property test for `/api/segments/summary` — Property 7: Segment Summary Percentages Sum to 100
    - **Property 7: For any RFM dataset, the percentages in GET /api/segments/summary sum to 100 (within floating-point tolerance)**
    - **Validates: Requirements 4.2**
    - Strategy: random RFM tables with varied segment distributions
    - Tag comment: `# Feature: rfm-analysis-project, Property 7: Segment Summary Percentages Sum to 100`
    - `@settings(max_examples=100)`

  - [ ]* 7.5 Write property test for `/api/rfm/top` — Property 8: Top-N Ranking Correctness
    - **Property 8: GET /api/rfm/top?n=N returns exactly min(n, total_customers) records, ranked by RFM_Score descending**
    - **Validates: Requirements 4.3**
    - Strategy: `st.integers(min_value=1, max_value=200)` for n; random RFM tables
    - Tag comment: `# Feature: rfm-analysis-project, Property 8: Top-N Ranking Correctness`
    - `@settings(max_examples=100)`

  - [ ]* 7.6 Write property test for `/api/rfm/top` — Property 9: Invalid Parameter Returns HTTP 400
    - **Property 9: Any request to GET /api/rfm/top with non-positive or non-integer n returns HTTP 400 with a detail field**
    - **Validates: Requirements 4.5**
    - Strategy: `st.one_of(st.integers(max_value=0), st.text().filter(lambda s: not s.lstrip("-").isdigit()))`
    - Tag comment: `# Feature: rfm-analysis-project, Property 9: Invalid Parameter Returns HTTP 400`
    - `@settings(max_examples=100)`

  - [ ]* 7.7 Write integration tests for all API endpoints (`backend/tests/test_api.py`)
    - `test_health_endpoint`: GET /api/health → 200, `{"status": "ok"}`
    - `test_api_rfm_returns_json`: GET /api/rfm → 200, JSON array
    - `test_api_segments_summary_returns_json`: GET /api/segments/summary → 200, JSON array
    - `test_api_rfm_top_default`: GET /api/rfm/top → 200, array of length 10
    - `test_cors_headers_present`: response includes `access-control-allow-origin` header
    - _Requirements: 4.4, 4.6, 6.5_

- [x] 8. Checkpoint — API layer
  - Run `uv run pytest backend/tests/ -v` and ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 9. Implement frontend (`frontend/`)
  - [x] 9.1 Create `frontend/index.html`
    - Single-page layout with a header, summary cards section, bar chart section, scatter plot section, and data table section
    - Load Chart.js 4.x from CDN; load `style.css` and all JS modules (`app.js`, `barChart.js`, `scatterPlot.js`, `dataTable.js`, `summaryCards.js`) as `<script>` tags
    - Include an error banner `<div id="error-banner">` hidden by default
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.6, 5.7_

  - [x] 9.2 Create `frontend/css/style.css`
    - Responsive grid layout (CSS Grid or Flexbox) that renders correctly at 768px and above
    - Card styles for summary cards, chart containers, and table wrapper
    - Error banner style (visible red/orange banner when `.visible` class is added)
    - _Requirements: 5.7_

  - [x] 9.3 Create `frontend/js/barChart.js`
    - Export `renderBarChart(segmentSummary)` that renders a Chart.js bar chart into `<canvas id="bar-chart">`
    - X-axis: segment names; Y-axis: customer count
    - _Requirements: 5.1_

  - [x] 9.4 Create `frontend/js/scatterPlot.js`
    - Export `renderScatterPlot(rfmData)` that renders a Chart.js scatter chart into `<canvas id="scatter-plot">`
    - X-axis: Recency; Y-axis: Monetary; each point colored by `Customer_Segment`
    - _Requirements: 5.2_

  - [x] 9.5 Create `frontend/js/dataTable.js`
    - Export `renderDataTable(rfmData)` that populates `<table id="rfm-table">` with columns: `CustomerID`, `Recency`, `Frequency`, `Monetary`, `RFM_Score`, `Customer_Segment`
    - Render one `<tr>` per customer record
    - _Requirements: 5.3_

  - [x] 9.6 Create `frontend/js/summaryCards.js`
    - Export `renderSummaryCards(rfmData, segmentSummary)` that fills three card elements:
      - Total customers = `rfmData.length`
      - Top segment = segment with highest count from `segmentSummary`
      - Average monetary = mean of all `Monetary` values in `rfmData`
    - _Requirements: 5.4_

  - [ ]* 9.7 Write property test for frontend rendering — Property 10: Frontend Rendering Completeness
    - **Property 10: `renderDataTable()` includes all 6 required columns for every record; `renderSummaryCards()` shows correct total count, top segment, and average monetary**
    - **Validates: Requirements 5.3, 5.4**
    - Implement as a Python test using `html.parser` / `BeautifulSoup` to parse the HTML output of the render functions called via a headless JS runner, OR implement as pure-Python tests against the summary computation logic extracted into a helper
    - Tag comment: `# Feature: rfm-analysis-project, Property 10: Frontend Rendering Completeness`
    - `@settings(max_examples=100)`

  - [x] 9.8 Create `frontend/js/app.js`
    - Fetch `GET /api/rfm`, `GET /api/segments/summary`, and `GET /api/rfm/top` in parallel using `Promise.all`
    - On success: call `renderBarChart`, `renderScatterPlot`, `renderDataTable`, `renderSummaryCards`
    - On fetch error or non-2xx response: show error banner with descriptive message
    - _Requirements: 5.5, 5.6_

- [x] 10. Create documentation (`backend/docs/`)
  - Create `backend/docs/rfm_methodology.md` explaining: what RFM is, how Recency/Frequency/Monetary are computed, why quantile binning is used, and how to interpret scores 1–5
  - Create `backend/docs/segment_mapping.md` with a table of all segment labels, their R/F score rules, and a plain-English description of each segment
  - _Requirements: 6.4_

- [x] 11. Create `backend/README.md`
  - Step-by-step setup instructions:
    1. Prerequisites (Python 3.11+, uv)
    2. Clone / download the project
    3. `cd backend && uv venv .venv && source .venv/bin/activate` (or Windows equivalent)
    4. `uv pip install -r requirements.txt`
    5. `uv run uvicorn main:app --reload`
    6. Open `frontend/index.html` in a browser
  - Section on running tests: `uv run pytest backend/tests/ -v`
  - Section on API endpoints with example `curl` commands
  - _Requirements: 1.3, 1.4_

- [x] 12. Create test infrastructure (`backend/tests/`)
  - Create `backend/tests/__init__.py`
  - Create `backend/tests/conftest.py` with shared pytest fixtures:
    - `sample_raw_df`: a small in-memory dataframe matching the raw CSV schema (including some null/negative rows)
    - `sample_clean_df`: the cleaned version of `sample_raw_df`
    - `sample_rfm_df`: a pre-computed RFM dataframe with scores and segments
    - `test_app`: a `TestClient` wrapping the FastAPI app with `sample_rfm_df` injected into `app.state`
  - Install test dependencies: `uv pip install pytest hypothesis httpx`
  - _Requirements: 1.1_

- [x] 13. Final checkpoint
  - Run `uv run pytest backend/tests/ -v --hypothesis-show-statistics` and ensure all tests pass
  - Verify `frontend/index.html` opens in a browser and all four visualizations render (bar chart, scatter plot, data table, summary cards)
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for a faster MVP
- Each task references specific requirements for traceability
- Checkpoints (tasks 6, 8, 13) ensure incremental validation at each layer boundary
- Property tests validate universal correctness properties using Hypothesis (`@settings(max_examples=100)`)
- Unit/integration tests validate specific examples and API contracts
- The dataset generator script (task 2) is a one-off utility; only the generated CSV is committed
