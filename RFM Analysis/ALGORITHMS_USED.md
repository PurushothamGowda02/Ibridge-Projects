# Algorithms Used in RFM Analysis Project

## Overview

This project uses several algorithms and computational techniques for customer segmentation and data analysis. Here's a comprehensive breakdown:

---

## 1. RFM ANALYSIS ALGORITHM

### Algorithm Type: **Statistical Segmentation Algorithm**

### Purpose:
Customer segmentation based on behavioral metrics

### Core Algorithm Steps:

```
INPUT: Transaction dataset with CustomerID, InvoiceDate, Amount
OUTPUT: Customer segments with RFM scores

ALGORITHM RFM_Analysis:
1. Data Aggregation (GroupBy Algorithm)
2. Metric Calculation
3. Quantile-Based Scoring (Statistical Binning)
4. Rule-Based Segmentation (Decision Tree Logic)
```

### Detailed Breakdown:

#### **Step 1: GroupBy Aggregation Algorithm**
- **Algorithm:** Hash-based GroupBy
- **Implementation:** Pandas `groupby()`
- **Complexity:** O(n) where n = number of transactions
- **Process:**
  ```python
  For each transaction:
    1. Hash CustomerID
    2. Group transactions by hash
    3. Aggregate metrics per group
  ```

#### **Step 2: Recency Calculation**
- **Algorithm:** Date Difference Calculation
- **Formula:** `Recency = (Reference_Date - Max(Purchase_Dates)).days`
- **Complexity:** O(n) per customer
- **Example:**
  ```
  Reference Date: 2024-05-01
  Last Purchase: 2024-04-15
  Recency = 16 days
  ```

#### **Step 3: Frequency Calculation**
- **Algorithm:** Distinct Count (Cardinality Estimation)
- **Formula:** `Frequency = COUNT(DISTINCT InvoiceNo)`
- **Complexity:** O(n) per customer
- **Example:**
  ```
  Invoices: [INV001, INV002, INV002, INV003]
  Frequency = 3 (unique invoices)
  ```

#### **Step 4: Monetary Calculation**
- **Algorithm:** Summation
- **Formula:** `Monetary = SUM(Quantity × UnitPrice)`
- **Complexity:** O(n) per customer
- **Example:**
  ```
  Amounts: [50.00, 75.50, 120.00]
  Monetary = 245.50
  ```

---

## 2. QUANTILE BINNING ALGORITHM

### Algorithm Type: **Statistical Ranking & Binning**

### Purpose:
Convert continuous metrics into discrete scores (1-5)

### Algorithm: **Quantile-Based Discretization**

```
ALGORITHM Quantile_Binning:
INPUT: Array of metric values, number of bins (q=5)
OUTPUT: Score array (1 to 5)

1. Sort values in ascending order
2. Divide into q equal-sized groups (quintiles)
3. Assign labels 1 to q
4. Handle edge cases (duplicates, NaN)
5. Return score array
```

### Mathematical Formula:

```
For metric M with n customers:

Quintile boundaries:
Q1 = 20th percentile
Q2 = 40th percentile
Q3 = 60th percentile
Q4 = 80th percentile
Q5 = 100th percentile

Score Assignment:
Score 1: M ≤ Q1
Score 2: Q1 < M ≤ Q2
Score 3: Q2 < M ≤ Q3
Score 4: Q3 < M ≤ Q4
Score 5: Q4 < M ≤ Q5
```

### Implementation:
```python
# Pandas qcut algorithm
score = pd.qcut(values, q=5, labels=[1,2,3,4,5], duplicates='drop')
```

### Complexity:
- **Time:** O(n log n) - due to sorting
- **Space:** O(n) - for storing scores

### Special Handling:

**Recency Inversion:**
```
Lower recency (more recent) = Higher score
Implementation: score = qcut(-recency, q=5)
```

**Duplicate Edge Handling:**
```
If duplicate bin edges exist:
  - Use duplicates='drop' parameter
  - Results in fewer than 5 bins
  - Fill NaN with score 1
```

---

## 3. RULE-BASED SEGMENTATION ALGORITHM

### Algorithm Type: **Decision Tree / Rule-Based Classification**

### Purpose:
Assign customers to segments based on RFM scores

### Algorithm: **Priority-Based Rule Matching**

```
ALGORITHM Segment_Assignment:
INPUT: R_Score, F_Score for each customer
OUTPUT: Customer_Segment label

Rules (evaluated in priority order):
1. IF R_Score ≥ 4 AND F_Score ≥ 4 → Champions
2. IF F_Score ≥ 4 AND R_Score ≥ 2 → Loyal Customers
3. IF R_Score ≥ 3 AND F_Score ≥ 2 → Potential Loyalists
4. IF R_Score ≥ 4 AND F_Score = 1 → New Customers
5. IF R_Score ≤ 2 AND F_Score ≥ 3 → At Risk
6. IF R_Score ≤ 2 AND F_Score ≤ 2 → Lost
7. ELSE → Others

Return first matching rule
```

### Decision Tree Representation:

```
                    Root
                     |
            ┌────────┴────────┐
            |                 |
        R_Score ≥ 4      R_Score < 4
            |                 |
    ┌───────┴───────┐   ┌─────┴─────┐
    |               |   |           |
F ≥ 4           F = 1  F ≥ 4    F < 4
    |               |   |           |
Champions    New Cust  Loyal    [More rules...]
```

### Complexity:
- **Time:** O(1) per customer (constant rule checks)
- **Space:** O(1) per customer
- **Total:** O(n) for n customers

### Implementation:
```python
def assign_segment(r_score, f_score):
    if r_score >= 4 and f_score >= 4:
        return "Champions"
    elif f_score >= 4 and r_score >= 2:
        return "Loyal Customers"
    # ... more rules
    else:
        return "Others"
```

---

## 4. DATA CLEANING ALGORITHMS

### Algorithm 1: **Null Value Removal**

```
ALGORITHM Remove_Nulls:
INPUT: DataFrame with required columns
OUTPUT: Cleaned DataFrame

For each row:
  If any required column is NULL:
    Remove row
  Else:
    Keep row

Complexity: O(n × m) where n=rows, m=columns
```

### Algorithm 2: **Invalid Amount Filtering**

```
ALGORITHM Filter_Invalid_Amounts:
INPUT: DataFrame with Quantity, UnitPrice
OUTPUT: Filtered DataFrame

For each row:
  Amount = Quantity × UnitPrice
  If Amount ≤ 0:
    Remove row (return/cancellation)
  Else:
    Keep row

Complexity: O(n)
```

---

## 5. SORTING ALGORITHMS

### Used For: Top-N customer retrieval

### Algorithm: **TimSort** (Python's default)

```
ALGORITHM Get_Top_N:
INPUT: RFM DataFrame, n (number of top customers)
OUTPUT: Top n customers by RFM_Score

1. Sort DataFrame by RFM_Score (descending)
2. Select first n rows
3. Return result

Complexity: O(n log n) for sorting
```

### Implementation:
```python
top_customers = rfm_df.sort_values('RFM_Score', ascending=False).head(n)
```

---

## 6. HASH-BASED ALGORITHMS

### Used For: Fast data lookups and grouping

### Algorithm: **Hash Table (Dictionary)**

```
ALGORITHM Store_RFM_Data:
INPUT: RFM DataFrame
OUTPUT: In-memory hash table

For each customer:
  key = CustomerID
  value = {Recency, Frequency, Monetary, Scores, Segment}
  hash_table[key] = value

Lookup Complexity: O(1) average case
```

---

## 7. DATE PARSING ALGORITHM

### Algorithm: **String-to-DateTime Conversion**

```
ALGORITHM Parse_Dates:
INPUT: Date string (various formats)
OUTPUT: DateTime object

1. Detect date format (regex pattern matching)
2. Parse components (year, month, day, time)
3. Validate date
4. Convert to standard format
5. Return DateTime object

Complexity: O(n) where n = number of dates
```

### Supported Formats:
- MM/DD/YYYY HH:MM
- YYYY-MM-DD HH:MM:SS
- DD-MM-YYYY
- ISO 8601

---

## 8. STATISTICAL ALGORITHMS

### Algorithm 1: **Mean Calculation**

```
ALGORITHM Calculate_Mean:
INPUT: Array of values
OUTPUT: Mean value

Sum = 0
For each value in array:
  Sum += value
Mean = Sum / Count(array)

Complexity: O(n)
```

### Algorithm 2: **Percentile Calculation**

```
ALGORITHM Calculate_Percentile:
INPUT: Sorted array, percentile (p)
OUTPUT: Value at percentile p

1. Sort array (if not sorted)
2. Calculate index: i = (p/100) × (n-1)
3. If i is integer: return array[i]
4. Else: interpolate between array[floor(i)] and array[ceil(i)]

Complexity: O(n log n) with sorting
```

---

## 9. AGGREGATION ALGORITHMS

### Algorithm: **MapReduce Pattern**

```
ALGORITHM Aggregate_Transactions:
INPUT: Transaction list
OUTPUT: Customer-level aggregates

MAP Phase:
  For each transaction:
    Emit (CustomerID, transaction_data)

SHUFFLE Phase:
  Group all transactions by CustomerID

REDUCE Phase:
  For each CustomerID:
    Aggregate metrics (Recency, Frequency, Monetary)
    Emit (CustomerID, aggregated_metrics)

Complexity: O(n) with hash-based grouping
```

---

## 10. VALIDATION ALGORITHMS

### Algorithm: **Schema Validation**

```
ALGORITHM Validate_CSV:
INPUT: CSV file
OUTPUT: Valid/Invalid + error messages

Required columns = [InvoiceNo, StockCode, Description, 
                   Quantity, InvoiceDate, UnitPrice, 
                   CustomerID, Country]

1. Read CSV header
2. For each required column:
     If column not in header:
       Add to missing_columns list
3. If missing_columns is not empty:
     Return Invalid + missing_columns
4. Else:
     Return Valid

Complexity: O(m) where m = number of columns
```

---

## ALGORITHM COMPLEXITY SUMMARY

| Algorithm | Time Complexity | Space Complexity | Use Case |
|-----------|----------------|------------------|----------|
| GroupBy Aggregation | O(n) | O(k) | Group transactions by customer |
| Quantile Binning | O(n log n) | O(n) | Score assignment |
| Rule-Based Segmentation | O(n) | O(1) | Segment assignment |
| Sorting (TimSort) | O(n log n) | O(n) | Top-N customers |
| Hash Table Lookup | O(1) avg | O(n) | Fast data retrieval |
| Date Parsing | O(n) | O(1) | Convert date strings |
| Mean Calculation | O(n) | O(1) | Statistics |
| Null Removal | O(n×m) | O(n) | Data cleaning |

**Overall System Complexity:**
- **Best Case:** O(n log n) - dominated by sorting
- **Average Case:** O(n log n)
- **Worst Case:** O(n²) - if hash collisions occur
- **Space:** O(n) - storing customer data

Where:
- n = number of transactions or customers
- m = number of columns
- k = number of unique customers

---

## OPTIMIZATION TECHNIQUES USED

### 1. **Vectorization**
- Use pandas vectorized operations instead of loops
- Example: `df['Amount'] = df['Quantity'] * df['UnitPrice']`
- Speedup: 10-100x faster than Python loops

### 2. **In-Memory Caching**
- Store computed RFM data in memory (app.state)
- Avoid recomputation on each request
- Trade-off: Memory for speed

### 3. **Lazy Evaluation**
- Only compute what's needed
- Example: Top-N query doesn't load all data

### 4. **Efficient Data Structures**
- Use pandas DataFrame (columnar storage)
- Hash tables for O(1) lookups
- Sorted arrays for binary search

### 5. **Early Termination**
- Stop processing when condition met
- Example: First matching segment rule

---

## ALGORITHM SELECTION RATIONALE

### Why Quantile Binning?
- **Fair distribution:** Each score has ~20% of customers
- **Adaptive:** Works with any data distribution
- **Interpretable:** Easy to explain to business users
- **Robust:** Handles outliers well

### Why Rule-Based Segmentation?
- **Transparent:** Business can understand and modify rules
- **Fast:** O(1) per customer
- **Flexible:** Easy to add new segments
- **Proven:** Industry-standard approach

### Why Hash-Based GroupBy?
- **Efficient:** O(n) average case
- **Scalable:** Works with large datasets
- **Built-in:** Leverages pandas optimization

### Why TimSort?
- **Hybrid:** Combines merge sort and insertion sort
- **Adaptive:** Fast on partially sorted data
- **Stable:** Preserves order of equal elements
- **Optimized:** Python's default, highly tuned

---

## MATHEMATICAL FOUNDATIONS

### 1. **Percentile Formula**
```
P(k) = (k/100) × (n + 1)

Where:
- P(k) = position of kth percentile
- n = number of data points
- k = percentile (0-100)
```

### 2. **Z-Score (Alternative Scoring Method)**
```
Z = (X - μ) / σ

Where:
- X = individual value
- μ = mean
- σ = standard deviation

Note: Not used in this project, but common alternative
```

### 3. **Weighted RFM Score (Alternative)**
```
RFM_Weighted = (w_R × R_Score) + (w_F × F_Score) + (w_M × M_Score)

Where:
- w_R, w_F, w_M = weights (sum to 1)

Note: Current project uses concatenation "RFM"
```

---

## ALGORITHM PSEUDOCODE

### Complete RFM Analysis Pipeline:

```
FUNCTION rfm_analysis(transactions_csv):
    // Step 1: Load and Clean
    df = load_csv(transactions_csv)
    df = remove_nulls(df, required_columns)
    df['Amount'] = df['Quantity'] * df['UnitPrice']
    df = filter_positive_amounts(df)
    
    // Step 2: Calculate Reference Date
    reference_date = max(df['InvoiceDate']) + 1 day
    
    // Step 3: Aggregate by Customer
    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (reference_date - max(x)).days,  // Recency
        'InvoiceNo': 'nunique',                                    // Frequency
        'Amount': 'sum'                                            // Monetary
    })
    
    // Step 4: Assign Scores
    rfm['R_Score'] = quantile_bin(-rfm['Recency'], q=5)  // Inverted
    rfm['F_Score'] = quantile_bin(rfm['Frequency'], q=5)
    rfm['M_Score'] = quantile_bin(rfm['Monetary'], q=5)
    rfm['RFM_Score'] = concat(R_Score, F_Score, M_Score)
    
    // Step 5: Assign Segments
    FOR each customer in rfm:
        segment = apply_segment_rules(customer.R_Score, customer.F_Score)
        customer['Customer_Segment'] = segment
    
    RETURN rfm
END FUNCTION
```

---

## CONCLUSION

This project uses a combination of:
- **Statistical algorithms** (quantile binning, aggregation)
- **Rule-based algorithms** (segment classification)
- **Sorting algorithms** (TimSort for ranking)
- **Hash-based algorithms** (fast lookups)
- **Data processing algorithms** (cleaning, validation)

All algorithms are chosen for:
- ✅ **Efficiency** - O(n log n) or better
- ✅ **Scalability** - Handle thousands of customers
- ✅ **Interpretability** - Business can understand results
- ✅ **Robustness** - Handle edge cases and outliers

---

**Document Version:** 1.0  
**Last Updated:** May 2026
