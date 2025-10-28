"""
Backup & Data Management System
Handles database backups, data export, security, and audit logs
"""

import database
import shutil
import os
from datetime import datetime, timedelta
import json

class BackupManager:
    """Backup and data management system"""
    
    BACKUP_DIR = "backups"
    
    @staticmethod
    def ensure_backup_directory():
        """Ensure backup directory exists"""
        if not os.path.exists(BackupManager.BACKUP_DIR):
            os.makedirs(BackupManager.BACKUP_DIR)
    
    @staticmethod
    def create_backup(description="Manual backup"):
        """Create database backup"""
        BackupManager.ensure_backup_directory()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"backup_{timestamp}.db"
        backup_path = os.path.join(BackupManager.BACKUP_DIR, backup_filename)
        
        try:
            # Copy database file
            shutil.copy2(database.DATABASE_NAME, backup_path)
            
            # Create metadata file
            metadata = {
                'timestamp': datetime.now().isoformat(),
                'description': description,
                'backup_file': backup_filename,
                'original_db': database.DATABASE_NAME
            }
            
            metadata_file = backup_path.replace('.db', '.json')
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            return True, backup_filename
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def get_backups():
        """Get list of all backups"""
        BackupManager.ensure_backup_directory()
        
        backups = []
        for file in os.listdir(BackupManager.BACKUP_DIR):
            if file.endswith('.db'):
                backup_path = os.path.join(BackupManager.BACKUP_DIR, file)
                metadata_file = backup_path.replace('.db', '.json')
                
                backup_info = {
                    'filename': file,
                    'path': backup_path,
                    'size': os.path.getsize(backup_path),
                    'created': datetime.fromtimestamp(os.path.getmtime(backup_path))
                }
                
                # Try to load metadata
                if os.path.exists(metadata_file):
                    try:
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                            backup_info['description'] = metadata.get('description', '')
                            backup_info['timestamp'] = metadata.get('timestamp', '')
                    except:
                        pass
                
                backups.append(backup_info)
        
        # Sort by creation time (newest first)
        backups.sort(key=lambda x: x['created'], reverse=True)
        return backups
    
    @staticmethod
    def restore_backup(backup_filename):
        """Restore database from backup"""
        backup_path = os.path.join(BackupManager.BACKUP_DIR, backup_filename)
        
        if not os.path.exists(backup_path):
            return False, "Backup file not found"
        
        try:
            # Create a backup of current database before restoring
            current_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safety_backup = f"pre_restore_{current_timestamp}.db"
            shutil.copy2(database.DATABASE_NAME, 
                        os.path.join(BackupManager.BACKUP_DIR, safety_backup))
            
            # Restore from backup
            shutil.copy2(backup_path, database.DATABASE_NAME)
            
            return True, f"Restored from backup. Safety backup created: {safety_backup}"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def delete_backup(backup_filename):
        """Delete a backup file"""
        backup_path = os.path.join(BackupManager.BACKUP_DIR, backup_filename)
        metadata_path = backup_path.replace('.db', '.json')
        
        try:
            if os.path.exists(backup_path):
                os.remove(backup_path)
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
            return True, "Backup deleted"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def cleanup_old_backups(days_to_keep=30):
        """Clean up backups older than specified days"""
        backups = BackupManager.get_backups()
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        deleted_count = 0
        for backup in backups:
            if backup['created'] < cutoff_date:
                success, _ = BackupManager.delete_backup(backup['filename'])
                if success:
                    deleted_count += 1
        
        return deleted_count
    
    @staticmethod
    def get_backup_stats():
        """Get backup statistics"""
        backups = BackupManager.get_backups()
        
        total_size = sum(b['size'] for b in backups)
        total_count = len(backups)
        
        # Oldest and newest backups
        oldest = backups[-1] if backups else None
        newest = backups[0] if backups else None
        
        return {
            'total_backups': total_count,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'oldest_backup': oldest['created'] if oldest else None,
            'newest_backup': newest['created'] if newest else None
        }


class DataExport:
    """Data export functionality"""
    
    @staticmethod
    def export_to_json(data, filename):
        """Export data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            return True, "Export successful"
        except Exception as e:
            return False, str(e)
    
    @staticmethod
    def export_orders_to_json(start_date=None, end_date=None, filename=None):
        """Export orders to JSON"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT o.*, oi.* FROM orders o JOIN order_items oi ON o.id = oi.order_id"
        params = []
        
        if start_date and end_date:
            query += " WHERE DATE(o.order_date) BETWEEN ? AND ?"
            params = [start_date, end_date]
        
        query += " ORDER BY o.order_date DESC"
        
        cursor.execute(query, params)
        
        orders = []
        for row in cursor.fetchall():
            orders.append(dict(row))
        
        conn.close()
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"orders_export_{timestamp}.json"
        
        return DataExport.export_to_json(orders, filename)
    
    @staticmethod
    def export_inventory_to_json(filename=None):
        """Export inventory data to JSON"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get ingredients
        cursor.execute("SELECT * FROM ingredients")
        ingredients = [dict(row) for row in cursor.fetchall()]
        
        # Get stock transactions
        cursor.execute("""
            SELECT st.*, i.name as ingredient_name 
            FROM stock_transactions st
            JOIN ingredients i ON st.ingredient_id = i.id
            ORDER BY st.timestamp DESC
        """)
        transactions = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        data = {
            'ingredients': ingredients,
            'stock_transactions': transactions,
            'export_date': datetime.now().isoformat()
        }
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"inventory_export_{timestamp}.json"
        
        return DataExport.export_to_json(data, filename)
    
    @staticmethod
    def export_accounting_to_json(start_date=None, end_date=None, filename=None):
        """Export accounting data to JSON"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get transactions
        query = "SELECT * FROM transactions"
        params = []
        
        if start_date and end_date:
            query += " WHERE DATE(date) BETWEEN ? AND ?"
            params = [start_date, end_date]
        
        query += " ORDER BY date DESC"
        cursor.execute(query, params)
        transactions = [dict(row) for row in cursor.fetchall()]
        
        # Get expenses
        query = "SELECT * FROM expenses"
        params = []
        
        if start_date and end_date:
            query += " WHERE DATE(date) BETWEEN ? AND ?"
            params = [start_date, end_date]
        
        query += " ORDER BY date DESC"
        cursor.execute(query, params)
        expenses = [dict(row) for row in cursor.fetchall()]
        
        # Get accounts
        cursor.execute("SELECT * FROM accounts")
        accounts = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        data = {
            'transactions': transactions,
            'expenses': expenses,
            'accounts': accounts,
            'export_date': datetime.now().isoformat()
        }
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"accounting_export_{timestamp}.json"
        
        return DataExport.export_to_json(data, filename)
    
    @staticmethod
    def export_staff_data_to_json(filename=None):
        """Export staff data to JSON"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get staff
        cursor.execute("SELECT * FROM staff")
        staff = [dict(row) for row in cursor.fetchall()]
        
        # Get attendance
        cursor.execute("""
            SELECT a.*, s.name as staff_name 
            FROM attendance a
            JOIN staff s ON a.staff_id = s.id
            ORDER BY a.date DESC
        """)
        attendance = [dict(row) for row in cursor.fetchall()]
        
        # Get salary payments
        cursor.execute("""
            SELECT sp.*, s.name as staff_name 
            FROM salary_payments sp
            JOIN staff s ON sp.staff_id = s.id
            ORDER BY sp.year DESC, sp.month DESC
        """)
        salary_payments = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        data = {
            'staff': staff,
            'attendance': attendance,
            'salary_payments': salary_payments,
            'export_date': datetime.now().isoformat()
        }
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"staff_data_export_{timestamp}.json"
        
        return DataExport.export_to_json(data, filename)
    
    @staticmethod
    def export_full_database_backup():
        """Export full database as backup JSON"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        backup_data = {
            'timestamp': datetime.now().isoformat(),
            'tables': {}
        }
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Export each table
        for table in tables:
            cursor.execute(f"SELECT * FROM {table}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            backup_data['tables'][table] = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"full_backup_{timestamp}.json"
        
        return DataExport.export_to_json(backup_data, filename)


class SecurityManager:
    """Security and authentication management"""
    
    @staticmethod
    def create_user_table():
        """Create users table for authentication"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
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
    
    @staticmethod
    def log_audit_event(user_id, username, action, details=None, ip_address=None):
        """Log audit event"""
        SecurityManager.create_user_table()
        
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO audit_logs (user_id, username, action, details, ip_address)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, action, details, ip_address))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_audit_logs(start_date=None, end_date=None, limit=100):
        """Get audit logs"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM audit_logs WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND DATE(timestamp) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(timestamp) <= ?"
            params.append(end_date)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        logs = cursor.fetchall()
        
        conn.close()
        return logs
    
    @staticmethod
    def get_audit_summary(start_date=None, end_date=None):
        """Get audit summary by action type"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        query = "SELECT action, COUNT(*) as count FROM audit_logs WHERE 1=1"
        params = []
        
        if start_date:
            query += " AND DATE(timestamp) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND DATE(timestamp) <= ?"
            params.append(end_date)
        
        query += " GROUP BY action ORDER BY count DESC"
        
        cursor.execute(query, params)
        summary = cursor.fetchall()
        
        conn.close()
        return summary


class AutoBackupScheduler:
    """Automatic backup scheduling"""
    
    @staticmethod
    def should_run_daily_backup():
        """Check if daily backup should run"""
        backup_file = os.path.join(BackupManager.BACKUP_DIR, 'last_backup_date.txt')
        
        if not os.path.exists(backup_file):
            return True
        
        try:
            with open(backup_file, 'r') as f:
                last_backup_date = datetime.fromisoformat(f.read().strip())
            
            # Run backup if last backup was more than 24 hours ago
            return (datetime.now() - last_backup_date).total_seconds() > 86400
        except:
            return True
    
    @staticmethod
    def record_backup_date():
        """Record backup date"""
        BackupManager.ensure_backup_directory()
        backup_file = os.path.join(BackupManager.BACKUP_DIR, 'last_backup_date.txt')
        
        with open(backup_file, 'w') as f:
            f.write(datetime.now().isoformat())
    
    @staticmethod
    def run_auto_backup():
        """Run automatic daily backup"""
        if AutoBackupScheduler.should_run_daily_backup():
            success, result = BackupManager.create_backup("Auto daily backup")
            if success:
                AutoBackupScheduler.record_backup_date()
                # Log backup event
                SecurityManager.log_audit_event(
                    None, 'system', 'auto_backup', 
                    f"Created automatic backup: {result}"
                )
            return success, result
        return False, "Backup already completed today"
