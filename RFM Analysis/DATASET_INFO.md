# RFM Analysis - Dataset Information

## 📊 Current Datasets

### Training Dataset: `backend/data/online_retail.csv`
- **Total Transactions:** 15,783 rows
- **Unique Customers:** 500 customers
- **Unique Invoices:** 5,244 invoices
- **Date Range:** January 1, 2023 - December 31, 2023
- **Countries:** 15 countries
- **Products:** 30 different products

**Customer Distribution:**
- Lost: 139 customers (27.8%)
- Champions: 117 customers (23.4%)
- Potential Loyalists: 108 customers (21.6%)
- Loyal Customers: 76 customers (15.2%)
- At Risk: 32 customers (6.4%)
- New Customers: 15 customers (3.0%)
- Others: 13 customers (2.6%)

### Test Dataset: `backend/data/test_dataset.csv`
- **Total Transactions:** 2,274 rows
- **Unique Customers:** 200 customers
- **Date Range:** May 1, 2024 - August 31, 2024
- **Countries:** 7 countries
- **Products:** 7 different products

## 🎯 RFM Analysis Explanation

### What is RFM?

RFM stands for:
- **R**ecency - How recently did the customer purchase?
- **F**requency - How often do they purchase?
- **M**onetary - How much do they spend?

### How It Works

1. **Data Input:** Upload CSV with transaction data
2. **Grouping:** Transactions are grouped by CustomerID
3. **Calculation:**
   - **Recency:** Days since last purchase
   - **Frequency:** Count of unique invoices
   - **Monetary:** Total amount spent (Quantity × UnitPrice)
4. **Scoring:** Each metric gets a score from 1-5 (5 is best)
5. **Segmentation:** Customers are assigned to segments based on scores

### Why Only X Customers?

**Important:** RFM analysis groups transactions by **unique CustomerID**.

**Example:**
- If you have 1,000 transactions from 50 different customers
- RFM analysis will return **50 customer records** (not 1,000)
- Each customer record shows their aggregated behavior

**Current Datasets:**
- Training data: 15,783 transactions → **500 unique customers**
- Test data: 2,274 transactions → **200 unique customers**

## 📁 Required CSV Format

Your CSV must have these 8 columns:

| Column | Type | Example |
|--------|------|---------|
| InvoiceNo | string | INV001 |
| StockCode | string | SKU001 |
| Description | string | Ceramic Coffee Mug |
| Quantity | integer | 5 |
| InvoiceDate | datetime | 01/15/2024 10:30 |
| UnitPrice | float | 12.99 |
| CustomerID | string | C00001 |
| Country | string | United Kingdom |

## 🔄 Generating New Datasets

### Generate Training Data (500 customers)

```bash
cd backend/data
python generate_large_dataset.py
```

This creates `online_retail.csv` with:
- 500 unique customers
- 1-20 transactions per customer
- Random dates in 2023
- 30 different products

### Generate Test Data (200 customers)

```bash
cd backend/data
python generate_test_dataset.py
```

This creates `test_dataset.csv` with:
- 200 unique customers
- 1-10 transactions per customer
- Random dates in May-August 2024
- 7 different products

### Customize Dataset Size

Edit the scripts and change:

```python
NUM_CUSTOMERS = 1000  # Change this number
MIN_TRANSACTIONS = 1
MAX_TRANSACTIONS = 50
```

## 📈 Understanding Results

### Example Output

If you upload a CSV with:
- 10,000 transaction rows
- 250 unique CustomerIDs

**You will get:**
- ✅ 250 RFM customer records
- ✅ Each record shows aggregated metrics for that customer
- ✅ Segment distribution across 250 customers

### Sample Customer Record

```json
{
  "CustomerID": "C00123",
  "Recency": 15,           // Last purchase 15 days ago
  "Frequency": 8,          // Made 8 purchases
  "Monetary": 456.78,      // Spent $456.78 total
  "R_Score": 5,            // Recency score (1-5)
  "F_Score": 4,            // Frequency score (1-5)
  "M_Score": 5,            // Monetary score (1-5)
  "RFM_Score": "545",      // Combined score
  "Customer_Segment": "Champions"  // Segment label
}
```

## 🎓 Customer Segments

### 1. Champions (R≥4, F≥4)
- **Who:** Best customers
- **Behavior:** Recent and frequent buyers
- **Action:** Reward them, ask for reviews

### 2. Loyal Customers (F≥4, R≥2)
- **Who:** Frequent buyers
- **Behavior:** Buy often but not recently
- **Action:** Re-engage with offers

### 3. Potential Loyalists (R≥3, F≥2)
- **Who:** Recent customers with potential
- **Behavior:** Moderate frequency
- **Action:** Nurture with loyalty programs

### 4. New Customers (R≥4, F=1)
- **Who:** First-time or infrequent buyers
- **Behavior:** Recent but low frequency
- **Action:** Onboard and engage

### 5. At Risk (R≤2, F≥3)
- **Who:** Previously frequent buyers
- **Behavior:** Haven't purchased recently
- **Action:** Win-back campaigns

### 6. Lost (R≤2, F≤2)
- **Who:** Inactive customers
- **Behavior:** Low recency and frequency
- **Action:** Re-activation campaigns

### 7. Others
- **Who:** Remaining customers
- **Behavior:** Don't fit other segments
- **Action:** Monitor and segment further

## 🧪 Testing the System

### Test with Included Data

1. **Start the application**
2. **Go to "Unseen Data Upload" tab**
3. **Upload:** `backend/data/test_dataset.csv`
4. **Expected Result:** 200 customer records

### Test with Your Own Data

1. **Prepare CSV** with 8 required columns
2. **Ensure unique CustomerIDs** (e.g., CUST001, CUST002, etc.)
3. **Upload** via the web interface
4. **Result:** One RFM record per unique CustomerID

## 💡 Tips

### Want More Customers in Results?

✅ **Add more unique CustomerIDs to your CSV**
- Not more rows with same CustomerID
- Each unique CustomerID = 1 RFM record

### Example:

**Wrong Approach (Still 2 customers):**
```csv
INV001,SKU001,Product,5,01/15/2024,10.00,CUST001,USA
INV002,SKU002,Product,3,01/16/2024,15.00,CUST001,USA
INV003,SKU003,Product,2,01/17/2024,20.00,CUST002,USA
INV004,SKU004,Product,1,01/18/2024,25.00,CUST002,USA
```
Result: 2 customers (CUST001, CUST002)

**Right Approach (4 customers):**
```csv
INV001,SKU001,Product,5,01/15/2024,10.00,CUST001,USA
INV002,SKU002,Product,3,01/16/2024,15.00,CUST002,USA
INV003,SKU003,Product,2,01/17/2024,20.00,CUST003,USA
INV004,SKU004,Product,1,01/18/2024,25.00,CUST004,USA
```
Result: 4 customers (CUST001, CUST002, CUST003, CUST004)

## 📞 Support

If you're not seeing the expected number of customers:

1. **Check unique CustomerIDs:**
   ```python
   import pandas as pd
   df = pd.read_csv('your_file.csv')
   print(f"Unique customers: {df['CustomerID'].nunique()}")
   ```

2. **Check for null values:**
   ```python
   print(df['CustomerID'].isnull().sum())
   ```

3. **View customer list:**
   ```python
   print(df['CustomerID'].unique())
   ```

---

**Last Updated:** May 26, 2026  
**Dataset Version:** 2.0 (500 customers)
