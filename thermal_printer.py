"""
Thermal Printer Module - ESC/POS
Using python-escpos library for reliable thermal printing
"""

import platform
from escpos.printer import Dummy

class ThermalPrinter:
    def __init__(self, printer_name=None):
        """
        Initialize thermal printer
        Args:
            printer_name: Name of printer (optional, uses default if None)
        """
        self.printer_name = printer_name
        
        # Hardcoded optimal settings for thermal printers
        self.margin_top = 0.1
        self.margin_bottom = 0.1
        self.margin_left = 0.1
        self.margin_right = 0.1
        self.paper_size = "58mm"
        self.font_family = "Courier"
        self.font_size = "10"
        self.font_style = "Normal"
        self.line_spacing = 1.0
        self.auto_cut = True
        
        # Create a dummy printer that outputs to Windows raw printer
        self.p = Dummy()
        
    def _print_to_windows_printer(self, content):
        """Send content to Windows printer using raw printing"""
        try:
            if platform.system() == 'Windows':
                import win32print
                
                # Get printer handle
                if self.printer_name:
                    printer_handle = win32print.OpenPrinter(self.printer_name)
                else:
                    default_printer = win32print.GetDefaultPrinter()
                    printer_handle = win32print.OpenPrinter(default_printer)
                
                try:
                    # content is already bytes (from _raw), just use it directly
                    output = content if isinstance(content, bytes) else content.encode('latin1', errors='ignore')
                    
                    # Start print job
                    job = win32print.StartDocPrinter(printer_handle, 1, ("Billing", None, "RAW"))
                    win32print.StartPagePrinter(printer_handle)
                    
                    # Send output to printer
                    import array
                    arr = array.array('B', output)
                    win32print.WritePrinter(printer_handle, arr)
                    
                    # End job
                    win32print.EndPagePrinter(printer_handle)
                    win32print.EndDocPrinter(printer_handle)
                    
                finally:
                    win32print.ClosePrinter(printer_handle)
                
                return True
            return False
        except Exception as e:
            print(f"Printer error: {e}")
            return False
    
    def print_bill(self, restaurant_name, table_number, items, 
                   subtotal, service_charge, gst_amount, total_amount, 
                   order_id, date, currency="₹"):
        """
        Print complete bill - Optimized for 58mm thermal printer
        Args:
            restaurant_name: Restaurant name
            table_number: Table number
            items: List of items with name, plate_type, price
            subtotal: Subtotal amount
            service_charge: Service charge
            gst_amount: GST amount
            total_amount: Total amount
            order_id: Order ID
            date: Date/time string
            currency: Currency symbol
        """
        try:
            # Replace Rupee symbol with 'Rs.' for thermal printer compatibility
            if currency == '₹':
                currency_print = 'Rs.'
            else:
                currency_print = currency
            
            # Build bill using python-escpos methods
            # Reset internal buffer
            self.p._buffer = b''
            
            # Reset printer
            self.p.hw('init')
            
            # Set font to condensed mode for maximum characters per line on 58mm paper
            # First select font A (standard font)
            self.p._raw(b'\x1B\x4D\x00')  # ESC M (Select character font) - 00 = Font A
            # Enable condensed mode for narrow characters (50% reduction)
            self.p._raw(b'\x0F')  # SI command - Enable condensed mode
            
            # Initialize printer with optimal settings for 58mm paper
            # Add top margin with newlines
            self.p._raw(b'\x0A\x0A')
            
            # For 58mm paper - Match sample format with 32 characters per line
            # Top separator
            self.p.set(align='center', bold=False)
            self.p.text('=' * 32 + '\n')
            
            # Restaurant name (centered, bold)
            self.p.set(align='center', bold=True)
            restaurant_display = f"  {restaurant_name.upper()}"[:32]
            self.p.text(restaurant_display + '\n')
            
            # Empty line
            self.p.set(align='center', bold=False)
            self.p.text('     ' + '\n')
            
            # Bottom separator
            self.p.text('=' * 32 + '\n')
            
            # Order details - Using real invoice number
            self.p.set(align='left')
            self.p.text(f'INV: #{order_id:05d}\n')
            self.p.text(f'DATE: {date}\n')
            self.p.text(f'TABLE: {table_number}\n')
            self.p.text('-' * 32 + '\n')
            self.p.text('\n')  # Empty line
            self.p.text('ITEM                   AMT\n')
            self.p.text('-' * 32 + '\n')
            
            # Print items with full name on multiple lines if needed
            for idx, item in enumerate(items, 1):
                name = item['name']
                plate_type = item['plate_type'].upper()
                price = item['price']
                
                # Format item name with plate type: "Item Name (TYPE)"
                item_name = f'{name} ({plate_type})'
                
                # If item name is longer than 20 chars, split into multiple lines
                if len(item_name) > 20:
                    # First line: First 20 chars of item name
                    item_part = item_name[:20]
                    self.p.text(item_part + '\n')
                    # Second line: Remaining chars + amount (right-aligned at position 32)
                    remaining = item_name[20:]
                    # Calculate how many spaces needed to align amount at char 32
                    remaining_len = len(remaining)
                    # Amount should be at position 21-32 (12 chars)
                    spaces_needed = 20 - remaining_len
                    amt_part = f'{price:.2f}'.rjust(12)
                    item_line = remaining.ljust(20) + amt_part + '\n'
                    self.p.text(item_line)
                else:
                    # Single line: Full item name + amount
                    item_part = item_name.ljust(20)
                    amt_part = f'{price:.2f}'.rjust(12)
                    item_line = item_part + amt_part + '\n'
                    self.p.text(item_line)
            
            # Print totals in the same format as sample
            self.p.text('-' * 32 + '\n')
            
            # Format: "LABEL:                   AMOUNT"
            # Label is left-aligned (20 chars), amount is right-aligned (12 chars)
            
            # Subtotal
            label = 'SUBTOTAL:'.ljust(20)
            amount = f'{subtotal:.2f}'.rjust(12)
            self.p.text(label + amount + '\n')
            
            if service_charge > 0:
                label = 'SERVICE:'.ljust(20)
                amount = f'{service_charge:.2f}'.rjust(12)
                self.p.text(label + amount + '\n')
            
            if gst_amount > 0:
                label = 'CGST:'.ljust(20)
                amount = f'{(gst_amount/2):.2f}'.rjust(12)
                self.p.text(label + amount + '\n')
                label = 'SGST:'.ljust(20)
                amount = f'{(gst_amount/2):.2f}'.rjust(12)
                self.p.text(label + amount + '\n')
            
            self.p.text('-' * 32 + '\n')
            
            # Total (bold)
            self.p.set(bold=True)
            label = 'TOTAL:'.ljust(20)
            amount = f'{total_amount:.2f}'.rjust(12)
            self.p.text(label + amount + '\n')
            self.p.set(bold=False)
            self.p.text('-' * 32 + '\n')
            
            # Print footer (centered "THANK YOU")
            self.p.set(align='center')
            self.p.text('        THANK YOU!' + '\n')
            self.p.text('\n')  # Empty line
            self.p.text('=' * 32 + '\n')
            self.p.text('\n')  # Empty line
            self.p.text('=' * 32 + '\n')
            
            # Feed paper for continuous paper (no cut needed)
            self.p._raw(b'\x1B\x64\x08')  # ESC d 8 (Feed 8 lines - enough space for tearing)
            
            # Get the raw output and send to Windows printer
            # output is a property that returns bytes
            content = self.p.output
            return self._print_to_windows_printer(content)
            
        except Exception as e:
            print(f"Print error: {e}")
            return False


def list_available_printers():
    """List available printers"""
    try:
        if platform.system() == 'Windows':
            import win32print
            printers = []
            for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1):
                printers.append(printer[2])
            return printers
        else:
            # Linux
            import subprocess
            result = subprocess.run(['lpstat', '-p'], capture_output=True, text=True)
            printers = []
            for line in result.stdout.split('\n'):
                if line.startswith('printer'):
                    printer_name = line.split()[1]
                    printers.append(printer_name)
            return printers
    except Exception as e:
        print(f"Error listing printers: {e}")
        return []


if __name__ == "__main__":
    # Test printer
    print("Thermal Printer Test")
    print("=" * 50)
    
    # List available printers
    printers = list_available_printers()
    print(f"\nAvailable printers:")
    for i, p in enumerate(printers, 1):
        print(f"{i}. {p}")
    
    if printers:
        print("\nTesting printer...")
        printer = ThermalPrinter()
        
        # Test print
        test_items = [
            {'name': 'Clear Soup', 'plate_type': 'single', 'price': 50},
            {'name': 'Chicken Lollipop', 'plate_type': 'full', 'price': 190}
        ]
        
        printer.print_bill(
            restaurant_name="Restaurant",
            table_number="5",
            items=test_items,
            subtotal=240,
            service_charge=0,
            gst_amount=12,
            total_amount=252,
            order_id=1,
            date="15/01/2025 14:30:25",
            currency="₹"
        )
        
        print("Print test completed!")
    else:
        print("\nNo printers found!")
