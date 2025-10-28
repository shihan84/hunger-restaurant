"""
Admin Panel for Restaurant Billing Software
Configure Telegram, GST, Menu Prices, and Service Charge
"""

import tkinter as tk
from tkinter import ttk, messagebox
import database

class AdminPanel:
    def __init__(self, parent, app_instance):
        """
        Initialize admin panel
        Args:
            parent: Parent window
            app_instance: Main app instance (for refreshing data)
        """
        self.parent = parent
        self.app_instance = app_instance
        
        # Create admin window
        self.admin_window = tk.Toplevel(parent)
        self.admin_window.title("Admin Panel - Settings")
        self.admin_window.geometry("1000x800")
        self.admin_window.configure(bg='#ecf0f1')
        
        # Make it modal
        self.admin_window.transient(parent)
        self.admin_window.grab_set()
        
        # Create tabs
        self.create_tabs()
    
    def create_tabs(self):
        """Create tabbed interface"""
        # Notebook for tabs
        notebook = ttk.Notebook(self.admin_window)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Telegram Settings Tab
        self.create_telegram_tab(notebook)
        
        # GST Configuration Tab
        self.create_gst_tab(notebook)
        
        # Menu Price Management Tab
        self.create_menu_price_tab(notebook)
        
        # Service Charge Tab
        self.create_service_charge_tab(notebook)
        
        # Printer Settings Tab
        self.create_printer_tab(notebook)
        
        # Inventory Management Tab
        self.create_inventory_tab(notebook)
        
        # Accounting Tab
        self.create_accounting_tab(notebook)
        
        # Purchase Management Tab
        self.create_purchase_tab(notebook)
        
        # Staff Management Tab
        self.create_staff_tab(notebook)
        
        # Analytics Dashboard Tab
        self.create_analytics_tab(notebook)
        
        # Backup & Security Tab
        self.create_backup_tab(notebook)
    
    def create_telegram_tab(self, notebook):
        """Create Telegram settings tab"""
        telegram_frame = tk.Frame(notebook, bg='white')
        notebook.add(telegram_frame, text="Telegram Settings")
        
        # Title
        title = tk.Label(
            telegram_frame,
            text="Telegram Notification Settings",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        # Get current settings
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT bot_token, chat_id, enabled FROM telegram_settings WHERE id = 1")
        settings = cursor.fetchone()
        conn.close()
        
        # Form fields
        form_frame = tk.Frame(telegram_frame, bg='white')
        form_frame.pack(padx=50, pady=20, fill='both', expand=True)
        
        # Bot Token
        tk.Label(
            form_frame,
            text="Bot Token:",
            font=('Arial', 12),
            bg='white'
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        self.bot_token_var = tk.StringVar(value=settings[0] if settings[0] else '')
        bot_token_entry = tk.Entry(
            form_frame,
            textvariable=self.bot_token_var,
            font=('Arial', 11),
            width=50
        )
        bot_token_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # Chat ID
        tk.Label(
            form_frame,
            text="Chat ID:",
            font=('Arial', 12),
            bg='white'
        ).grid(row=1, column=0, sticky='w', pady=10)
        
        self.chat_id_var = tk.StringVar(value=settings[1] if settings[1] else '')
        chat_id_entry = tk.Entry(
            form_frame,
            textvariable=self.chat_id_var,
            font=('Arial', 11),
            width=50
        )
        chat_id_entry.grid(row=1, column=1, pady=10, padx=10)
        
        # Enabled checkbox
        self.telegram_enabled_var = tk.BooleanVar(value=bool(settings[2]))
        enabled_check = tk.Checkbutton(
            form_frame,
            text="Enable Telegram Notifications",
            variable=self.telegram_enabled_var,
            font=('Arial', 12),
            bg='white'
        )
        enabled_check.grid(row=2, column=0, columnspan=2, pady=20)
        
        # Test button
        test_btn = tk.Button(
            form_frame,
            text="Test Connection",
            font=('Arial', 10, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.test_telegram_connection
        )
        test_btn.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Save button
        save_btn = tk.Button(
            form_frame,
            text="Save Settings",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.save_telegram_settings
        )
        save_btn.grid(row=4, column=0, columnspan=2, pady=20)
    
    def create_gst_tab(self, notebook):
        """Create GST configuration tab"""
        gst_frame = tk.Frame(notebook, bg='white')
        notebook.add(gst_frame, text="GST Configuration")
        
        # Title
        title = tk.Label(
            gst_frame,
            text="GST Tax Configuration",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        # Get current settings
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT gst_number, gst_enabled FROM restaurant_settings WHERE id = 1")
        settings = cursor.fetchone()
        conn.close()
        
        # Form fields
        form_frame = tk.Frame(gst_frame, bg='white')
        form_frame.pack(padx=50, pady=20, fill='both', expand=True)
        
        # GST Number
        tk.Label(
            form_frame,
            text="GST Number:",
            font=('Arial', 12),
            bg='white'
        ).grid(row=0, column=0, sticky='w', pady=10)
        
        self.gst_number_var = tk.StringVar(value=settings[0] if settings[0] else '')
        gst_number_entry = tk.Entry(
            form_frame,
            textvariable=self.gst_number_var,
            font=('Arial', 11),
            width=40
        )
        gst_number_entry.grid(row=0, column=1, pady=10, padx=10)
        
        # GST Enabled checkbox
        self.gst_enabled_var = tk.BooleanVar(value=bool(settings[1]))
        gst_enabled_check = tk.Checkbutton(
            form_frame,
            text="Enable GST (5% on subtotal)",
            variable=self.gst_enabled_var,
            font=('Arial', 12),
            bg='white'
        )
        gst_enabled_check.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Info label
        info_label = tk.Label(
            form_frame,
            text="Note: GST is calculated as 5% of subtotal.",
            font=('Arial', 10, 'italic'),
            bg='white',
            fg='#7f8c8d'
        )
        info_label.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Save button
        save_btn = tk.Button(
            form_frame,
            text="Save GST Settings",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.save_gst_settings
        )
        save_btn.grid(row=3, column=0, columnspan=2, pady=30)
    
    def create_menu_price_tab(self, notebook):
        """Create menu price management tab"""
        menu_frame = tk.Frame(notebook, bg='white')
        notebook.add(menu_frame, text="Menu Prices")
        
        # Title
        title = tk.Label(
            menu_frame,
            text="Update Menu Item Prices",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        # Instructions
        info_label = tk.Label(
            menu_frame,
            text="Select a category and item to update price",
            font=('Arial', 11),
            bg='white',
            fg='#7f8c8d'
        )
        info_label.pack(pady=5)
        
        # Add New Item button
        add_item_btn = tk.Button(
            menu_frame,
            text="+ Add New Menu Item",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.open_add_item_window
        )
        add_item_btn.pack(pady=10)
        
        # Controls frame
        controls_frame = tk.Frame(menu_frame, bg='white')
        controls_frame.pack(padx=20, pady=10, fill='x')
        
        # Category selection
        tk.Label(
            controls_frame,
            text="Category:",
            font=('Arial', 11),
            bg='white'
        ).pack(side='left', padx=5)
        
        self.category_combo = ttk.Combobox(controls_frame, font=('Arial', 11), width=30)
        self.category_combo.pack(side='left', padx=5)
        self.category_combo.bind('<<ComboboxSelected>>', self.load_items_for_category)
        
        # Item selection (create before load_categories)
        tk.Label(
            controls_frame,
            text="Item:",
            font=('Arial', 11),
            bg='white'
        ).pack(side='left', padx=10)
        
        self.item_combo = ttk.Combobox(controls_frame, font=('Arial', 11), width=30)
        self.item_combo.pack(side='left', padx=5)
        self.item_combo.bind('<<ComboboxSelected>>', self.load_item_details)
        
        # Initialize items_data
        self.items_data = {}
        
        # Current price display (CREATE BEFORE load_categories)
        price_frame = tk.Frame(menu_frame, bg='white')
        price_frame.pack(padx=50, pady=20, fill='both', expand=True)
        
        tk.Label(
            price_frame,
            text="Current Prices:",
            font=('Arial', 12, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=10)
        
        self.current_price_label = tk.Label(
            price_frame,
            text="Select an item to view current prices",
            font=('Arial', 11),
            bg='white',
            fg='#7f8c8d'
        )
        self.current_price_label.pack(anchor='w', pady=5)
        
        # Load categories (after creating ALL widgets)
        self.load_categories()
        
        # Update price fields
        update_frame = tk.Frame(price_frame, bg='white')
        update_frame.pack(fill='x', pady=20)
        
        tk.Label(
            update_frame,
            text="Single Price (₹):",
            font=('Arial', 11),
            bg='white'
        ).grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
        self.single_price_var = tk.StringVar()
        single_price_entry = tk.Entry(
            update_frame,
            textvariable=self.single_price_var,
            font=('Arial', 11),
            width=15
        )
        single_price_entry.grid(row=0, column=1, padx=10, pady=10)
        
        tk.Label(
            update_frame,
            text="Full Price (₹):",
            font=('Arial', 11),
            bg='white'
        ).grid(row=1, column=0, sticky='w', padx=10, pady=10)
        
        self.full_price_var = tk.StringVar()
        full_price_entry = tk.Entry(
            update_frame,
            textvariable=self.full_price_var,
            font=('Arial', 11),
            width=15
        )
        full_price_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Update button
        update_btn = tk.Button(
            price_frame,
            text="Update Price",
            font=('Arial', 12, 'bold'),
            bg='#e67e22',
            fg='white',
            command=self.update_menu_price
        )
        update_btn.pack(pady=20)
    
    def create_service_charge_tab(self, notebook):
        """Create service charge settings tab"""
        sc_frame = tk.Frame(notebook, bg='white')
        notebook.add(sc_frame, text="Service Charge")
        
        # Title
        title = tk.Label(
            sc_frame,
            text="Service Charge Configuration",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        # Get current settings
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT service_charge_rate FROM restaurant_settings WHERE id = 1")
        settings = cursor.fetchone()
        conn.close()
        
        # Form fields
        form_frame = tk.Frame(sc_frame, bg='white')
        form_frame.pack(padx=50, pady=20, fill='both', expand=True)
        
        # Service charge rate
        tk.Label(
            form_frame,
            text="Service Charge Rate (%):",
            font=('Arial', 12),
            bg='white'
        ).grid(row=0, column=0, sticky='w', pady=20)
        
        self.sc_rate_var = tk.StringVar(value=str(settings[0]) if settings[0] else '0')
        sc_rate_entry = tk.Entry(
            form_frame,
            textvariable=self.sc_rate_var,
            font=('Arial', 11),
            width=20
        )
        sc_rate_entry.grid(row=0, column=1, pady=20, padx=10)
        
        # Info label
        info_label = tk.Label(
            form_frame,
            text="Service charge is calculated as percentage of subtotal.\nLeave as 0 to disable.",
            font=('Arial', 10, 'italic'),
            bg='white',
            fg='#7f8c8d',
            justify='left'
        )
        info_label.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Save button
        save_btn = tk.Button(
            form_frame,
            text="Save Service Charge Settings",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.save_service_charge_settings
        )
        save_btn.grid(row=2, column=0, columnspan=2, pady=40)
    
    def load_categories(self):
        """Load categories for combo box"""
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM categories ORDER BY name")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        self.category_combo['values'] = categories
        if categories:
            self.category_combo.current(0)
            self.load_items_for_category()
    
    def load_items_for_category(self, event=None):
        """Load items for selected category"""
        category = self.category_combo.get()
        if not category:
            return
        
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, price_single, price_full 
            FROM menu_items 
            WHERE category = ?
            ORDER BY name
        """, (category,))
        
        items = cursor.fetchall()
        conn.close()
        
        self.items_data = {row[1]: row for row in items}
        self.item_combo['values'] = list(self.items_data.keys())
        self.item_combo.set('')
        self.current_price_label.config(text="Select an item to view current prices")
    
    def load_item_details(self, event=None):
        """Load price details for selected item"""
        item_name = self.item_combo.get()
        if not item_name or item_name not in self.items_data:
            return
        
        item_data = self.items_data[item_name]
        item_id, name, price_single, price_full = item_data
        
        # Update display
        single_text = f"₹{price_single:.0f}" if price_single else "Not set"
        full_text = f"₹{price_full:.0f}" if price_full else "Not set"
        
        self.current_price_label.config(
            text=f"Single: {single_text} | Full: {full_text}",
            fg='#2c3e50'
        )
        
        # Set entry values
        self.single_price_var.set(str(price_single) if price_single else '')
        self.full_price_var.set(str(price_full) if price_full else '')
    
    def test_telegram_connection(self):
        """Test Telegram connection"""
        import telegram_notifier
        success, message = telegram_notifier.test_telegram_connection()
        
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
    
    def save_telegram_settings(self):
        """Save Telegram settings"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE telegram_settings 
            SET bot_token = ?, chat_id = ?, enabled = ?
            WHERE id = 1
        """, (
            self.bot_token_var.get(),
            self.chat_id_var.get(),
            1 if self.telegram_enabled_var.get() else 0
        ))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "Telegram settings saved successfully!")
    
    def save_gst_settings(self):
        """Save GST settings"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE restaurant_settings 
            SET gst_number = ?, gst_enabled = ?
            WHERE id = 1
        """, (
            self.gst_number_var.get(),
            1 if self.gst_enabled_var.get() else 0
        ))
        
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Success", "GST settings saved successfully!")
    
    def update_menu_price(self):
        """Update menu item price"""
        item_name = self.item_combo.get()
        if not item_name or item_name not in self.items_data:
            messagebox.showwarning("No Item", "Please select an item to update")
            return
        
        single_price = self.single_price_var.get()
        full_price = self.full_price_var.get()
        
        try:
            single_price = float(single_price) if single_price else None
            full_price = float(full_price) if full_price else None
            
            if single_price and single_price <= 0:
                messagebox.showerror("Error", "Price must be greater than 0")
                return
            
            if full_price and full_price <= 0:
                messagebox.showerror("Error", "Price must be greater than 0")
                return
            
            if single_price is None:
                messagebox.showerror("Error", "Single price is required")
                return
            
            conn = database.get_connection()
            cursor = conn.cursor()
            
            # Update price and availability
            is_available = 1 if single_price > 0 else 0
            
            cursor.execute("""
                UPDATE menu_items 
                SET price_single = ?, price_full = ?, is_available = ?
                WHERE name = ? AND category = ?
            """, (single_price, full_price, is_available, item_name, self.category_combo.get()))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", f"Price updated for {item_name}")
            
            # Reload item details
            self.load_items_for_category()
            self.item_combo.set(item_name)
            self.load_item_details()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for prices")
    
    def open_add_item_window(self):
        """Open window to add new menu item"""
        add_window = tk.Toplevel(self.admin_window)
        add_window.title("Add New Menu Item")
        add_window.geometry("500x500")
        add_window.configure(bg='white')
        add_window.transient(self.admin_window)
        add_window.grab_set()
        
        # Title
        title = tk.Label(
            add_window,
            text="Add New Menu Item",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(add_window, bg='white')
        form_frame.pack(padx=40, pady=20)
        
        # Item Name
        tk.Label(form_frame, text="Item Name *:", font=('Arial', 11), bg='white').grid(row=0, column=0, sticky='w', padx=10, pady=10)
        name_entry = tk.Entry(form_frame, font=('Arial', 11), width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Category
        tk.Label(form_frame, text="Category *:", font=('Arial', 11), bg='white').grid(row=1, column=0, sticky='w', padx=10, pady=10)
        category_combo = ttk.Combobox(form_frame, font=('Arial', 11), width=28, values=[
            'CHINESE VEGETARIAN', 'CHINESE NON-VEGETARIAN', 
            'INDIAN VEGETARIAN', 'INDIAN NON-VEGETARIAN', 'THALIS'
        ])
        category_combo.grid(row=1, column=1, padx=10, pady=10)
        
        # Food Type
        tk.Label(form_frame, text="Food Type *:", font=('Arial', 11), bg='white').grid(row=2, column=0, sticky='w', padx=10, pady=10)
        food_type_var = tk.StringVar(value='veg')
        food_type_frame = tk.Frame(form_frame, bg='white')
        food_type_frame.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        tk.Radiobutton(food_type_frame, text="Vegetarian", variable=food_type_var, value='veg', bg='white', font=('Arial', 11)).pack(side='left')
        tk.Radiobutton(food_type_frame, text="Non-Vegetarian", variable=food_type_var, value='non-veg', bg='white', font=('Arial', 11)).pack(side='left', padx=10)
        
        # Single Price
        tk.Label(form_frame, text="Single Price (₹) *:", font=('Arial', 11), bg='white').grid(row=3, column=0, sticky='w', padx=10, pady=10)
        single_price_entry = tk.Entry(form_frame, font=('Arial', 11), width=15)
        single_price_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')
        
        # Full Price
        tk.Label(form_frame, text="Full Price (₹):", font=('Arial', 11), bg='white').grid(row=4, column=0, sticky='w', padx=10, pady=10)
        full_price_entry = tk.Entry(form_frame, font=('Arial', 11), width=15)
        full_price_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')
        
        def save_item():
            """Save new menu item"""
            name = name_entry.get().strip()
            category = category_combo.get()
            food_type = food_type_var.get()
            single_price_str = single_price_entry.get().strip()
            full_price_str = full_price_entry.get().strip()
            
            # Validation
            if not name:
                messagebox.showerror("Error", "Item name is required")
                return
            
            if not category:
                messagebox.showerror("Error", "Category is required")
                return
            
            try:
                single_price = float(single_price_str)
                if single_price <= 0:
                    raise ValueError("Price must be greater than 0")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid single price")
                return
            
            full_price = None
            if full_price_str:
                try:
                    full_price = float(full_price_str)
                    if full_price <= 0:
                        raise ValueError("Price must be greater than 0")
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid full price")
                    return
            
            # Save to database
            try:
                conn = database.get_connection()
                cursor = conn.cursor()
                
                # Check if item already exists
                cursor.execute("SELECT id FROM menu_items WHERE name = ? AND category = ?", (name, category))
                if cursor.fetchone():
                    messagebox.showerror("Error", f"Item '{name}' already exists in {category}")
                    conn.close()
                    return
                
                # Insert new item
                cursor.execute("""
                    INSERT INTO menu_items 
                    (name, price_single, price_full, category, food_type, plate_type, is_available)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (name, single_price, full_price, category, food_type, 'single', 1))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", f"Item '{name}' added successfully!")
                
                # Refresh the menu in main app
                if self.app_instance:
                    self.app_instance.load_categories()
                    self.app_instance.select_category(category)
                
                # Close window
                add_window.destroy()
                
                # Refresh admin panel
                self.load_items_for_category()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add item: {str(e)}")
        
        # Buttons
        btn_frame = tk.Frame(add_window, bg='white')
        btn_frame.pack(pady=30)
        
        tk.Button(
            btn_frame,
            text="Save",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            command=save_item,
            width=12
        ).pack(side='left', padx=10)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            font=('Arial', 11, 'bold'),
            bg='#95a5a6',
            fg='white',
            command=add_window.destroy,
            width=12
        ).pack(side='left', padx=10)
    
    def save_service_charge_settings(self):
        """Save service charge settings"""
        try:
            rate = float(self.sc_rate_var.get())
            
            if rate < 0 or rate > 100:
                messagebox.showerror("Error", "Service charge rate must be between 0 and 100")
                return
            
            conn = database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE restaurant_settings 
                SET service_charge_rate = ?
                WHERE id = 1
            """, (rate,))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Service charge settings saved successfully!")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for service charge rate")
    
    def create_printer_tab(self, notebook):
        """Create printer settings tab"""
        # Create main container with scrollbar
        main_container = tk.Frame(notebook, bg='white')
        notebook.add(main_container, text="Printer Settings")
        
        # Create canvas for scrolling
        canvas = tk.Canvas(main_container, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Use scrollable_frame as printer_frame
        printer_frame = scrollable_frame
        
        # Title
        title = tk.Label(
            printer_frame,
            text="Thermal Printer Configuration",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        # Load saved settings
        self.load_printer_settings()
        
        # Printer detection frame
        detection_frame = tk.Frame(printer_frame, bg='white')
        detection_frame.pack(padx=50, pady=20, fill='x')
        
        # Printer selection
        tk.Label(
            detection_frame,
            text="Select Printer:",
            font=('Arial', 12, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=5)
        
        self.printer_combo = ttk.Combobox(detection_frame, font=('Arial', 11), state='readonly')
        self.printer_combo.pack(fill='x', pady=5)
        
        tk.Label(
            detection_frame,
            text="Detected Printers:",
            font=('Arial', 12, 'bold'),
            bg='white'
        ).pack(anchor='w', pady=(10, 5))
        
        # Printer list
        self.printer_listbox = tk.Listbox(
            detection_frame,
            font=('Arial', 11),
            height=4
        )
        self.printer_listbox.pack(fill='x', pady=5)
        
        # Detect button
        detect_btn = tk.Button(
            detection_frame,
            text="Detect Printers",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            command=self.detect_printers
        )
        detect_btn.pack(pady=10)
        
        # Printer status
        self.printer_status_label = tk.Label(
            detection_frame,
            text="Click 'Detect Printers' to check printer connection",
            font=('Arial', 10),
            bg='white',
            fg='#7f8c8d'
        )
        self.printer_status_label.pack(pady=5)
        
        # Test print button
        test_print_btn = tk.Button(
            detection_frame,
            text="Test Print",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.test_printer
        )
        test_print_btn.pack(pady=10)
        
        # Separator
        separator = tk.Label(
            printer_frame,
            text="Page Setup",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        separator.pack(pady=(30, 10))
        
        # Page setup frame
        setup_frame = tk.Frame(printer_frame, bg='white')
        setup_frame.pack(padx=50, pady=10, fill='both', expand=True)
        
        # Margins section
        margins_frame = tk.LabelFrame(
            setup_frame,
            text="Margins (inches)",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        margins_frame.pack(fill='x', pady=10)
        
        # Top margin
        tk.Label(margins_frame, text="Top:", font=('Arial', 10), bg='white').grid(row=0, column=0, padx=5, pady=5)
        self.margin_top_var = tk.StringVar(value="0.1")
        tk.Entry(margins_frame, textvariable=self.margin_top_var, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        # Bottom margin
        tk.Label(margins_frame, text="Bottom:", font=('Arial', 10), bg='white').grid(row=0, column=2, padx=5, pady=5)
        self.margin_bottom_var = tk.StringVar(value="0.1")
        tk.Entry(margins_frame, textvariable=self.margin_bottom_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        
        # Left margin
        tk.Label(margins_frame, text="Left:", font=('Arial', 10), bg='white').grid(row=1, column=0, padx=5, pady=5)
        self.margin_left_var = tk.StringVar(value="0.1")
        tk.Entry(margins_frame, textvariable=self.margin_left_var, width=10).grid(row=1, column=1, padx=5, pady=5)
        
        # Right margin
        tk.Label(margins_frame, text="Right:", font=('Arial', 10), bg='white').grid(row=1, column=2, padx=5, pady=5)
        self.margin_right_var = tk.StringVar(value="0.1")
        tk.Entry(margins_frame, textvariable=self.margin_right_var, width=10).grid(row=1, column=3, padx=5, pady=5)
        
        # Layout section
        layout_frame = tk.LabelFrame(
            setup_frame,
            text="Print Layout",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#2c3e50',
            padx=10,
            pady=10
        )
        layout_frame.pack(fill='x', pady=10)
        
        # Paper size
        tk.Label(layout_frame, text="Paper Size:", font=('Arial', 10), bg='white').grid(row=0, column=0, padx=5, pady=5)
        self.paper_size_var = tk.StringVar(value="58mm")
        paper_sizes = ["58mm", "80mm"]
        paper_combo = ttk.Combobox(layout_frame, textvariable=self.paper_size_var, values=paper_sizes, width=15)
        paper_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # Font family
        tk.Label(layout_frame, text="Font:", font=('Arial', 10), bg='white').grid(row=0, column=2, padx=5, pady=5)
        self.font_family_var = tk.StringVar(value="Courier")
        font_families = ["Courier", "Arial", "Times"]
        font_family_combo = ttk.Combobox(layout_frame, textvariable=self.font_family_var, values=font_families, width=15)
        font_family_combo.grid(row=0, column=3, padx=5, pady=5)
        
        # Font size
        tk.Label(layout_frame, text="Font Size:", font=('Arial', 10), bg='white').grid(row=1, column=0, padx=5, pady=5)
        self.font_size_var = tk.StringVar(value="8")
        font_sizes = ["6", "8", "10", "12", "14", "16"]
        font_combo = ttk.Combobox(layout_frame, textvariable=self.font_size_var, values=font_sizes, width=15)
        font_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Font style
        tk.Label(layout_frame, text="Font Style:", font=('Arial', 10), bg='white').grid(row=1, column=2, padx=5, pady=5)
        self.font_style_var = tk.StringVar(value="Normal")
        font_styles = ["Normal", "Bold", "Italic", "Bold Italic"]
        font_style_combo = ttk.Combobox(layout_frame, textvariable=self.font_style_var, values=font_styles, width=15)
        font_style_combo.grid(row=1, column=3, padx=5, pady=5)
        
        # Line spacing
        tk.Label(layout_frame, text="Line Spacing:", font=('Arial', 10), bg='white').grid(row=2, column=0, padx=5, pady=5)
        self.line_spacing_var = tk.StringVar(value="1")
        line_spacing_entry = tk.Entry(layout_frame, textvariable=self.line_spacing_var, width=15)
        line_spacing_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Paper cut
        self.auto_cut_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            layout_frame,
            text="Auto Cut Paper After Print",
            variable=self.auto_cut_var,
            font=('Arial', 10),
            bg='white'
        ).grid(row=2, column=2, columnspan=2, padx=5, pady=5)
        
        # Save settings button
        save_setup_btn = tk.Button(
            setup_frame,
            text="Save Page Setup",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            command=self.save_page_setup
        )
        save_setup_btn.pack(pady=20)
        
        # Auto detect on tab creation
        self.detect_printers()
    
    def detect_printers(self):
        """Detect available printers"""
        import thermal_printer
        printers = thermal_printer.list_available_printers()
        
        self.printer_listbox.delete(0, tk.END)
        
        if printers:
            for printer in printers:
                self.printer_listbox.insert(tk.END, printer)
            
            # Update combo box
            self.printer_combo['values'] = printers
            
            # Set saved printer if available
            if hasattr(self, 'saved_printer_name') and self.saved_printer_name:
                if self.saved_printer_name in printers:
                    self.printer_combo.set(self.saved_printer_name)
                else:
                    self.printer_combo.set(printers[0])
            elif printers:
                self.printer_combo.set(printers[0])
            
            self.printer_status_label.config(
                text=f"✓ {len(printers)} printer(s) detected",
                fg='#27ae60'
            )
        else:
            self.printer_combo['values'] = []
            self.printer_status_label.config(
                text="✗ No printers detected",
                fg='#e74c3c'
            )
    
    def test_printer(self):
        """Test printer"""
        try:
            import thermal_printer
            printer = thermal_printer.ThermalPrinter()
            
            test_items = [
                {'name': 'Test Item 1', 'plate_type': 'single', 'price': 100},
                {'name': 'Test Item 2', 'plate_type': 'full', 'price': 200}
            ]
            
            success = printer.print_bill(
                restaurant_name="HUNGER Family Restaurant",
                table_number="TEST",
                items=test_items,
                subtotal=300,
                service_charge=0,
                gst_amount=15,
                total_amount=315,
                order_id=999,
                date="TEST DATE",
                currency="₹"
            )
            
            if success:
                messagebox.showinfo("Success", "Test print successful!")
            else:
                messagebox.showerror("Error", "Failed to print")
        except Exception as e:
            messagebox.showerror("Error", f"Printer error: {str(e)}")
    
    def save_page_setup(self):
        """Save page setup settings"""
        try:
            # Validate margins
            margin_top = float(self.margin_top_var.get())
            margin_bottom = float(self.margin_bottom_var.get())
            margin_left = float(self.margin_left_var.get())
            margin_right = float(self.margin_right_var.get())
            line_spacing = float(self.line_spacing_var.get())
            
            if margin_top < 0 or margin_bottom < 0 or margin_left < 0 or margin_right < 0:
                messagebox.showerror("Error", "Margins cannot be negative")
                return
            
            if line_spacing < 0.5 or line_spacing > 3:
                messagebox.showerror("Error", "Line spacing must be between 0.5 and 3")
                return
            
            # Get settings
            printer_name = self.printer_combo.get()
            paper_size = self.paper_size_var.get()
            font_family = self.font_family_var.get()
            font_size = self.font_size_var.get()
            font_style = self.font_style_var.get()
            auto_cut = self.auto_cut_var.get()
            
            # Save to database
            conn = database.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE printer_settings
                SET printer_name = ?,
                    margin_top = ?,
                    margin_bottom = ?,
                    margin_left = ?,
                    margin_right = ?,
                    paper_size = ?,
                    font_family = ?,
                    font_size = ?,
                    font_style = ?,
                    line_spacing = ?,
                    auto_cut = ?
                WHERE id = 1
            """, (
                printer_name,
                margin_top,
                margin_bottom,
                margin_left,
                margin_right,
                paper_size,
                font_family,
                font_size,
                font_style,
                line_spacing,
                1 if auto_cut else 0
            ))
            
            conn.commit()
            conn.close()
            
            messagebox.showinfo(
                "Success", 
                f"Printer settings saved successfully!\n\n"
                f"Printer: {printer_name or 'Default'}\n"
                f"Margins: Top={margin_top}\", Bottom={margin_bottom}\", Left={margin_left}\", Right={margin_right}\"\n"
                f"Paper Size: {paper_size}\n"
                f"Font: {font_family} {font_size}pt ({font_style})\n"
                f"Line Spacing: {line_spacing}\n"
                f"Auto Cut: {'Yes' if auto_cut else 'No'}"
            )
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all fields")
    
    def load_printer_settings(self):
        """Load saved printer settings from database"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM printer_settings WHERE id = 1")
        settings = cursor.fetchone()
        conn.close()
        
        if settings:
            self.saved_printer_name = settings['printer_name'] if settings['printer_name'] else ''
            
            # Set margin values
            if not hasattr(self, 'margin_top_var'):
                self.margin_top_var = tk.StringVar(value=str(settings['margin_top']))
                self.margin_bottom_var = tk.StringVar(value=str(settings['margin_bottom']))
                self.margin_left_var = tk.StringVar(value=str(settings['margin_left']))
                self.margin_right_var = tk.StringVar(value=str(settings['margin_right']))
                self.line_spacing_var = tk.StringVar(value=str(settings['line_spacing']))
                self.paper_size_var = tk.StringVar(value=settings['paper_size'])
                self.font_family_var = tk.StringVar(value=settings['font_family'])
                self.font_size_var = tk.StringVar(value=str(settings['font_size']))
                self.font_style_var = tk.StringVar(value=settings['font_style'])
                self.auto_cut_var = tk.BooleanVar(value=bool(settings['auto_cut']))
    
    def create_inventory_tab(self, notebook):
        """Create inventory management tab"""
        inv_frame = tk.Frame(notebook, bg='white')
        notebook.add(inv_frame, text="Inventory")
        
        title = tk.Label(
            inv_frame,
            text="Inventory Management",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        info_label = tk.Label(
            inv_frame,
            text="Inventory management features coming soon...\n\nAccess via Inventory Manager Module",
            font=('Arial', 11),
            bg='white',
            fg='#7f8c8d',
            justify='center'
        )
        info_label.pack(pady=50)
    
    def create_accounting_tab(self, notebook):
        """Create accounting tab"""
        acc_frame = tk.Frame(notebook, bg='white')
        notebook.add(acc_frame, text="Accounting")
        
        title = tk.Label(
            acc_frame,
            text="Accounting & Financial Reports",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        # Buttons frame
        btn_frame = tk.Frame(acc_frame, bg='white')
        btn_frame.pack(pady=20)
        
        # Daily Sales Report button
        daily_btn = tk.Button(
            btn_frame,
            text="Daily Sales Report",
            font=('Arial', 11, 'bold'),
            bg='#3498db',
            fg='white',
            width=25,
            command=self.show_daily_sales_report
        )
        daily_btn.pack(pady=10, padx=10)
        
        # Sales Report button
        sales_btn = tk.Button(
            btn_frame,
            text="Sales Report (Custom Date)",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            width=25,
            command=self.show_sales_report
        )
        sales_btn.pack(pady=10, padx=10)
        
        # Profit & Loss button
        pl_btn = tk.Button(
            btn_frame,
            text="Profit & Loss Statement",
            font=('Arial', 11, 'bold'),
            bg='#e67e22',
            fg='white',
            width=25,
            command=self.show_profit_loss
        )
        pl_btn.pack(pady=10, padx=10)
        
        # Balance Sheet button
        balance_btn = tk.Button(
            btn_frame,
            text="Balance Sheet",
            font=('Arial', 11, 'bold'),
            bg='#9b59b6',
            fg='white',
            width=25,
            command=self.show_balance_sheet
        )
        balance_btn.pack(pady=10, padx=10)
    
    def show_daily_sales_report(self):
        """Show daily sales report"""
        from datetime import date
        import accounting
        from tkinter import scrolledtext
        
        report = accounting.AccountingSystem.get_daily_sales_report(date.today())
        
        # Create report window
        report_window = tk.Toplevel(self.admin_window)
        report_window.title("Daily Sales Report")
        report_window.geometry("800x600")
        report_window.configure(bg='white')
        
        # Title
        title = tk.Label(
            report_window,
            text=f"Daily Sales Report - {report['date']}",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=10)
        
        # Report text
        report_text = scrolledtext.ScrolledText(
            report_window,
            font=('Courier', 10),
            bg='#f8f9fa',
            wrap='word'
        )
        report_text.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Format report
        report_content = f"Daily Sales Report\n"
        report_content += f"{'='*60}\n\n"
        report_content += f"Date: {report['date']}\n"
        report_content += f"Total Orders: {report['total_orders']}\n"
        report_content += f"Total Sales: ₹{report['total_sales']:.2f}\n"
        report_content += f"GST: ₹{report['total_gst']:.2f}\n"
        report_content += f"Service Charge: ₹{report['total_service_charge']:.2f}\n"
        report_content += f"Final Revenue: ₹{report['total_final']:.2f}\n"
        
        report_text.insert('1.0', report_content)
        report_text.config(state='disabled')
    
    def show_sales_report(self):
        """Show sales report with custom date range"""
        from tkinter import scrolledtext
        from datetime import datetime
        
        # Create date selection window
        date_window = tk.Toplevel(self.admin_window)
        date_window.title("Select Date Range")
        date_window.geometry("400x200")
        date_window.configure(bg='white')
        
        tk.Label(date_window, text="Start Date (YYYY-MM-DD):", font=('Arial', 11), bg='white').pack(pady=10)
        start_entry = tk.Entry(date_window, font=('Arial', 11), width=20)
        start_entry.pack(pady=5)
        start_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        tk.Label(date_window, text="End Date (YYYY-MM-DD):", font=('Arial', 11), bg='white').pack(pady=10)
        end_entry = tk.Entry(date_window, font=('Arial', 11), width=20)
        end_entry.pack(pady=5)
        end_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        def generate_report():
            start_date = start_entry.get()
            end_date = end_entry.get()
            date_window.destroy()
            
            import accounting
            report = accounting.AccountingSystem.get_sales_report(start_date, end_date)
            
            # Show report
            report_window = tk.Toplevel(self.admin_window)
            report_window.title(f"Sales Report - {start_date} to {end_date}")
            report_window.geometry("900x600")
            report_window.configure(bg='white')
            
            title = tk.Label(
                report_window,
                text=f"Sales Report - {start_date} to {end_date}",
                font=('Arial', 14, 'bold'),
                bg='white',
                fg='#2c3e50'
            )
            title.pack(pady=10)
            
            report_text = scrolledtext.ScrolledText(
                report_window,
                font=('Courier', 9),
                bg='#f8f9fa',
                wrap='word'
            )
            report_text.pack(fill='both', expand=True, padx=20, pady=10)
            
            # Format report
            content = f"Sales Report\n{'='*80}\n\n"
            content += f"Period: {report['period']}\n"
            content += f"Total Orders: {report['summary']['order_count']}\n"
            content += f"Total Sales: ₹{report['summary']['total_sales']:.2f}\n"
            content += f"Total GST: ₹{report['summary']['total_gst']:.2f}\n"
            content += f"Total Service Charge: ₹{report['summary']['total_service']:.2f}\n"
            content += f"Total Revenue: ₹{report['summary']['total_revenue']:.2f}\n\n"
            content += f"{'Order ID':<10}{'Date':<20}{'Table':<10}{'Amount':>15}\n"
            content += f"{'-'*60}\n"
            
            for order in report['orders'][:50]:  # Show first 50 orders
                order_id, order_date, table, total, gst, service, final, item_count = order
                content += f"{order_id:<10}{order_date.strftime('%Y-%m-%d %H:%M'):<20}{table or 'Takeaway':<10}{final:>15.2f}\n"
            
            report_text.insert('1.0', content)
            report_text.config(state='disabled')
        
        tk.Button(
            date_window,
            text="Generate Report",
            font=('Arial', 11, 'bold'),
            bg='#27ae60',
            fg='white',
            command=generate_report
        ).pack(pady=20)
    
    def show_profit_loss(self):
        """Show profit & loss statement"""
        from tkinter import scrolledtext
        import accounting
        
        from tkinter import messagebox
        messagebox.showinfo("Info", "Profit & Loss statement feature is available in the Accounting module. Use Sales Report for revenue tracking.")
    
    def show_balance_sheet(self):
        """Show balance sheet"""
        from tkinter import scrolledtext
        import accounting
        
        from tkinter import messagebox
        messagebox.showinfo("Info", "Balance Sheet feature is available in the Accounting module. Use Sales Report for financial tracking.")
    
    def create_purchase_tab(self, notebook):
        """Create purchase management tab"""
        pur_frame = tk.Frame(notebook, bg='white')
        notebook.add(pur_frame, text="Purchases")
        
        title = tk.Label(
            pur_frame,
            text="Purchase & Supplier Management",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        info_label = tk.Label(
            pur_frame,
            text="Purchase management features coming soon...\n\nAccess via Purchase Management Module",
            font=('Arial', 11),
            bg='white',
            fg='#7f8c8d',
            justify='center'
        )
        info_label.pack(pady=50)
    
    def create_staff_tab(self, notebook):
        """Create staff management tab"""
        staff_frame = tk.Frame(notebook, bg='white')
        notebook.add(staff_frame, text="Staff")
        
        title = tk.Label(
            staff_frame,
            text="Staff & Payroll Management",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        info_label = tk.Label(
            staff_frame,
            text="Staff management features coming soon...\n\nAccess via Staff Management Module",
            font=('Arial', 11),
            bg='white',
            fg='#7f8c8d',
            justify='center'
        )
        info_label.pack(pady=50)
    
    def create_analytics_tab(self, notebook):
        """Create analytics dashboard tab"""
        analytics_frame = tk.Frame(notebook, bg='white')
        notebook.add(analytics_frame, text="Analytics")
        
        title = tk.Label(
            analytics_frame,
            text="Analytics Dashboard",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        info_label = tk.Label(
            analytics_frame,
            text="Analytics dashboard coming soon...\n\nAccess via Analytics Module",
            font=('Arial', 11),
            bg='white',
            fg='#7f8c8d',
            justify='center'
        )
        info_label.pack(pady=50)
    
    def create_backup_tab(self, notebook):
        """Create backup & security tab"""
        backup_frame = tk.Frame(notebook, bg='white')
        notebook.add(backup_frame, text="Backup & Security")
        
        title = tk.Label(
            backup_frame,
            text="Backup & Data Management",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        title.pack(pady=20)
        
        info_label = tk.Label(
            backup_frame,
            text="Backup & security features coming soon...\n\nAccess via Backup Manager Module",
            font=('Arial', 11),
            bg='white',
            fg='#7f8c8d',
            justify='center'
        )
        info_label.pack(pady=50)
