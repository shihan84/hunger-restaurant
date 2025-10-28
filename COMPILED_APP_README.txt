================================================================================
    HUNGER FAMILY RESTAURANT - BILLING SOFTWARE
    Compiled Application Readme
================================================================================

LICENSE: Warchaswaa Media Pvt Ltd
© 2024 All rights reserved

================================================================================
OVERVIEW
================================================================================

This is the standalone executable version of the HUNGER Family Restaurant 
Billing Software. The application includes all features:

- Order Management & Billing
- Thermal Printer Support (58mm)
- Admin Panel with Settings
- Inventory Management
- Accounting & Financial Reports
- Purchase Order Management
- Staff Management & Payroll
- Analytics Dashboard
- Backup & Data Management
- Automation & Alerts
- Telegram Integration

================================================================================
SYSTEM REQUIREMENTS
================================================================================

Minimum Requirements:
- Windows 7/8/10/11 (64-bit)
- 100 MB free disk space
- 4 GB RAM
- USB or Network printer connection (for thermal printing)

================================================================================
INSTALLATION
================================================================================

1. Extract the HUNGER_Billing_Software.exe file to your desired location
2. Double-click HUNGER_Billing_Software.exe to launch the application
3. The application will create a database file (restaurant_billing.db) 
   automatically on first run

================================================================================
FIRST TIME SETUP
================================================================================

1. Launch the application
2. Click "SETTINGS" button in the footer
3. Configure the following in the Admin Panel:
   
   a) Restaurant Settings Tab:
      - Update restaurant name (default: HUNGER Family Restaurant)
      - Set GST settings if applicable
      - Configure service charge
      - Select currency
   
   b) Menu & Prices Tab:
      - Add menu categories
      - Add menu items with prices
      - Set food type (veg/non-veg)
      - Configure plate types (single/full)
   
   c) Printer Settings Tab:
      - Select your thermal printer (default: POS-58)
      - Configure page setup
      - Test print
      - Save settings

   d) Telegram Settings Tab:
      - Enter Telegram Bot Token
      - Enter Chat ID
      - Enable/disable notifications

   e) Other tabs for additional features:
      - Inventory: Add ingredients and manage stock
      - Accounting: View financial reports
      - Purchase: Manage suppliers and orders
      - Staff: Manage staff and payroll
      - Analytics: View business insights
      - Backup: Configure automatic backups

================================================================================
USAGE
================================================================================

1. START A NEW ORDER:
   - Select a category from the left panel
   - Choose menu items from the center panel
   - Select plate type (SINGLE/FULL) for items with dual pricing
   - Items will be added to the cart on the right
   
2. GENERATE BILL:
   - Click "GENERATE BILL" button
   - Enter table number (or leave empty for takeaway)
   - Review the bill
   - Click "Print Bill" to print receipt
   - Select payment method: Cash, Card, or UPI
   - Order will be processed and printed

3. ADMIN FUNCTIONS:
   - Click "SETTINGS" to open Admin Panel
   - Configure all settings as needed
   - View reports and analytics
   - Manage inventory, staff, and suppliers

4. KEYBOARD SHORTCUTS:
   - F11: Toggle fullscreen mode
   - ESC: Exit fullscreen mode

================================================================================
DATABASE
================================================================================

- Database file: restaurant_billing.db
- Location: Same folder as the executable
- Format: SQLite3 database
- Backup: Use the Backup tab in Admin Panel to create backups

================================================================================
THERMAL PRINTER
================================================================================

Supported Printers:
- 58mm thermal printers with ESC/POS commands
- Default printer: POS-58
- Printer settings are configurable in Admin Panel

Print Format:
- Optimized for 58mm thermal paper
- 32 characters per line
- Auto-cut enabled
- Customizable margins and fonts

================================================================================
TROUBLESHOOTING
================================================================================

1. APPLICATION WON'T START:
   - Check Windows system requirements
   - Run as Administrator if needed
   - Check antivirus software isn't blocking it

2. PRINTER NOT WORKING:
   - Verify printer is connected and turned on
   - Check printer name in Printer Settings
   - Test print from Admin Panel
   - Install printer drivers if needed

3. DATABASE ERRORS:
   - Ensure write permissions in the folder
   - Check disk space available
   - Backup and restore database if corrupted

4. TELEGRAM NOT WORKING:
   - Verify Bot Token and Chat ID are correct
   - Check internet connection
   - Ensure Telegram notifications are enabled

================================================================================
UPDATES & BACKUP
================================================================================

Updates:
- Replace the executable with the new version
- Database will be preserved automatically

Backup:
- Use the Backup tab in Admin Panel
- Automatic daily backups are recommended
- Store backups in a safe location

================================================================================
SUPPORT
================================================================================

For support and updates, contact:
- License: Warchaswaa Media Pvt Ltd
- © 2024 All rights reserved

================================================================================
CHANGELOG - Version 1.0
================================================================================

- Initial release
- Complete order management and billing
- Thermal printer support (58mm)
- Admin panel with all settings
- Inventory management
- Accounting and financial reports
- Purchase order management
- Staff management and payroll
- Analytics dashboard
- Backup and data management
- Automation and alerts
- Telegram integration
- Optimized bill format for 58mm thermal printer

================================================================================
