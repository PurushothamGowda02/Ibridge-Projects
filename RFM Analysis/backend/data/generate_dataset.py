"""
generate_dataset.py
-------------------
One-off script to generate a realistic e-commerce transaction dataset
(online_retail.csv) for the RFM Analysis project.

Output: backend/data/online_retail.csv
Columns: InvoiceNo, StockCode, Description, Quantity, InvoiceDate,
         UnitPrice, CustomerID, Country
"""

import csv
import random
from datetime import datetime, timedelta

# ── Seed for reproducibility ──────────────────────────────────────────────────
random.seed(42)

# ── Product catalogue (50 products) ──────────────────────────────────────────
PRODUCTS = [
    ("P001", "Ceramic Mug"),
    ("P002", "Wooden Frame"),
    ("P003", "Scented Candle"),
    ("P004", "Cotton Tote Bag"),
    ("P005", "Leather Wallet"),
    ("P006", "Glass Vase"),
    ("P007", "Bamboo Cutting Board"),
    ("P008", "Stainless Steel Bottle"),
    ("P009", "Knitted Throw Blanket"),
    ("P010", "Decorative Cushion"),
    ("P011", "Porcelain Bowl"),
    ("P012", "Wicker Basket"),
    ("P013", "Linen Napkin Set"),
    ("P014", "Copper Lantern"),
    ("P015", "Marble Coaster Set"),
    ("P016", "Jute Rug"),
    ("P017", "Terracotta Pot"),
    ("P018", "Wooden Spoon Set"),
    ("P019", "Beeswax Wrap"),
    ("P020", "Recycled Glass Jar"),
    ("P021", "Embroidered Pillowcase"),
    ("P022", "Handmade Soap Bar"),
    ("P023", "Dried Flower Wreath"),
    ("P024", "Rattan Tray"),
    ("P025", "Velvet Jewellery Box"),
    ("P026", "Cork Trivet"),
    ("P027", "Macrame Wall Hanging"),
    ("P028", "Soy Wax Candle"),
    ("P029", "Linen Tea Towel"),
    ("P030", "Wooden Serving Board"),
    ("P031", "Enamel Mug"),
    ("P032", "Pressed Flower Card"),
    ("P033", "Seed Paper Notebook"),
    ("P034", "Bamboo Toothbrush Set"),
    ("P035", "Organic Cotton Pouch"),
    ("P036", "Recycled Tote Bag"),
    ("P037", "Handwoven Coaster"),
    ("P038", "Ceramic Plant Pot"),
    ("P039", "Wooden Bookmark"),
    ("P040", "Glass Candle Holder"),
    ("P041", "Felt Storage Basket"),
    ("P042", "Linen Bread Bag"),
    ("P043", "Beeswax Polish"),
    ("P044", "Wooden Clothes Hanger"),
    ("P045", "Reusable Beeswax Wrap"),
    ("P046", "Handmade Beeswax Candle"),
    ("P047", "Organic Lavender Sachet"),
    ("P048", "Recycled Paper Gift Bag"),
    ("P049", "Wooden Puzzle"),
    ("P050", "Ceramic Soap Dish"),
]

# ── Countries with realistic weights ─────────────────────────────────────────
COUNTRIES = ["United Kingdom", "Germany", "France", "USA", "Australia", "Canada", "India"]
COUNTRY_WEIGHTS = [0.50, 0.12, 0.12, 0.10, 0.06, 0.05, 0.05]

# ── Unit prices per product (fixed, realistic) ────────────────────────────────
UNIT_PRICES = {code: round(random.uniform(1.99, 99.99), 2) for code, _ in PRODUCTS}

# ── Date range: Jan 2023 – Dec 2023 ──────────────────────────────────────────
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2023, 12, 31, 23, 59)
DATE_RANGE_SECONDS = int((END_DATE - START_DATE).total_seconds())


def random_date() -> str:
    """Return a random datetime string within 2023 in MM/DD/YYYY HH:MM format."""
    offset = random.randint(0, DATE_RANGE_SECONDS)
    dt = START_DATE + timedelta(seconds=offset)
    return dt.strftime("%m/%d/%Y %H:%M")


def main():
    # ── Build customer pool (~4 000 unique customers) ─────────────────────────
    customer_ids = [f"C{i}" for i in range(1001, 5001)]  # C1001 – C5000

    # Assign each customer a country (stays consistent per customer)
    customer_country = {
        cid: random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0]
        for cid in customer_ids
    }

    # ── Build invoice pool (~2 000 unique invoices) ───────────────────────────
    # Each invoice belongs to one customer; customers can have multiple invoices
    # Using 2200 invoices × avg ~5.5 items = ~12,100 rows to ensure 12,000+ target
    invoice_ids = [f"INV{i}" for i in range(10001, 12201)]  # INV10001 – INV12200

    # Assign invoices to customers with a skewed distribution (repeat buyers)
    # ~20% of customers are "frequent" buyers who get more invoices
    frequent_customers = random.sample(customer_ids, k=800)
    invoice_customer = {}
    for inv in invoice_ids:
        if random.random() < 0.40:
            invoice_customer[inv] = random.choice(frequent_customers)
        else:
            invoice_customer[inv] = random.choice(customer_ids)

    # Each invoice gets a single date
    invoice_date = {inv: random_date() for inv in invoice_ids}

    # ── Generate rows ─────────────────────────────────────────────────────────
    rows = []
    for inv in invoice_ids:
        cid = invoice_customer[inv]
        country = customer_country[cid]
        inv_date = invoice_date[inv]
        num_items = random.randint(3, 8)
        products_chosen = random.sample(PRODUCTS, k=min(num_items, len(PRODUCTS)))

        for stock_code, description in products_chosen:
            # Quantity: ~5% negative (returns)
            if random.random() < 0.05:
                quantity = -random.randint(1, 5)
            else:
                quantity = random.randint(1, 10)

            # UnitPrice: ~3% zero
            if random.random() < 0.03:
                unit_price = 0.00
            else:
                unit_price = UNIT_PRICES[stock_code]

            # CustomerID: ~8% null
            customer_id_val = "" if random.random() < 0.08 else cid

            rows.append({
                "InvoiceNo": inv,
                "StockCode": stock_code,
                "Description": description,
                "Quantity": quantity,
                "InvoiceDate": inv_date,
                "UnitPrice": unit_price,
                "CustomerID": customer_id_val,
                "Country": country,
            })

    # ── Write CSV ─────────────────────────────────────────────────────────────
    output_path = "backend/data/online_retail.csv"
    fieldnames = ["InvoiceNo", "StockCode", "Description", "Quantity",
                  "InvoiceDate", "UnitPrice", "CustomerID", "Country"]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Dataset written to {output_path}")
    print(f"Total rows (excluding header): {len(rows):,}")
    print(f"Unique invoices: {len(invoice_ids):,}")
    print(f"Unique customers in pool: {len(customer_ids):,}")


if __name__ == "__main__":
    main()
