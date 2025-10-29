"""Check menu items and prices in database"""
import sqlite3

db_path = "restaurant_billing.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all menu items with their prices
cursor.execute("""
    SELECT name, category, price_single, price_full, is_available
    FROM menu_items
    ORDER BY category, name
""")

items = cursor.fetchall()

print("=" * 80)
print("MENU ITEMS IN DATABASE")
print("=" * 80)

current_category = None
total_items = 0
with_prices = 0
without_prices = 0
new_items_count = 0

for name, category, price_single, price_full, is_available in items:
    total_items += 1
    
    if current_category != category:
        if current_category:
            print()
        print(f"\n[{category}]")
        current_category = category
    
    if price_single and price_single > 0:
        with_prices += 1
        if price_full:
            price_str = f"Rs.{price_single:.0f} / Rs.{price_full:.0f}"
        else:
            price_str = f"Rs.{price_single:.0f}"
        status = "[OK]" if is_available else "[X]"
        print(f"  {status} {name:40} {price_str}")
    else:
        without_prices += 1
        print(f"  [X] {name:40} [NO PRICE]")

print("\n" + "=" * 80)
print(f"SUMMARY:")
print(f"  Total items: {total_items}")
print(f"  Items with prices: {with_prices}")
print(f"  Items without prices: {without_prices}")
print("=" * 80)

conn.close()

