# Release Notes - HUNGER Family Restaurant Billing Software v1.2

## Version 1.2 - January 2025

### New Features

#### 🔍 **Global Menu Search**
- Added comprehensive search functionality that searches across ALL menu categories
- Search box now says "🔍 Search All Items:" for clarity
- Results show item name with category information (e.g., "Chicken Curry (Main Course)")
- Real-time search results as you type
- Clear button (✕) to reset search
- No longer limited to currently selected category

#### 📏 **Paper Feed Configuration**
- Set paper feed to exactly 4 lines after bill print
- Perfect spacing for continuous long paper rolls
- No automatic cutting - designed for manual tearing
- Consistent spacing between bills

### Improvements

#### 🖨️ **Printer Configuration**
- Removed paper cutting functionality (as per requirements)
- Optimized for continuous paper feeding
- Better spacing for bill separation
- More reliable printing with fixed 4-line feed

### Bug Fixes

- **CRITICAL FIX**: Fixed database persistence issue - menu items and all data now save properly in compiled app
- Fixed search functionality to work across all categories instead of just selected category
- Improved search result display with category labels
- Updated paper feed from variable to fixed 4 lines
- Database now stored in executable directory instead of temp folder for data persistence

### Technical Changes

- **Updated `database.py` to fix persistence in compiled apps**
  - Database now stored in executable directory instead of temp folder
  - Automatically copies database from bundled version on first run
  - All menu additions, price updates, and settings now persist correctly
- Updated `thermal_printer.py` to use fixed 4-line feed command
- Enhanced `apply_search_filter()` to search across all categories
- Modified search query to include category field in results
- Improved search UI with better labeling

### Compatibility

- Compatible with all existing databases
- No migration required from v1.1
- Works with all previously configured settings
- Printer settings preserved

### Installation

1. Close any running instance of the application
2. Download `HUNGER_Billing_Software.exe` from the release
3. Replace the old executable in your installation directory
4. The desktop shortcut has been automatically updated

### Previous Versions

#### v1.1 (Previous Release)
- Invoice number reset on bill deletion
- Fixed double bill printing on payment button double-click
- Telegram notifications for bill deletion
- Selective bill deletion feature

#### v1.0 (Initial Release)
- Complete billing system
- Menu management
- Thermal printer integration
- Telegram notifications
- Admin panel
- Full accounting and reporting

### License

Copyright (c) 2025 Warchaswaa Media Pvt Ltd.
All rights reserved.

This software is proprietary and confidential.
Unauthorized copying, distribution, or use is strictly prohibited.

### Support

For issues, feature requests, or support, please contact Warchaswaa Media Pvt Ltd.

---

**Version 1.2** | **HUNGER Family Restaurant** | **Powered by Warchaswaa Media Pvt Ltd**

