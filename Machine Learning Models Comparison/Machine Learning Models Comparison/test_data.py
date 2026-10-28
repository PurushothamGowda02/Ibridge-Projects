"""
Quick script to test if your CSV data is suitable for the ML comparison tool.
Usage: python test_data.py your_data.csv target_column_name
"""

import sys
import pandas as pd
from pathlib import Path


def test_dataset(csv_path: str, target_col: str = None):
    """Test if a CSV file is suitable for ML model comparison."""
    
    print(f"\n{'='*60}")
    print(f"Testing Dataset: {csv_path}")
    print(f"{'='*60}\n")
    
    # Test 1: Can we load the file?
    try:
        df = pd.read_csv(csv_path)
        print("✅ File loaded successfully")
        print(f"   Shape: {df.shape[0]} rows × {df.shape[1]} columns\n")
    except Exception as e:
        print(f"❌ Failed to load file: {e}")
        return False
    
    # Test 2: Show basic info
    print("📊 Dataset Overview:")
    print(f"   Columns: {', '.join(df.columns.tolist())}")
    print(f"   Total missing values: {df.isnull().sum().sum()}")
    print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n")
    
    # Test 3: Show column details
    print("📋 Column Details:")
    for col in df.columns:
        dtype = df[col].dtype
        missing = df[col].isnull().sum()
        unique = df[col].nunique()
        print(f"   • {col:20s} | Type: {str(dtype):10s} | Missing: {missing:5d} | Unique: {unique:5d}")
    print()
    
    # Test 4: If target column specified, analyze it
    if target_col:
        if target_col not in df.columns:
            print(f"❌ Target column '{target_col}' not found in dataset!")
            print(f"   Available columns: {', '.join(df.columns.tolist())}")
            return False
        
        print(f"🎯 Target Column Analysis: '{target_col}'")
        n_unique = df[target_col].nunique()
        n_samples = len(df)
        
        print(f"   Unique values: {n_unique}")
        print(f"   Total samples: {n_samples}")
        
        # Check if suitable for classification
        if n_unique == n_samples:
            print("   ❌ PROBLEM: Every row has a unique value (likely an ID column)")
            print("   → This cannot be used as a target for classification")
            return False
        elif n_unique == 1:
            print("   ❌ PROBLEM: Only 1 unique value")
            print("   → Need at least 2 classes for classification")
            return False
        elif n_unique > 100:
            print(f"   ⚠️  WARNING: {n_unique} unique classes is very high")
            print("   → This might be better suited for regression")
            print("   → Training will be slow and may use lots of memory")
        elif n_unique < 2:
            print("   ❌ PROBLEM: Less than 2 unique values")
            return False
        else:
            print(f"   ✅ Good: {n_unique} classes is suitable for classification")
        
        # Show class distribution
        print(f"\n   Class Distribution:")
        value_counts = df[target_col].value_counts()
        if n_unique <= 20:
            for val, count in value_counts.items():
                pct = count / n_samples * 100
                print(f"      {val}: {count} ({pct:.1f}%)")
        else:
            print(f"      (Too many classes to display - showing top 10)")
            for val, count in value_counts.head(10).items():
                pct = count / n_samples * 100
                print(f"      {val}: {count} ({pct:.1f}%)")
        
        # Check for class imbalance
        min_class_size = value_counts.min()
        if min_class_size < 5:
            print(f"\n   ⚠️  WARNING: Smallest class has only {min_class_size} samples")
            print("   → May cause issues with train/test split")
        
        print()
    
    # Test 5: Suggest ID columns to drop
    print("💡 Recommendations:")
    
    potential_ids = []
    for col in df.columns:
        if col == target_col:
            continue
        unique_ratio = df[col].nunique() / len(df)
        if unique_ratio > 0.95:
            potential_ids.append(col)
    
    if potential_ids:
        print(f"   Columns that look like IDs (consider dropping):")
        for col in potential_ids:
            print(f"      • {col}")
    
    # Check for high missing values
    high_missing = []
    for col in df.columns:
        missing_pct = df[col].isnull().sum() / len(df) * 100
        if missing_pct > 50:
            high_missing.append((col, missing_pct))
    
    if high_missing:
        print(f"\n   Columns with >50% missing values:")
        for col, pct in high_missing:
            print(f"      • {col}: {pct:.1f}% missing")
    
    print(f"\n{'='*60}")
    print("✅ Dataset appears suitable for ML model comparison!")
    print(f"{'='*60}\n")
    
    if target_col:
        print("Next steps:")
        print("1. Upload this CSV in the Streamlit app")
        print(f"2. Select '{target_col}' as the target column")
        if potential_ids:
            print(f"3. Drop these ID columns: {', '.join(potential_ids)}")
        print("4. Click 'Run Model Comparison' button")
    
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_data.py <csv_file> [target_column]")
        print("\nExample:")
        print("  python test_data.py data/telco_churn.csv Churn")
        print("  python test_data.py my_data.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    target_col = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(csv_path).exists():
        print(f"❌ File not found: {csv_path}")
        sys.exit(1)
    
    test_dataset(csv_path, target_col)
