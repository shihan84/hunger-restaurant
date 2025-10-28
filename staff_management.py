"""
Staff Management & Payroll System
Handles staff information, attendance, leaves, and salary payments
"""

import database
from datetime import datetime, timedelta

class StaffManagement:
    """Staff management system for HR operations"""
    
    # Define allowed roles
    ROLES = ['Admin', 'Manager', 'Cashier', 'Waiter', 'Chef', 'Other']
    
    # Define leave types
    LEAVE_TYPES = ['casual', 'sick', 'emergency', 'paid', 'unpaid']
    
    @staticmethod
    def add_staff(name, role, salary, contact='', email='', address=''):
        """Add a new staff member"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            if role not in StaffManagement.ROLES:
                conn.close()
                return False, f"Invalid role. Must be one of: {', '.join(StaffManagement.ROLES)}"
            
            cursor.execute("""
                INSERT INTO staff (name, role, salary, contact, email, address, joining_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'active')
            """, (name, role, salary, contact, email, address, datetime.now().strftime('%Y-%m-%d')))
            
            conn.commit()
            staff_id = cursor.lastrowid
            conn.close()
            return True, f"Staff added successfully with ID: {staff_id}"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def update_staff(staff_id, name=None, role=None, salary=None, contact=None, 
                     email=None, address=None, status=None):
        """Update staff information"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            updates = []
            params = []
            
            if name:
                updates.append("name = ?")
                params.append(name)
            if role:
                if role not in StaffManagement.ROLES:
                    conn.close()
                    return False, f"Invalid role. Must be one of: {', '.join(StaffManagement.ROLES)}"
                updates.append("role = ?")
                params.append(role)
            if salary is not None:
                updates.append("salary = ?")
                params.append(salary)
            if contact is not None:
                updates.append("contact = ?")
                params.append(contact)
            if email is not None:
                updates.append("email = ?")
                params.append(email)
            if address is not None:
                updates.append("address = ?")
                params.append(address)
            if status:
                updates.append("status = ?")
                params.append(status)
            
            if not updates:
                conn.close()
                return False, "No fields to update"
            
            params.append(staff_id)
            
            cursor.execute(f"""
                UPDATE staff SET {', '.join(updates)} WHERE id = ?
            """, params)
            
            conn.commit()
            conn.close()
            return True, "Staff updated successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_staff(staff_id=None):
        """Get staff information"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if staff_id:
            cursor.execute("SELECT * FROM staff WHERE id = ?", (staff_id,))
            result = cursor.fetchone()
        else:
            cursor.execute("SELECT * FROM staff ORDER BY name")
            result = cursor.fetchall()
        
        conn.close()
        return result
    
    @staticmethod
    def record_checkin(staff_id, check_in_time=None):
        """Record staff check-in"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            if not check_in_time:
                check_in_time = datetime.now().strftime('%H:%M:%S')
            
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Check if already checked in today
            cursor.execute("""
                SELECT id FROM attendance WHERE staff_id = ? AND date = ?
            """, (staff_id, today))
            
            existing = cursor.fetchone()
            
            if existing:
                conn.close()
                return False, "Already checked in today"
            
            cursor.execute("""
                INSERT INTO attendance (staff_id, date, check_in, status)
                VALUES (?, ?, ?, 'present')
            """, (staff_id, today, check_in_time))
            
            conn.commit()
            conn.close()
            return True, "Check-in recorded successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def record_checkout(staff_id, check_out_time=None):
        """Record staff check-out"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            if not check_out_time:
                check_out_time = datetime.now().strftime('%H:%M:%S')
            
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Get check-in record
            cursor.execute("""
                SELECT check_in FROM attendance WHERE staff_id = ? AND date = ?
            """, (staff_id, today))
            
            record = cursor.fetchone()
            
            if not record:
                conn.close()
                return False, "No check-in found for today"
            
            if record[0] is None:
                conn.close()
                return False, "Check-in time missing"
            
            # Calculate total hours
            check_in_time = datetime.strptime(f"{today} {record[0]}", '%Y-%m-%d %H:%M:%S')
            checkout_time = datetime.strptime(f"{today} {check_out_time}", '%Y-%m-%d %H:%M:%S')
            total_hours = (checkout_time - check_in_time).total_seconds() / 3600
            
            cursor.execute("""
                UPDATE attendance 
                SET check_out = ?, total_hours = ?
                WHERE staff_id = ? AND date = ?
            """, (check_out_time, total_hours, staff_id, today))
            
            conn.commit()
            conn.close()
            return True, f"Check-out recorded. Total hours: {total_hours:.2f}"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def mark_attendance(staff_id, date, status, notes=''):
        """Manually mark attendance (present/absent/late/leave/half_day)"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO attendance (staff_id, date, status, notes)
                VALUES (?, ?, ?, ?)
            """, (staff_id, date, status, notes))
            
            conn.commit()
            conn.close()
            return True, "Attendance marked successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_attendance(staff_id=None, date=None, start_date=None, end_date=None):
        """Get attendance records"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if staff_id and date:
            cursor.execute("""
                SELECT a.*, s.name as staff_name
                FROM attendance a
                JOIN staff s ON a.staff_id = s.id
                WHERE a.staff_id = ? AND a.date = ?
            """, (staff_id, date))
        elif staff_id and start_date and end_date:
            cursor.execute("""
                SELECT a.*, s.name as staff_name
                FROM attendance a
                JOIN staff s ON a.staff_id = s.id
                WHERE a.staff_id = ? AND a.date BETWEEN ? AND ?
                ORDER BY a.date DESC
            """, (staff_id, start_date, end_date))
        elif start_date and end_date:
            cursor.execute("""
                SELECT a.*, s.name as staff_name
                FROM attendance a
                JOIN staff s ON a.staff_id = s.id
                WHERE a.date BETWEEN ? AND ?
                ORDER BY a.date DESC, s.name
            """, (start_date, end_date))
        else:
            cursor.execute("""
                SELECT a.*, s.name as staff_name
                FROM attendance a
                JOIN staff s ON a.staff_id = s.id
                ORDER BY a.date DESC, s.name
            """)
        
        records = cursor.fetchall()
        conn.close()
        return records
    
    @staticmethod
    def get_attendance_summary(staff_id, start_date, end_date):
        """Get attendance summary for a staff member"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                status,
                COUNT(*) as count
            FROM attendance
            WHERE staff_id = ? AND date BETWEEN ? AND ?
            GROUP BY status
        """, (staff_id, start_date, end_date))
        
        summary = cursor.fetchall()
        
        cursor.execute("""
            SELECT SUM(total_hours) FROM attendance
            WHERE staff_id = ? AND date BETWEEN ? AND ?
        """, (staff_id, start_date, end_date))
        
        total_hours = cursor.fetchone()[0] or 0
        
        conn.close()
        return summary, total_hours
    
    @staticmethod
    def apply_leave(staff_id, leave_type, start_date, end_date, reason=''):
        """Apply for leave"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            if leave_type not in StaffManagement.LEAVE_TYPES:
                conn.close()
                return False, f"Invalid leave type. Must be one of: {', '.join(StaffManagement.LEAVE_TYPES)}"
            
            # Calculate days
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            days = (end - start).days + 1
            
            cursor.execute("""
                INSERT INTO leave_requests 
                (staff_id, leave_type, start_date, end_date, days, reason, status)
                VALUES (?, ?, ?, ?, ?, ?, 'pending')
            """, (staff_id, leave_type, start_date, end_date, days, reason))
            
            conn.commit()
            leave_id = cursor.lastrowid
            conn.close()
            return True, f"Leave application submitted. ID: {leave_id}"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def update_leave_status(leave_id, status):
        """Approve or reject leave request"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE leave_requests SET status = ? WHERE id = ?
            """, (status, leave_id))
            
            conn.commit()
            conn.close()
            return True, f"Leave {status} successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_leave_requests(status=None):
        """Get leave requests"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT l.*, s.name as staff_name
                FROM leave_requests l
                JOIN staff s ON l.staff_id = s.id
                WHERE l.status = ?
                ORDER BY l.applied_date DESC
            """, (status,))
        else:
            cursor.execute("""
                SELECT l.*, s.name as staff_name
                FROM leave_requests l
                JOIN staff s ON l.staff_id = s.id
                ORDER BY l.applied_date DESC
            """)
        
        requests = cursor.fetchall()
        conn.close()
        return requests
    
    @staticmethod
    def calculate_salary(staff_id, month, year):
        """Calculate salary for a staff member"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        # Get staff basic salary
        cursor.execute("SELECT salary FROM staff WHERE id = ?", (staff_id,))
        staff = cursor.fetchone()
        
        if not staff:
            conn.close()
            return False, "Staff not found"
        
        basic_salary = staff[0]
        
        # Get attendance for the month
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year}-12-31"
        else:
            end_date = f"{year}-{(month+1):02d}-01"
            end_date = (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT COUNT(*) FROM attendance 
            WHERE staff_id = ? AND date BETWEEN ? AND ? AND status IN ('present', 'late', 'half_day')
        """, (staff_id, start_date, end_date))
        
        present_days = cursor.fetchone()[0]
        
        # Get total days in month
        total_days = (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1
        
        # Calculate deductions for absent days
        absent_days = total_days - present_days
        deduction_per_day = basic_salary / 30
        deductions = absent_days * deduction_per_day
        
        # Get any bonuses or additional deductions from previous records
        cursor.execute("""
            SELECT bonuses, deductions FROM salary_payments
            WHERE staff_id = ? AND month = ? AND year = ?
        """, (staff_id, month, year))
        
        existing = cursor.fetchone()
        bonuses = existing[0] if existing else 0
        additional_deductions = existing[1] - deductions if existing else 0
        
        total_deductions = deductions + additional_deductions
        total_amount = basic_salary - total_deductions + bonuses
        
        conn.close()
        
        return {
            'basic_salary': basic_salary,
            'present_days': present_days,
            'absent_days': absent_days,
            'deductions': total_deductions,
            'bonuses': bonuses,
            'total_amount': max(0, total_amount)
        }
    
    @staticmethod
    def generate_salary(staff_id, month, year, bonuses=0, additional_deductions=0):
        """Generate salary record for a staff member"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            # Get calculated salary
            salary_data = StaffManagement.calculate_salary(staff_id, month, year)
            
            if not salary_data:
                conn.close()
                return False, "Could not calculate salary"
            
            # Add bonuses and deductions
            total_deductions = salary_data['deductions'] + additional_deductions
            total_bonuses = bonuses
            
            total_amount = salary_data['basic_salary'] - total_deductions + total_bonuses
            total_amount = max(0, total_amount)
            
            # Insert or update salary payment record
            cursor.execute("""
                INSERT OR REPLACE INTO salary_payments 
                (staff_id, month, year, basic_salary, deductions, bonuses, total_amount, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
            """, (staff_id, month, year, salary_data['basic_salary'], 
                  total_deductions, total_bonuses, total_amount))
            
            conn.commit()
            conn.close()
            return True, "Salary generated successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def pay_salary(staff_id, month, year, payment_method='cash', notes=''):
        """Record salary payment"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                UPDATE salary_payments 
                SET payment_date = ?, payment_method = ?, notes = ?, status = 'paid'
                WHERE staff_id = ? AND month = ? AND year = ?
            """, (datetime.now().strftime('%Y-%m-%d'), payment_method, 
                  notes, staff_id, month, year))
            
            # Get salary details for expense recording
            cursor.execute("""
                SELECT total_amount FROM salary_payments
                WHERE staff_id = ? AND month = ? AND year = ?
            """, (staff_id, month, year))
            
            salary_amount = cursor.fetchone()[0]
            
            # Record as expense
            cursor.execute("""
                INSERT INTO expenses 
                (date, category, amount, description, payment_method)
                VALUES (?, 'Staff Salary', ?, ?, ?)
            """, (datetime.now().strftime('%Y-%m-%d'), salary_amount,
                  f'Salary payment for staff #{staff_id}', payment_method))
            
            conn.commit()
            conn.close()
            return True, "Salary payment recorded successfully"
        except Exception as e:
            conn.close()
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_salary_history(staff_id=None):
        """Get salary payment history"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        if staff_id:
            cursor.execute("""
                SELECT sp.*, s.name as staff_name
                FROM salary_payments sp
                JOIN staff s ON sp.staff_id = s.id
                WHERE sp.staff_id = ?
                ORDER BY sp.year DESC, sp.month DESC
            """, (staff_id,))
        else:
            cursor.execute("""
                SELECT sp.*, s.name as staff_name
                FROM salary_payments sp
                JOIN staff s ON sp.staff_id = s.id
                ORDER BY sp.year DESC, sp.month DESC
            """)
        
        history = cursor.fetchall()
        conn.close()
        return history
    
    @staticmethod
    def get_pending_salary_payments():
        """Get pending salary payments"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT sp.*, s.name as staff_name
            FROM salary_payments sp
            JOIN staff s ON sp.staff_id = s.id
            WHERE sp.status = 'pending'
            ORDER BY sp.year DESC, sp.month DESC
        """)
        
        pending = cursor.fetchall()
        conn.close()
        return pending
    
    @staticmethod
    def get_monthly_payroll(month, year):
        """Get monthly payroll summary"""
        conn = database.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as staff_count,
                SUM(total_amount) as total_payout,
                SUM(CASE WHEN status = 'paid' THEN total_amount ELSE 0 END) as paid_amount,
                SUM(CASE WHEN status = 'pending' THEN total_amount ELSE 0 END) as pending_amount
            FROM salary_payments
            WHERE month = ? AND year = ?
        """, (month, year))
        
        summary = cursor.fetchone()
        conn.close()
        return summary
