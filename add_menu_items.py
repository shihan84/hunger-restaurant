"""
Add Menu Items to Database
Adds all menu items exactly as specified
"""

import database

def add_menu_items():
    """Add all menu items to database"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Clear existing menu items
    cursor.execute("DELETE FROM menu_items")
    
    # Define all menu items
    menu_items = []
    
    # ===== CHINESE VEGETARIAN =====
    
    # Veg Soup
    menu_items.extend([
        ("Clear Soup", 50, 90, "CHINESE VEGETARIAN", "veg", "single"),
        ("Manchow Soup", 50, 90, "CHINESE VEGETARIAN", "veg", "single"),
        ("Hot & Sour Soup", 50, 90, "CHINESE VEGETARIAN", "veg", "single"),
        ("Lemon Coriander Soup", 60, 120, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg Royal Soup", 60, 120, "CHINESE VEGETARIAN", "veg", "single"),
    ])
    
    # Veg Starter
    menu_items.extend([
        ("Chinese Bhel", 90, 150, "CHINESE VEGETARIAN", "veg", "single"),
        ("Manchurian", 90, 150, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg Chilli", 90, 150, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg Crispy", 90, 150, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg 65", 90, 150, "CHINESE VEGETARIAN", "veg", "single"),
        ("Potato Chilly", 90, 150, "CHINESE VEGETARIAN", "veg", "single"),
        ("Paneer Chilli", 120, 250, "CHINESE VEGETARIAN", "veg", "single"),
        ("Paneer Manchurian", 120, 250, "CHINESE VEGETARIAN", "veg", "single"),
        ("Paneer Schezwan", 120, 250, "CHINESE VEGETARIAN", "veg", "single"),
        ("Paneer 65", 120, 250, "CHINESE VEGETARIAN", "veg", "single"),
    ])
    
    # Veg Noodles
    menu_items.extend([
        ("Hakka Noodles", 80, 140, "CHINESE VEGETARIAN", "veg", "single"),
        ("Schezwan Noodles", 100, 160, "CHINESE VEGETARIAN", "veg", "single"),
        ("Triple Fried Noodles", 110, 190, "CHINESE VEGETARIAN", "veg", "single"),
        ("Chopper Noodles", 110, 190, "CHINESE VEGETARIAN", "veg", "single"),
        ("Paneer Noodles", 120, 210, "CHINESE VEGETARIAN", "veg", "single"),
    ])
    
    # Veg Main Course (Rice)
    menu_items.extend([
        ("Veg Fried Rice", 80, 140, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg Garlic Rice", 90, 150, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg Combo Rice", 90, 160, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg Chopper Rice", 110, 200, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg Manchurian Rice", 110, 190, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg Tripple Schezwan Rice", 110, 190, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg Honkong Fried Rice", 110, 190, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg Singpore Fried Rice", 110, 190, "CHINESE VEGETARIAN", "veg", "single"),
        ("Veg Paneer Fried Rice", 110, 210, "CHINESE VEGETARIAN", "veg", "single"),
    ])
    
    # ===== CHINESE NON-VEGETARIAN =====
    
    # Non-Veg Soup
    menu_items.extend([
        ("Chicken Clear Soup", 70, 140, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Manchow Soup", 70, 140, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Hot & Sour Soup", 70, 140, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Lemon Coriander Soup", 80, 160, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Royal Soup", 80, 160, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Egg Soup", 70, 140, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
    ])
    
    # Non-Veg Starter
    menu_items.extend([
        ("Chicken Lollipop", 80, 190, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Egg Chilli", 70, 150, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Chinese Bhel", 100, 160, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Manchurian", 100, 180, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Chilli", 100, 180, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Garlic", 110, 200, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken 65", 120, 200, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Crispy", 120, 200, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Schezwan", 120, 200, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Prawns Chilli", 90, 210, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Prawns Manchurian", 250, None, "CHINESE NON-VEGETARIAN", "non-veg", "single"),  # Single only
    ])
    
    # Non-Veg Noodles
    menu_items.extend([
        ("Chicken Hakka Noodles", 90, 160, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Schezwan Noodles", 100, 180, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Manchurian Noodles", 110, 210, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Tripple Fried Noodles", 120, 230, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Chopper Noodles", 130, 240, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
        ("Prawns Schezwan Noodles", 140, 270, "CHINESE NON-VEGETARIAN", "non-veg", "single"),
    ])
    
    # ===== INDIAN VEGETARIAN =====
    
    # Delightful Indian Snacks
    menu_items.extend([
        ("Pyaz Ki Kachori (Rajasthani Style)", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Dal Ki Kachori (Rajasthani Style)", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Hing Ki Kachori (Kota Kachori Style)", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Pani Puri", 25, None, "INDIAN VEGETARIAN", "veg", "single"),  # Single only
        ("Aloo Tikki (North Style)", 30, None, "INDIAN VEGETARIAN", "veg", "single"),  # Single only
    ])
    
    # Parathas
    menu_items.extend([
        ("Aloo Ka Paratha", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Paner Ka Paratha", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
    ])
    
    # Delicacies Of South
    menu_items.extend([
        ("Mendu Wada", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Idli", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Plain Dosa", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Masala Dosa", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Mysore Dosa", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Cheese Masala Dosa", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Butter Cheese Masala Dosa", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Tomato Uttapam", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Onion Uttapam", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Poha", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Upma", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Plain Pav Bhaji", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Butter Pav Bhaji", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Cheese Pav Bhaji", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
    ])
    
    # Veg Main Course (Gravy)
    menu_items.extend([
        ("Dal Fry", 100, None, "INDIAN VEGETARIAN", "veg", "single"),  # Single only
        ("Dal Tadka", 120, None, "INDIAN VEGETARIAN", "veg", "single"),  # Single only
        ("Dal Kohlapuri", 120, None, "INDIAN VEGETARIAN", "veg", "single"),  # Single only
        ("Dal Palak", 150, None, "INDIAN VEGETARIAN", "veg", "single"),  # Single only
        ("Mix Veg", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Veg Kadhai", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Veg Kohlapuri", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Bhindi Masala", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Aloo Palak", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Palak Paner", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Matter Paner", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Kadhai Paner", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Paner Tikka Masala", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
    ])
    
    # Rice
    menu_items.extend([
        ("Steam Rice", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Jeera Rice", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Veg Biryani", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Paner Biryani", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Veg Hydrabadi Biryani", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
    ])
    
    # Bread (Roti)
    menu_items.extend([
        ("Tandoori Roti", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Plain Naan", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Garlic Naan", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
        ("Tawa Chapati", 0, None, "INDIAN VEGETARIAN", "veg", "single"),
    ])
    
    # ===== INDIAN NON-VEGETARIAN =====
    
    # Non-Veg Main Course
    menu_items.extend([
        ("Chicken Liver Masala", 100, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Pota Kalegi Fry", 100, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Masala", 150, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Tikka Masala", 170, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Tawa", 170, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Kadhai", 170, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Hydrabadi", 170, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Kohlapuri", 170, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Makhni", 190, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Maharaja", 600, 250, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Note: Price format
        ("Prawns Masala", 0, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),
        ("Prawns Curry", 0, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),
        ("Pomfret Curry / Masala", 0, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),
    ])
    
    # Rice
    menu_items.extend([
        ("Egg Biryani", 130, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Pulao", 170, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Biryani", 180, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Prawns Biryani", 230, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
    ])
    
    # Tandoor Ka Tadka
    menu_items.extend([
        ("Tandoori Chicken", 180, 350, "INDIAN NON-VEGETARIAN", "non-veg", "single"),
        ("Schezwan Tandoori", 190, 430, "INDIAN NON-VEGETARIAN", "non-veg", "single"),
        ("Chicken Tikka (8Pcs)", 230, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Hariyali Kebab (8Pcs)", 250, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Paner Tikka (8Pcs)", 250, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Banjara Kebab (8Pcs)", 290, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
        ("Chicken Chilli Milli Kebab (8Pcs)", 290, None, "INDIAN NON-VEGETARIAN", "non-veg", "single"),  # Single only
    ])
    
    # ===== THALIS =====
    menu_items.extend([
        ("Special Veg Thali", 0, None, "THALIS", "veg", "single"),
        ("Veg Thali", 0, None, "THALIS", "veg", "single"),
        ("Egg Thali", 0, None, "THALIS", "non-veg", "single"),
        ("Fish Thali", 0, None, "THALIS", "non-veg", "single"),
        ("Chicken Thali", 0, None, "THALIS", "non-veg", "single"),
    ])
    
    # Insert all menu items
    for name, price_single, price_full, category, food_type, plate_type in menu_items:
        # If price_single is 0, item is not available
        is_available = 1 if price_single > 0 else 0
        
        cursor.execute("""
            INSERT INTO menu_items 
            (name, price_single, price_full, category, food_type, plate_type, is_available)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, price_single if price_single > 0 else None, price_full, category, food_type, plate_type, is_available))
    
    conn.commit()
    conn.close()
    
    print(f"Successfully added {len(menu_items)} menu items to the database!")

if __name__ == "__main__":
    add_menu_items()
