# Release Notes - HUNGER Family Restaurant Billing Software v1.3

## Version 1.3 - January 2025

### New Features

#### 📅 **Business Day Logic (1 AM to 1 AM)**
- Implemented business day counting from 1:00 AM to 1:00 AM (next day)
- All orders automatically tagged with correct business date
- Perfect for restaurants closing after midnight
- Sales reports and analytics use business_date for accurate day tracking

### Improvements

#### 🗄️ **Database Schema Enhancement**
- Added `business_date` column to `orders` table
- Automatic business date calculation for all new orders
- Existing orders migrated with correct business dates
- Database persistence verified and tested

#### 🎨 **UI Updates**
- Added copyright footer "© 2025 Warchaswaa Media Pvt Ltd. All Rights Reserved. | Version 1.3"
- Clean header without Open/Close buttons
- Improved layout and spacing

### Bug Fixes

- Fixed database persistence in compiled applications
- Fixed business_date column migration for existing databases
- Improved order date tracking for late-night operations
- Enhanced day counting accuracy for reports

### Technical Changes

- Updated `database.py` with `get_business_date()` and `get_business_date_string()` functions
- Modified order insertion to include `business_date` field
- Updated all queries to use `business_date` for day-based operations
- Database schema migration supports existing installations

### Business Day Logic

Orders are now counted by business day (1 AM to 1 AM):
- 12:00 AM - 12:59 AM → Previous business day
- 1:00 AM - 11:59 PM → Current business day

Example:
- Order at 11:45 PM on Jan 20 → Business Date: Jan 20
- Order at 12:30 AM on Jan 21 → Business Date: Jan 20
- Order at 1:05 AM on Jan 21 → Business Date: Jan 21

### Database Migration

If upgrading from v1.2 or earlier:
1. Run the application
2. The `business_date` column will be automatically added
3. Existing orders will be migrated with correct business dates
4. No manual migration needed

### Installation

1. Close any running instance of the application
2. Download `HUNGER_Billing_Software.exe` from the release
3. Replace the old executable in your installation directory
4. The desktop shortcut has been automatically updated to v1.3

### Previous Versions

#### v1.2 (Previous Release)
- Global menu search across all categories
- 4-line paper feed configuration
- Database persistence fix
- Copyright and version footer

#### v1.1 (Earlier)
- Invoice number reset on bill deletion
- Fixed double bill printing
- Telegram notifications

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

**Version 1.3** | **HUNGER Family Restaurant** | **Powered by Warchaswaa Media Pvt Ltd**

