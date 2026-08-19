import csv
import json
from pathlib import Path

SCRIPTS_ROUTE = Path(__file__).parent
CSV_PATH = SCRIPTS_ROUTE / "utils/ventas.csv"


with open(CSV_PATH, "r", encoding="utf8", newline="") as data:
    data_read = csv.DictReader(data)
    json_data = {"total_quantity": 0, "average_price": 0.0, "max_product_sale": ""}
    product_count = 0
    total_price = 0.0
    max_quantity_seen = 0
    max_product = ""

    for row in data_read:
        quantity = int(row["cantidad"])
        json_data["total_quantity"] += quantity

        price = float(row["precio"])
        total_price += price

        if quantity > max_quantity_seen:
            max_quantity_seen = quantity
            max_product = row["producto"]

        product_count += 1
    json_data["average_price"] = total_price / product_count
    json_data["max_product_sale"] = max_product

SCRIPTS_ROUTE = Path(__file__).parent
JSON_PATH = SCRIPTS_ROUTE / "utils/data.json"
with open(JSON_PATH, "w", encoding="utf8", newline="") as json_archive:
    json.dump(json_data, json_archive, indent=4, ensure_ascii=False)
