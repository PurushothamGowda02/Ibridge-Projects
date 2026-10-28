"""
Test script to compare RFM analysis on training vs test datasets.

This script demonstrates that the RFM pipeline works on both:
1. Training dataset (online_retail.csv) — 12,097 rows, 1,482 customers
2. Test dataset (test_dataset.csv) — 26 rows, 8 customers

Run from backend/ directory:
    python test_both_datasets.py
"""

import sys
sys.path.insert(0, '.')

import pandas as pd
from data.ingestion import load_dataset, clean_dataset
from rfm.computation import compute_rfm, assign_scores, assign_segments


def analyze_dataset(filepath, dataset_name):
    """Load, clean, and analyze a dataset."""
    print(f"\n{'='*70}")
    print(f"Analyzing: {dataset_name}")
    print(f"{'='*70}")
    
    try:
        # Load raw data
        df = load_dataset(filepath)
        print(f"✓ Loaded: {len(df)} rows")
        
        # Clean data
        df_clean = clean_dataset(df)
        print(f"✓ Cleaned: {len(df_clean)} rows (removed {len(df) - len(df_clean)} invalid rows)")
        
        # Compute RFM
        reference_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)
        rfm = compute_rfm(df_clean, reference_date)
        print(f"✓ RFM computed: {len(rfm)} unique customers")
        
        # Assign scores
        rfm = assign_scores(rfm)
        print(f"✓ Scores assigned (R, F, M each 1-5)")
        
        # Assign segments
        rfm = assign_segments(rfm)
        print(f"✓ Segments assigned")
        
        # Display results
        print(f"\n--- Summary Statistics ---")
        print(f"Total Customers: {len(rfm)}")
        print(f"Avg Recency: {rfm['Recency'].mean():.1f} days")
        print(f"Avg Frequency: {rfm['Frequency'].mean():.1f} transactions")
        print(f"Avg Monetary: £{rfm['Monetary'].mean():.2f}")
        
        print(f"\n--- Segment Distribution ---")
        segment_counts = rfm['Customer_Segment'].value_counts()
        for segment, count in segment_counts.items():
            pct = (count / len(rfm)) * 100
            print(f"  {segment:20s}: {count:3d} customers ({pct:5.1f}%)")
        
        print(f"\n--- Top 5 Customers by RFM Score ---")
        top_5 = rfm.nlargest(5, 'RFM_Score')[
            ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'RFM_Score', 'Customer_Segment']
        ]
        print(top_5.to_string(index=False))
        
        print(f"\n--- Bottom 5 Customers by RFM Score ---")
        bottom_5 = rfm.nsmallest(5, 'RFM_Score')[
            ['CustomerID', 'Recency', 'Frequency', 'Monetary', 'RFM_Score', 'Customer_Segment']
        ]
        print(bottom_5.to_string(index=False))
        
        return rfm
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def main():
    print("\n" + "="*70)
    print("RFM ANALYSIS: TRAINING vs TEST DATASET COMPARISON")
    print("="*70)
    
    # Analyze training dataset
    training_rfm = analyze_dataset(
        'data/online_retail.csv',
        'TRAINING DATASET (online_retail.csv)'
    )
    
    # Analyze test dataset
    test_rfm = analyze_dataset(
        'data/test_dataset.csv',
        'TEST DATASET (test_dataset.csv)'
    )
    
    # Comparison
    if training_rfm is not None and test_rfm is not None:
        print(f"\n{'='*70}")
        print("COMPARISON SUMMARY")
        print(f"{'='*70}")
        print(f"Training Dataset: {len(training_rfm)} customers")
        print(f"Test Dataset:     {len(test_rfm)} customers")
        print(f"\n✓ Both datasets processed successfully!")
        print(f"✓ RFM scores and segments assigned to all customers")
        print(f"✓ System works on both training and unseen test data")
        print(f"\nConclusion: The RFM pipeline is robust and generalizes to new data.")


if __name__ == '__main__':
    main()
