"""Sync databases between development and compiled app"""
import sqlite3
import os

# Check development database
dev_db = "restaurant_billing.db"
dist_db = "dist/restaurant_billing.db"

print("=" * 60)
print("DATABASE SYNC TOOL")
print("=" * 60)

if os.path.exists(dev_db):
    conn = sqlite3.connect(dev_db)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    dev_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM menu_items WHERE price_single IS NOT NULL AND price_single > 0")
    dev_with_prices = cursor.fetchone()[0]
    
    print(f"\nDevelopment database ({dev_db}):")
    print(f"  Total menu items: {dev_count}")
    print(f"  Items with prices: {dev_with_prices}")
    
    conn.close()
else:
    print(f"\n[ERROR] Development database not found: {dev_db}")

if os.path.exists(dist_db):
    conn = sqlite3.connect(dist_db)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    dist_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM menu_items WHERE price_single IS NOT NULL AND price_single > 0")
    dist_with_prices = cursor.fetchone()[0]
    
    print(f"\nCompiled app database ({dist_db}):")
    print(f"  Total menu items: {dist_count}")
    print(f"  Items with prices: {dist_with_prices}")
    
    conn.close()
else:
    print(f"\n[WARNING] Compiled app database not found: {dist_db}")

# Copy development database to dist
if os.path.exists(dev_db) and os.path.exists("dist"):
    print(f"\n" + "=" * 60)
    print("SYNCING DATABASE...")
    print("=" * 60)
    
    import shutil
    shutil.copy2(dev_db, dist_db)
    print(f"[OK] Copied {dev_db} to {dist_db}")
    
    # Verify
    conn = sqlite3.connect(dist_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    new_count = cursor.fetchone()[0]
    conn.close()
    
    print(f"[OK] Compiled app database now has {new_count} menu items")
    print(f"\n[OK] Database synced! The compiled app will now show updated menu items.")
else:
    print(f"\n[ERROR] Cannot sync - missing database or dist folder")

print("\n" + "=" * 60)

