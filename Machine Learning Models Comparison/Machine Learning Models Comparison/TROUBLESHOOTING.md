# Troubleshooting Guide: External Data Upload Issues

## Problem: "My uploaded data is not getting trained"

### Solution Steps:

### 1. **Click the "Run Model Comparison" Button**
   - **Most Common Issue**: After uploading your CSV, you MUST click the "🚀 Run Model Comparison" button
   - Simply uploading the file only loads it into memory - it doesn't automatically train models
   - Look for the green button below the target column selection

### 2. **Select the Correct Target Column**
   - The target column should be your **classification label** (what you want to predict)
   - ❌ **Don't select**: ID columns, names, continuous numbers (unless binned)
   - ✅ **Do select**: Categorical columns like "Churn" (Yes/No), "Survived" (0/1), "Category" (A/B/C)

### 3. **Check Your Data Format**
   Your CSV should:
   - Have a header row with column names
   - Have at least 2 unique values in the target column
   - Not have the target column as an ID (every row unique)
   - Be properly formatted CSV (comma-separated)

### 4. **Verify Dataset Requirements**
   - **Minimum samples**: At least 50 rows recommended
   - **Target column**: Should have 2-100 unique classes (for classification)
   - **Features**: At least 1 feature column (besides target)
   - **Missing values**: Some are OK, but not entire columns

---

## Common Error Messages and Solutions

### Error: "Every row has a unique value"
**Cause**: You selected an ID column as the target  
**Solution**: Select a different column that represents categories/classes

### Error: "Too many unique classes"
**Cause**: Target has 100+ unique values (might be continuous data)  
**Solution**: 
- If it's truly categorical, proceed anyway (will be slow)
- If it's continuous (prices, ages), consider binning into categories
- Or use regression instead of classification

### Error: "Only 1 unique value"
**Cause**: Target column has no variation  
**Solution**: Check your data - you need at least 2 different classes

### Error: "Cross-validation failed"
**Cause**: Some classes have very few samples  
**Solution**: This is just a warning - training will continue without CV

---

## Step-by-Step Upload Process

1. **Select "Upload CSV"** radio button
2. **Click "Browse files"** and select your CSV file
3. **Wait for success message**: "✅ Loaded [filename] with shape (rows, columns)"
4. **Review the dataset preview** table
5. **Select your target column** from the dropdown
6. **Optionally drop ID columns** (customerID, PassengerId, etc.)
7. **Click "🚀 Run Model Comparison"** button
8. **Wait for training** - you'll see a progress bar
9. **View results** - accuracy, charts, and download options

---

## Example: Good vs Bad Target Columns

### ❌ Bad Target Columns (Don't Use):
- `customerID` - Every row is unique (ID column)
- `transaction_amount` - Continuous number (use regression)
- `timestamp` - Date/time (not a category)
- `name` - Text with many unique values

### ✅ Good Target Columns (Use These):
- `Churn` - Binary (Yes/No or 0/1)
- `Survived` - Binary (0/1)
- `product_category` - Multiple categories (Electronics, Clothing, etc.)
- `risk_level` - Ordinal (Low/Medium/High)
- `customer_segment` - Multiple groups (A/B/C/D)

---

## Still Having Issues?

### Check the Console/Terminal
If you ran the app with `streamlit run app.py`, check the terminal for error messages

### Verify Your CSV File
Open your CSV in a text editor or Excel to ensure:
- It's actually comma-separated
- Column names are in the first row
- No special characters causing parsing issues

### Test with Built-in Dataset First
1. Select "Use built-in Telco Churn CSV"
2. Click "Run Model Comparison"
3. If this works, the issue is with your uploaded data format

### Dataset Size Limits
- Very large files (>100MB) may cause memory issues
- Very small files (<50 rows) may not train well
- Optimal: 1,000 - 100,000 rows

---

## Quick Checklist

Before clicking "Run Model Comparison", verify:

- [ ] CSV file uploaded successfully (green checkmark)
- [ ] Dataset preview shows your data correctly
- [ ] Target column selected (not an ID column)
- [ ] Target has 2+ unique values
- [ ] ID columns added to "drop" list (optional but recommended)
- [ ] Ready to click the green "Run Model Comparison" button

---

## Need More Help?

Check these files:
- `README.md` - General project information
- `QUICK_START.md` - Getting started guide
- `PROJECT_SUMMARY.md` - Project overview

Or review the example datasets in the `data/` folder to see proper formatting.
