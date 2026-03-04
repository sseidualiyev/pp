import re
import json
import os

folder = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(folder, "raw.txt")

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

product_lines = re.findall(r"\d+\.\s*(.+?)\n\d", text, re.DOTALL)
products = [p.strip().replace("\n", " ") for p in product_lines]

products = [re.sub(r"^\[RX\]-", "", p).strip() for p in products]

price_matches = re.findall(r"\d[\d\s]*,\d{2}", text)
prices = [int(p.replace(" ", "").replace(",", "")) for p in price_matches[:len(products)]]

total_match = re.search(r"ИТОГО:\s*\n?([\d\s]+,\d{2})", text)
total = int(total_match.group(1).replace(" ", "").replace(",", "")) if total_match else sum(prices)

datetime_match = re.search(r"Время:\s*([\d./]+)\s*([\d:]+)", text)
date = datetime_match.group(1) if datetime_match else ""
time = datetime_match.group(2) if datetime_match else ""

payment_match = re.search(r"Банковская карта:\s*([\d\s]+)", text)
payment_method = "Card" if payment_match else "Cash"

receipt_data = {
    "products": [{"name": name, "price": price} for name, price in zip(products, prices)],
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(receipt_data, ensure_ascii=False, indent=2))
