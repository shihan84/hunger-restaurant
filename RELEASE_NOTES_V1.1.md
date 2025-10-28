# HUNGER Family Restaurant - Billing Software
## Release Notes v1.1

**Release Date**: January 2025  
**License**: Warchaswaa Media Pvt Ltd  
**Copyright**: © 2024 Warchaswaa Media Pvt Ltd. All rights reserved.

---

## What's New in v1.1

### 🐛 **Bug Fixes**

1. **Fixed Double-Click Payment Issue**
   - Prevented duplicate bills from accidental double-clicks
   - Added processing flag to block simultaneous payments
   - Improved error handling and user feedback
   - Now creates only ONE bill per payment regardless of clicks

2. **Fixed Menu Price Update**
   - Enhanced error checking for price updates
   - Better feedback when update fails
   - Shows row count to confirm changes
   - Auto-refreshes main menu after price update

3. **Fixed Report Display**
   - Corrected key errors in sales reports
   - Proper handling of empty report data
   - Better error messages for failed reports

### ✨ **New Features**

1. **Selective Bill Deletion**
   - List all bills with details
   - Checkbox selection for specific bills
   - Delete individual or multiple bills
   - Automatic invoice number reset when all bills deleted
   - Telegram notification on bill deletion

2. **Accounting Reports**
   - Daily Sales Report with summaries
   - Custom Date Range Sales Report
   - Financial summary with totals
   - Order details and breakdowns

3. **Add New Menu Items**
   - Simple form to add items
   - Category, type (Veg/Non-Veg), and pricing
   - Validation and duplicate checking
   - Instant menu refresh after adding

4. **Remove Items from Cart**
   - Remove button (✕) on each cart item
   - Better cart display with item frames
   - Real-time cart update

5. **Invoice Number Management**
   - Real invoice numbers (#00001, #00002, etc.)
   - Automatic reset when all bills deleted
   - Proper sequencing throughout

### 🔧 **Improvements**

- Better error handling throughout the application
- Enhanced user feedback messages
- Improved database transaction handling
- Telegram notification updates
- More robust payment processing

---

## Previous Features (v1.0)

### Core Features
- Fullscreen POS interface
- 5 menu categories with 124+ items
- Real-time cart management
- Professional bill generation
- Multiple payment modes (Cash/Card/UPI)
- GST & Service Charge support

### Thermal Printing
- ESC/POS 58mm printer support
- 32-character optimized layout
- Automatic paper cutting
- CGST/SGST split on bills

### Admin Panel (11 Tabs)
- Telegram Settings
- GST Configuration
- Menu Prices Management
- Service Charge Settings
- Printer Settings
- Inventory Management
- Accounting & Reports
- Purchase Orders
- Staff Management
- Analytics Dashboard
- Backup & Security

### Telegram Integration
- Order notifications
- Payment notifications
- Bot commands: `/today`, `/sales`, `/bills`, `/bill`, `/menu`

---

## Installation

### Quick Start

1. **Run the executable**:
   - Go to `dist` folder
   - Run `HUNGER_Billing_Software.exe`

2. **Or run from source**:
   ```bash
   python main.py
   ```

### First-Time Setup

1. Open Admin Panel (Settings button)
2. Configure Telegram Settings (bot token & chat ID)
3. Configure GST Settings (if needed)
4. Set up Menu Prices
5. Configure Service Charge (optional)
6. Set up Printer (optional)

---

## System Requirements

- **OS**: Windows 10 or later
- **RAM**: 2 GB minimum (4 GB recommended)
- **Storage**: 100 MB free space
- **Display**: 1024x768 or higher
- **Printer**: ESC/POS thermal printer (optional)
- **Network**: Internet connection (for Telegram)

---

## Usage Guide

### Taking an Order

1. Select category from left panel
2. Click "Add" to add items (Single or Full plate)
3. View cart in right panel
4. Click "Generate Bill"
5. Enter table number (optional for takeaway)
6. Select payment method
7. Single bill created (no duplicates!)

### Managing Menu Items

1. Settings > Menu Prices > "+ Add New Menu Item"
2. Fill in: Name, Category, Type, Prices
3. Click "Save"
4. Menu updates automatically

### Deleting Bills

1. Settings > Accounting > "⚠️ Delete All Bills"
2. Select bills using checkboxes
3. Click "Delete Selected Bills"
4. Confirm deletion
5. Invoice numbers reset if all bills deleted

### Reports

1. Settings > Accounting
2. Click "Daily Sales Report"
3. OR "Sales Report (Custom Date)"
4. View financial summaries

### Telegram Bot

Send to your bot:
- `/today` - Today's sales
- `/sales` - Last 30 days report
- `/bills` - List all bills today
- `/bill 123` - Get bill #123 details
- `/menu` - Menu summary

---

## Technical Details

### Changes in v1.1

**Files Modified:**
- `app.py` - Double-click fix, cart improvements
- `admin_panel.py` - Reports, bill deletion, menu add
- `telegram_notifier.py` - Improved notifications
- `thermal_printer.py` - Better formatting

### Build Information

- **Python**: 3.14
- **GUI**: Tkinter
- **Database**: SQLite3
- **Build Tool**: PyInstaller
- **License**: Warchaswaa Media Pvt Ltd
- **Copyright**: © 2024

---

## Bug Fixes Details

### Double-Click Prevention
**Issue**: Rapid double-clicks created duplicate bills  
**Solution**: Added processing flag to prevent concurrent payments  
**Impact**: Only one bill created per payment action

### Invoice Reset
**Issue**: Invoice numbers didn't reset after deleting all bills  
**Solution**: Auto-reset sequences when all bills deleted  
**Impact**: Fresh start with #00001 after cleanup

### Menu Price Update
**Issue**: Price updates sometimes didn't work  
**Solution**: Better error checking and row count validation  
**Impact**: Reliable price updates with feedback

---

## Upgrade from v1.0

If upgrading from v1.0:

1. **Backup your data**:
   - Copy `restaurant_billing.db` to backup location
   - Export data via Admin Panel if needed

2. **Install v1.1**:
   - Download new `HUNGER_Billing_Software.exe`
   - Replace old executable
   - Keep your database file

3. **Check Settings**:
   - Verify Telegram configuration
   - Review GST settings
   - Confirm menu items

---

## Known Issues

1. **Thermal Printer**: Paper cutting requires manual tear if printer doesn't support auto-cut
2. **Telegram**: Requires internet connection
3. **Database**: SQLite is single-user only
4. **Reports**: Limited export functionality

---

## Support

For issues or questions, contact Warchaswaa Media Pvt Ltd.

---

## License

Copyright © 2024 Warchaswaa Media Pvt Ltd. All rights reserved.

Proprietary Software License - Unauthorized copying, modification, distribution, or use prohibited without express written permission.

---

## Changelog

### v1.1 (January 2025)
- Fixed double-click payment issue
- Added selective bill deletion
- Added accounting reports
- Added menu item add feature
- Added cart remove functionality
- Improved invoice number management
- Enhanced error handling
- Better user feedback

### v1.0 (Initial Release)
- Complete billing system
- Thermal printer support
- Telegram integration
- Admin panel with 11 tabs
- Inventory management
- Full documentation

---

## Credits

**Developer**: AI Assistant  
**Company**: Warchaswaa Media Pvt Ltd  
**Client**: HUNGER Family Restaurant  
**License**: Proprietary Software License

