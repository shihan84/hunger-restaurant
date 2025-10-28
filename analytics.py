"""
Analytics & Reporting System
Comprehensive dashboard analytics and business intelligence
"""

import database
from datetime import datetime, timedelta
import calendar

class Analytics:
    """Analytics and reporting system for business intelligence"""
    
    @staticmethod
    def get_today_summary():
        """Get today's business summary"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Total orders today
        cursor.execute("""
            SELECT COUNT(*) FROM orders 
            WHERE DATE(order_date) = ?
        """, (today,))
        total_orders = cursor.fetchone()[0]
        
        # Total revenue today
        cursor.execute("""
            SELECT COALESCE(SUM(final_amount), 0) FROM orders 
            WHERE DATE(order_date) = ?
        """, (today,))
        total_revenue = cursor.fetchone()[0]
        
        # Get revenue by payment method
        cursor.execute("""
            SELECT payment_method, SUM(final_amount) as amount
            FROM orders o
            JOIN transactions t ON o.id = t.order_id
            WHERE DATE(o.order_date) = ?
            GROUP BY payment_method
        """, (today,))
        payment_methods = cursor.fetchall()
        
        payment_breakdown = {}
        for row in payment_methods:
            payment_breakdown[row['payment_method']] = row['amount']
        
        conn.close()
        
        return {
            'date': today,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'payment_methods': payment_breakdown
        }
    
    @staticmethod
    def get_popular_items(date_range='today', limit=10):
        """Get most popular menu items"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if date_range == 'today':
            start_date = datetime.now().strftime('%Y-%m-%d')
            end_date = start_date
        elif date_range == 'week':
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        elif date_range == 'month':
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        else:
            start_date = None
            end_date = None
        
        if start_date:
            cursor.execute("""
                SELECT mi.name, mi.category, SUM(oi.quantity) as total_quantity, 
                       SUM(oi.total) as total_revenue
                FROM order_items oi
                JOIN menu_items mi ON oi.menu_item_id = mi.id
                JOIN orders o ON oi.order_id = o.id
                WHERE DATE(o.order_date) BETWEEN ? AND ?
                GROUP BY mi.id
                ORDER BY total_quantity DESC
                LIMIT ?
            """, (start_date, end_date, limit))
        else:
            cursor.execute("""
                SELECT mi.name, mi.category, SUM(oi.quantity) as total_quantity, 
                       SUM(oi.total) as total_revenue
                FROM order_items oi
                JOIN menu_items mi ON oi.menu_item_id = mi.id
                GROUP BY mi.id
                ORDER BY total_quantity DESC
                LIMIT ?
            """, (limit,))
        
        popular_items = cursor.fetchall()
        conn.close()
        
        return popular_items
    
    @staticmethod
    def get_monthly_revenue_trend(months=6):
        """Get monthly revenue trend"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                strftime('%Y-%m', order_date) as month,
                COUNT(*) as total_orders,
                SUM(final_amount) as revenue,
                SUM(CASE WHEN t.type = 'cash' THEN final_amount ELSE 0 END) as cash_revenue,
                SUM(CASE WHEN t.type = 'card' THEN final_amount ELSE 0 END) as card_revenue,
                SUM(CASE WHEN t.type = 'upi' THEN final_amount ELSE 0 END) as upi_revenue
            FROM orders o
            LEFT JOIN transactions t ON o.id = t.order_id
            WHERE order_date >= date('now', '-' || ? || ' months')
            GROUP BY month
            ORDER BY month ASC
        """, (months,))
        
        trend = cursor.fetchall()
        conn.close()
        
        return trend
    
    @staticmethod
    def get_expense_breakdown(start_date=None, end_date=None):
        """Get expense breakdown by category"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if start_date and end_date:
            cursor.execute("""
                SELECT 
                    category,
                    COUNT(*) as count,
                    SUM(amount) as total_amount
                FROM expenses
                WHERE date BETWEEN ? AND ?
                GROUP BY category
                ORDER BY total_amount DESC
            """, (start_date, end_date))
        else:
            # Default to current month
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute("""
                SELECT 
                    category,
                    COUNT(*) as count,
                    SUM(amount) as total_amount
                FROM expenses
                WHERE date BETWEEN ? AND ?
                GROUP BY category
                ORDER BY total_amount DESC
            """, (start_date, end_date))
        
        breakdown = cursor.fetchall()
        conn.close()
        
        return breakdown
    
    @staticmethod
    def get_profit_margin(start_date=None, end_date=None):
        """Get profit margin analysis"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if not start_date or not end_date:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Get total revenue
        cursor.execute("""
            SELECT COALESCE(SUM(final_amount), 0) FROM orders
            WHERE DATE(order_date) BETWEEN ? AND ?
        """, (start_date, end_date))
        total_revenue = cursor.fetchone()[0]
        
        # Get total expenses
        cursor.execute("""
            SELECT COALESCE(SUM(amount), 0) FROM expenses
            WHERE DATE(date) BETWEEN ? AND ?
        """, (start_date, end_date))
        total_expenses = cursor.fetchone()[0]
        
        # Get COGS (cost of goods sold)
        cursor.execute("""
            SELECT COALESCE(SUM(st.quantity * i.cost_per_unit), 0)
            FROM stock_transactions st
            JOIN ingredients i ON st.ingredient_id = i.id
            WHERE st.transaction_type = 'out'
            AND DATE(st.timestamp) BETWEEN ? AND ?
        """, (start_date, end_date))
        cogs = cursor.fetchone()[0]
        
        # Calculate profit
        gross_profit = total_revenue - cogs
        net_profit = gross_profit - total_expenses
        
        # Calculate margins
        revenue_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        conn.close()
        
        return {
            'total_revenue': total_revenue,
            'cogs': cogs,
            'gross_profit': gross_profit,
            'total_expenses': total_expenses,
            'net_profit': net_profit,
            'profit_margin': revenue_margin
        }
    
    @staticmethod
    def get_tax_summary(period='month'):
        """Get tax summary"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if period == 'month':
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        elif period == 'quarter':
            current_quarter = (datetime.now().month - 1) // 3
            start_date = datetime.now().replace(month=current_quarter*3+1, day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        else:  # year
            start_date = datetime.now().replace(month=1, day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Get GST collected from orders
        cursor.execute("""
            SELECT 
                COALESCE(SUM(gst_amount), 0) as gst_collected,
                COALESCE(SUM(final_amount - gst_amount), 0) as taxable_amount
            FROM orders
            WHERE DATE(order_date) BETWEEN ? AND ? AND gst_enabled = 1
        """, (start_date, end_date))
        
        tax_data = cursor.fetchone()
        conn.close()
        
        return {
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'gst_collected': tax_data['gst_collected'],
            'taxable_amount': tax_data['taxable_amount']
        }
    
    @staticmethod
    def get_low_stock_items(threshold_percentage=20):
        """Get low stock items"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                i.*,
                CASE 
                    WHEN i.min_stock > 0 AND i.current_stock > 0 
                    THEN (i.current_stock / i.min_stock * 100)
                    ELSE 0 
                END as stock_percentage
            FROM ingredients i
            WHERE i.min_stock > 0 
            AND i.current_stock <= (i.min_stock * ?)
            ORDER BY i.current_stock ASC
        """, (threshold_percentage / 100,))
        
        low_stock = cursor.fetchall()
        conn.close()
        
        return low_stock
    
    @staticmethod
    def get_high_cost_ingredients(limit=10):
        """Get highest cost ingredients"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                i.name,
                i.current_stock,
                i.cost_per_unit,
                (i.current_stock * i.cost_per_unit) as total_value
            FROM ingredients i
            ORDER BY total_value DESC
            LIMIT ?
        """, (limit,))
        
        high_cost = cursor.fetchall()
        conn.close()
        
        return high_cost
    
    @staticmethod
    def get_wastage_analysis(start_date=None, end_date=None):
        """Get wastage analysis"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if not start_date or not end_date:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT 
                i.name,
                i.unit,
                SUM(st.quantity) as waste_quantity,
                SUM(st.quantity * i.cost_per_unit) as waste_value
            FROM stock_transactions st
            JOIN ingredients i ON st.ingredient_id = i.id
            WHERE st.transaction_type = 'out'
            AND st.reason LIKE '%waste%'
            AND DATE(st.timestamp) BETWEEN ? AND ?
            GROUP BY i.id
            ORDER BY waste_value DESC
        """, (start_date, end_date))
        
        wastage = cursor.fetchall()
        conn.close()
        
        return wastage
    
    @staticmethod
    def get_staff_orders_performance(start_date=None, end_date=None):
        """Get staff performance by orders handled"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if not start_date or not end_date:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Note: This assumes order_staff_id field exists in orders table
        # If not implemented, returns empty result
        try:
            cursor.execute("""
                SELECT 
                    s.name,
                    s.role,
                    COUNT(o.id) as orders_handled,
                    SUM(o.final_amount) as total_sales
                FROM staff s
                LEFT JOIN orders o ON o.staff_id = s.id
                WHERE o.order_date BETWEEN ? AND ?
                GROUP BY s.id
                ORDER BY orders_handled DESC
            """, (start_date, end_date))
        except:
            # Table doesn't have staff_id column yet
            conn.close()
            return []
        
        performance = cursor.fetchall()
        conn.close()
        
        return performance
    
    @staticmethod
    def get_attendance_summary(start_date=None, end_date=None):
        """Get staff attendance summary"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if not start_date or not end_date:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT 
                s.name,
                s.role,
                COUNT(CASE WHEN a.status = 'present' THEN 1 END) as present_days,
                COUNT(CASE WHEN a.status = 'absent' THEN 1 END) as absent_days,
                COUNT(CASE WHEN a.status = 'late' THEN 1 END) as late_days,
                COUNT(CASE WHEN a.status = 'leave' THEN 1 END) as leave_days,
                SUM(a.total_hours) as total_hours
            FROM staff s
            LEFT JOIN attendance a ON s.id = a.staff_id
            WHERE a.date BETWEEN ? AND ?
            GROUP BY s.id
            ORDER BY present_days DESC
        """, (start_date, end_date))
        
        attendance = cursor.fetchall()
        conn.close()
        
        return attendance
    
    @staticmethod
    def get_category_performance(start_date=None, end_date=None):
        """Get sales performance by category"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if not start_date or not end_date:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT 
                mi.category,
                COUNT(DISTINCT o.id) as order_count,
                SUM(oi.quantity) as total_items,
                SUM(oi.total) as total_revenue
            FROM orders o
            JOIN order_items oi ON o.id = oi.order_id
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            WHERE DATE(o.order_date) BETWEEN ? AND ?
            GROUP BY mi.category
            ORDER BY total_revenue DESC
        """, (start_date, end_date))
        
        category_perf = cursor.fetchall()
        conn.close()
        
        return category_perf
    
    @staticmethod
    def get_hourly_sales_trend(date=None):
        """Get hourly sales trend for a specific date"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT 
                strftime('%H', order_date) as hour,
                COUNT(*) as order_count,
                SUM(final_amount) as revenue
            FROM orders
            WHERE DATE(order_date) = ?
            GROUP BY hour
            ORDER BY hour ASC
        """, (date,))
        
        hourly = cursor.fetchall()
        conn.close()
        
        return hourly
    
    @staticmethod
    def get_table_occupancy(start_date=None, end_date=None):
        """Get table occupancy analysis"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if not start_date or not end_date:
            start_date = datetime.now().strftime('%Y-%m-%d')
            end_date = start_date
        
        # Get unique tables used
        cursor.execute("""
            SELECT 
                table_number,
                COUNT(*) as usage_count,
                AVG(final_amount) as avg_order_value
            FROM orders
            WHERE DATE(order_date) BETWEEN ? AND ?
            AND table_number IS NOT NULL AND table_number != ''
            GROUP BY table_number
            ORDER BY usage_count DESC
        """, (start_date, end_date))
        
        tables = cursor.fetchall()
        
        # Get total orders by table
        cursor.execute("""
            SELECT COUNT(DISTINCT table_number) as unique_tables,
                   COUNT(*) as total_orders
            FROM orders
            WHERE DATE(order_date) BETWEEN ? AND ?
            AND table_number IS NOT NULL AND table_number != ''
        """, (start_date, end_date))
        
        summary = cursor.fetchone()
        conn.close()
        
        return {
            'tables': tables,
            'unique_tables': summary['unique_tables'],
            'total_orders': summary['total_orders']
        }
    
    @staticmethod
    def get_customer_preferences():
        """Get customer preferences analysis"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Most ordered items
        cursor.execute("""
            SELECT 
                mi.name,
                mi.food_type,
                SUM(oi.quantity) as total_orders,
                SUM(oi.total) as total_revenue
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            GROUP BY mi.id
            ORDER BY total_orders DESC
            LIMIT 20
        """)
        
        top_items = cursor.fetchall()
        
        # Veg vs Non-Veg preference
        cursor.execute("""
            SELECT 
                mi.food_type,
                COUNT(*) as order_count,
                SUM(oi.quantity) as total_quantity
            FROM order_items oi
            JOIN menu_items mi ON oi.menu_item_id = mi.id
            GROUP BY mi.food_type
        """)
        
        food_pref = cursor.fetchall()
        
        conn.close()
        
        return {
            'top_items': top_items,
            'food_preference': food_pref
        }
    
    @staticmethod
    def get_inventory_turnover(ingredient_id=None, days=30):
        """Get inventory turnover rate"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        if ingredient_id:
            cursor.execute("""
                SELECT 
                    i.name,
                    i.current_stock,
                    SUM(CASE WHEN st.transaction_type = 'out' THEN st.quantity ELSE 0 END) as total_out,
                    SUM(CASE WHEN st.transaction_type = 'in' THEN st.quantity ELSE 0 END) as total_in
                FROM ingredients i
                LEFT JOIN stock_transactions st ON i.id = st.ingredient_id
                WHERE i.id = ? AND DATE(st.timestamp) >= ?
                GROUP BY i.id
            """, (ingredient_id, start_date))
        else:
            cursor.execute("""
                SELECT 
                    i.name,
                    i.current_stock,
                    SUM(CASE WHEN st.transaction_type = 'out' THEN st.quantity ELSE 0 END) as total_out,
                    SUM(CASE WHEN st.transaction_type = 'in' THEN st.quantity ELSE 0 END) as total_in
                FROM ingredients i
                LEFT JOIN stock_transactions st ON i.id = st.ingredient_id AND DATE(st.timestamp) >= ?
                GROUP BY i.id
                ORDER BY total_out DESC
                LIMIT 20
            """, (start_date,))
        
        turnover = cursor.fetchall()
        conn.close()
        
        return turnover
    
    @staticmethod
    def get_staff_efficiency_report(staff_id=None, start_date=None, end_date=None):
        """Get staff efficiency report"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if not start_date or not end_date:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        if staff_id:
            # Get staff-specific data
            cursor.execute("""
                SELECT 
                    s.name,
                    s.role,
                    COUNT(DISTINCT a.date) as days_worked,
                    SUM(a.total_hours) as total_hours,
                    AVG(a.total_hours) as avg_hours_per_day
                FROM staff s
                LEFT JOIN attendance a ON s.id = a.staff_id
                WHERE s.id = ? AND a.date BETWEEN ? AND ?
            """, (staff_id, start_date, end_date))
        else:
            # Get all staff
            cursor.execute("""
                SELECT 
                    s.name,
                    s.role,
                    COUNT(DISTINCT a.date) as days_worked,
                    SUM(a.total_hours) as total_hours,
                    AVG(a.total_hours) as avg_hours_per_day
                FROM staff s
                LEFT JOIN attendance a ON s.id = a.staff_id
                WHERE a.date BETWEEN ? AND ?
                GROUP BY s.id
                ORDER BY total_hours DESC
            """, (start_date, end_date))
        
        efficiency = cursor.fetchall()
        conn.close()
        
        return efficiency
    
    @staticmethod
    def get_profitability_analysis(start_date=None, end_date=None):
        """Get detailed profitability analysis"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if not start_date or not end_date:
            start_date = datetime.now().replace(day=1).strftime('%Y-%m-%d')
            end_date = datetime.now().strftime('%Y-%m-%d')
        
        # Revenue
        cursor.execute("""
            SELECT COALESCE(SUM(final_amount), 0) FROM orders
            WHERE DATE(order_date) BETWEEN ? AND ?
        """, (start_date, end_date))
        revenue = cursor.fetchone()[0]
        
        # COGS
        cursor.execute("""
            SELECT COALESCE(SUM(st.quantity * i.cost_per_unit), 0)
            FROM stock_transactions st
            JOIN ingredients i ON st.ingredient_id = i.id
            WHERE st.transaction_type = 'out'
            AND st.reason LIKE '%order%'
            AND DATE(st.timestamp) BETWEEN ? AND ?
        """, (start_date, end_date))
        cogs = cursor.fetchone()[0]
        
        # Expenses
        cursor.execute("""
            SELECT category, SUM(amount) as total
            FROM expenses
            WHERE DATE(date) BETWEEN ? AND ?
            GROUP BY category
        """, (start_date, end_date))
        expenses_by_category = cursor.fetchall()
        
        total_expenses = sum(e['total'] for e in expenses_by_category)
        
        # Calculate margins
        gross_profit = revenue - cogs
        net_profit = gross_profit - total_expenses
        
        gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
        net_margin = (net_profit / revenue * 100) if revenue > 0 else 0
        
        conn.close()
        
        return {
            'revenue': revenue,
            'cogs': cogs,
            'gross_profit': gross_profit,
            'gross_margin': gross_margin,
            'expenses_by_category': expenses_by_category,
            'total_expenses': total_expenses,
            'net_profit': net_profit,
            'net_margin': net_margin,
            'start_date': start_date,
            'end_date': end_date
        }
    
    @staticmethod
    def get_dashboard_widgets():
        """Get all dashboard widgets data"""
        return {
            'today_summary': Analytics.get_today_summary(),
            'popular_items': Analytics.get_popular_items('today', 5),
            'monthly_trend': Analytics.get_monthly_revenue_trend(6),
            'expense_breakdown': Analytics.get_expense_breakdown(),
            'profit_margin': Analytics.get_profit_margin(),
            'tax_summary': Analytics.get_tax_summary('month'),
            'low_stock': Analytics.get_low_stock_items(),
            'attendance_summary': Analytics.get_attendance_summary()
        }
