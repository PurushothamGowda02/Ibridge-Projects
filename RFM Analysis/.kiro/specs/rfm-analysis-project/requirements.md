# Requirements Document

## Introduction

This project is a full-stack RFM (Recency, Frequency, Monetary) Analysis application designed as a final-year project for BCA students. It demonstrates how customer segmentation can be performed on retail/e-commerce transaction data using the RFM model. The backend is built in Python and handles data ingestion, RFM score computation, and customer segmentation. The frontend visualizes the results through interactive charts and tables. The project uses a rich, realistic e-commerce dataset modelled after the UCI Online Retail dataset, containing line-item transaction records from which monetary values are derived. The project is structured to be educational, well-documented, and easy to set up using `uv` for virtual environment management.

---

## Glossary

- **RFM**: A customer segmentation technique based on three metrics — Recency (how recently a customer purchased), Frequency (how often they purchase), and Monetary (how much they spend).
- **Recency**: The number of days since a customer's last transaction relative to a reference date.
- **Frequency**: The total number of transactions made by a customer within the dataset period.
- **Monetary**: The total amount spent by a customer within the dataset period.
- **RFM_Score**: A composite score derived by combining the individual R, F, and M scores (each on a 1–5 scale).
- **Customer_Segment**: A label assigned to a customer based on their RFM_Score (e.g., "Champions", "At Risk", "Lost").
- **Dataset**: The input transaction data in CSV format modelled after the UCI Online Retail dataset. Each row is a line-item record with columns: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, and `Country`.
- **Amount**: A derived value computed as `Quantity × UnitPrice` for each line-item row. Not a raw column in the dataset.
- **InvoiceNo**: A unique identifier for each invoice/transaction. Multiple rows may share the same `InvoiceNo` (one per line item).
- **StockCode**: A product/item code identifying the purchased item.
- **Description**: A human-readable name for the purchased item.
- **Quantity**: The number of units of the item purchased in a line-item row.
- **UnitPrice**: The price per unit of the item in the line-item row.
- **Country**: The country where the customer is located.
- **Backend**: The Python-based server application responsible for data processing, RFM computation, and exposing a REST API.
- **Frontend**: The web-based user interface that consumes the Backend API and renders visualizations.
- **API**: The REST interface exposed by the Backend for the Frontend to consume.
- **uv**: A fast Python package and virtual environment manager used in place of `venv` or `conda`.
- **Segment_Distribution**: The count and percentage of customers in each Customer_Segment.

---

## Requirements

### Requirement 1: Project Setup and Environment Management

**User Story:** As a BCA student, I want a clearly defined project setup process, so that I can run the application locally without environment conflicts.

#### Acceptance Criteria

1. THE Backend SHALL manage its Python dependencies using `uv` as the virtual environment and package manager.
2. THE Backend SHALL include a `requirements.txt` file generated via `uv pip freeze` that lists all runtime dependencies with pinned versions.
3. THE Backend SHALL include a `README.md` with step-by-step setup instructions covering environment creation, dependency installation, and application startup.
4. WHEN a student follows the README instructions, THE Backend SHALL start successfully without manual dependency resolution.

---

### Requirement 2: Dataset Ingestion

**User Story:** As a BCA student, I want the application to load a realistic transaction dataset, so that RFM analysis can be performed on rich, real-world-style data.

#### Acceptance Criteria

1. THE Backend SHALL include a sample e-commerce/retail transaction dataset in CSV format with at least 10,000 line-item rows and the following columns: `InvoiceNo`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `UnitPrice`, `CustomerID`, and `Country`.
2. THE Backend SHALL derive an `Amount` value for each row by computing `Quantity × UnitPrice`; `Amount` SHALL NOT be a raw column in the dataset.
3. WHEN the Backend starts, THE Backend SHALL load the dataset from a configurable file path specified in a configuration file or environment variable.
4. IF the dataset file is not found at the configured path, THEN THE Backend SHALL log a descriptive error message and exit with a non-zero status code.
5. IF the dataset contains rows with null values in `CustomerID`, `InvoiceDate`, `Quantity`, or `UnitPrice`, THEN THE Backend SHALL discard those rows and log the count of discarded rows.
6. IF the dataset contains rows where the derived `Amount` is less than or equal to zero, THEN THE Backend SHALL discard those rows and log the count of discarded rows.

---

### Requirement 3: RFM Score Computation

**User Story:** As a BCA student, I want the system to compute RFM scores for each customer, so that I can understand the segmentation logic.

#### Acceptance Criteria

1. WHEN the dataset is loaded and cleaned, THE Backend SHALL compute the Recency value for each customer as the number of days between the customer's most recent `InvoiceDate` and the reference date (the maximum `InvoiceDate` in the dataset).
2. WHEN the dataset is loaded and cleaned, THE Backend SHALL compute the Frequency value for each customer as the total count of distinct transactions for that customer.
3. WHEN the dataset is loaded and cleaned, THE Backend SHALL compute the Monetary value for each customer as the sum of all derived `Amount` values (`Quantity × UnitPrice`) for that customer.
4. THE Backend SHALL assign an R_Score, F_Score, and M_Score to each customer by dividing customers into 5 equal quantile bins, where a score of 5 represents the most favorable value (lowest Recency, highest Frequency, highest Monetary).
5. THE Backend SHALL compute the RFM_Score for each customer as the concatenation of R_Score, F_Score, and M_Score (e.g., "555", "312").
6. THE Backend SHALL assign a Customer_Segment label to each customer based on their RFM_Score using a predefined mapping that covers at minimum the segments: "Champions", "Loyal Customers", "Potential Loyalists", "At Risk", "Lost", and "New Customers".

---

### Requirement 4: REST API

**User Story:** As a BCA student, I want the backend to expose a REST API, so that the frontend can retrieve RFM results programmatically.

#### Acceptance Criteria

1. THE API SHALL expose a `GET /api/rfm` endpoint that returns the full RFM results as a JSON array, where each element contains `CustomerID`, `Recency`, `Frequency`, `Monetary`, `R_Score`, `F_Score`, `M_Score`, `RFM_Score`, and `Customer_Segment`.
2. THE API SHALL expose a `GET /api/segments/summary` endpoint that returns the Segment_Distribution as a JSON array, where each element contains `segment`, `count`, and `percentage`.
3. THE API SHALL expose a `GET /api/rfm/top` endpoint that accepts an optional query parameter `n` (default 10) and returns the top `n` customers ranked by RFM_Score.
4. WHEN a client sends a request to any API endpoint, THE API SHALL respond with the appropriate HTTP status code and a JSON body.
5. IF a client sends a request with an invalid query parameter value, THEN THE API SHALL respond with HTTP 400 and a JSON error message describing the invalid parameter.
6. THE API SHALL include CORS headers to allow requests from the Frontend origin.

---

### Requirement 5: Frontend Visualization

**User Story:** As a BCA student, I want a web interface that visualizes RFM results, so that I can present and interpret the analysis clearly.

#### Acceptance Criteria

1. THE Frontend SHALL display a bar chart showing the Segment_Distribution (number of customers per Customer_Segment).
2. THE Frontend SHALL display a scatter plot with Recency on the x-axis and Monetary on the y-axis, with each point colored by Customer_Segment.
3. THE Frontend SHALL display a data table listing all customers with their `CustomerID`, `Recency`, `Frequency`, `Monetary`, `RFM_Score`, and `Customer_Segment` columns.
4. THE Frontend SHALL display a summary card section showing the total number of customers, the top segment by count, and the average Monetary value.
5. WHEN the Frontend loads, THE Frontend SHALL fetch data from the Backend API and render all visualizations without requiring a page reload.
6. IF the Backend API is unreachable, THEN THE Frontend SHALL display a user-friendly error message indicating that the data could not be loaded.
7. THE Frontend SHALL be responsive and render correctly on screen widths of 768px and above.

---

### Requirement 6: Code Quality and Educational Structure

**User Story:** As a BCA student, I want the codebase to be well-structured and commented, so that I can understand and explain each component during evaluation.

#### Acceptance Criteria

1. THE Backend SHALL organize code into clearly separated modules: data ingestion, RFM computation, and API routing.
2. THE Backend SHALL include inline comments and docstrings for all functions explaining the purpose, parameters, and return values.
3. THE Frontend SHALL organize code into clearly separated components: chart components, table component, and summary card component.
4. THE Backend SHALL include a `docs/` folder containing a brief explanation of the RFM methodology and the segment mapping logic used in the project.
5. THE Backend SHALL expose a `GET /api/health` endpoint that returns HTTP 200 with a JSON body `{"status": "ok"}` to allow students to verify the server is running.
