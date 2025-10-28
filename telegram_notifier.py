"""
Telegram Notification System
Handles order notifications via Telegram Bot
"""

import requests
import database
from datetime import datetime

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

def is_telegram_enabled():
    """Check if Telegram notifications are enabled"""
    settings = get_telegram_settings()
    return settings['enabled'] if settings else False

def send_telegram_message(message):
    """Send message to Telegram"""
    settings = get_telegram_settings()
    
    if not settings or not settings['enabled']:
        return False
    
    bot_token = settings['bot_token']
    chat_id = settings['chat_id']
    
    if not bot_token or not chat_id:
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram notification failed: {e}")
        return False

def format_order_message(order_number, table_number, items, total_amount, order_type="NEW"):
    """Format order message for Telegram"""
    if order_type == "NEW":
        header = f"🆕 <b>NEW ORDER #{order_number:03d}</b>\n"
    elif order_type == "PAID":
        header = f"💰 <b>ORDER PAID #{order_number:03d}</b>\n"
    else:
        header = f"📋 <b>ORDER #{order_number:03d}</b>\n"
    
    message = header
    message += f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    message += f"🪑 <b>Table:</b> {table_number if table_number else 'Takeaway'}\n"
    message += f"💵 <b>Total:</b> ₹{total_amount:.2f}\n\n"
    
    message += "<b>Items:</b>\n"
    for item in items:
        name = item['name']
        quantity = item.get('quantity', 1)
        plate_type = item['plate_type'].upper()
        price = item['price']
        message += f"• {quantity}x {name} ({plate_type}) - ₹{price:.0f}\n"
    
    return message

def send_new_order_notification(order_number, table_number, items, total_amount):
    """Send new order notification"""
    if not is_telegram_enabled():
        return False
    
    message = format_order_message(order_number, table_number, items, total_amount, "NEW")
    return send_telegram_message(message)

def send_payment_notification(order_number, table_number, total_amount, payment_mode="Cash"):
    """Send order payment notification"""
    if not is_telegram_enabled():
        return False
    
    header = f"💰 <b>ORDER PAID #{order_number:03d}</b>\n"
    message = header
    message += f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    message += f"🪑 <b>Table:</b> {table_number if table_number else 'Takeaway'}\n"
    message += f"💳 <b>Payment:</b> {payment_mode}\n"
    message += f"💵 <b>Amount:</b> ₹{total_amount:.2f}\n"
    
    return send_telegram_message(message)

def test_telegram_connection():
    """Test Telegram connection"""
    if not is_telegram_enabled():
        return False, "Telegram notifications are disabled"
    
    test_message = f"✅ <b>Telegram Connection Test</b>\n"
    test_message += f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
    test_message += "This is a test message from Restaurant Billing System."
    
    success = send_telegram_message(test_message)
    
    if success:
        return True, "Telegram connection successful!"
    else:
        return False, "Failed to send test message. Check bot token and chat ID."


if __name__ == "__main__":
    # Test telegram connection
    success, message = test_telegram_connection()
    print(message)
