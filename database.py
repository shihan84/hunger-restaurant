import sqlite3
import os
import sys

DATABASE_NAME = "restaurant_billing.db"

def get_database_path():
    """Get the database file path, handling both development and compiled environments"""
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        # Always use executable directory for compiled app to ensure data persistence
        exe_dir = os.path.dirname(sys.executable)
        db_path = os.path.join(exe_dir, DATABASE_NAME)
        
        # Create database in executable directory if it doesn't exist
        if not os.path.exists(db_path):
            # Try to copy from temp folder if exists
            temp_db = os.path.join(sys._MEIPASS, DATABASE_NAME)
            if os.path.exists(temp_db):
                import shutil
                shutil.copy2(temp_db, db_path)
    else:
        # Running in development mode
        db_path = DATABASE_NAME
    
    return db_path

def get_connection():
    """Create and return database connection"""
    db_path = get_database_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialize database with all required tables and default data"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)
    
    # Create menu_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price_single REAL,
            price_full REAL,
            category TEXT NOT NULL,
            food_type TEXT NOT NULL CHECK(food_type IN ('veg', 'non-veg')),
            plate_type TEXT NOT NULL CHECK(plate_type IN ('single', 'full')),
            is_available INTEGER DEFAULT 1,
            FOREIGN KEY (category) REFERENCES categories(name)
        )
    """)
    
    # Create orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number TEXT,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            gst_amount REAL DEFAULT 0,
            service_charge REAL DEFAULT 0,
            discount REAL DEFAULT 0,
            final_amount REAL NOT NULL,
            status TEXT DEFAULT 'active'
        )
    """)
    
    # Create order_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            menu_item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id),
            FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
        )
    """)
    
    # Create restaurant_settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurant_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_name TEXT DEFAULT 'Restaurant',
            address TEXT DEFAULT '',
            gst_number TEXT DEFAULT '',
            gst_enabled INTEGER DEFAULT 0,
            service_charge_rate REAL DEFAULT 0,
            currency TEXT DEFAULT '₹'
        )
    """)
    
    # Insert default categories
    default_categories = [
        'CHINESE VEGETARIAN',
        'CHINESE NON-VEGETARIAN',
        'INDIAN VEGETARIAN',
        'INDIAN NON-VEGETARIAN',
        'THALIS'
    ]
    
    for category in default_categories:
        cursor.execute("""
            INSERT OR IGNORE INTO categories (name) VALUES (?)
        """, (category,))
    
    # Create telegram_settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telegram_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bot_token TEXT DEFAULT '',
            chat_id TEXT DEFAULT '',
            enabled INTEGER DEFAULT 0
        )
    """)
    
    # Create printer_settings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS printer_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            printer_name TEXT DEFAULT '',
            margin_top REAL DEFAULT 0.1,
            margin_bottom REAL DEFAULT 0.1,
            margin_left REAL DEFAULT 0.1,
            margin_right REAL DEFAULT 0.1,
            paper_size TEXT DEFAULT '58mm',
            font_family TEXT DEFAULT 'Courier',
            font_size TEXT DEFAULT '8',
            font_style TEXT DEFAULT 'Normal',
            line_spacing REAL DEFAULT 1.0,
            auto_cut INTEGER DEFAULT 1
        )
    """)
    
    # Insert default printer settings
    cursor.execute("""
        INSERT OR IGNORE INTO printer_settings 
        (id, printer_name, margin_top, margin_bottom, margin_left, margin_right, 
         paper_size, font_family, font_size, font_style, line_spacing, auto_cut)
        VALUES (1, '', 0.1, 0.1, 0.1, 0.1, '58mm', 'Courier', '8', 'Normal', 1.0, 1)
    """)
    
    # Insert default restaurant settings
    cursor.execute("""
        INSERT OR REPLACE INTO restaurant_settings 
        (id, restaurant_name, gst_enabled) 
        VALUES (1, 'HUNGER Family Restaurant', 0)
    """)
    
    # Insert default telegram settings
    cursor.execute("""
        INSERT OR IGNORE INTO telegram_settings 
        (id, bot_token, chat_id, enabled)
        VALUES (1, '8391823641:AAHuRZlop8M_0zNSMnk1iiGkGTCORCc7qks', '-4816754138', 0)
    """)
    
    # Create suppliers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT DEFAULT '',
            address TEXT DEFAULT '',
            created_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create ingredients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            unit TEXT NOT NULL DEFAULT 'kg',
            current_stock REAL DEFAULT 0,
            min_stock REAL DEFAULT 0,
            cost_per_unit REAL DEFAULT 0
        )
    """)
    
    # Create menu_ingredients table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            menu_item_id INTEGER NOT NULL,
            ingredient_id INTEGER NOT NULL,
            quantity_required REAL NOT NULL,
            FOREIGN KEY (menu_item_id) REFERENCES menu_items(id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
        )
    """)
    
    # Create stock_transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_id INTEGER NOT NULL,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('in', 'out')),
            quantity REAL NOT NULL,
            reason TEXT DEFAULT '',
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
        )
    """)
    
    # Create accounts table for accounting
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('cash', 'bank', 'credit')),
            balance REAL DEFAULT 0
        )
    """)
    
    # Create default cash account
    cursor.execute("""
        INSERT OR IGNORE INTO accounts (id, name, type, balance)
        VALUES (1, 'Cash Account', 'cash', 0)
    """)
    
    # Create transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            account_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('debit', 'credit')),
            amount REAL NOT NULL,
            description TEXT DEFAULT '',
            order_id INTEGER,
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    """)
    
    # Create expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT DEFAULT '',
            payment_method TEXT DEFAULT 'cash'
        )
    """)
    
    # Create tax_records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tax_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            period TEXT NOT NULL,
            gst_collected REAL DEFAULT 0,
            gst_paid REAL DEFAULT 0,
            net_amount REAL DEFAULT 0
        )
    """)
    
    # Create purchase_orders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            po_number TEXT NOT NULL UNIQUE,
            supplier_id INTEGER NOT NULL,
            order_date TEXT NOT NULL,
            expected_date TEXT,
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'received', 'cancelled')),
            total_amount REAL DEFAULT 0,
            notes TEXT DEFAULT '',
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
        )
    """)
    
    # Create purchase_order_items table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            po_id INTEGER NOT NULL,
            ingredient_id INTEGER NOT NULL,
            quantity_ordered REAL NOT NULL,
            quantity_received REAL DEFAULT 0,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (po_id) REFERENCES purchase_orders(id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(id)
        )
    """)
    
    # Create accounts_payable table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS accounts_payable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER NOT NULL,
            po_id INTEGER,
            amount_due REAL NOT NULL,
            due_date TEXT,
            status TEXT DEFAULT 'unpaid' CHECK(status IN ('unpaid', 'partially_paid', 'paid')),
            payment_terms TEXT DEFAULT 'Net 30',
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
            FOREIGN KEY (po_id) REFERENCES purchase_orders(id)
        )
    """)
    
    # Create supplier_payments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS supplier_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER NOT NULL,
            ap_id INTEGER,
            payment_date TEXT NOT NULL,
            amount_paid REAL NOT NULL,
            payment_method TEXT DEFAULT 'cash',
            reference_number TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
            FOREIGN KEY (ap_id) REFERENCES accounts_payable(id)
        )
    """)
    
    # Create staff table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staff (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Admin', 'Manager', 'Cashier', 'Waiter', 'Chef', 'Other')),
            salary REAL NOT NULL DEFAULT 0,
            contact TEXT DEFAULT '',
            email TEXT DEFAULT '',
            address TEXT DEFAULT '',
            joining_date TEXT DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'inactive', 'terminated'))
        )
    """)
    
    # Create attendance table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            check_in TEXT,
            check_out TEXT,
            total_hours REAL DEFAULT 0,
            status TEXT DEFAULT 'present' CHECK(status IN ('present', 'absent', 'late', 'leave', 'half_day')),
            notes TEXT DEFAULT '',
            FOREIGN KEY (staff_id) REFERENCES staff(id),
            UNIQUE(staff_id, date)
        )
    """)
    
    # Create salary_payments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salary_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER NOT NULL,
            month INTEGER NOT NULL CHECK(month BETWEEN 1 AND 12),
            year INTEGER NOT NULL,
            basic_salary REAL NOT NULL,
            deductions REAL DEFAULT 0,
            bonuses REAL DEFAULT 0,
            total_amount REAL NOT NULL,
            payment_date TEXT,
            payment_method TEXT DEFAULT 'cash',
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'paid', 'partial')),
            notes TEXT DEFAULT '',
            FOREIGN KEY (staff_id) REFERENCES staff(id),
            UNIQUE(staff_id, month, year)
        )
    """)
    
    # Create leave_requests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id INTEGER NOT NULL,
            leave_type TEXT DEFAULT 'casual' CHECK(leave_type IN ('casual', 'sick', 'emergency', 'paid', 'unpaid')),
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            days INTEGER NOT NULL,
            reason TEXT DEFAULT '',
            status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
            applied_date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (staff_id) REFERENCES staff(id)
        )
    """)
    
    # Create users table for authentication
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'cashier',
            created_date TEXT DEFAULT CURRENT_TIMESTAMP,
            last_login TEXT,
            status TEXT DEFAULT 'active'
        )
    """)
    
    # Create audit_logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

def test_connection():
    """Test database connection"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        print("Database connection successful!")
        print(f"Tables found: {[table[0] for table in tables]}")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == "__main__":
    # Initialize database when script is run directly
    init_database()
    test_connection()
