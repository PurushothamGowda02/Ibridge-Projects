"""
Generate a large RFM dataset with many unique customers.
"""
import pandas as pd
import random
from datetime import datetime, timedelta

# Configuration
NUM_CUSTOMERS = 500  # Number of unique customers
MIN_TRANSACTIONS = 1  # Minimum transactions per customer
MAX_TRANSACTIONS = 20  # Maximum transactions per customer
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 4, 30)

# Product catalog
PRODUCTS = [
    ("SKU001", "Ceramic Coffee Mug", 12.99),
    ("SKU002", "Stainless Steel Bottle", 24.99),
    ("SKU003", "Organic Cotton T-Shirt", 18.50),
    ("SKU004", "Bamboo Cutting Board", 32.99),
    ("SKU005", "Leather Wallet", 45.00),
    ("SKU006", "Glass Vase Set", 28.75),
    ("SKU007", "Wooden Spoon Set", 15.99),
    ("SKU008", "Scented Candle", 9.99),
    ("SKU009", "Knitted Throw Blanket", 49.99),
    ("SKU010", "Decorative Cushion", 22.50),
    ("SKU011", "Stainless Steel Kettle", 35.99),
    ("SKU012", "Linen Napkin Set", 8.99),
    ("SKU013", "Bamboo Toothbrush Set", 6.99),
    ("SKU014", "Ceramic Soap Dish", 11.50),
    ("SKU015", "Organic Cotton Pouch", 7.99),
    ("SKU016", "Wooden Serving Board", 38.99),
    ("SKU017", "Glass Water Bottle", 19.99),
    ("SKU018", "Eco-Friendly Soap", 4.99),
    ("SKU019", "Bamboo Desk Organizer", 29.99),
    ("SKU020", "Linen Bedsheet Set", 59.99),
    ("SKU021", "Stainless Steel Lunch Box", 34.99),
    ("SKU022", "Organic Cotton Socks", 5.99),
    ("SKU023", "Wooden Cutting Board", 26.99),
    ("SKU024", "Glass Jar Set", 16.99),
    ("SKU025", "Bamboo Hairbrush", 14.99),
    ("SKU026", "Ceramic Plate Set", 42.99),
    ("SKU027", "Linen Kitchen Towel", 3.99),
    ("SKU028", "Stainless Steel Straws", 8.99),
    ("SKU029", "Organic Cotton Pillow", 39.99),
    ("SKU030", "Bamboo Plant Pot", 18.99),
]

COUNTRIES = [
    "United Kingdom", "United States", "Canada", "Germany", "France",
    "Spain", "Italy", "Netherlands", "Belgium", "Australia",
    "Sweden", "Norway", "Poland", "Denmark", "Finland"
]

def random_date(start, end):
    """Generate a random datetime between start and end."""
    delta = end - start
    random_days = random.randint(0, delta.days)
    random_seconds = random.randint(0, 86400)
    return start + timedelta(days=random_days, seconds=random_seconds)

def generate_dataset():
    """Generate a large dataset with many customers."""
    records = []
    invoice_counter = 1
    
    for customer_num in range(1, NUM_CUSTOMERS + 1):
        customer_id = f"C{customer_num:05d}"  # C00001, C00002, etc.
        country = random.choice(COUNTRIES)
        
        # Random number of transactions for this customer
        num_transactions = random.randint(MIN_TRANSACTIONS, MAX_TRANSACTIONS)
        
        # Generate transactions for this customer
        for _ in range(num_transactions):
            invoice_no = f"INV{invoice_counter:06d}"
            invoice_date = random_date(START_DATE, END_DATE)
            
            # Random number of items in this transaction (1-5)
            num_items = random.randint(1, 5)
            
            for _ in range(num_items):
                stock_code, description, unit_price = random.choice(PRODUCTS)
                quantity = random.randint(1, 10)
                
                records.append({
                    "InvoiceNo": invoice_no,
                    "StockCode": stock_code,
                    "Description": description,
                    "Quantity": quantity,
                    "InvoiceDate": invoice_date.strftime("%m/%d/%Y %H:%M"),
                    "UnitPrice": unit_price,
                    "CustomerID": customer_id,
                    "Country": country
                })
            
            invoice_counter += 1
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Sort by date
    df['InvoiceDate_dt'] = pd.to_datetime(df['InvoiceDate'])
    df = df.sort_values('InvoiceDate_dt')
    df = df.drop('InvoiceDate_dt', axis=1)
    
    return df

if __name__ == "__main__":
    print("Generating large dataset...")
    df = generate_dataset()
    
    # Save to CSV
    output_file = "online_retail.csv"
    df.to_csv(output_file, index=False)
    
    print(f"✅ Dataset generated: {output_file}")
    print(f"   Total rows: {len(df)}")
    print(f"   Unique customers: {df['CustomerID'].nunique()}")
    print(f"   Unique invoices: {df['InvoiceNo'].nunique()}")
    print(f"   Date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
    print(f"   Countries: {df['Country'].nunique()}")
    
    # Show sample
    print("\nSample data:")
    print(df.head(10))
