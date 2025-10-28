# HUNGER Family Restaurant - Billing Software
## Release Notes v1.0

**Release Date**: January 2025  
**License**: Warchaswaa Media Pvt Ltd  
**Copyright**: © 2024 Warchaswaa Media Pvt Ltd. All rights reserved.

---

## What's New in This Release

### 🎉 Version 1.0 - Complete Billing Software

This is the first stable release of HUNGER Family Restaurant Billing Software, featuring comprehensive order management, billing, thermal printing, and business intelligence features.

---

## Key Features

### 1. 🍽️ Complete Order Management
- Fullscreen POS-style interface
- Category-based menu navigation (5 categories)
- 124+ menu items with single/full pricing
- Real-time cart with remove functionality
- Table number management

### 2. 💰 Billing & Payments
- Professional bill generation
- GST calculation (5% configurable)
- Service charge support
- Multiple payment modes: Cash, Card, UPI
- Real invoice numbering (#00001, #00002, etc.)

### 3. 🖨️ Thermal Printing
- ESC/POS printer support for 58mm paper
- Automatic paper cutting
- 32-character optimized layout
- Full item name display (multi-line support)
- Restaurant name and footer
- CGST/SGST split on bills

### 4. 📱 Telegram Integration
- Real-time order notifications
- Payment notifications
- Telegram bot commands:
  - `/today` - Today's sales summary
  - `/sales` - 30-day sales report
  - `/bills` - List today's bills
  - `/bill <number>` - Get bill details
  - `/menu` - Menu summary

### 5. ⚙️ Admin Panel (11 Tabs)
- **Telegram Settings**: Configure bot token and chat ID
- **GST Configuration**: Enable/disable GST, set GST number
- **Menu Prices**: Update existing prices, add new menu items
- **Service Charge**: Configure service charge rate
- **Printer Settings**: Detect printers, test print, save settings
- **Inventory**: Track ingredients, recipes, and stock
- **Accounting**: Financial reports, P&L, balance sheet
- **Purchases**: Purchase orders, supplier payments
- **Staff**: Attendance tracking, payroll, leave management
- **Analytics**: Dashboard with business intelligence
- **Backup & Security**: Automatic backups, data export

### 6. 📊 Business Intelligence
- Sales reports (daily, weekly, monthly)
- Profit & Loss statements
- Balance Sheet
- Inventory tracking
- Purchase order management
- Staff attendance and payroll
- Financial alerts
- Performance metrics

### 7. 🔐 Security & Backup
- Automatic daily backups
- Data export (JSON, CSV)
- Audit logs
- User authentication (planned)
- Security management

### 8. 🤖 Automation
- Auto purchase orders (low stock alerts)
- Supplier price comparison
- Financial alerts
- Performance alerts
- Tax payment reminders

---

## Installation

### Prerequisites
- Windows 10 or later
- Python 3.7 or later (for development)

### Quick Start

1. **Run the executable**:
   - Go to `dist` folder
   - Run `HUNGER_Billing_Software.exe`

2. **Or run from source**:
   ```bash
   python main.py
   ```

### First-Time Setup

1. Open the Admin Panel (click "Settings" button)
2. Configure Telegram Settings:
   - Enter your bot token
   - Enter your chat ID
   - Test connection
3. Configure GST Settings:
   - Enable GST if needed
   - Enter your GST number
4. Set up Menu Prices:
   - Update existing prices
   - Add new menu items
5. Configure Service Charge (optional)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10 or later
- **RAM**: 2 GB
- **Storage**: 100 MB free space
- **Display**: 1024x768 or higher resolution
- **Printer**: ESC/POS thermal printer (optional)

### Recommended Requirements
- **OS**: Windows 11
- **RAM**: 4 GB
- **Storage**: 500 MB free space
- **Display**: 1920x1080 (Full HD)
- **Network**: Internet connection (for Telegram)

---

## Usage Guide

### Taking an Order

1. Select a category from the left panel
2. Browse menu items in the center panel
3. Click "Add" to add items to cart (Single or Full)
4. View cart in right panel
5. Click "Generate Bill"
6. Enter table number (or leave empty for takeaway)
7. Select payment method
8. Order is processed and receipt is printed automatically

### Managing Menu Items

1. Open Admin Panel
2. Go to "Menu Prices" tab
3. Click "+ Add New Menu Item"
4. Fill in the form:
   - Item Name
   - Category
   - Food Type (Veg/Non-Veg)
   - Single Price
   - Full Price (optional)
5. Click "Save"

### Telegram Bot Commands

Send these commands to your configured Telegram bot:

- `/start` - Show welcome message
- `/help` - List all commands
- `/today` - Today's sales report
- `/sales` - Last 30 days sales
- `/bills` - List today's bills
- `/bill 123` - Get bill #123 details
- `/menu` - Menu summary by category

---

## Database

All data is stored in `restaurant_billing.db` (SQLite database).

### Location
- **Development**: In project root folder
- **Compiled**: In executable directory (same folder as exe file)

### Backup
- Automatic daily backups in `backups` folder
- Use Admin Panel > Backup & Security tab to export data

---

## Technical Details

### Technology Stack
- **Language**: Python 3.14
- **GUI**: Tkinter
- **Database**: SQLite3
- **Thermal Printer**: ESC/POS commands via python-escpos
- **Telegram**: Python requests library
- **Build**: PyInstaller

### Module Structure
```
app.py              - Main application GUI
database.py         - Database operations
admin_panel.py      - Admin panel interface
thermal_printer.py  - Printer control
telegram_bot.py     - Telegram bot commands
telegram_notifier.py - Order notifications
inventory_manager.py - Inventory management
accounting.py       - Accounting system
purchase_management.py - Purchase orders
staff_management.py - Staff & payroll
analytics.py        - Business intelligence
backup_manager.py   - Backup & security
automation.py       - Automation & alerts
```

---

## Known Issues & Limitations

1. **Thermal Printer**: Paper cutting requires manual tear if printer doesn't support auto-cut
2. **Telegram**: Requires internet connection for notifications
3. **Database**: SQLite is single-user, not suitable for multi-user scenarios
4. **Excel Export**: Limited to available data at time of export

---

## Future Enhancements

- Multi-user support
- Cloud backup integration
- Mobile app companion
- Advanced analytics
- Multi-currency support
- Tax filing integration
- Integration with accounting software

---

## Support

For issues, questions, or feature requests, please contact Warchaswaa Media Pvt Ltd.

---

## License

Copyright © 2024 Warchaswaa Media Pvt Ltd. All rights reserved.

This software is proprietary and confidential. Unauthorized copying, modification, distribution, or use of this software, via any medium, is strictly prohibited without the express written permission of Warchaswaa Media Pvt Ltd.

---

## Credits

**Developer**: AI Assistant  
**Company**: Warchaswaa Media Pvt Ltd  
**Client**: HUNGER Family Restaurant  
**License**: Proprietary Software License

