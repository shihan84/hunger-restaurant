"""
Inventory Management System
Handles ingredients, recipes, stock tracking, and auto-deduction on orders
"""

import sqlite3
import database
from datetime import datetime

class InventoryManager:
    """Inventory management system"""
    
    # Standard units for ingredients
    UNITS = ['kg', 'grams', 'liters', 'pieces', 'packets']
    
    @staticmethod
    def add_ingredient(name, unit='kg', current_stock=0, min_stock=0, cost_per_unit=0):
        """Add a new ingredient"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO ingredients (name, unit, current_stock, min_stock, cost_per_unit)
                VALUES (?, ?, ?, ?, ?)
            """, (name, unit, current_stock, min_stock, cost_per_unit))
            
            conn.commit()
            ingredient_id = cursor.lastrowid
            
            # Record initial stock transaction
            cursor.execute("""
                INSERT INTO stock_transactions 
                (ingredient_id, transaction_type, quantity, reason)
                VALUES (?, ?, ?, ?)
            """, (ingredient_id, 'in', current_stock, 'Initial stock'))
            
            conn.commit()
            conn.close()
            return True, "Ingredient added successfully"
        except sqlite3.IntegrityError:
            conn.close()
            return False, "Ingredient name already exists"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def update_ingredient(ingredient_id, name, unit, min_stock, cost_per_unit):
        """Update ingredient details"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE ingredients 
                SET name = ?, unit = ?, min_stock = ?, cost_per_unit = ?
                WHERE id = ?
            """, (name, unit, min_stock, cost_per_unit, ingredient_id))
            
            conn.commit()
            conn.close()
            return True, "Ingredient updated successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_ingredients():
        """Get all ingredients"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, unit, current_stock, min_stock, cost_per_unit
            FROM ingredients
            ORDER BY name
        """)
        
        ingredients = cursor.fetchall()
        conn.close()
        return ingredients
    
    @staticmethod
    def get_ingredient(ingredient_id):
        """Get single ingredient"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM ingredients WHERE id = ?", (ingredient_id,))
        ingredient = cursor.fetchone()
        conn.close()
        return ingredient
    
    @staticmethod
    def add_stock(ingredient_id, quantity, reason=''):
        """Add stock to ingredient"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            # Update current stock
            cursor.execute("""
                UPDATE ingredients 
                SET current_stock = current_stock + ?
                WHERE id = ?
            """, (quantity, ingredient_id))
            
            # Record transaction
            cursor.execute("""
                INSERT INTO stock_transactions 
                (ingredient_id, transaction_type, quantity, reason)
                VALUES (?, 'in', ?, ?)
            """, (ingredient_id, quantity, reason))
            
            conn.commit()
            conn.close()
            return True, "Stock added successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def remove_stock(ingredient_id, quantity, reason=''):
        """Remove stock from ingredient"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            # Check if sufficient stock
            cursor.execute("SELECT current_stock FROM ingredients WHERE id = ?", (ingredient_id,))
            result = cursor.fetchone()
            
            if not result or result[0] < quantity:
                conn.close()
                return False, "Insufficient stock"
            
            # Update current stock
            cursor.execute("""
                UPDATE ingredients 
                SET current_stock = current_stock - ?
                WHERE id = ?
            """, (quantity, ingredient_id))
            
            # Record transaction
            cursor.execute("""
                INSERT INTO stock_transactions 
                (ingredient_id, transaction_type, quantity, reason)
                VALUES (?, 'out', ?, ?)
            """, (ingredient_id, quantity, reason))
            
            conn.commit()
            conn.close()
            return True, "Stock removed successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_low_stock_items():
        """Get ingredients with low stock"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, name, unit, current_stock, min_stock
            FROM ingredients
            WHERE current_stock <= min_stock
            ORDER BY current_stock ASC
        """)
        
        low_stock = cursor.fetchall()
        conn.close()
        return low_stock
    
    @staticmethod
    def check_stock_availability(ingredient_id, quantity):
        """Check if sufficient stock available"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT current_stock FROM ingredients WHERE id = ?", (ingredient_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0] >= quantity
        return False
    
    @staticmethod
    def deduct_order_stock(order_items):
        """
        Auto-deduct stock when order is placed
        Args:
            order_items: List of dict with 'item_id', 'quantity', 'plate_type'
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        transaction_summary = []
        
        try:
            for item in order_items:
                menu_item_id = item['item_id']
                quantity = item.get('quantity', 1)
                
                # Get recipe for this menu item
                cursor.execute("""
                    SELECT ingredient_id, quantity_required
                    FROM menu_ingredients
                    WHERE menu_item_id = ?
                """, (menu_item_id,))
                
                recipe = cursor.fetchall()
                
                if not recipe:
                    # No recipe defined, skip
                    continue
                
                for ingredient_record in recipe:
                    ingredient_id = ingredient_record[0]
                    quantity_per_item = ingredient_record[1]
                    total_quantity_needed = quantity_per_item * quantity
                    
                    # Check stock availability
                    if not InventoryManager.check_stock_availability(ingredient_id, total_quantity_needed):
                        # Stock insufficient
                        ingredient_name = InventoryManager.get_ingredient(ingredient_id)[1]
                        transaction_summary.append({
                            'ingredient': ingredient_name,
                            'status': 'insufficient',
                            'required': total_quantity_needed
                        })
                        continue
                    
                    # Deduct stock
                    success, message = InventoryManager.remove_stock(
                        ingredient_id, 
                        total_quantity_needed, 
                        reason=f"Order: Menu Item #{menu_item_id}"
                    )
                    
                    if success:
                        ingredient_name = InventoryManager.get_ingredient(ingredient_id)[1]
                        transaction_summary.append({
                            'ingredient': ingredient_name,
                            'status': 'deducted',
                            'quantity': total_quantity_needed
                        })
            
            conn.close()
            return True, transaction_summary
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def set_recipe(menu_item_id, ingredients_data):
        """
        Set recipe for a menu item
        Args:
            menu_item_id: Menu item ID
            ingredients_data: List of dict with 'ingredient_id', 'quantity_required'
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            # Delete existing recipe
            cursor.execute("DELETE FROM menu_ingredients WHERE menu_item_id = ?", (menu_item_id,))
            
            # Insert new recipe
            for ingredient in ingredients_data:
                cursor.execute("""
                    INSERT INTO menu_ingredients (menu_item_id, ingredient_id, quantity_required)
                    VALUES (?, ?, ?)
                """, (menu_item_id, ingredient['ingredient_id'], ingredient['quantity_required']))
            
            conn.commit()
            conn.close()
            return True, "Recipe saved successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_recipe(menu_item_id):
        """Get recipe for a menu item"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT mi.ingredient_id, i.name, i.unit, mi.quantity_required
            FROM menu_ingredients mi
            JOIN ingredients i ON mi.ingredient_id = i.id
            WHERE mi.menu_item_id = ?
        """, (menu_item_id,))
        
        recipe = cursor.fetchall()
        conn.close()
        return recipe
    
    @staticmethod
    def get_transaction_history(ingredient_id=None, limit=50):
        """Get stock transaction history"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if ingredient_id:
            cursor.execute("""
                SELECT st.*, i.name as ingredient_name
                FROM stock_transactions st
                JOIN ingredients i ON st.ingredient_id = i.id
                WHERE st.ingredient_id = ?
                ORDER BY st.timestamp DESC
                LIMIT ?
            """, (ingredient_id, limit))
        else:
            cursor.execute("""
                SELECT st.*, i.name as ingredient_name
                FROM stock_transactions st
                JOIN ingredients i ON st.ingredient_id = i.id
                ORDER BY st.timestamp DESC
                LIMIT ?
            """, (limit,))
        
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    
    @staticmethod
    def add_supplier(name, contact='', address=''):
        """Add a new supplier"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO suppliers (name, contact, address)
                VALUES (?, ?, ?)
            """, (name, contact, address))
            
            conn.commit()
            conn.close()
            return True, "Supplier added successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_suppliers():
        """Get all suppliers"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM suppliers ORDER BY name")
        suppliers = cursor.fetchall()
        conn.close()
        return suppliers
