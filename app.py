"""
HUNGER Family Restaurant - Billing Software
Complete Order Management, Billing, Thermal Printing, Admin Panel, Inventory, Accounting, Purchase, Staff Management, Analytics Dashboard, Backup System & Automation

License: Warchaswaa Media Pvt Ltd
© 2024 All rights reserved
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import database
import telegram_notifier
import telegram_bot
import thermal_printer
import admin_panel
import inventory_manager
import accounting
import sqlite3
from datetime import datetime

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HUNGER Family Restaurant - Billing Software")
        
        # Fullscreen setup
        self.fullscreen = True
        self.root.attributes('-fullscreen', True)
        self.root.configure(background='#f5f5f5')
        
        # Bind keys
        self.root.bind('<F11>', self.toggle_fullscreen)
        self.root.bind('<Escape>', self.exit_fullscreen)
        
        # Initialize data
        self.categories = []
        self.menu_items = {}
        self.current_category = None
        self.order_cart = []
        
        # Load data
        self.load_restaurant_data()
        self.load_categories()
        
        # Create UI
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Load default category
        if self.categories:
            self.select_category(self.categories[0])
        
        # Start Telegram bot polling
        telegram_bot.start_bot_polling()
    
    def load_restaurant_data(self):
        """Load restaurant settings"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM restaurant_settings WHERE id = 1")
        settings = cursor.fetchone()
        
        if settings:
            self.restaurant_name = settings[1] if settings[1] else "HUNGER Family Restaurant"
            self.currency = settings[6] if settings[6] else "₹"
        else:
            self.restaurant_name = "HUNGER Family Restaurant"
            self.currency = "₹"
        
        # Check telegram status
        cursor.execute("SELECT enabled FROM telegram_settings WHERE id = 1")
        telegram = cursor.fetchone()
        self.telegram_enabled = telegram[0] if telegram else False
        
        conn.close()
    
    def load_categories(self):
        """Load all categories"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM categories ORDER BY name")
        rows = cursor.fetchall()
        self.categories = [row[0] for row in rows]
        
        conn.close()
    
    def create_header(self):
        """Create header with restaurant name and Telegram status"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Restaurant name
        title_label = tk.Label(
            header_frame,
            text=self.restaurant_name.upper(),
            font=('Arial', 24, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(side='left', padx=20, pady=20)
        
        # Right side frame for status buttons
        status_frame = tk.Frame(header_frame, bg='#2c3e50')
        status_frame.pack(side='right', padx=20, pady=10)
        
        # Check if restaurant is open/closed
        self.restaurant_open = self.get_restaurant_status()
        
        # Open/Close button
        self.status_btn = tk.Button(
            status_frame,
            text="✓ OPEN" if self.restaurant_open else "✗ CLOSED",
            font=('Arial', 12, 'bold'),
            bg='#27ae60' if self.restaurant_open else '#e74c3c',
            fg='white',
            activebackground='#229954' if self.restaurant_open else '#c0392b',
            relief='flat',
            padx=20,
            pady=5,
            command=self.toggle_restaurant_status
        )
        self.status_btn.pack(side='left', padx=5)
        
        # Telegram status
        telegram_status = "✓ Telegram Active" if self.telegram_enabled else "Telegram Disabled"
        telegram_label = tk.Label(
            status_frame,
            text=telegram_status,
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#3498db' if self.telegram_enabled else '#95a5a6'
        )
        telegram_label.pack(side='left', padx=10)
        
        # Clock
        self.clock_label = tk.Label(
            status_frame,
            text="",
            font=('Arial', 12),
            bg='#2c3e50',
            fg='white'
        )
        self.clock_label.pack(side='left', padx=10)
        self.update_clock()
    
    def update_clock(self):
        """Update clock every second"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
    
    def get_restaurant_status(self):
        """Check if restaurant is currently open"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get latest open/close status from restaurant_status table
        try:
            cursor.execute("SELECT is_open FROM restaurant_status ORDER BY timestamp DESC LIMIT 1")
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return bool(result[0])
            else:
                # Default to open if no status recorded
                return True
        except sqlite3.OperationalError:
            # Table doesn't exist yet
            conn.close()
            return True
    
    def toggle_restaurant_status(self):
        """Toggle restaurant open/close status"""
        # Toggle status
        self.restaurant_open = not self.restaurant_open
        
        # Update database
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Create restaurant_status table if it doesn't exist
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS restaurant_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    is_open INTEGER NOT NULL,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Insert status change
            cursor.execute("""
                INSERT INTO restaurant_status (is_open, timestamp)
                VALUES (?, ?)
            """, (1 if self.restaurant_open else 0, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            conn.commit()
        except Exception as e:
            print(f"Error updating restaurant status: {e}")
        finally:
            conn.close()
        
        # Update button appearance
        if self.restaurant_open:
            self.status_btn.config(
                text="✓ OPEN",
                bg='#27ae60',
                activebackground='#229954'
            )
        else:
            self.status_btn.config(
                text="✗ CLOSED",
                bg='#e74c3c',
                activebackground='#c0392b'
            )
        
        # Show notification
        messagebox.showinfo(
            "Restaurant Status",
            "Restaurant is now " + ("OPEN" if self.restaurant_open else "CLOSED")
        )
    
    def create_main_content(self):
        """Create main content area with left, center, and right panels"""
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left Panel - Category Navigation
        self.create_category_panel(main_frame)
        
        # Center Panel - Menu Items
        self.create_menu_panel(main_frame)
        
        # Right Panel - Order Cart
        self.create_cart_panel(main_frame)
    
    def create_category_panel(self, parent):
        """Create category navigation panel"""
        category_frame = tk.LabelFrame(
            parent,
            text="CATEGORIES",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50',
            width=250
        )
        category_frame.pack(side='left', fill='both', padx=(0, 5))
        category_frame.pack_propagate(False)
        
        # Category buttons
        self.category_buttons = {}
        for category in self.categories:
            btn = tk.Button(
                category_frame,
                text=category,
                font=('Arial', 10, 'bold'),
                bg='#3498db',
                fg='white',
                activebackground='#2980b9',
                activeforeground='white',
                relief='flat',
                height=2,
                command=lambda c=category: self.select_category(c)
            )
            btn.pack(fill='x', padx=5, pady=3)
            self.category_buttons[category] = btn
    
    def create_menu_panel(self, parent):
        """Create menu items display panel"""
        menu_frame = tk.LabelFrame(
            parent,
            text="MENU",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        menu_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Search box
        search_frame = tk.Frame(menu_frame, bg='white')
        search_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(
            search_frame,
            text="🔍 Search All Items:",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left', padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Arial', 11),
            width=30
        )
        search_entry.pack(side='left', padx=5, fill='x', expand=True)
        
        # Clear search button
        clear_btn = tk.Button(
            search_frame,
            text="✕",
            font=('Arial', 9),
            bg='#e74c3c',
            fg='white',
            width=3,
            command=lambda: self.search_var.set('')
        )
        clear_btn.pack(side='left', padx=2)
        
        # Canvas with scrollbar for menu items
        canvas = tk.Canvas(menu_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(menu_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='white')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        self.menu_container = scrollable_frame
        
        # Configure grid columns for equal distribution
        for i in range(3):
            self.menu_container.grid_columnconfigure(i, weight=1, uniform="menu_col")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_cart_panel(self, parent):
        """Create order cart panel"""
        cart_frame = tk.LabelFrame(
            parent,
            text="ORDER CART",
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50',
            width=350
        )
        cart_frame.pack(side='right', fill='both', padx=(5, 0))
        cart_frame.pack_propagate(False)
        
        # Cart items counter
        count_frame = tk.Frame(cart_frame, bg='white')
        count_frame.pack(fill='x', padx=5, pady=(5, 0))
        
        tk.Label(
            count_frame,
            text="Items:",
            font=('Arial', 9),
            bg='white',
            fg='#7f8c8d'
        ).pack(side='left')
        
        self.cart_count_label = tk.Label(
            count_frame,
            text="0",
            font=('Arial', 9, 'bold'),
            bg='white',
            fg='#3498db'
        )
        self.cart_count_label.pack(side='left', padx=5)
        
        # Cart items display with scrollbar using Canvas for better control
        cart_display_frame = tk.Frame(cart_frame, bg='white')
        cart_display_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create a canvas with scrollbar
        self.cart_canvas = tk.Canvas(cart_display_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar_cart = ttk.Scrollbar(cart_display_frame, orient="vertical", command=self.cart_canvas.yview)
        self.cart_scrollable_frame = tk.Frame(self.cart_canvas)
        
        self.cart_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))
        )
        
        self.cart_canvas.create_window((0, 0), window=self.cart_scrollable_frame, anchor="nw")
        self.cart_canvas.configure(yscrollcommand=scrollbar_cart.set)
        
        self.cart_canvas.pack(side='left', fill='both', expand=True)
        scrollbar_cart.pack(side='right', fill='y')
        
        # Total display
        total_frame = tk.Frame(cart_frame, bg='white')
        total_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(
            total_frame,
            text="TOTAL:",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        ).pack(side='left')
        
        self.total_label = tk.Label(
            total_frame,
            text=f"{self.currency} 0.00",
            font=('Arial', 14, 'bold'),
            bg='white',
            fg='#e74c3c'
        )
        self.total_label.pack(side='right')
    
    def create_footer(self):
        """Create footer with action buttons"""
        footer_frame = tk.Frame(self.root, bg='#34495e', height=60)
        footer_frame.pack(fill='x', pady=(10, 0))
        footer_frame.pack_propagate(False)
        
        # New Order button
        btn_new_order = tk.Button(
            footer_frame,
            text="NEW ORDER",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            activebackground='#2980b9',
            activeforeground='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.new_order
        )
        btn_new_order.pack(side='left', padx=10, pady=10)
        
        # Generate Bill button
        btn_bill = tk.Button(
            footer_frame,
            text="GENERATE BILL",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            activebackground='#229954',
            activeforeground='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.generate_bill
        )
        btn_bill.pack(side='left', padx=10, pady=10)
        
        # Settings button
        btn_settings = tk.Button(
            footer_frame,
            text="SETTINGS",
            font=('Arial', 12, 'bold'),
            bg='#95a5a6',
            fg='white',
            activebackground='#7f8c8d',
            activeforeground='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.open_settings
        )
        btn_settings.pack(side='right', padx=10, pady=10)
        
        # Fullscreen hint
        hint_label = tk.Label(
            footer_frame,
            text="F11: Toggle Fullscreen | ESC: Exit Fullscreen",
            font=('Arial', 9),
            bg='#34495e',
            fg='#bdc3c7'
        )
        hint_label.pack(side='right', padx=10)
        
        # Copyright notice with version
        copyright_label = tk.Label(
            footer_frame,
            text="© 2025 Warchaswaa Media Pvt Ltd. All Rights Reserved. | Version 1.2",
            font=('Arial', 8),
            bg='#34495e',
            fg='#bdc3c7'
        )
        copyright_label.pack(side='left', padx=10)
    
    def select_category(self, category):
        """Select a category and display its menu items"""
        self.current_category = category
        
        # Update button states
        for cat, btn in self.category_buttons.items():
            if cat == category:
                btn.config(bg='#2980b9')
            else:
                btn.config(bg='#3498db')
        
        # Clear and load menu items
        for widget in self.menu_container.winfo_children():
            widget.destroy()
        
        self.load_menu_items(category)
    
    def load_menu_items(self, category):
        """Load menu items for selected category"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Load all items including those with price 0 (not available)
        cursor.execute("""
            SELECT id, name, price_single, price_full, food_type, is_available
            FROM menu_items 
            WHERE category = ?
            ORDER BY name
        """, (category,))
        
        items = cursor.fetchall()
        conn.close()
        
        if not items:
            no_item_label = tk.Label(
                self.menu_container,
                text="No items available in this category",
                font=('Arial', 12),
                bg='white',
                fg='#7f8c8d'
            )
            no_item_label.grid(row=0, column=0, pady=50)
            return
        
        # Display menu items in grid layout (3 columns)
        for idx, item in enumerate(items):
            item_id, name, price_single, price_full, food_type, is_available = item
            
            # Determine if item is available (price > 0)
            available = is_available == 1 and price_single is not None and price_single > 0
            
            # Calculate grid position
            row = idx // 3
            col = idx % 3
            
            # Use different background for unavailable items
            bg_color = '#d5d8dc' if not available else '#ecf0f1'
            
            # Create card frame with fixed width
            item_frame = tk.Frame(
                self.menu_container,
                bg=bg_color,
                relief='raised',
                borderwidth=1,
                width=280
            )
            item_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            item_frame.grid_propagate(False)
            
            # Item name and type
            name_frame = tk.Frame(item_frame, bg=bg_color)
            name_frame.pack(fill='x', padx=10, pady=8)
            
            # Food type indicator
            type_color = '#27ae60' if food_type == 'veg' else '#e74c3c'
            tk.Label(
                name_frame,
                text="●" if food_type == 'veg' else "●",
                font=('Arial', 16),
                bg=bg_color,
                fg=type_color
            ).pack(side='left', padx=(0, 5))
            
            name_color = '#7f8c8d' if not available else '#2c3e50'
            tk.Label(
                name_frame,
                text=name + (" (Price Pending)" if not available else ""),
                font=('Arial', 10, 'bold' if available else 'normal'),
                bg=bg_color,
                fg=name_color,
                wraplength=180
            ).pack(side='left', padx=(0, 10))
            
            # Price display
            price_frame = tk.Frame(item_frame, bg=bg_color)
            price_frame.pack(fill='x', padx=10, pady=5)
            
            if available:
                if price_full:
                    price_text = f"{self.currency} {price_single:.0f} / {self.currency} {price_full:.0f}"
                else:
                    price_text = f"{self.currency} {price_single:.0f}"
                
                tk.Label(
                    price_frame,
                    text=price_text,
                    font=('Arial', 9, 'bold'),
                    bg=bg_color,
                    fg='#27ae60'
                ).pack(side='left')
            else:
                tk.Label(
                    price_frame,
                    text="Price Pending",
                    font=('Arial', 9, 'italic'),
                    bg=bg_color,
                    fg='#7f8c8d'
                ).pack(side='left')
            
            # Add buttons
            button_frame = tk.Frame(item_frame, bg=bg_color)
            button_frame.pack(fill='x', padx=10, pady=(0, 10))
            
            if available and price_single is not None:
                if price_full:
                    btn_single = tk.Button(
                        button_frame,
                        text=f"SINGLE\n{self.currency} {price_single:.0f}",
                        font=('Arial', 8, 'bold'),
                        bg='#3498db',
                        fg='white',
                        activebackground='#2980b9',
                        relief='flat',
                        padx=8,
                        pady=8,
                        command=lambda i=item_id, p=price_single, t='single': self.add_to_cart(i, name, p, t)
                    )
                    btn_single.pack(side='left', padx=(0, 5), fill='both', expand=True)
                    
                    btn_full = tk.Button(
                        button_frame,
                        text=f"FULL\n{self.currency} {price_full:.0f}",
                        font=('Arial', 8, 'bold'),
                        bg='#27ae60',
                        fg='white',
                        activebackground='#229954',
                        relief='flat',
                        padx=8,
                        pady=8,
                        command=lambda i=item_id, p=price_full, t='full': self.add_to_cart(i, name, p, t)
                    )
                    btn_full.pack(side='left', fill='both', expand=True)
                else:
                    btn_add = tk.Button(
                        button_frame,
                        text=f"ADD\n{self.currency} {price_single:.0f}",
                        font=('Arial', 8, 'bold'),
                        bg='#9b59b6',
                        fg='white',
                        activebackground='#8e44ad',
                        relief='flat',
                        padx=8,
                        pady=8,
                        command=lambda i=item_id, p=price_single, t='single': self.add_to_cart(i, name, p, t)
                    )
                    btn_add.pack(fill='x')
            else:
                # Unavailable item - no buttons
                tk.Label(
                    button_frame,
                    text="Not Available",
                    font=('Arial', 9, 'italic'),
                    bg=bg_color,
                    fg='#7f8c8d'
                ).pack()
    
    def on_search_change(self, *args):
        """Handle search text change"""
        self.apply_search_filter()
    
    def apply_search_filter(self):
        """Apply search filter across all categories"""
        if not hasattr(self, 'search_var'):
            return
        
        search_text = self.search_var.get().lower().strip()
        
        # Clear and reload with filter
        for widget in self.menu_container.winfo_children():
            widget.destroy()
        
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if search_text:
            # Search across all categories
            cursor.execute("""
                SELECT id, name, price_single, price_full, food_type, is_available, category
                FROM menu_items 
                WHERE name LIKE ?
                ORDER BY category, name
            """, (f'%{search_text}%',))
        else:
            # If no search text, show current category items
            if self.current_category:
                cursor.execute("""
                    SELECT id, name, price_single, price_full, food_type, is_available, category
                    FROM menu_items 
                    WHERE category = ?
                    ORDER BY name
                """, (self.current_category,))
            else:
                conn.close()
                return
        
        items = cursor.fetchall()
        conn.close()
        
        if not items:
            no_item_label = tk.Label(
                self.menu_container,
                text="No items found" if search_text else "No items available in this category",
                font=('Arial', 12),
                bg='white',
                fg='#7f8c8d'
            )
            no_item_label.grid(row=0, column=0, pady=50)
            return
        
        # Display filtered items
        for idx, item in enumerate(items):
            item_id, name, price_single, price_full, food_type, is_available, category = item
            
            available = is_available == 1 and price_single is not None and price_single > 0
            
            # Determine background color
            bg_color = '#ecf0f1'
            
            # Create item frame
            item_frame = tk.Frame(self.menu_container, bg=bg_color, relief='solid', bd=1)
            row = idx // 3
            col = idx % 3
            item_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
            
            # Item name with category (if searching)
            if search_text:
                item_text = f"{name}\n({category})"
            else:
                item_text = name
                
            tk.Label(
                item_frame,
                text=item_text,
                font=('Arial', 10, 'bold'),
                bg=bg_color,
                fg='#2c3e50',
                wraplength=200,
                justify='center'
            ).pack(pady=(10, 5))
            
            # Price display
            if available and price_single is not None:
                if price_full:
                    price_text = f"{self.currency} {price_single:.0f} / {self.currency} {price_full:.0f}"
                else:
                    price_text = f"{self.currency} {price_single:.0f}"
                tk.Label(
                    item_frame,
                    text=price_text,
                    font=('Arial', 9),
                    bg=bg_color,
                    fg='#27ae60'
                ).pack()
            else:
                tk.Label(
                    item_frame,
                    text="Price Pending",
                    font=('Arial', 9, 'italic'),
                    bg=bg_color,
                    fg='#7f8c8d'
                ).pack()
            
            # Add buttons
            button_frame = tk.Frame(item_frame, bg=bg_color)
            button_frame.pack(fill='x', padx=10, pady=(0, 10))
            
            if available and price_single is not None:
                if price_full:
                    btn_single = tk.Button(
                        button_frame,
                        text=f"SINGLE\n{self.currency} {price_single:.0f}",
                        font=('Arial', 8, 'bold'),
                        bg='#3498db',
                        fg='white',
                        activebackground='#2980b9',
                        relief='flat',
                        padx=8,
                        pady=8,
                        command=lambda i=item_id, p=price_single, t='single': self.add_to_cart(i, name, p, t)
                    )
                    btn_single.pack(side='left', padx=(0, 5), fill='both', expand=True)
                    
                    btn_full = tk.Button(
                        button_frame,
                        text=f"FULL\n{self.currency} {price_full:.0f}",
                        font=('Arial', 8, 'bold'),
                        bg='#27ae60',
                        fg='white',
                        activebackground='#229954',
                        relief='flat',
                        padx=8,
                        pady=8,
                        command=lambda i=item_id, p=price_full, t='full': self.add_to_cart(i, name, p, t)
                    )
                    btn_full.pack(side='left', fill='both', expand=True)
                else:
                    btn_add = tk.Button(
                        button_frame,
                        text=f"ADD\n{self.currency} {price_single:.0f}",
                        font=('Arial', 9, 'bold'),
                        bg='#3498db',
                        fg='white',
                        activebackground='#2980b9',
                        relief='flat',
                        padx=8,
                        pady=8,
                        command=lambda i=item_id, p=price_single, t='single': self.add_to_cart(i, name, p, t)
                    )
                    btn_add.pack(fill='x')
            else:
                tk.Label(
                    button_frame,
                    text="Not Available",
                    font=('Arial', 9, 'italic'),
                    bg=bg_color,
                    fg='#7f8c8d'
                ).pack()
    
    def add_to_cart(self, item_id, name, price, plate_type):
        """Add item to cart"""
        self.order_cart.append({
            'item_id': item_id,
            'name': name,
            'price': price,
            'plate_type': plate_type
        })
        self.update_cart_display()
    
    def update_cart_display(self):
        """Update cart display and total"""
        # Clear all widgets in cart_scrollable_frame
        for widget in self.cart_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Update cart count
        cart_count = len(self.order_cart)
        self.cart_count_label.config(text=str(cart_count))
        
        if not self.order_cart:
            empty_label = tk.Label(
                self.cart_scrollable_frame,
                text="Cart is empty",
                font=('Arial', 11),
                bg='#f8f9fa',
                fg='#7f8c8d'
            )
            empty_label.pack(pady=20)
            self.total_label.config(text=f"{self.currency} 0.00")
            return
        
        # Display cart items
        total = 0
        for idx, item in enumerate(self.order_cart):
            # Create frame for each cart item
            item_frame = tk.Frame(self.cart_scrollable_frame, bg='white', relief='solid', bd=1)
            item_frame.pack(fill='x', padx=2, pady=2)
            
            # Item info on the left
            item_info_frame = tk.Frame(item_frame, bg='white')
            item_info_frame.pack(side='left', fill='both', expand=True)
            
            item_label = tk.Label(
                item_info_frame,
                text=f"{idx+1}. {item['name']}\n    {item['plate_type'].upper()} - {self.currency} {item['price']:.0f}",
                font=('Arial', 10),
                bg='white',
                fg='#2c3e50',
                anchor='w',
                justify='left'
            )
            item_label.pack(side='left', padx=5, pady=5)
            
            # Remove button on the right
            remove_btn = tk.Button(
                item_frame,
                text="✕",
                font=('Arial', 12, 'bold'),
                bg='#e74c3c',
                fg='white',
                width=3,
                cursor='hand2',
                command=lambda i=idx: self.remove_from_cart(i)
            )
            remove_btn.pack(side='right', padx=5, pady=5)
            
            total += item['price']
        
        # Update total
        self.total_label.config(text=f"{self.currency} {total:.2f}")
    
    def remove_from_cart(self, index):
        """Remove item from cart by index"""
        if 0 <= index < len(self.order_cart):
            self.order_cart.pop(index)
            self.update_cart_display()
    
    def new_order(self):
        """Clear current order"""
        if self.order_cart:
            if messagebox.askyesno("New Order", "Clear current order and start new?"):
                self.order_cart = []
                self.update_cart_display()
    
    def generate_bill(self):
        """Generate bill for current order"""
        if not self.order_cart:
            messagebox.showwarning("Empty Cart", "Please add items to cart first")
            return
        
        # Ask for table number
        table_number = simpledialog.askstring(
            "Table Number",
            "Enter table number (or leave empty for takeaway):",
            initialvalue=""
        )
        
        if table_number is None:
            return  # User cancelled
        
        # Calculate totals
        subtotal = sum(item['price'] for item in self.order_cart)
        
        # Get restaurant settings for GST and service charge
        conn = database.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT gst_enabled, service_charge_rate FROM restaurant_settings WHERE id = 1")
        settings = cursor.fetchone()
        
        gst_enabled = settings[0] if settings[0] else 0
        service_charge_rate = settings[1] if settings[1] else 0
        
        service_charge = (subtotal * service_charge_rate / 100) if service_charge_rate > 0 else 0
        gst_amount = (subtotal * 0.05) if gst_enabled else 0
        total_amount = subtotal + service_charge + gst_amount
        
        conn.close()
        
        # Create bill window
        self.show_bill_window(table_number, self.order_cart, subtotal, service_charge, gst_amount, total_amount)
    
    def show_bill_window(self, table_number, items, subtotal, service_charge, gst_amount, total_amount):
        """Show bill window with payment options"""
        # Create bill window
        bill_window = tk.Toplevel(self.root)
        bill_window.title("Bill")
        bill_window.geometry("600x700")
        bill_window.configure(bg='#f5f5f5')
        
        # Make it modal
        bill_window.transient(self.root)
        bill_window.grab_set()
        
        # Bill header
        header_frame = tk.Frame(bill_window, bg='#2c3e50', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text=f"{self.restaurant_name.upper()} - BILL",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        ).pack(pady=20)
        
        # Bill content
        content_frame = tk.Frame(bill_window, bg='white')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Bill details
        bill_text = tk.Text(
            content_frame,
            font=('Courier', 10),
            bg='white',
            wrap='word',
            height=25
        )
        bill_text.pack(fill='both', expand=True, pady=10)
        
        # Build bill text - Matching 58mm thermal printer format
        bill_content = f"{'':^50}\n"
        bill_content += f"{self.restaurant_name.upper():^50}\n"
        bill_content += f"{'':^50}\n"
        bill_content += f"{'-'*50}\n"
        bill_content += "INV: #PREVIEW\n"
        bill_content += f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
        bill_content += f"Table: {table_number if table_number else 'Takeaway'}\n"
        bill_content += f"{'-'*50}\n\n"
        
        # Items with optimized spacing for 58mm printer
        for idx, item in enumerate(items, 1):
            name = item['name']
            # Truncate long names
            if len(name) > 18:
                name = name[:15] + "..."
            
            plate_type = item['plate_type'].upper()
            price = item['price']
            
            # Format to match thermal printer layout
            bill_content += f"{idx}. {name}\n"
            
            # Plate type and price with proper spacing
            plate_display = f"   {plate_type}"[:10]
            price_display = f"{self.currency} {price:.0f}"[:14]
            spacing = ' ' * (22 - len(plate_display))
            bill_content += f"{plate_display}{spacing}{price_display}\n\n"
        
        bill_content += f"{'-'*50}\n"
        bill_content += f"Subtotal         {self.currency} {subtotal:7.2f}\n"
        
        if service_charge > 0:
            bill_content += f"Service Charge   {self.currency} {service_charge:7.2f}\n"
        
        if gst_amount > 0:
            bill_content += f"GST (5%)         {self.currency} {gst_amount:7.2f}\n"
        
        bill_content += f"{'='*50}\n"
        bill_content += f"TOTAL            {self.currency} {total_amount:7.2f}\n"
        bill_content += f"{'='*50}\n\n"
        
        # Add footer
        bill_content += f"{'':^50}\n"
        bill_content += f"{'THANK YOU':^50}\n"
        bill_content += f"{'VISIT AGAIN':^50}\n"
        bill_content += f"{'':^50}\n"
        
        bill_text.insert('1.0', bill_content)
        bill_text.config(state='disabled')
        
        # Add Print Bill button before payment buttons
        def print_bill_now():
            """Print bill to thermal printer"""
            try:
                printer = thermal_printer.ThermalPrinter(printer_name="POS-58")
                printer.print_bill(
                    restaurant_name=self.restaurant_name,
                    table_number=table_number if table_number else "Takeaway",
                    items=items,
                    subtotal=subtotal,
                    service_charge=service_charge,
                    gst_amount=gst_amount,
                    total_amount=total_amount,
                    order_id=999,  # Temporary ID for preview
                    date=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                    currency=self.currency
                )
                messagebox.showinfo("Print Success", "Bill sent to POS-58 printer!")
            except Exception as e:
                messagebox.showerror("Print Error", f"Could not print bill: {e}")
        
        # Print button
        print_btn = tk.Button(
            content_frame,
            text="Print Bill",
            font=('Arial', 11, 'bold'),
            bg='#9b59b6',
            fg='white',
            command=print_bill_now
        )
        print_btn.pack(pady=5)
        
        # Payment buttons
        payment_frame = tk.Frame(content_frame, bg='white')
        payment_frame.pack(fill='x', pady=10)
        
        # Add processing flag to prevent double-clicks
        payment_processing = {'active': False}
        
        def process_payment(mode):
            # Prevent double-clicks
            if payment_processing['active']:
                return
            
            # Set processing flag
            payment_processing['active'] = True
            
            try:
                # Save order to database
                order_id = self.save_order_to_db(table_number, items, subtotal, service_charge, gst_amount, total_amount)
            
                # Record accounting transaction
                accounting.AccountingSystem.record_order_transaction(order_id, total_amount, mode)
                
                # Deduct stock for order
                success, transaction_summary = inventory_manager.InventoryManager.deduct_order_stock(items)
                if not success:
                    print(f"Stock deduction warning: {transaction_summary}")
                
                # Send Telegram notifications
                telegram_notifier.send_new_order_notification(
                    order_id, table_number, items, total_amount
                )
                telegram_notifier.send_payment_notification(
                    order_id, table_number, total_amount, mode
                )
                
                # Print thermal receipt
                try:
                    printer = thermal_printer.ThermalPrinter(printer_name="POS-58")
                    printer.print_bill(
                        restaurant_name=self.restaurant_name,
                        table_number=table_number if table_number else "Takeaway",
                        items=items,
                        subtotal=subtotal,
                        service_charge=service_charge,
                        gst_amount=gst_amount,
                        total_amount=total_amount,
                        order_id=order_id,
                        date=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
                        currency=self.currency
                    )
                except Exception as e:
                    print(f"Print error: {e}")
                    messagebox.showwarning("Print Error", f"Could not print receipt: {e}")
                
                messagebox.showinfo("Success", f"Order #{order_id:03d} processed successfully!")
                
                # Clear cart
                self.order_cart = []
                self.update_cart_display()
                
                # Close bill window
                bill_window.destroy()
            
            except Exception as e:
                messagebox.showerror("Payment Error", f"Failed to process payment: {str(e)}")
            finally:
                # Reset processing flag
                payment_processing['active'] = False
        
        # Payment mode buttons
        btn_cash = tk.Button(
            payment_frame,
            text="Cash Payment",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white',
            command=lambda: process_payment("Cash")
        )
        btn_cash.pack(side='left', expand=True, padx=5)
        
        btn_card = tk.Button(
            payment_frame,
            text="Card Payment",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            command=lambda: process_payment("Card")
        )
        btn_card.pack(side='left', expand=True, padx=5)
        
        btn_upi = tk.Button(
            payment_frame,
            text="UPI Payment",
            font=('Arial', 12, 'bold'),
            bg='#e67e22',
            fg='white',
            command=lambda: process_payment("UPI")
        )
        btn_upi.pack(side='left', expand=True, padx=5)
    
    def save_order_to_db(self, table_number, items, subtotal, service_charge, gst_amount, total_amount):
        """Save order to database"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get business date for restaurant day counting
        business_date = database.get_business_date_string()
        
        # Insert order
        cursor.execute("""
            INSERT INTO orders 
            (table_number, order_date, business_date, total_amount, gst_amount, service_charge, 
             discount, final_amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            table_number,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            business_date,
            subtotal,
            gst_amount,
            service_charge,
            0,
            total_amount,
            'completed'
        ))
        
        order_id = cursor.lastrowid
        
        # Insert order items
        for item in items:
            cursor.execute("""
                INSERT INTO order_items 
                (order_id, menu_item_id, quantity, price, total)
                VALUES (?, ?, ?, ?, ?)
            """, (
                order_id,
                item['item_id'],
                1,
                item['price'],
                item['price']
            ))
        
        conn.commit()
        conn.close()
        
        return order_id
    
    def open_settings(self):
        """Open settings window"""
        admin_panel.AdminPanel(self.root, self)
    
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        self.fullscreen = not self.fullscreen
        self.root.attributes('-fullscreen', self.fullscreen)
    
    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode"""
        self.fullscreen = False
        self.root.attributes('-fullscreen', False)


def main():
    """Main entry point"""
    # Initialize database
    database.init_database()
    
    # Create and run application
    root = tk.Tk()
    app = RestaurantApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
          