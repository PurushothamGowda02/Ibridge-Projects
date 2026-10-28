# Design Document: RFM Analysis Full-Stack Project

## Overview

This document describes the technical design for a full-stack RFM (Recency, Frequency, Monetary) Analysis application. The system ingests a UCI Online Retail-style CSV dataset, computes RFM scores and customer segments in Python, exposes the results via a FastAPI REST API, and renders interactive visualizations in a plain HTML/CSS/JS frontend using Chart.js.

The project is structured for educational clarity: every module is small, focused, and heavily commented. A `docs/` folder explains the RFM methodology and segment mapping. The virtual environment is managed with `uv`.

### Goals

- Demonstrate end-to-end data pipeline: raw CSV → cleaned data → RFM scores → REST API → browser visualizations.
- Serve as a BCA final-year project that is easy to set up, run, and explain during evaluation.
- Provide a reference implementation of RFM segmentation with pandas quantile binning.

### Non-Goals

- Real-time data ingestion or streaming.
- User authentication or multi-tenancy.
- Production deployment (Docker, cloud hosting, etc.).

---

## Architecture

The system is split into two independently runnable parts that communicate over HTTP.

```
┌─────────────────────────────────────────────────────────┐
│                        Browser                          │
│  index.html + app.js + chart.js + style.css             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │BarChart  │ │Scatter   │ │DataTable │ │SummaryCard│  │
│  │Component │ │Component │ │Component │ │Component  │  │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └─────┬─────┘  │
│       └────────────┴────────────┴─────────────┘         │
│                    fetch() calls                         │
└──────────────────────────┬──────────────────────────────┘
                           │ HTTP/JSON (CORS enabled)
┌──────────────────────────▼──────────────────────────────┐
│                  FastAPI Backend                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │               api/router.py                      │   │
│  │  GET /api/health  GET /api/rfm  GET /api/rfm/top │   │
│  │  GET /api/segments/summary                       │   │
│  └──────────────────────┬───────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────▼───────────────────────────┐   │
│  │           rfm/computation.py                     │   │
│  │  compute_rfm()  assign_scores()  assign_segments()│  │
│  └──────────────────────┬───────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────▼───────────────────────────┐   │
│  │           data/ingestion.py                      │   │
│  │  load_dataset()  clean_dataset()                 │   │
│  └──────────────────────┬───────────────────────────┘   │
│                         │                               │
│              data/online_retail.csv                     │
└─────────────────────────────────────────────────────────┘
```

### Technology Choices

| Layer | Technology | Rationale |
|---|---|---|
| Backend language | Python 3.11+ | Pandas ecosystem, familiar to BCA students |
| Web framework | FastAPI | Auto-generated docs, type hints, async support |
| Data processing | pandas | Industry-standard for tabular data |
| Virtual env | uv | Fast, modern, single-tool replacement for pip+venv |
| Frontend | Plain HTML/CSS/JS | Zero build step, easy to inspect and explain |
| Charts | Chart.js 4.x (CDN) | Lightweight, well-documented, no npm required |

---

## Components and Interfaces

### Backend Module Structure

```
backend/
├── main.py                  # FastAPI app factory, startup event
├── config.py                # Settings (dataset path, CORS origins)
├── data/
│   ├── __init__.py
│   └── ingestion.py         # load_dataset(), clean_dataset()
├── rfm/
│   ├── __init__.py
│   └── computation.py       # compute_rfm(), assign_scores(), assign_segments()
├── api/
│   ├── __init__.py
│   └── router.py            # FastAPI APIRouter with all endpoints
├── docs/
│   ├── rfm_methodology.md   # Explanation of RFM theory
│   └── segment_mapping.md   # Segment label rules
├── data/
│   └── online_retail.csv    # Sample dataset (10,000+ rows)
├── requirements.txt
└── README.md
```

### Frontend Structure

```
frontend/
├── index.html               # Single page, loads all components
├── css/
│   └── style.css            # Responsive layout, card styles
└── js/
    ├── app.js               # Entry point: fetches API, wires components
    ├── barChart.js          # Segment distribution bar chart
    ├── scatterPlot.js       # Recency vs Monetary scatter plot
    ├── dataTable.js         # Customer RFM data table
    └── summaryCards.js      # Total customers, top segment, avg monetary
```

### Backend Public Interfaces

#### `data/ingestion.py`

```python
def load_dataset(filepath: str) -> pd.DataFrame:
    """
    Load the raw CSV dataset from the given filepath.

    Parameters
    ----------
    filepath : str
        Absolute or relative path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Raw dataframe with all original columns.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the given path.
    """

def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw dataset by removing invalid rows and deriving Amount.

    Rules applied (in order):
    1. Drop rows with null CustomerID, InvoiceDate, Quantity, or UnitPrice.
    2. Derive Amount = Quantity × UnitPrice.
    3. Drop rows where Amount <= 0.
    4. Log the count of dropped rows at each step.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe as returned by load_dataset().

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with an additional 'Amount' column.
    """
```

#### `rfm/computation.py`

```python
def compute_rfm(df: pd.DataFrame, reference_date: pd.Timestamp) -> pd.DataFrame:
    """
    Aggregate cleaned line-item data into per-customer RFM metrics.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe with Amount column.
    reference_date : pd.Timestamp
        The date used as 'today' for Recency calculation (max InvoiceDate).

    Returns
    -------
    pd.DataFrame
        One row per CustomerID with columns:
        CustomerID, Recency, Frequency, Monetary.
    """

def assign_scores(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Assign R_Score, F_Score, M_Score (1–5) using quantile binning.

    Score of 5 = most favorable:
    - R_Score 5 = lowest Recency (most recent)
    - F_Score 5 = highest Frequency
    - M_Score 5 = highest Monetary

    Parameters
    ----------
    rfm : pd.DataFrame
        Dataframe with Recency, Frequency, Monetary columns.

    Returns
    -------
    pd.DataFrame
        Input dataframe with R_Score, F_Score, M_Score, RFM_Score columns added.
    """

def assign_segments(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Map each customer's RFM_Score to a Customer_Segment label.

    Segment mapping covers at minimum:
    Champions, Loyal Customers, Potential Loyalists,
    At Risk, Lost, New Customers.

    Parameters
    ----------
    rfm : pd.DataFrame
        Dataframe with RFM_Score column.

    Returns
    -------
    pd.DataFrame
        Input dataframe with Customer_Segment column added.
    """
```

#### `api/router.py` — Endpoint Contracts

| Method | Path | Query Params | Response |
|---|---|---|---|
| GET | `/api/health` | — | `{"status": "ok"}` |
| GET | `/api/rfm` | — | Array of RFM records |
| GET | `/api/segments/summary` | — | Array of segment distribution records |
| GET | `/api/rfm/top` | `n` (int, default 10) | Array of top-n RFM records |

**RFM record schema:**
```json
{
  "CustomerID": "12345",
  "Recency": 14,
  "Frequency": 8,
  "Monetary": 1234.56,
  "R_Score": 4,
  "F_Score": 5,
  "M_Score": 4,
  "RFM_Score": "454",
  "Customer_Segment": "Loyal Customers"
}
```

**Segment summary record schema:**
```json
{
  "segment": "Champions",
  "count": 312,
  "percentage": 18.5
}
```

**Error response schema (HTTP 400):**
```json
{
  "detail": "Invalid value for parameter 'n': must be a positive integer."
}
```

### Frontend Component Interfaces

Each JS component exports a single `render(data)` function:

```javascript
// barChart.js
function renderBarChart(segmentSummary) { /* ... */ }

// scatterPlot.js
function renderScatterPlot(rfmData) { /* ... */ }

// dataTable.js
function renderDataTable(rfmData) { /* ... */ }

// summaryCards.js
function renderSummaryCards(rfmData, segmentSummary) { /* ... */ }
```

`app.js` orchestrates all fetches and calls each render function once data is available.

---

## Data Models

### Raw CSV Row

| Column | Type | Notes |
|---|---|---|
| InvoiceNo | string | Invoice identifier; multiple rows per invoice |
| StockCode | string | Product code |
| Description | string | Product name |
| Quantity | integer | Units purchased; may be negative (returns) |
| InvoiceDate | datetime string | Format: `MM/DD/YYYY HH:MM` |
| UnitPrice | float | Price per unit; may be zero or negative |
| CustomerID | string/float | May be null; cast to string after cleaning |
| Country | string | Customer country |

### Derived: Amount

```
Amount = Quantity × UnitPrice
```

Rows where `Amount <= 0` are discarded (returns, cancellations, free items).

### Per-Customer RFM Table (after aggregation)

| Column | Type | Description |
|---|---|---|
| CustomerID | string | Unique customer identifier |
| Recency | int | Days since last purchase (lower = better) |
| Frequency | int | Count of distinct invoices |
| Monetary | float | Sum of Amount across all invoices |
| R_Score | int (1–5) | Recency quantile score |
| F_Score | int (1–5) | Frequency quantile score |
| M_Score | int (1–5) | Monetary quantile score |
| RFM_Score | string | Concatenation of R, F, M scores (e.g., "455") |
| Customer_Segment | string | Segment label derived from RFM_Score |

### Segment Mapping

The segment mapping uses R_Score and F_Score as primary discriminators (Monetary is captured in M_Score but segment labels follow industry convention):

| Segment | Rule (approximate) |
|---|---|
| Champions | R=5, F=4–5 |
| Loyal Customers | F=4–5, R=3–4 |
| Potential Loyalists | R=4–5, F=2–3 |
| New Customers | R=4–5, F=1 |
| At Risk | R=2–3, F=3–5 |
| Lost | R=1–2, F=1–2 |
| Others | All remaining combinations |

The mapping is implemented as a lookup function that checks RFM_Score patterns using a priority-ordered list of rules.

### Application State (Frontend)

```javascript
// Held in memory after initial fetch; never persisted
{
  rfmData: [...],          // Full array from GET /api/rfm
  segmentSummary: [...],   // Array from GET /api/segments/summary
  topCustomers: [...]      // Array from GET /api/rfm/top
}
```

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system — essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Amount Derivation

*For any* row with a given Quantity and UnitPrice, the derived Amount value must equal exactly `Quantity × UnitPrice`.

**Validates: Requirements 2.2**

### Property 2: Dataset Cleaning Removes All Invalid Rows

*For any* input dataframe, after calling `clean_dataset()`, the resulting dataframe must contain no rows where `CustomerID`, `InvoiceDate`, `Quantity`, or `UnitPrice` is null, and no rows where the derived `Amount` is less than or equal to zero.

**Validates: Requirements 2.5, 2.6**

### Property 3: RFM Aggregation Correctness

*For any* cleaned dataframe grouped by `CustomerID`, the computed RFM table must satisfy all three of the following simultaneously:
- `Recency` equals `(reference_date - max(InvoiceDate)).days` for that customer
- `Frequency` equals the count of distinct `InvoiceNo` values for that customer
- `Monetary` equals the sum of all `Amount` values for that customer

**Validates: Requirements 3.1, 3.2, 3.3**

### Property 4: Score Assignment Invariants

*For any* valid RFM table, after calling `assign_scores()`, the following must all hold:
- Every `R_Score`, `F_Score`, and `M_Score` value is an integer in the range [1, 5]
- `RFM_Score` equals the string concatenation of `str(R_Score) + str(F_Score) + str(M_Score)` for every customer
- Customers with lower Recency (more recent) receive higher or equal R_Score compared to customers with higher Recency
- Customers with higher Frequency receive higher or equal F_Score compared to customers with lower Frequency
- Customers with higher Monetary receive higher or equal M_Score compared to customers with lower Monetary

**Validates: Requirements 3.4, 3.5**

### Property 5: Segment Assignment Completeness

*For any* RFM table (including all 125 possible RFM_Score combinations from "111" to "555"), after calling `assign_segments()`, every customer must have a non-null `Customer_Segment` value drawn from the defined set: {"Champions", "Loyal Customers", "Potential Loyalists", "New Customers", "At Risk", "Lost", "Others"}.

**Validates: Requirements 3.6**

### Property 6: API /api/rfm Response Schema

*For any* valid dataset loaded by the backend, the `GET /api/rfm` response must be a JSON array where every element contains exactly the fields: `CustomerID`, `Recency`, `Frequency`, `Monetary`, `R_Score`, `F_Score`, `M_Score`, `RFM_Score`, and `Customer_Segment`, each with the correct type.

**Validates: Requirements 4.1**

### Property 7: Segment Summary Percentages Sum to 100

*For any* RFM dataset, the `GET /api/segments/summary` response must be a JSON array where the sum of all `percentage` values equals 100 (within floating-point tolerance), and every element contains `segment`, `count`, and `percentage`.

**Validates: Requirements 4.2**

### Property 8: Top-N Ranking Correctness

*For any* valid positive integer `n` and any RFM dataset, the `GET /api/rfm/top?n=N` response must return exactly `min(n, total_customers)` records, and those records must be the top-ranked customers by `RFM_Score` in descending lexicographic order.

**Validates: Requirements 4.3**

### Property 9: Invalid Parameter Returns HTTP 400

*For any* request to `GET /api/rfm/top` with a non-positive integer or non-integer value for `n`, the API must respond with HTTP status 400 and a JSON body containing a `detail` field describing the invalid parameter.

**Validates: Requirements 4.5**

### Property 10: Frontend Rendering Completeness

*For any* array of RFM records and segment summary data, the frontend rendering functions must produce output that:
- `renderDataTable()`: includes all six required columns (`CustomerID`, `Recency`, `Frequency`, `Monetary`, `RFM_Score`, `Customer_Segment`) for every record
- `renderSummaryCards()`: displays a total customer count equal to the length of the RFM array, a top segment equal to the most frequent `Customer_Segment`, and an average monetary value equal to the mean of all `Monetary` values

**Validates: Requirements 5.3, 5.4**

---

## Error Handling

### Backend Error Handling

| Scenario | Behavior |
|---|---|
| Dataset file not found | Log descriptive error, raise `FileNotFoundError`, exit with non-zero status |
| Null values in key columns | Drop rows, log count of dropped rows at INFO level |
| Amount ≤ 0 after derivation | Drop rows, log count of dropped rows at INFO level |
| Invalid `n` query parameter | Return HTTP 400 with JSON `{"detail": "..."}` |
| Unexpected server error | Return HTTP 500 with JSON `{"detail": "Internal server error"}` |

### Frontend Error Handling

| Scenario | Behavior |
|---|---|
| Backend API unreachable | Display a visible error banner: "Could not load data. Please ensure the backend server is running." |
| Fetch returns non-2xx status | Display error banner with status code |
| Empty dataset (no customers after cleaning) | Display "No data available" message in place of charts and table |

### Logging Strategy

The backend uses Python's standard `logging` module at the following levels:
- `INFO`: dataset loaded, row counts before/after cleaning, server startup
- `WARNING`: rows discarded during cleaning
- `ERROR`: file not found, unexpected exceptions

---

## Testing Strategy

### Overview

The project uses a dual testing approach:
- **Unit/property tests** (pytest + Hypothesis) for backend pure functions
- **Example-based integration tests** (pytest + httpx) for API endpoints
- **Manual/smoke tests** for frontend rendering and setup verification

### Property-Based Testing

The backend's pure functions (`clean_dataset`, `compute_rfm`, `assign_scores`, `assign_segments`) are well-suited for property-based testing because they are deterministic transformations over tabular data with a large input space.

**Library**: [Hypothesis](https://hypothesis.readthedocs.io/) for Python

**Configuration**: Each property test runs a minimum of 100 examples (`@settings(max_examples=100)`).

**Tag format**: Each test is tagged with a comment:
```python
# Feature: rfm-analysis-project, Property N: <property_text>
```

#### Property Tests

| Test | Property | Hypothesis Strategy |
|---|---|---|
| `test_amount_derivation` | Property 1 | `st.integers()` × `st.floats()` for Quantity/UnitPrice |
| `test_cleaning_removes_invalid_rows` | Property 2 | `st.dataframes()` with random null patterns and negative amounts |
| `test_rfm_aggregation_correctness` | Property 3 | `st.dataframes()` with random CustomerID/InvoiceDate/Amount combos |
| `test_score_assignment_invariants` | Property 4 | `st.dataframes()` with random Recency/Frequency/Monetary values |
| `test_segment_assignment_completeness` | Property 5 | `st.sampled_from()` over all 125 RFM_Score combinations |
| `test_api_rfm_schema` | Property 6 | Random datasets loaded into test app via `TestClient` |
| `test_segment_summary_percentages` | Property 7 | Random RFM tables passed to summary computation |
| `test_top_n_ranking` | Property 8 | `st.integers(min_value=1)` for n, random RFM tables |
| `test_invalid_n_returns_400` | Property 9 | `st.one_of(st.integers(max_value=0), st.text())` for invalid n |
| `test_frontend_rendering_completeness` | Property 10 | Random RFM record arrays |

### Unit / Example-Based Tests

| Test | Validates |
|---|---|
| `test_load_dataset_file_not_found` | Req 2.4: FileNotFoundError on missing file |
| `test_health_endpoint` | Req 6.5: GET /api/health returns 200 + `{"status": "ok"}` |
| `test_api_endpoints_return_json` | Req 4.4: All endpoints return JSON with correct status |
| `test_cors_headers_present` | Req 4.6: CORS headers in response |
| `test_frontend_error_on_api_failure` | Req 5.6: Error banner shown when fetch fails |

### Test File Structure

```
backend/
└── tests/
    ├── conftest.py              # Shared fixtures (test app, sample dataframes)
    ├── test_ingestion.py        # Unit + property tests for data/ingestion.py
    ├── test_computation.py      # Unit + property tests for rfm/computation.py
    └── test_api.py              # Integration tests for api/router.py
```

### Running Tests

```bash
# Install test dependencies
uv pip install pytest hypothesis httpx

# Run all tests
uv run pytest backend/tests/ -v

# Run with Hypothesis verbose output
uv run pytest backend/tests/ -v --hypothesis-show-statistics
```

### Frontend Testing

Frontend JS components are tested manually by opening `index.html` in a browser with the backend running. Smoke checks:
- Bar chart renders with correct segment labels
- Scatter plot shows points colored by segment
- Data table is sortable and shows all columns
- Summary cards show correct aggregated values
- Error banner appears when backend is stopped
