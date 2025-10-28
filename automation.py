"""
Automation & Alerts System
Handles automatic purchase orders, financial alerts, and performance alerts
"""

import database
from datetime import datetime, timedelta
import json

class Automation:
    """Automation and alerts system"""
    
    @staticmethod
    def check_stock_levels():
        """Check all stock levels and return low stock items"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get ingredients below minimum stock
        cursor.execute("""
            SELECT id, name, current_stock, min_stock, unit
            FROM ingredients
            WHERE current_stock <= min_stock AND min_stock > 0
        """)
        
        low_stock_items = cursor.fetchall()
        conn.close()
        
        return low_stock_items
    
    @staticmethod
    def auto_generate_purchase_order(ingredient_id, supplier_id=None, quantity=None):
        """Automatically generate purchase order for low stock item"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get ingredient details
        cursor.execute("SELECT name, min_stock, unit FROM ingredients WHERE id = ?", (ingredient_id,))
        ingredient = cursor.fetchone()
        
        if not ingredient:
            conn.close()
            return False, "Ingredient not found"
        
        ingredient_name, min_stock, unit = ingredient
        
        # Determine supplier if not provided
        if not supplier_id:
            # Get supplier who last supplied this ingredient (from purchase orders)
            cursor.execute("""
                SELECT po.supplier_id, COUNT(*) as order_count
                FROM purchase_orders po
                JOIN purchase_order_items poi ON po.id = poi.po_id
                WHERE poi.ingredient_id = ?
                GROUP BY po.supplier_id
                ORDER BY order_count DESC
                LIMIT 1
            """, (ingredient_id,))
            
            supplier_data = cursor.fetchone()
            if supplier_data:
                supplier_id = supplier_data['supplier_id']
            else:
                # Use first available supplier
                cursor.execute("SELECT id FROM suppliers LIMIT 1")
                supplier_data = cursor.fetchone()
                if not supplier_data:
                    conn.close()
                    return False, "No suppliers available"
                supplier_id = supplier_data['id']
        
        # Determine quantity if not provided (order 2x minimum stock)
        if not quantity:
            quantity = min_stock * 2
        
        # Get average price from last purchase
        cursor.execute("""
            SELECT AVG(unit_price) as avg_price
            FROM purchase_order_items
            WHERE ingredient_id = ?
        """, (ingredient_id,))
        
        price_data = cursor.fetchone()
        estimated_price = price_data['avg_price'] if price_data['avg_price'] else 0
        
        # Generate PO number
        po_number = f"PO-{datetime.now().strftime('%Y%m%d')}-{ingredient_id}"
        
        # Create purchase order
        cursor.execute("""
            INSERT INTO purchase_orders 
            (po_number, supplier_id, order_date, expected_date, status, notes)
            VALUES (?, ?, ?, ?, 'pending', ?)
        """, (
            po_number,
            supplier_id,
            datetime.now().strftime('%Y-%m-%d'),
            (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            f"Auto-generated for low stock: {ingredient_name}"
        ))
        
        po_id = cursor.lastrowid
        
        # Add item to PO
        cursor.execute("""
            INSERT INTO purchase_order_items
            (po_id, ingredient_id, quantity_ordered, unit_price, total_price)
            VALUES (?, ?, ?, ?, ?)
        """, (po_id, ingredient_id, quantity, estimated_price, quantity * estimated_price))
        
        conn.commit()
        conn.close()
        
        return True, f"Purchase order created: {po_number}"
    
    @staticmethod
    def check_all_low_stock_and_create_pos():
        """Check all low stock items and create purchase orders"""
        low_stock_items = Automation.check_stock_levels()
        
        created_pos = []
        for item in low_stock_items:
            success, message = Automation.auto_generate_purchase_order(item['id'])
            if success:
                created_pos.append({
                    'ingredient': item['name'],
                    'message': message
                })
        
        return created_pos
    
    @staticmethod
    def compare_supplier_prices(ingredient_id):
        """Compare prices from different suppliers for an ingredient"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                s.name as supplier_name,
                AVG(poi.unit_price) as avg_price,
                MIN(poi.unit_price) as min_price,
                MAX(poi.unit_price) as max_price,
                COUNT(*) as order_count
            FROM purchase_order_items poi
            JOIN purchase_orders po ON poi.po_id = po.id
            JOIN suppliers s ON po.supplier_id = s.id
            WHERE poi.ingredient_id = ?
            GROUP BY s.id
            ORDER BY avg_price ASC
        """, (ingredient_id,))
        
        prices = cursor.fetchall()
        conn.close()
        
        return prices


class FinancialAlerts:
    """Financial alerts and notifications"""
    
    @staticmethod
    def check_cash_balance():
        """Check cash account balance and alert if low"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get cash account balance
        cursor.execute("SELECT balance FROM accounts WHERE type = 'cash' LIMIT 1")
        cash_data = cursor.fetchone()
        
        conn.close()
        
        if not cash_data:
            return None, "No cash account found"
        
        balance = cash_data['balance']
        
        # Low balance threshold: 10000
        if balance < 10000:
            return True, f"Low cash balance: INR {balance:.2f}"
        
        return False, None
    
    @staticmethod
    def check_high_expenses(days=7, threshold=50000):
        """Check for high expenses in recent period"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT SUM(amount) as total_expenses
            FROM expenses
            WHERE DATE(date) >= ?
        """, (start_date,))
        
        data = cursor.fetchone()
        total_expenses = data['total_expenses'] if data['total_expenses'] else 0
        
        conn.close()
        
        if total_expenses > threshold:
            return True, f"High expenses in last {days} days: INR {total_expenses:.2f}"
        
        return False, None
    
    @staticmethod
    def check_tax_payment_due():
        """Check if tax payment is due soon"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get GST settings
        cursor.execute("SELECT gst_enabled FROM restaurant_settings WHERE id = 1")
        gst_data = cursor.fetchone()
        
        if not gst_data or not gst_data['gst_enabled']:
            conn.close()
            return False, "GST not enabled"
        
        # Check for tax records in current month
        current_month = datetime.now().strftime('%Y-%m')
        
        cursor.execute("""
            SELECT SUM(gst_collected) as gst_collected
            FROM tax_records
            WHERE period LIKE ?
        """, (f"{current_month}%",))
        
        data = cursor.fetchone()
        gst_collected = data['gst_collected'] if data['gst_collected'] else 0
        
        conn.close()
        
        # Alert if significant GST collected and no record for this month
        if gst_collected == 0:
            # Check if we're near month end (last 3 days)
            days_left_in_month = 30 - datetime.now().day
            if days_left_in_month <= 3:
                return True, f"Tax payment due soon. Month ends in {days_left_in_month} days."
        
        return False, None
    
    @staticmethod
    def get_all_financial_alerts():
        """Get all financial alerts"""
        alerts = []
        
        # Check cash balance
        is_low, message = FinancialAlerts.check_cash_balance()
        if is_low:
            alerts.append({'type': 'low_cash', 'message': message, 'priority': 'high'})
        
        # Check high expenses
        is_high, message = FinancialAlerts.check_high_expenses()
        if is_high:
            alerts.append({'type': 'high_expenses', 'message': message, 'priority': 'medium'})
        
        # Check tax payment
        is_due, message = FinancialAlerts.check_tax_payment_due()
        if is_due:
            alerts.append({'type': 'tax_due', 'message': message, 'priority': 'high'})
        
        return alerts


class PerformanceAlerts:
    """Performance alerts and notifications"""
    
    @staticmethod
    def check_sales_target(target_amount=50000, days=1):
        """Check if sales target is met"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT COALESCE(SUM(final_amount), 0) as total_sales
            FROM orders
            WHERE DATE(order_date) >= ?
        """, (start_date,))
        
        data = cursor.fetchone()
        total_sales = data['total_sales'] if data['total_sales'] else 0
        
        conn.close()
        
        if total_sales < target_amount:
            remaining = target_amount - total_sales
            return False, f"Sales target not met. Need INR {remaining:.2f} more"
        
        return True, f"Sales target met: INR {total_sales:.2f}"
    
    @staticmethod
    def check_staff_attendance_issues():
        """Check for staff attendance issues"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Check for frequent absences
        current_month = datetime.now().replace(day=1).strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT 
                s.name,
                s.role,
                COUNT(CASE WHEN a.status = 'absent' THEN 1 END) as absent_count,
                COUNT(CASE WHEN a.status = 'late' THEN 1 END) as late_count
            FROM staff s
            LEFT JOIN attendance a ON s.id = a.staff_id
            WHERE s.status = 'active' AND a.date >= ?
            GROUP BY s.id
            HAVING absent_count > 3 OR late_count > 5
        """, (current_month,))
        
        issues = cursor.fetchall()
        conn.close()
        
        if issues:
            alerts = []
            for issue in issues:
                message = f"{issue['name']} ({issue['role']}): {issue['absent_count']} absences, {issue['late_count']} late days"
                alerts.append({
                    'type': 'attendance_issue',
                    'message': message,
                    'priority': 'medium',
                    'staff_name': issue['name']
                })
            return alerts
        
        return []
    
    @staticmethod
    def check_inventory_discrepancies():
        """Check for inventory discrepancies"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Check for ingredients with inconsistent stock
        # (current_stock that doesn't match expected based on transactions)
        
        cursor.execute("""
            SELECT 
                i.id,
                i.name,
                i.current_stock,
                COALESCE(
                    (SELECT SUM(CASE WHEN st.transaction_type = 'in' THEN st.quantity ELSE -st.quantity END)
                     FROM stock_transactions st
                     WHERE st.ingredient_id = i.id),
                    0
                ) as calculated_stock
            FROM ingredients i
            WHERE ABS(i.current_stock - COALESCE(
                (SELECT SUM(CASE WHEN st.transaction_type = 'in' THEN st.quantity ELSE -st.quantity END)
                 FROM stock_transactions st
                 WHERE st.ingredient_id = i.id),
                0
            )) > 1
        """)
        
        discrepancies = cursor.fetchall()
        conn.close()
        
        alerts = []
        for discrepancy in discrepancies:
            diff = discrepancy['current_stock'] - discrepancy['calculated_stock']
            message = f"{discrepancy['name']}: Stock discrepancy of {diff:.2f}"
            alerts.append({
                'type': 'inventory_discrepancy',
                'message': message,
                'priority': 'high',
                'ingredient': discrepancy['name']
            })
        
        return alerts
    
    @staticmethod
    def check_slow_moving_items(days=30):
        """Check for slow moving menu items"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        # Get all menu items
        cursor.execute("SELECT id, name FROM menu_items")
        all_items = cursor.fetchall()
        
        # Get items with no orders in the period
        cursor.execute("""
            SELECT DISTINCT mi.id
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE DATE(o.order_date) >= ?
        """, (start_date,))
        
        ordered_items = {row['id'] for row in cursor.fetchall()}
        
        slow_moving = []
        for item in all_items:
            if item['id'] not in ordered_items:
                slow_moving.append(item['name'])
        
        conn.close()
        
        if slow_moving:
            return True, f"Slow moving items (no orders in {days} days): {', '.join(slow_moving[:5])}"
        
        return False, None
    
    @staticmethod
    def get_all_performance_alerts():
        """Get all performance alerts"""
        alerts = []
        
        # Check sales target
        target_met, message = PerformanceAlerts.check_sales_target()
        if not target_met:
            alerts.append({'type': 'sales_target', 'message': message, 'priority': 'low'})
        
        # Check attendance
        attendance_alerts = PerformanceAlerts.check_staff_attendance_issues()
        alerts.extend(attendance_alerts)
        
        # Check inventory discrepancies
        inventory_alerts = PerformanceAlerts.check_inventory_discrepancies()
        alerts.extend(inventory_alerts)
        
        # Check slow moving items
        is_slow, message = PerformanceAlerts.check_slow_moving_items()
        if is_slow:
            alerts.append({'type': 'slow_moving', 'message': message, 'priority': 'low'})
        
        return alerts


class AutomationManager:
    """Main automation manager"""
    
    @staticmethod
    def run_daily_automation():
        """Run all daily automation tasks"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'tasks': []
        }
        
        # Auto-generate purchase orders for low stock
        created_pos = Automation.check_all_low_stock_and_create_pos()
        if created_pos:
            results['tasks'].append({
                'task': 'auto_purchase_orders',
                'status': 'completed',
                'count': len(created_pos),
                'details': created_pos
            })
        
        # Get all alerts
        financial_alerts = FinancialAlerts.get_all_financial_alerts()
        performance_alerts = PerformanceAlerts.get_all_performance_alerts()
        
        if financial_alerts or performance_alerts:
            results['tasks'].append({
                'task': 'alerts_generated',
                'status': 'completed',
                'financial_alerts': len(financial_alerts),
                'performance_alerts': len(performance_alerts)
            })
        
        results['alerts'] = {
            'financial': financial_alerts,
            'performance': performance_alerts
        }
        
        return results
    
    @staticmethod
    def get_supplier_recommendation(ingredient_id):
        """Get best supplier recommendation for an ingredient"""
        prices = Automation.compare_supplier_prices(ingredient_id)
        
        if not prices:
            return None, "No purchase history for this ingredient"
        
        # Best supplier is the one with lowest average price
        best_supplier = prices[0] if prices else None
        
        if best_supplier:
            return True, {
                'supplier_name': best_supplier['supplier_name'],
                'avg_price': best_supplier['avg_price'],
                'order_count': best_supplier['order_count']
            }
        
        return False, "No supplier data available"
    
    @staticmethod
    def get_all_alerts_summary():
        """Get summary of all alerts"""
        financial = FinancialAlerts.get_all_financial_alerts()
        performance = PerformanceAlerts.get_all_performance_alerts()
        
        return {
            'financial_alerts_count': len(financial),
            'performance_alerts_count': len(performance),
            'total_alerts': len(financial) + len(performance),
            'alerts_by_priority': {
                'high': len([a for a in financial + performance if a.get('priority') == 'high']),
                'medium': len([a for a in financial + performance if a.get('priority') == 'medium']),
                'low': len([a for a in financial + performance if a.get('priority') == 'low'])
            },
            'timestamp': datetime.now().isoformat()
        }
