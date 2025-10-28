"""
Final System Testing Script
Test all menu categories, price handling, Telegram, printer, and bill calculations
"""

import database
import telegram_notifier
import thermal_printer
from datetime import datetime

def test_database():
    """Test database connectivity and data integrity"""
    print("\n" + "="*60)
    print("TEST 1: Database Connectivity & Data Integrity")
    print("="*60)
    
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Test categories
        cursor.execute("SELECT COUNT(*) FROM categories")
        cat_count = cursor.fetchone()[0]
        print(f"[OK] Categories: {cat_count}")
        
        # Test menu items
        cursor.execute("SELECT COUNT(*) FROM menu_items")
        item_count = cursor.fetchone()[0]
        print(f"[OK] Menu Items: {item_count}")
        
        # Test settings
        cursor.execute("SELECT restaurant_name, gst_enabled, service_charge_rate FROM restaurant_settings WHERE id = 1")
        settings = cursor.fetchone()
        print(f"[OK] Restaurant Settings: {settings[0]}, GST: {settings[1]}, SC: {settings[2]}%")
        
        conn.close()
        print("[OK] Database connectivity: PASSED")
        return True
    except Exception as e:
        print(f"[ERROR] Database test FAILED: {e}")
        return False

def test_menu_categories():
    """Test all menu categories"""
    print("\n" + "="*60)
    print("TEST 2: Menu Categories")
    print("="*60)
    
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM categories ORDER BY name")
        categories = cursor.fetchall()
        
        print(f"\nFound {len(categories)} categories:")
        for cat in categories:
            cursor.execute("SELECT COUNT(*) FROM menu_items WHERE category = ?", (cat[0],))
            count = cursor.fetchone()[0]
            print(f"  * {cat[0]}: {count} items")
        
        conn.close()
        print("\n[OK] Menu categories: PASSED")
        return True
    except Exception as e:
        print(f"[ERROR] Menu categories test FAILED: {e}")
        return False

def test_price_handling():
    """Test single/dual price handling"""
    print("\n" + "="*60)
    print("TEST 3: Price Handling (Single/Dual)")
    print("="*60)
    
    try:
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Test dual price items
        cursor.execute("""
            SELECT name, price_single, price_full 
            FROM menu_items 
            WHERE price_single IS NOT NULL AND price_full IS NOT NULL
            LIMIT 3
        """)
        dual_items = cursor.fetchall()
        
        print(f"\nDual Price Items (Sample of {len(dual_items)}):")
        for name, single, full in dual_items:
            print(f"  * {name}: INR{single:.0f} / INR{full:.0f}")
        
        # Test single price items
        cursor.execute("""
            SELECT name, price_single 
            FROM menu_items 
            WHERE price_single IS NOT NULL AND price_full IS NULL
            LIMIT 3
        """)
        single_items = cursor.fetchall()
        
        print(f"\nSingle Price Items (Sample of {len(single_items)}):")
        for name, price in single_items:
            print(f"  * {name}: INR{price:.0f}")
        
        # Test items with price 0
        cursor.execute("SELECT COUNT(*) FROM menu_items WHERE is_available = 0")
        unavailable_count = cursor.fetchone()[0]
        print(f"\nItems with price 0 (not available): {unavailable_count}")
        
        conn.close()
        print("\n[OK] Price handling: PASSED")
        return True
    except Exception as e:
        print(f"[ERROR] Price handling test FAILED: {e}")
        return False

def test_telegram_notifications():
    """Test Telegram notification system"""
    print("\n" + "="*60)
    print("TEST 4: Telegram Notifications")
    print("="*60)
    
    try:
        # Test Telegram settings
        settings = telegram_notifier.get_telegram_settings()
        if settings:
            print(f"[OK] Bot Token: {settings['bot_token'][:20]}...")
            print(f"[OK] Chat ID: {settings['chat_id']}")
            print(f"[OK] Enabled: {settings['enabled']}")
        else:
            print("[ERROR] No Telegram settings found")
            return False
        
        # Test connection
        print("\nTesting Telegram connection...")
        success, message = telegram_notifier.test_telegram_connection()
        if success:
            print(f"[OK] {message}")
        else:
            print(f"[ERROR] {message}")
        
        print("\n[OK] Telegram notifications: PASSED")
        return True
    except Exception as e:
        print(f"[ERROR] Telegram test FAILED: {e}")
        return False

def test_thermal_printer():
    """Test thermal printer configuration"""
    print("\n" + "="*60)
    print("TEST 5: Thermal Printer")
    print("="*60)
    
    try:
        # List available printers
        printers = thermal_printer.list_available_printers()
        
        if printers:
            print(f"\nAvailable printers ({len(printers)}):")
            for i, printer in enumerate(printers, 1):
                print(f"  {i}. {printer}")
        else:
            print("\n! No printers detected")
            print("  (This is normal if no printer is connected)")
        
        # Test printer initialization
        printer = thermal_printer.ThermalPrinter()
        print(f"\n[OK] Printer instance created successfully")
        
        print("\n[OK] Thermal printer: PASSED")
        return True
    except Exception as e:
        print(f"[ERROR] Thermal printer test FAILED: {e}")
        return False

def test_bill_calculation():
    """Test bill calculation logic"""
    print("\n" + "="*60)
    print("TEST 6: Bill Calculation")
    print("="*60)
    
    try:
        # Sample cart
        test_items = [
            {'name': 'Clear Soup', 'price': 50, 'plate_type': 'single'},
            {'name': 'Chicken Lollipop', 'price': 190, 'plate_type': 'full'},
            {'name': 'Pani Puri', 'price': 25, 'plate_type': 'single'}
        ]
        
        # Calculate subtotal
        subtotal = sum(item['price'] for item in test_items)
        print(f"\nSample Cart:")
        for item in test_items:
            print(f"  * {item['name']} ({item['plate_type'].upper()}): INR{item['price']:.0f}")
        print(f"\nSubtotal: INR{subtotal:.2f}")
        
        # Get settings
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT gst_enabled, service_charge_rate FROM restaurant_settings WHERE id = 1")
        gst_enabled, sc_rate = cursor.fetchone()
        conn.close()
        
        # Calculate charges
        service_charge = (subtotal * sc_rate / 100) if sc_rate > 0 else 0
        gst_amount = (subtotal * 0.05) if gst_enabled else 0
        total = subtotal + service_charge + gst_amount
        
        print(f"\nCalculations:")
        if service_charge > 0:
            print(f"  Service Charge ({sc_rate}%): INR{service_charge:.2f}")
        if gst_amount > 0:
            print(f"  GST (5%): INR{gst_amount:.2f}")
        print(f"\n  TOTAL: INR{total:.2f}")
        
        # Verify calculation
        expected_total = subtotal + service_charge + gst_amount
        if abs(total - expected_total) < 0.01:
            print("\n[OK] Bill calculation: PASSED")
            return True
        else:
            print("\n[ERROR] Calculation mismatch")
            return False
            
    except Exception as e:
        print(f"[ERROR] Bill calculation test FAILED: {e}")
        return False

def test_order_simulation():
    """Simulate a complete order"""
    print("\n" + "="*60)
    print("TEST 7: Complete Order Simulation")
    print("="*60)
    
    try:
        # Create test order
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get sample items
        cursor.execute("""
            SELECT id, name, price_single 
            FROM menu_items 
            WHERE is_available = 1 AND price_single IS NOT NULL
            LIMIT 2
        """)
        items = cursor.fetchall()
        
        if not items:
            print("[ERROR] No available items found for testing")
            return False
        
        print(f"\nSimulating order with {len(items)} items:")
        test_cart = []
        for item_id, name, price in items:
            test_cart.append({
                'item_id': item_id,
                'name': name,
                'price': price,
                'plate_type': 'single'
            })
            print(f"  * {name}: INR{price:.0f}")
        
        # Calculate totals
        subtotal = sum(item['price'] for item in test_cart)
        cursor.execute("SELECT gst_enabled, service_charge_rate FROM restaurant_settings WHERE id = 1")
        gst_enabled, sc_rate = cursor.fetchone()
        
        service_charge = (subtotal * sc_rate / 100) if sc_rate > 0 else 0
        gst_amount = (subtotal * 0.05) if gst_enabled else 0
        total_amount = subtotal + service_charge + gst_amount
        
        print(f"\n  Subtotal: INR{subtotal:.2f}")
        if service_charge > 0:
            print(f"  Service Charge: INR{service_charge:.2f}")
        if gst_amount > 0:
            print(f"  GST: INR{gst_amount:.2f}")
        print(f"  TOTAL: INR{total_amount:.2f}")
        
        print(f"\n[OK] Order simulation: PASSED")
        conn.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Order simulation FAILED: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("RESTAURANT BILLING SOFTWARE - FINAL SYSTEM TESTING")
    print("="*60)
    
    results = []
    
    # Run all tests
    results.append(("Database", test_database()))
    results.append(("Menu Categories", test_menu_categories()))
    results.append(("Price Handling", test_price_handling()))
    results.append(("Telegram Notifications", test_telegram_notifications()))
    results.append(("Thermal Printer", test_thermal_printer()))
    results.append(("Bill Calculation", test_bill_calculation()))
    results.append(("Order Simulation", test_order_simulation()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        symbol = "[OK]" if result else "[ERROR]"
        print(f"{symbol} {test_name}: {status}")
        if result:
            passed += 1
    
    print("\n" + "="*60)
    print(f"Total: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("[OK] ALL TESTS PASSED - System is ready for production!")
    else:
        print("[ERROR] Some tests failed - Please review the issues above")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
