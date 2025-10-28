"""
Accounting System for Restaurant Billing
Handles sales reports, expenses, profit & loss, balance sheet, and tax management
"""

import database
from datetime import datetime, timedelta

class AccountingSystem:
    """Accounting system for financial management"""
    
    @staticmethod
    def get_daily_sales_report(date=None):
        """Get daily sales report"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get orders for the day
        cursor.execute("""
            SELECT o.id, o.total_amount, o.gst_amount, o.final_amount, o.service_charge,
                   oi.menu_item_id, oi.quantity, oi.price as item_price,
                   mi.name as item_name
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.order_id
            LEFT JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE DATE(o.order_date) = ?
            AND o.status = 'completed'
        """, (date,))
        
        orders_data = cursor.fetchall()
        conn.close()
        
        # Process data
        total_sales = 0
        total_gst = 0
        total_service_charge = 0
        total_final = 0
        items_sold = {}
        
        for order in orders_data:
            order_id, total, gst, final, service, menu_id, qty, item_price, item_name = order
            
            if order_id not in [o[0] for o in orders_data if o[0] == order_id]:
                # Count each order once
                total_sales += total or 0
                total_gst += gst or 0
                total_service_charge += service or 0
                total_final += final or 0
            
            if item_name:
                if item_name not in items_sold:
                    items_sold[item_name] = {'quantity': 0, 'revenue': 0}
                items_sold[item_name]['quantity'] += qty or 0
                items_sold[item_name]['revenue'] += (item_price or 0) * (qty or 0)
        
        return {
            'date': date,
            'total_sales': total_sales,
            'total_gst': total_gst,
            'total_service_charge': total_service_charge,
            'total_revenue': total_final,
            'items_sold': items_sold,
            'order_count': len(set([o[0] for o in orders_data]))
        }
    
    @staticmethod
    def get_payment_method_breakdown(start_date=None, end_date=None):
        """Get payment method breakdown"""
        if start_date is None:
            start_date = datetime.now().strftime('%Y-%m-%d')
        if end_date is None:
            end_date = start_date
        
        # Note: Payment method is not stored in orders table currently
        # This is a placeholder for future implementation
        return {
            'cash': 0,
            'card': 0,
            'upi': 0,
            'total': 0
        }
    
    @staticmethod
    def add_expense(date, category, amount, description='', payment_method='cash'):
        """Add an expense"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO expenses (date, category, amount, description, payment_method)
                VALUES (?, ?, ?, ?, ?)
            """, (date, category, amount, description, payment_method))
            
            conn.commit()
            conn.close()
            return True, "Expense added successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_expenses(start_date=None, end_date=None):
        """Get expenses within date range"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if start_date and end_date:
            cursor.execute("""
                SELECT * FROM expenses
                WHERE date BETWEEN ? AND ?
                ORDER BY date DESC
            """, (start_date, end_date))
        else:
            cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
        
        expenses = cursor.fetchall()
        conn.close()
        return expenses
    
    @staticmethod
    def get_expense_summary(start_date=None, end_date=None):
        """Get expense summary by category"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if start_date and end_date:
            cursor.execute("""
                SELECT category, SUM(amount) as total
                FROM expenses
                WHERE date BETWEEN ? AND ?
                GROUP BY category
                ORDER BY total DESC
            """, (start_date, end_date))
        else:
            cursor.execute("""
                SELECT category, SUM(amount) as total
                FROM expenses
                GROUP BY category
                ORDER BY total DESC
            """)
        
        summary = cursor.fetchall()
        conn.close()
        return summary
    
    @staticmethod
    def get_profit_loss(start_date=None, end_date=None):
        """Calculate Profit & Loss statement"""
        if start_date is None:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Get revenue from orders
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(final_amount) as revenue
            FROM orders
            WHERE DATE(order_date) BETWEEN ? AND ?
            AND status = 'completed'
        """, (start_date, end_date))
        
        revenue_result = cursor.fetchone()
        revenue = revenue_result[0] if revenue_result[0] else 0
        
        # Get expenses
        cursor.execute("""
            SELECT SUM(amount) as expenses
            FROM expenses
            WHERE date BETWEEN ? AND ?
        """, (start_date, end_date))
        
        expenses_result = cursor.fetchone()
        expenses = expenses_result[0] if expenses_result[0] else 0
        
        # Get ingredient costs (COGS)
        cursor.execute("""
            SELECT SUM(oi.quantity * mi.cost_per_unit) as cogs
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            JOIN menu_ingredients ming ON oi.menu_item_id = ming.menu_item_id
            JOIN ingredients ing ON ming.ingredient_id = ing.id
            WHERE DATE(o.order_date) BETWEEN ? AND ?
            AND o.status = 'completed'
        """, (start_date, end_date))
        
        cogs_result = cursor.fetchone()
        cogs = cogs_result[0] if cogs_result[0] else 0
        
        conn.close()
        
        # Calculate metrics
        gross_profit = revenue - cogs
        net_profit = gross_profit - expenses
        
        return {
            'period': f"{start_date} to {end_date}",
            'revenue': revenue,
            'cost_of_goods_sold': cogs,
            'gross_profit': gross_profit,
            'expenses': expenses,
            'net_profit': net_profit
        }
    
    @staticmethod
    def get_inventory_valuation():
        """Calculate current inventory valuation"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(current_stock * cost_per_unit) as valuation
            FROM ingredients
        """)
        
        result = cursor.fetchone()
        valuation = result[0] if result[0] else 0
        
        conn.close()
        return valuation
    
    @staticmethod
    def get_balance_sheet():
        """Get balance sheet"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get accounts balance
        cursor.execute("SELECT SUM(balance) as total FROM accounts")
        cash_bank = cursor.fetchone()[0] or 0
        
        # Get inventory valuation
        inventory_value = AccountingSystem.get_inventory_valuation()
        
        # Calculate total assets
        total_assets = cash_bank + inventory_value
        
        # Get total expenses as liabilities estimate
        cursor.execute("SELECT SUM(amount) FROM expenses")
        total_expenses = cursor.fetchone()[0] or 0
        
        # Get total revenue
        cursor.execute("SELECT SUM(final_amount) FROM orders WHERE status = 'completed'")
        total_revenue = cursor.fetchone()[0] or 0
        
        # Calculate equity
        equity = total_revenue - total_expenses
        
        conn.close()
        
        return {
            'assets': {
                'cash_bank': cash_bank,
                'inventory': inventory_value,
                'total_assets': total_assets
            },
            'liabilities': {
                'expenses': total_expenses,
                'total_liabilities': total_expenses
            },
            'equity': equity
        }
    
    @staticmethod
    def get_tax_summary(start_date=None, end_date=None):
        """Get tax summary"""
        if start_date is None:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT SUM(gst_amount) as gst_collected
            FROM orders
            WHERE DATE(order_date) BETWEEN ? AND ?
            AND status = 'completed'
        """, (start_date, end_date))
        
        result = cursor.fetchone()
        gst_collected = result[0] if result[0] else 0
        
        conn.close()
        
        return {
            'period': f"{start_date} to {end_date}",
            'gst_collected': gst_collected,
            'gst_paid': 0,  # Would need supplier invoices for this
            'net_gst': gst_collected
        }
    
    @staticmethod
    def record_order_transaction(order_id, amount, payment_method='cash'):
        """Record order transaction in accounting"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            # Determine account based on payment method
            if payment_method.lower() == 'cash':
                account_id = 1  # Default cash account
            else:
                # For card/UPI, use cash account for now
                # In production, you'd have separate bank accounts
                account_id = 1
            
            # Record credit (money coming in)
            cursor.execute("""
                INSERT INTO transactions (date, account_id, type, amount, description, order_id)
                VALUES (?, ?, 'credit', ?, ?, ?)
            """, (datetime.now().strftime('%Y-%m-%d'), account_id, amount, f'Order #{order_id}', order_id))
            
            # Update account balance
            cursor.execute("""
                UPDATE accounts SET balance = balance + ? WHERE id = ?
            """, (amount, account_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            conn.close()
            print(f"Error recording transaction: {e}")
            return False
    
    @staticmethod
    def get_sales_report(start_date=None, end_date=None):
        """Comprehensive sales report"""
        if start_date is None:
            start_date = datetime.now().strftime('%Y-%m-%d')
        if end_date is None:
            end_date = start_date
        
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                o.id as order_id,
                o.order_date,
                o.table_number,
                o.total_amount,
                o.gst_amount,
                o.service_charge,
                o.final_amount,
                COUNT(DISTINCT oi.id) as item_count
            FROM orders o
            LEFT JOIN order_items oi ON o.id = oi.order_id
            WHERE DATE(o.order_date) BETWEEN ? AND ?
            AND o.status = 'completed'
            GROUP BY o.id
            ORDER BY o.order_date DESC
        """, (start_date, end_date))
        
        orders = cursor.fetchall()
        
        # Calculate totals
        cursor.execute("""
            SELECT 
                COUNT(*) as order_count,
                SUM(total_amount) as total_sales,
                SUM(gst_amount) as total_gst,
                SUM(service_charge) as total_service,
                SUM(final_amount) as total_revenue
            FROM orders
            WHERE DATE(order_date) BETWEEN ? AND ?
            AND status = 'completed'
        """, (start_date, end_date))
        
        totals = cursor.fetchone()
        conn.close()
        
        return {
            'period': f"{start_date} to {end_date}",
            'orders': orders,
            'summary': {
                'total_orders': totals[0] or 0,
                'total_sales': totals[1] or 0,
                'total_gst': totals[2] or 0,
                'total_service_charge': totals[3] or 0,
                'total_revenue': totals[4] or 0
            }
        }
    
    @staticmethod
    def get_account_summary():
        """Get summary of all accounts"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, type, balance FROM accounts ORDER BY type, name")
        accounts = cursor.fetchall()
        conn.close()
        
        return accounts
    
    @staticmethod
    def get_recent_transactions(limit=50):
        """Get recent transactions"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT t.*, a.name as account_name
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            ORDER BY t.date DESC, t.id DESC
            LIMIT ?
        """, (limit,))
        
        transactions = cursor.fetchall()
        conn.close()
        
        return transactions
