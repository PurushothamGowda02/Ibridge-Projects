"""Generate test dataset with many customers."""
import pandas as pd
import random
from datetime import datetime, timedelta

NUM_CUSTOMERS = 200
PRODUCTS = [
    ('SKU001', 'Ceramic Coffee Mug', 12.99),
    ('SKU002', 'Stainless Steel Bottle', 24.99),
    ('SKU003', 'Organic Cotton T-Shirt', 18.50),
    ('SKU004', 'Bamboo Cutting Board', 32.99),
    ('SKU005', 'Leather Wallet', 45.00),
    ('SKU006', 'Glass Vase Set', 28.75),
    ('SKU007', 'Wooden Spoon Set', 15.99),
]
COUNTRIES = ['United Kingdom', 'United States', 'Canada', 'Germany', 'France', 'Spain', 'Italy']

records = []
invoice_counter = 1
START_DATE = datetime(2024, 5, 1)
END_DATE = datetime(2024, 8, 31)

for customer_num in range(1, NUM_CUSTOMERS + 1):
    customer_id = f'C{customer_num+20000:05d}'
    country = random.choice(COUNTRIES)
    num_transactions = random.randint(1, 10)
    
    for _ in range(num_transactions):
        invoice_no = f'TEST{invoice_counter:05d}'
        delta = END_DATE - START_DATE
        random_days = random.randint(0, delta.days)
        random_seconds = random.randint(0, 86400)
        invoice_date = START_DATE + timedelta(days=random_days, seconds=random_seconds)
        
        num_items = random.randint(1, 3)
        for _ in range(num_items):
            stock_code, description, unit_price = random.choice(PRODUCTS)
            quantity = random.randint(1, 5)
            records.append({
                'InvoiceNo': invoice_no,
                'StockCode': stock_code,
                'Description': description,
                'Quantity': quantity,
                'InvoiceDate': invoice_date.strftime('%m/%d/%Y %H:%M'),
                'UnitPrice': unit_price,
                'CustomerID': customer_id,
                'Country': country
            })
        invoice_counter += 1

df = pd.DataFrame(records)
df.to_csv('test_dataset.csv', index=False)
print(f'Test dataset: {len(df)} rows, {df["CustomerID"].nunique()} customers')
