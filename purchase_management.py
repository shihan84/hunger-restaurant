"""
Purchase Order & Supplier Management System
Handles purchase orders, supplier payments, and accounts payable
"""

import database
from datetime import datetime, timedelta

class PurchaseManagement:
    """Purchase management system for suppliers and orders"""
    
    @staticmethod
    def create_purchase_order(supplier_id, items, expected_date=None, notes=''):
        """
        Create a new purchase order
        Args:
            supplier_id: Supplier ID
            items: List of dict with 'ingredient_id', 'quantity_ordered', 'unit_price'
            expected_date: Expected delivery date (YYYY-MM-DD)
            notes: Optional notes
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            # Generate PO number
            today = datetime.now().strftime('%Y%m%d')
            cursor.execute("SELECT COUNT(*) FROM purchase_orders WHERE po_number LIKE ?", (f'PO-{today}-%',))
            count = cursor.fetchone()[0]
            po_number = f"PO-{today}-{count+1:03d}"
            
            # Calculate total
            total_amount = sum(item['quantity_ordered'] * item['unit_price'] for item in items)
            
            # Insert purchase order
            cursor.execute("""
                INSERT INTO purchase_orders 
                (po_number, supplier_id, order_date, expected_date, status, total_amount, notes)
                VALUES (?, ?, ?, ?, 'pending', ?, ?)
            """, (
                po_number,
                supplier_id,
                datetime.now().strftime('%Y-%m-%d'),
                expected_date,
                total_amount,
                notes
            ))
            
            po_id = cursor.lastrowid
            
            # Insert purchase order items
            for item in items:
                quantity = item['quantity_ordered']
                unit_price = item['unit_price']
                total_price = quantity * unit_price
                
                cursor.execute("""
                    INSERT INTO purchase_order_items 
                    (po_id, ingredient_id, quantity_ordered, quantity_received, unit_price, total_price)
                    VALUES (?, ?, ?, 0, ?, ?)
                """, (po_id, item['ingredient_id'], quantity, unit_price, total_price))
            
            # Create accounts payable entry
            if expected_date:
                due_date = expected_date
            else:
                due_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            
            cursor.execute("""
                INSERT INTO accounts_payable 
                (supplier_id, po_id, amount_due, due_date, status, payment_terms)
                VALUES (?, ?, ?, ?, 'unpaid', 'Net 30')
            """, (supplier_id, po_id, total_amount, due_date))
            
            conn.commit()
            conn.close()
            return True, po_number, po_id
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}", None
    
    @staticmethod
    def receive_purchase_order(po_id, received_items):
        """
        Receive items from purchase order
        Args:
            po_id: Purchase order ID
            received_items: List of dict with 'ingredient_id', 'quantity_received'
        """
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            for item in received_items:
                ingredient_id = item['ingredient_id']
                quantity_received = item['quantity_received']
                
                # Update quantity received
                cursor.execute("""
                    UPDATE purchase_order_items 
                    SET quantity_received = quantity_received + ?
                    WHERE po_id = ? AND ingredient_id = ?
                """, (quantity_received, po_id, ingredient_id))
                
                # Add stock to inventory
                import inventory_manager
                success, message = inventory_manager.InventoryManager.add_stock(
                    ingredient_id,
                    quantity_received,
                    reason=f'PO #{po_id}'
                )
                
                if not success:
                    conn.close()
                    return False, f"Stock update failed: {message}"
            
            # Check if all items received
            cursor.execute("""
                SELECT COUNT(*) FROM purchase_order_items 
                WHERE po_id = ? AND quantity_received < quantity_ordered
            """, (po_id,))
            pending_count = cursor.fetchone()[0]
            
            if pending_count == 0:
                # Mark PO as received
                cursor.execute("""
                    UPDATE purchase_orders SET status = 'received' WHERE id = ?
                """, (po_id,))
            
            conn.commit()
            conn.close()
            return True, "Items received successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_purchase_orders(status=None):
        """Get all purchase orders"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT po.*, s.name as supplier_name
                FROM purchase_orders po
                JOIN suppliers s ON po.supplier_id = s.id
                WHERE po.status = ?
                ORDER BY po.order_date DESC
            """, (status,))
        else:
            cursor.execute("""
                SELECT po.*, s.name as supplier_name
                FROM purchase_orders po
                JOIN suppliers s ON po.supplier_id = s.id
                ORDER BY po.order_date DESC
            """)
        
        orders = cursor.fetchall()
        conn.close()
        return orders
    
    @staticmethod
    def get_purchase_order(po_id):
        """Get single purchase order with items"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get PO details
        cursor.execute("""
            SELECT po.*, s.name as supplier_name, s.contact
            FROM purchase_orders po
            JOIN suppliers s ON po.supplier_id = s.id
            WHERE po.id = ?
        """, (po_id,))
        
        po = cursor.fetchone()
        
        if not po:
            conn.close()
            return None
        
        # Get PO items
        cursor.execute("""
            SELECT poi.*, i.name as ingredient_name, i.unit
            FROM purchase_order_items poi
            JOIN ingredients i ON poi.ingredient_id = i.id
            WHERE poi.po_id = ?
        """, (po_id,))
        
        items = cursor.fetchall()
        conn.close()
        
        return {'po': po, 'items': items}
    
    @staticmethod
    def get_accounts_payable_summary():
        """Get accounts payable summary"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                ap.*,
                s.name as supplier_name,
                s.contact,
                po.po_number
            FROM accounts_payable ap
            JOIN suppliers s ON ap.supplier_id = s.id
            LEFT JOIN purchase_orders po ON ap.po_id = po.id
            ORDER BY ap.due_date ASC
        """)
        
        payable = cursor.fetchall()
        conn.close()
        return payable
    
    @staticmethod
    def get_outstanding_balance():
        """Get total outstanding balance"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(amount_due) as total_balance
            FROM accounts_payable
            WHERE status IN ('unpaid', 'partially_paid')
        """)
        
        result = cursor.fetchone()
        total = result[0] if result[0] else 0
        
        conn.close()
        return total
    
    @staticmethod
    def record_supplier_payment(supplier_id, ap_id, amount_paid, payment_method='cash', reference='', notes=''):
        """Record payment to supplier"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            # Insert payment record
            cursor.execute("""
                INSERT INTO supplier_payments 
                (supplier_id, ap_id, payment_date, amount_paid, payment_method, reference_number, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                supplier_id,
                ap_id,
                datetime.now().strftime('%Y-%m-%d'),
                amount_paid,
                payment_method,
                reference,
                notes
            ))
            
            # Update accounts payable
            cursor.execute("SELECT amount_due FROM accounts_payable WHERE id = ?", (ap_id,))
            ap_record = cursor.fetchone()
            
            if ap_record:
                current_due = ap_record[0]
                new_due = current_due - amount_paid
                
                # Determine status
                if new_due <= 0:
                    status = 'paid'
                elif new_due < current_due:
                    status = 'partially_paid'
                else:
                    status = 'unpaid'
                
                cursor.execute("""
                    UPDATE accounts_payable 
                    SET amount_due = ?, status = ?
                    WHERE id = ?
                """, (max(0, new_due), status, ap_id))
            
            # Record as expense transaction
            cursor.execute("""
                INSERT INTO expenses 
                (date, category, amount, description, payment_method)
                VALUES (?, 'Supplier Payment', ?, ?, ?)
            """, (
                datetime.now().strftime('%Y-%m-%d'),
                amount_paid,
                f'Payment to supplier #{supplier_id}',
                payment_method
            ))
            
            conn.commit()
            conn.close()
            return True, "Payment recorded successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_supplier_history(supplier_id):
        """Get purchase history for a supplier"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT po.*, poi.ingredient_id, poi.quantity_ordered, poi.quantity_received,
                   poi.unit_price, poi.total_price, i.name as ingredient_name
            FROM purchase_orders po
            JOIN purchase_order_items poi ON po.id = poi.po_id
            JOIN ingredients i ON poi.ingredient_id = i.id
            WHERE po.supplier_id = ?
            ORDER BY po.order_date DESC
        """, (supplier_id,))
        
        history = cursor.fetchall()
        conn.close()
        return history
    
    @staticmethod
    def get_supplier_payment_history(supplier_id):
        """Get payment history for a supplier"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM supplier_payments
            WHERE supplier_id = ?
            ORDER BY payment_date DESC
        """, (supplier_id,))
        
        payments = cursor.fetchall()
        conn.close()
        return payments
    
    @staticmethod
    def get_overdue_invoices():
        """Get overdue invoices"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT ap.*, s.name as supplier_name, po.po_number
            FROM accounts_payable ap
            JOIN suppliers s ON ap.supplier_id = s.id
            LEFT JOIN purchase_orders po ON ap.po_id = po.id
            WHERE ap.status IN ('unpaid', 'partially_paid')
            AND ap.due_date < ?
            ORDER BY ap.due_date ASC
        """, (today,))
        
        overdue = cursor.fetchall()
        conn.close()
        return overdue
    
    @staticmethod
    def cancel_purchase_order(po_id):
        """Cancel a purchase order"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE purchase_orders SET status = 'cancelled' WHERE id = ?
            """, (po_id,))
            
            # Update accounts payable
            cursor.execute("""
                UPDATE accounts_payable 
                SET status = 'paid' 
                WHERE po_id = ? AND status IN ('unpaid', 'partially_paid')
            """, (po_id,))
            
            conn.commit()
            conn.close()
            return True, "Purchase order cancelled"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_supplier_balance(supplier_id):
        """Get total amount owed to a supplier"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(amount_due) as balance
            FROM accounts_payable
            WHERE supplier_id = ? AND status IN ('unpaid', 'partially_paid')
        """, (supplier_id,))
        
        result = cursor.fetchone()
        balance = result[0] if result[0] else 0
        
        conn.close()
        return balance
    
    @staticmethod
    def get_purchase_summary(start_date=None, end_date=None):
        """Get purchase summary for date range"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if start_date and end_date:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_orders,
                    SUM(total_amount) as total_spent,
                    COUNT(CASE WHEN status = 'received' THEN 1 END) as received_orders,
                    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_orders
                FROM purchase_orders
                WHERE order_date BETWEEN ? AND ?
            """, (start_date, end_date))
        else:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_orders,
                    SUM(total_amount) as total_spent,
                    COUNT(CASE WHEN status = 'received' THEN 1 END) as received_orders,
                    COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_orders
                FROM purchase_orders
            """)
        
        summary = cursor.fetchone()
        conn.close()
        return summary
