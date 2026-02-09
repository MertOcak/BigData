# -*- coding: utf-8 -*-
"""Generate 10,000 rows of random sample data for sample_data.csv."""

import random
from datetime import datetime, timedelta

# English column names and values
PRODUCTS = ["Product A", "Product B", "Product C"]
CATEGORIES = ["Electronics", "Apparel", "Home"]
REGIONS = ["Istanbul", "Ankara", "Izmir", "Bursa", "Antalya", "Adana", "Konya", "Gaziantep"]
PRODUCT_PRICE_RANGE = {
    "Product A": (250.0, 350.0),
    "Product B": (70.0, 120.0),
    "Product C": (120.0, 200.0),
}

FIELDNAMES = ["date", "product", "category", "sales_quantity", "unit_price", "region"]


def random_date(start_year=2026, end_year=2026):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def main():
    rows = []
    for _ in range(10000):
        product = random.choice(PRODUCTS)
        price_min, price_max = PRODUCT_PRICE_RANGE[product]
        unit_price = round(random.uniform(price_min, price_max), 2)
        dt = random_date()
        category = random.choice(CATEGORIES)
        sales_quantity = random.randint(10, 500)
        region = random.choice(REGIONS)
        rows.append({
            "date": dt.strftime("%Y-%m-%d"),
            "product": product,
            "category": category,
            "sales_quantity": sales_quantity,
            "unit_price": unit_price,
            "region": region,
        })

    with open("sample_data.csv", "w", encoding="utf-8-sig", newline="") as f:
        import csv
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        w.writeheader()
        w.writerows(rows)

    print("sample_data.csv updated: 10,000 rows of random data written.")


if __name__ == "__main__":
    main()
