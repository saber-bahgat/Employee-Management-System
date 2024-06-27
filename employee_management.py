import sqlite3
from datetime import datetime

conn = sqlite3.connect("employee_management.db")
cur = conn.cursor()

# Create employees table if not exists
cur.execute("""CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position TEXT NOT NULL,
                salary INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Absent',
                date TEXT NOT NULL DEFAULT (datetime('now','localtime'))
            )""")
conn.commit()
conn.close()

def add_employee(name, position, salary):
    conn = sqlite3.connect("employee_management.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO employees(name, position, salary) VALUES (?, ?, ?)", (name, position, salary))
    conn.commit()
    conn.close()

def update_employee(employee_id, name=None, position=None, salary=None):
    conn = sqlite3.connect("employee_management.db")
    cur = conn.cursor()
    
    if name is not None:
        cur.execute("UPDATE employees SET name = ? WHERE id = ?", (name, employee_id))
    if position is not None:
        cur.execute("UPDATE employees SET position = ? WHERE id = ?", (position, employee_id))
    if salary is not None:
        cur.execute("UPDATE employees SET salary = ? WHERE id = ?", (salary, employee_id))
    
    conn.commit()
    conn.close()

def record_attendance(employee_id, status):
    conn = sqlite3.connect('employee_management.db')
    cur = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("UPDATE employees SET status = ?, date = ? WHERE id = ?", (status, date, employee_id))
    conn.commit()
    conn.close()

def view_attendance_report():
    conn = sqlite3.connect('employee_management.db')
    cur = conn.cursor()
    cur.execute('SELECT id, name, status, date FROM employees')
    records = cur.fetchall()
    conn.close()
    return records

def view_salary_report():
    conn = sqlite3.connect('employee_management.db')
    cur = conn.cursor()
    cur.execute('SELECT id, name, position, salary FROM employees')
    records = cur.fetchall()
    conn.close()
    return records

def main():
    print("Welcome to Employee Management System!")
    while True:
        print("\nMenu:")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Record Employee Attendance")
        print("4. View Attendance Report")
        print("5. View Salary Report")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            print("\n# Add Employee!")
            name = input("Enter employee name: ")
            position = input("Enter employee position: ")
            salary = int(input("Enter employee salary: "))
            add_employee(name, position, salary)
            print("Employee added successfully!")
            print("-" * 15)

        elif choice == '2':
            print("\n# Update Employee!")
            employee_id = int(input("Enter employee ID to update: "))
            name = input("Enter new name (leave blank to skip): ")
            position = input("Enter new position (leave blank to skip): ")
            salary = input("Enter new salary (leave blank to skip): ")

            if name or position or salary:
                update_employee(employee_id, name, position, salary)
                print("Employee information updated successfully!")
                print("-" * 15)
            else:
                print("No updates provided.")

        elif choice == '3':
            print("\n# Record Employee Attendance!")
            employee_id = int(input("Enter employee ID to record attendance: "))
            status = input("Enter attendance status (Present/Absent): ")
            record_attendance(employee_id, status)
            print("Attendance recorded successfully!")
            print("-" * 15)

        elif choice == '4':
            print("\n# Attendance Report!")
            attendance_report = view_attendance_report()
            if attendance_report:
                print("ID | Name | Status | Date")
                print("-" * 30)
                for record in attendance_report:
                    print(f"{record[0]} | {record[1]} | {record[2]} | {record[3]}")

                print("-" * 15)
            else:
                print("No attendance records found.")

        elif choice == '5':
            print("\n# Salary Report!")
            salary_report = view_salary_report()
            if salary_report:
                print("ID | Name | Position | Salary")
                print("-" * 30)
                for record in salary_report:
                    print(f"{record[0]} | {record[1]} | {record[2]} | {record[3]}")

                print("-" * 15) 
            else:
                print("No salary records found.")

        elif choice == '6':
            print("Exiting program... Goodbye!")
            break

        else:
            print("Invalid choice! Please enter a number from 1 to 6.")

if __name__ == "__main__":
    main()
