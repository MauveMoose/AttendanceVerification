from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import pymysql

def mark_attendance_window():
    # Color palette
    bg_color = "#CAF0F8"
    btn_color = "#00B4D8"
    btn_fg_color = "white"
    label_color = "#03045E"

    # Database configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'system',
        'database': 'Project'
    }

    def mark():
        date = cal.get_date()
        present_students = []
        for i in range(len(student_checkboxes)):
            if student_checkboxes[i].instate(["!disabled"]):  # Check if checkbox is checked
                present_students.append(student_ids[i])
        if present_students:
            try:
                for student_id in present_students:
                    cursor.execute("INSERT INTO Attendance11 (date, svv_net_id) VALUES (%s, %s)", (date, student_id))
                connection.commit()
                messagebox.showinfo("Success", "Attendance marked successfully!")
            except pymysql.IntegrityError as e:
                messagebox.showerror("Error", "Duplicate entry: " + str(e))
            except pymysql.DatabaseError as e:
                messagebox.showerror("Error", "Database error: " + str(e))
        else:
            messagebox.showwarning("Warning", "No students selected!")

    attendance_window = Toplevel()
    attendance_window.title("Mark Attendance")

    Label(attendance_window, text="Select Date:", font=('Arial', 12), bg=bg_color).pack(pady=10)
    cal = Calendar(attendance_window, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)

    Label(attendance_window, text="Select Present Students:", font=('Arial', 12), bg=bg_color).pack(pady=10)

    # Connect to the database
    connection = pymysql.connect(**db_config)

    # Create a cursor object
    cursor = connection.cursor()

    # Create Attendance table if not exists
    create_attendance_table_query = """
    CREATE TABLE IF NOT EXISTS Attendance11 (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        svv_net_id VARCHAR(50),
        FOREIGN KEY (svv_net_id) REFERENCES STUD1(svv_net_id)
    );
    """
    cursor.execute(create_attendance_table_query)
    connection.commit()

    # Fetch student names and IDs from the database
    cursor.execute("SELECT svv_net_id FROM STUD1")
    students = cursor.fetchall()

    student_checkboxes = []
    student_ids = []
    for student in students:
        student_id = student[0]
        student_ids.append(student_id)
        checkbox = ttk.Checkbutton(attendance_window, text=student_id)
        checkbox.pack()
        student_checkboxes.append(checkbox)

    Button(attendance_window, text="Mark Attendance", command=mark, bg=btn_color).pack(pady=10)

def open_mark_attendance_window():
    mark_attendance_window()

root = Tk()
root.title("Attendance System")

Button(root, text="Mark Attendance", command=open_mark_attendance_window).pack(pady=20)

mainloop()
