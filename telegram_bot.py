"""
Telegram Bot Commands
Handles bot commands for bill management and sales reports
"""

import requests
import database
from datetime import datetime, timedelta
import json
import time
import threading

def get_telegram_settings():
    """Get Telegram settings from database"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT bot_token, chat_id, enabled FROM telegram_settings WHERE id = 1")
    settings = cursor.fetchone()
    
    conn.close()
    
    if settings:
        return {
            'bot_token': settings[0],
            'chat_id': settings[1],
            'enabled': settings[2] == 1
        }
    return None

def send_telegram_message(chat_id, message, reply_markup=None):
    """Send message to Telegram"""
    settings = get_telegram_settings()
    
    if not settings or not settings['enabled']:
        return False
    
    bot_token = settings['bot_token']
    
    if not bot_token:
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    if reply_markup:
        payload['reply_markup'] = reply_markup
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code != 200:
            print(f"Telegram API error: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram message failed: {e}")
        return False

def get_daily_sales(date=None):
    """Get daily sales report"""
    if not date:
        date = datetime.now().date()
    
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Get orders for the date
    cursor.execute("""
        SELECT id, table_number, order_date, final_amount 
        FROM orders 
        WHERE DATE(order_date) = ? AND status = 'completed'
        ORDER BY order_date DESC
    """, (date,))
    
    orders = cursor.fetchall()
    
    # Calculate totals
    total_sales = sum(order[3] for order in orders)
    total_orders = len(orders)
    
    conn.close()
    
    return {
        'date': date,
        'total_orders': total_orders,
        'total_sales': total_sales,
        'orders': orders
    }

def get_total_sales_message(days=30):
    """Get total sales message for specified days"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
    
    # Get total sales
    cursor.execute("""
        SELECT COUNT(*), SUM(final_amount) 
        FROM orders 
        WHERE order_date >= ? AND status = 'completed'
    """, (cutoff_date,))
    
    result = cursor.fetchone()
    total_orders = result[0] or 0
    total_sales = result[1] or 0
    
    # Get today's sales
    today = datetime.now().date()
    cursor.execute("""
        SELECT COUNT(*), SUM(final_amount) 
        FROM orders 
        WHERE DATE(order_date) = ? AND status = 'completed'
    """, (today,))
    
    result = cursor.fetchone()
    today_orders = result[0] or 0
    today_sales = result[1] or 0
    
    conn.close()
    
    message = f"*Sales Report ({days} Days)*\n\n"
    message += f"*Today:*\n"
    message += f"   Orders: {today_orders}\n"
    message += f"   Sales: INR {today_sales:.2f}\n\n"
    message += f"*Last {days} Days:*\n"
    message += f"   Total Orders: {total_orders}\n"
    message += f"   Total Sales: INR {total_sales:.2f}\n"
    
    return message

def get_bills_list(date=None, limit=10):
    """Get list of bills"""
    if not date:
        date = datetime.now().date()
    
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, table_number, order_date, final_amount 
        FROM orders 
        WHERE DATE(order_date) = ? AND status = 'completed'
        ORDER BY order_date DESC
        LIMIT ?
    """, (date, limit))
    
    orders = cursor.fetchall()
    conn.close()
    
    return orders

def get_bill_details(order_id):
    """Get detailed bill information"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Get order details
    cursor.execute("""
        SELECT id, table_number, order_date, total_amount, 
               service_charge, gst_amount, discount, final_amount, status
        FROM orders 
        WHERE id = ?
    """, (order_id,))
    
    order = cursor.fetchone()
    
    if not order:
        conn.close()
        return None
    
    # Get order items
    cursor.execute("""
        SELECT oi.quantity, mi.name, oi.price, oi.total
        FROM order_items oi
        JOIN menu_items mi ON oi.menu_item_id = mi.id
        WHERE oi.order_id = ?
    """, (order_id,))
    
    items = cursor.fetchall()
    conn.close()
    
    return {
        'order': order,
        'items': items
    }

def format_bill_message(bill_data):
    """Format bill details as message"""
    order = bill_data['order']
    items = bill_data['items']
    
    order_id, table_number, order_date, total_amount, service_charge, gst_amount, discount, final_amount, status = order
    
    message = f"*Bill #{order_id:03d}*\n\n"
    message += f"Date: {order_date}\n"
    message += f"Table: {table_number or 'Takeaway'}\n\n"
    message += "*Items:*\n"
    
    for item in items:
        quantity, name, price, item_total = item
        message += f"• {quantity}x {name}\n"
        message += f"  INR {item_total:.2f}\n"
    
    message += f"\n*Subtotal:* INR {total_amount:.2f}\n"
    if service_charge > 0:
        message += f"*Service Charge:* INR {service_charge:.2f}\n"
    if gst_amount > 0:
        message += f"*GST (5%):* INR {gst_amount:.2f}\n"
    if discount > 0:
        message += f"*Discount:* INR {discount:.2f}\n"
    message += f"*TOTAL:* INR {final_amount:.2f}\n"
    
    return message

def format_bills_list_message(orders):
    """Format bills list as message"""
    if not orders:
        return "No bills found for today."
    
    message = f"Bills ({datetime.now().strftime('%d/%m/%Y')})\n\n"
    
    for order in orders:
        order_id, table_number, order_date, final_amount = order
        table_display = table_number or 'Takeaway'
        message += f"Bill #{order_id:03d} | Table: {table_display} | Rs {final_amount:.2f}\n"
        message += f"Date: {order_date}\n\n"
    
    message += f"Total Bills: {len(orders)}"
    
    return message

def get_menu_summary():
    """Get menu summary"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Get menu item counts by category
    cursor.execute("""
        SELECT category, COUNT(*) 
        FROM menu_items 
        GROUP BY category
    """)
    
    categories = cursor.fetchall()
    
    # Get total items
    cursor.execute("SELECT COUNT(*) FROM menu_items")
    total_items = cursor.fetchone()[0]
    
    conn.close()
    
    message = f"*Menu Summary*\n\n"
    message += f"Total Items: {total_items}\n\n"
    message += "*By Category:*\n"
    
    for category, count in categories:
        message += f"• {category}: {count} items\n"
    
    return message

def test_bot_commands():
    """Test all bot commands"""
    print("=" * 60)
    print("Testing Telegram Bot Commands")
    print("=" * 60)
    
    # Test daily sales
    print("\n1. Daily Sales Report:")
    daily_sales = get_daily_sales()
    print(f"   Date: {daily_sales['date']}")
    print(f"   Orders: {daily_sales['total_orders']}")
    print(f"   Sales: INR {daily_sales['total_sales']:.2f}")
    
    # Test total sales
    print("\n2. Total Sales (30 days):")
    sales_msg = get_total_sales_message(30)
    print(sales_msg)
    
    # Test bills list
    print("\n3. Bills List:")
    bills = get_bills_list(limit=5)
    print(f"   Found {len(bills)} bills")
    for bill in bills:
        print(f"   Bill #{bill[0]} - INR {bill[3]:.2f}")
    
    # Test menu summary
    print("\n4. Menu Summary:")
    menu_msg = get_menu_summary()
    print(menu_msg)
    
    print("\n" + "=" * 60)
    print("Bot Command Tests Completed!")
    print("=" * 60)

# Telegram Bot Polling
_bot_polling_active = False
_bot_thread = None

def handle_bot_message(message):
    """Handle incoming bot message"""
    try:
        text = message.get('text', '')
        chat_id = message.get('chat', {}).get('id')
        
        if not text or not text.startswith('/'):
            return
        
        command = text.split()[0].lower()
        
        if command == '/start':
            response = "*Welcome to HUNGER Family Restaurant Bot!*\n\n"
            response += "*Available Commands:*\n"
            response += "/help - Show all commands\n"
            response += "/today - Today's sales report\n"
            response += "/sales - Sales report (last 30 days)\n"
            response += "/bills - List today's bills\n"
            response += "/bill <number> - Get bill details\n"
            response += "/menu - Menu summary"
            send_telegram_message(chat_id, response)
        
        elif command == '/help':
            response = "*Available Commands:*\n\n"
            response += "/today - Today's sales summary\n"
            response += "/sales - Sales report (last 30 days)\n"
            response += "/bills - List all bills today\n"
            response += "/bill <number> - Get bill #number details\n"
            response += "/menu - Menu summary by category\n"
            response += "\n*Usage Examples:*\n"
            response += "/today - See today's orders and revenue\n"
            response += "/bill 123 - Get details of bill #123"
            send_telegram_message(chat_id, response)
        
        elif command == '/today':
            daily_sales = get_daily_sales()
            response = f"*Today's Sales Report*\n\n"
            response += f"*Date:* {daily_sales['date']}\n"
            response += f"*Total Orders:* {daily_sales['total_orders']}\n"
            response += f"*Total Sales:* INR {daily_sales['total_sales']:.2f}\n\n"
            
            if daily_sales['total_orders'] > 0:
                response += "*Recent Orders:*\n"
                for order in daily_sales['orders'][:5]:
                    order_id, table_num, order_date, amount = order
                    response += f"#{order_id:03d} | Table: {table_num or 'Takeaway'} | INR {amount:.2f}\n"
            
            send_telegram_message(chat_id, response)
        
        elif command == '/sales':
            sales_msg = get_total_sales_message(30)
            send_telegram_message(chat_id, sales_msg)
        
        elif command == '/bills':
            try:
                bills = get_bills_list(limit=20)
                print(f"Found {len(bills)} bills")
                bills_msg = format_bills_list_message(bills)
                print(f"Formatted message length: {len(bills_msg)}")
                success = send_telegram_message(chat_id, bills_msg)
                if not success:
                    print(f"Failed to send bills message")
            except Exception as e:
                print(f"Error in /bills command: {e}")
                send_telegram_message(chat_id, f"Error: {str(e)}")
        
        elif command.startswith('/bill'):
            parts = text.split()
            if len(parts) > 1:
                try:
                    order_id = int(parts[1])
                    bill_data = get_bill_details(order_id)
                    if bill_data:
                        bill_msg = format_bill_message(bill_data)
                        send_telegram_message(chat_id, bill_msg)
                    else:
                        send_telegram_message(chat_id, f"Bill #{order_id} not found.")
                except ValueError:
                    send_telegram_message(chat_id, "Invalid bill number. Use: /bill <number>")
            else:
                send_telegram_message(chat_id, "Usage: /bill <number>")
        
        elif command == '/menu':
            menu_msg = get_menu_summary()
            send_telegram_message(chat_id, menu_msg)
        
        else:
            send_telegram_message(chat_id, "Unknown command. Type /help for available commands.")
    
    except Exception as e:
        print(f"Error handling bot message: {e}")

def poll_telegram_bot():
    """Poll Telegram bot for updates"""
    global _bot_polling_active
    
    settings = get_telegram_settings()
    if not settings or not settings['enabled']:
        print("Telegram bot is disabled in settings")
        return
    
    bot_token = settings['bot_token']
    if not bot_token:
        print("Bot token not configured")
        return
    
    last_update_id = 0
    
    print("Telegram bot polling started...")
    
    while _bot_polling_active:
        try:
            url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
            params = {'offset': last_update_id + 1, 'timeout': 5}
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('ok'):
                    updates = data.get('result', [])
                    
                    for update in updates:
                        last_update_id = update['update_id']
                        message = update.get('message')
                        
                        if message:
                            handle_bot_message(message)
                
        except Exception as e:
            print(f"Bot polling error: {e}")
            time.sleep(5)
    
    print("Telegram bot polling stopped")

def start_bot_polling():
    """Start bot polling in background thread"""
    global _bot_polling_active, _bot_thread
    
    if _bot_polling_active:
        return
    
    _bot_polling_active = True
    _bot_thread = threading.Thread(target=poll_telegram_bot, daemon=True)
    _bot_thread.start()

def stop_bot_polling():
    """Stop bot polling"""
    global _bot_polling_active
    _bot_polling_active = False

if __name__ == "__main__":
    test_bot_commands()
