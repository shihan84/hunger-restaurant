# How to Create a Release on GitHub

The tag v1.0 has been pushed to GitHub. Now you need to create a release through the web interface:

## Steps to Create GitHub Release

1. **Go to your repository**: https://github.com/shihan84/hunger-restaurant

2. **Click on "Releases"** in the right sidebar (or go to: https://github.com/shihan84/hunger-restaurant/releases)

3. **Click "Draft a new release"**

4. **Fill in the release details**:
   - **Choose a tag**: v1.0 (should already exist)
   - **Release title**: HUNGER Family Restaurant Billing Software v1.0
   - **Description**: Copy the content from `RELEASE_NOTES.md` (see below)

5. **Click "Publish release"**

---

## Release Description (Copy this text)

```markdown
# 🍽️ HUNGER Family Restaurant Billing Software v1.0

**First Stable Release** - Complete restaurant billing system with order management, thermal printing, Telegram integration, and business intelligence.

## 📦 What's New

### Core Features
- ✅ Fullscreen POS-style interface
- ✅ Category-based menu navigation (5 categories)
- ✅ 124+ menu items with single/full pricing
- ✅ Real-time cart with remove functionality
- ✅ Professional bill generation with GST & Service Charge

### Thermal Printing
- ✅ ESC/POS 58mm printer support
- ✅ 32-character optimized layout
- ✅ Full item name display (multi-line)
- ✅ Automatic paper cutting
- ✅ CGST/SGST split on bills

### Telegram Integration
- ✅ Real-time order & payment notifications
- ✅ Bot commands: `/today`, `/sales`, `/bills`, `/bill <number>`, `/menu`
- ✅ Configurable bot token & chat ID

### Admin Panel (11 Tabs)
- ✅ Telegram Settings
- ✅ GST Configuration
- ✅ Menu Prices (update & add new items)
- ✅ Service Charge Settings
- ✅ Printer Settings
- ✅ Inventory Management
- ✅ Accounting & Financial Reports
- ✅ Purchase Management
- ✅ Staff Management
- ✅ Analytics Dashboard
- ✅ Backup & Security

### Business Intelligence
- ✅ Sales reports (daily/weekly/monthly)
- ✅ Profit & Loss statements
- ✅ Balance Sheet
- ✅ Inventory tracking
- ✅ Purchase order management
- ✅ Staff attendance & payroll
- ✅ Financial & performance alerts

## 🖥️ System Requirements

- **OS**: Windows 10 or later
- **RAM**: 2 GB minimum (4 GB recommended)
- **Storage**: 100 MB free space
- **Display**: 1024x768 or higher
- **Printer**: ESC/POS thermal printer (optional)

## 🚀 Installation

### Option 1: Run Executable
1. Download `HUNGER_Billing_Software.exe` from this release
2. Double-click to run
3. Configure settings through Admin Panel

### Option 2: Run from Source
```bash
git clone https://github.com/shihan84/hunger-restaurant.git
cd hunger-restaurant
pip install -r requirements.txt
python main.py
```

## 📋 Quick Start Guide

1. Run the application
2. Open Admin Panel (Settings button)
3. Configure Telegram Settings
4. Set up GST & Service Charge
5. Update menu prices or add new items
6. Start taking orders!

## 📱 Telegram Bot Commands

Send these to your Telegram bot:

- `/today` - Today's sales summary
- `/sales` - Last 30 days sales report
- `/bills` - List today's bills
- `/bill 123` - Get bill #123 details
- `/menu` - Menu summary by category

## 📄 Database

All data stored in `restaurant_billing.db` (SQLite)
- Location: Same folder as executable (in compiled version)
- Automatic daily backups available in Admin Panel

## 🛠️ Build Information

- **Python**: 3.14
- **GUI**: Tkinter
- **Database**: SQLite3
- **Build Tool**: PyInstaller
- **License**: Warchaswaa Media Pvt Ltd
- **Copyright**: © 2024

## 📝 Documentation

- See `README.md` for full documentation
- See `RELEASE_NOTES.md` for detailed changelog

## 🔐 License

Copyright © 2024 Warchaswaa Media Pvt Ltd. All rights reserved.

Proprietary Software License - Unauthorized copying, modification, distribution, or use prohibited without express written permission.

## 🙏 Credits

**Developer**: AI Assistant  
**Company**: Warchaswaa Media Pvt Ltd  
**Client**: HUNGER Family Restaurant

---

**Download**: See "Assets" section below for the executable file.
```

---

## Need Help?

If you have trouble creating the release, here's what to do:

1. Go to: https://github.com/shihan84/hunger-restaurant/releases/new
2. Select "v1.0" as the tag
3. Enter title and description as shown above
4. Click "Publish release"

The compiled executable (`HUNGER_Billing_Software.exe`) is in the `dist` folder of your local repository. You can upload it as an asset to the release or create a zip file containing it.

**Note**: Due to file size, it's recommended to upload the executable separately or provide a download link rather than committing it to the repository.

