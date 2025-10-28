# HUNGER Family Restaurant - Billing Software

A comprehensive Python Tkinter-based billing software for Indian restaurants with GST support, Telegram notifications, and complete order management.

## License

Copyright © 2024 Warchaswaa Media Pvt Ltd. All rights reserved.

This software is proprietary and confidential. Unauthorized copying, modification, distribution, or use of this software, via any medium, is strictly prohibited without the express written permission of Warchaswaa Media Pvt Ltd.

For licensing inquiries, please contact Warchaswaa Media Pvt Ltd.

**License Type**: Proprietary Software License  
**Owner**: Warchaswaa Media Pvt Ltd  
**Copyright Year**: 2024

## Features

- **Fullscreen GUI**: Modern Tkinter interface with category navigation
- **Menu Management**: 124+ menu items with single/full pricing
- **Order Cart**: Real-time cart updates with item counter
- **Bill Generation**: Professional bill printing with GST and service charge
- **Thermal Printing**: ESC/POS thermal printer support for 58mm receipts
- **Telegram Notifications**: Real-time order and payment notifications
- **Payment Processing**: Cash, Card, and UPI payment modes
- **Admin Panel**: Configuration for Telegram, GST, Menu Prices, and Service Charge
- **Inventory Management**: Track ingredients, recipes, stock levels, and auto-deduct on orders
- **Accounting System**: Comprehensive financial management with sales reports, P&L, balance sheet, and tax tracking
- **Purchase Management**: Purchase orders, supplier payments, and accounts payable tracking
- **Staff Management**: Staff database, attendance tracking, leaves, and payroll system
- **Analytics Dashboard**: Comprehensive business intelligence, reporting, and dashboard widgets
- **Backup & Security**: Automatic backups, data export, audit logs, and user authentication
- **Automation & Alerts**: Auto purchase orders, financial alerts, performance alerts, and supplier price comparison
- **Database Management**: SQLite database with complete restaurant schema
- **GST Support**: Configurable GST with Indian tax structure (5%)
- **Service Charge**: Optional service charge calculation
- **Currency**: Indian Rupees (₹)

## Project Status

✅ **STEP 1**: Database Setup (Complete)  
✅ **STEP 2**: GUI Implementation (Complete)  
✅ **STEP 3**: Complete Menu Added (Complete)  
✅ **STEP 4**: Telegram Notifications (Complete)  
✅ **STEP 5**: Order Management & Billing (Complete)  
✅ **STEP 6**: Thermal Printer Support (Complete)  
✅ **STEP 7**: Admin Panel (Complete)  
✅ **STEP 8**: Final Testing (Complete)  
✅ **STEP 9**: Inventory Management System (Complete)  
✅ **STEP 10**: Accounting System (Complete)  
✅ **STEP 11**: Purchase Management (Complete)  
✅ **STEP 12**: Staff Management (Complete)  
✅ **STEP 13**: Analytics Dashboard (Complete)  
✅ **STEP 14**: Backup & Data Management (Complete)  
✅ **STEP 15**: Integration & Automation (Complete)

## Project Structure

```
rest/
├── database.py              # Database setup and connection
├── main.py                  # Main application entry point
├── app.py                   # Main Tkinter GUI application
├── telegram_notifier.py     # Telegram notification system
├── thermal_printer.py       # Thermal printer ESC/POS support
├── admin_panel.py          # Admin panel for settings management
├── inventory_manager.py    # Inventory management system
├── accounting.py           # Accounting and financial reporting system
├── purchase_management.py  # Purchase orders and supplier management
├── staff_management.py     # Staff, attendance, and payroll management
├── analytics.py            # Analytics and reporting system
├── backup_manager.py       # Backup, security, and data export system
├── automation.py           # Automation, alerts, and integration system
├── add_menu_items.py        # Menu items population script
├── test_system.py          # Comprehensive system testing script
├── requirements.txt         # Python dependencies
├── restaurant_billing.db    # SQLite database file
└── README.md               # This file
```

## Setup

### Requirements

- Python 3.x
- tkinter (usually included with Python)
- sqlite3 (included in Python standard library)
- requests (pip install requests)

### Installation

1. Clone or download this project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the database initialization:

```bash
python database.py
```

This will create `restaurant_billing.db` with all required tables.

## Database Schema

### Tables

- **categories**: Menu categories (Starters, Main Course, etc.)
- **menu_items**: Food items with price_single, price_full, category, plate type (single/full), and availability
- **orders**: Order headers with billing information
- **order_items**: Individual items in each order
- **restaurant_settings**: Restaurant configuration including GST settings
- **telegram_settings**: Telegram bot configuration for notifications
- **suppliers**: Supplier information for inventory purchases
- **ingredients**: Ingredient details (name, unit, stock levels, cost)
- **menu_ingredients**: Recipe mapping (links menu items to ingredients)
- **stock_transactions**: Complete history of stock in/out transactions
- **accounts**: Chart of accounts (cash, bank, credit)
- **transactions**: All financial transactions linked to accounts and orders
- **expenses**: Expense tracking with categories and payment methods
- **tax_records**: GST and tax liability records
- **purchase_orders**: Purchase order headers with supplier and status
- **purchase_order_items**: Individual items in purchase orders
- **accounts_payable**: Track money owed to suppliers
- **supplier_payments**: Payment history to suppliers
- **staff**: Staff information with roles and salaries
- **attendance**: Daily check-in/check-out records
- **salary_payments**: Monthly salary records with bonuses and deductions
- **leave_requests**: Staff leave applications and approval tracking
- **users**: User authentication and role-based access
- **audit_logs**: System audit trail for security

### Default Categories

1. CHINESE VEGETARIAN
2. CHINESE NON-VEGETARIAN
3. INDIAN VEGETARIAN
4. INDIAN NON-VEGETARIAN
5. THALIS

## Usage

### Running the Application

```bash
# Run the main application
python main.py
```

### Running Tests

```bash
# Run comprehensive system tests
python test_system.py
```

### Key Features

- **F11**: Toggle fullscreen mode
- **ESC**: Exit fullscreen mode
- **Categories**: Click category buttons to navigate menu
- **Add to Cart**: Select Single or Full plate type
- **Generate Bill**: Create bill with table number input
- **Payment**: Choose payment method (Cash/Card/UPI)
- **Settings**: Open admin panel for configuration

### Order Workflow

1. Select a category from the left panel
2. Browse menu items in the center panel
3. Click "Add" buttons (Single/Full) to add items to cart
4. View cart in right panel with item counter
5. Click "Generate Bill" when ready
6. Enter table number (or leave empty for takeaway)
7. Review bill and select payment method
8. Order is saved and Telegram notifications are sent
9. Cart clears automatically

## Notes

- **GST**: 5% GST is calculated on subtotal when enabled
- **Service Charge**: Configurable percentage-based service charge
- **Currency**: Indian Rupees (₹) throughout the application
- **Dual Pricing**: Menu items support SINGLE and FULL prices (e.g., 50/90, 70/140)
- **Single Pricing**: Some items only have single price (auto-selected)
- **Price Pending**: Items with price 0 are marked "Price Pending" and disabled
- **Telegram**: Pre-configured bot token and chat ID, enabled by default
- **Notifications**: Sends NEW ORDER and ORDER PAID notifications to Telegram
- **Order Management**: All orders are saved to database with complete item details
- **Fullscreen**: Optimized for touchscreen/POS systems
- **Thermal Printer**: Automatic receipt printing after payment, 58mm paper, Courier 8 font, strict margins (0.1 inch)
- **Admin Panel**: Tabbed interface for managing Telegram settings, GST configuration, menu prices, and service charge
- **Inventory System**: Automatic stock deduction when orders are paid, ingredient tracking, recipe management, low stock alerts
- **Accounting**: Automatic transaction recording, sales reports, expense tracking, profit & loss statements, balance sheet, tax management
- **Purchase Management**: Create purchase orders, track delivery status, receive stock against POs, manage accounts payable, supplier payment tracking
- **Staff Management**: Add/manage staff, track attendance with check-in/out, leave management, automatic salary calculation with attendance-based deductions, payroll payment tracking
- **Analytics Dashboard**: Today's summary, financial overview, inventory alerts, staff performance, sales analysis, customer preferences, profitability analysis, and comprehensive reporting
- **Backup & Security**: Automatic daily backups, data export (JSON), restore functionality, audit logging, user authentication with role-based access, and security management
- **Automation & Alerts**: Automatic purchase order generation for low stock items, supplier price comparison, financial alerts (low cash, high expenses, tax due), performance alerts (sales targets, attendance, inventory discrepancies, slow-moving items), and daily automation tasks

## License

**Warchaswaa Media Pvt Ltd**

© 2024 HUNGER Family Restaurant. All rights reserved.
