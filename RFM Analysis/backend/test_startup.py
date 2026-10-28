"""
Test script to diagnose startup issues
Run from backend/ directory: python test_startup.py
"""

import sys
sys.path.insert(0, '.')

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s — %(message)s")
logger = logging.getLogger(__name__)

try:
    logger.info("Step 1: Importing modules...")
    from config import DATASET_PATH, CORS_ORIGINS
    logger.info(f"  ✓ Config loaded: DATASET_PATH={DATASET_PATH}, CORS_ORIGINS={CORS_ORIGINS}")
    
    logger.info("Step 2: Loading dataset...")
    from data.ingestion import load_dataset, clean_dataset
    df = load_dataset(DATASET_PATH)
    logger.info(f"  ✓ Dataset loaded: {len(df)} rows")
    
    logger.info("Step 3: Cleaning dataset...")
    df_clean = clean_dataset(df)
    logger.info(f"  ✓ Dataset cleaned: {len(df_clean)} rows")
    
    logger.info("Step 4: Computing RFM...")
    import pandas as pd
    from rfm.computation import compute_rfm, assign_scores, assign_segments
    reference_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)
    rfm = compute_rfm(df_clean, reference_date)
    logger.info(f"  ✓ RFM computed: {len(rfm)} customers")
    
    logger.info("Step 5: Assigning scores...")
    rfm = assign_scores(rfm)
    logger.info(f"  ✓ Scores assigned")
    
    logger.info("Step 6: Assigning segments...")
    rfm = assign_segments(rfm)
    logger.info(f"  ✓ Segments assigned")
    
    logger.info("Step 7: Testing API...")
    from main import create_app
    app = create_app()
    logger.info(f"  ✓ App created successfully")
    
    logger.info("\n✓✓✓ ALL TESTS PASSED ✓✓✓")
    logger.info(f"Ready to serve {len(rfm)} customers")
    
except Exception as e:
    logger.error(f"\n✗✗✗ ERROR ✗✗✗")
    logger.error(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
