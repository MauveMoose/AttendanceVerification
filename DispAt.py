from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import pymysql
from datetime import datetime

# Global variables for selected month and year
selected_month = None
selected_year = None
student_id = None

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'system',
    'database': 'Project'
}

# Connect to the database
connection = pymysql.connect(**db_config)

# Create a cursor object
cursor = connection.cursor()

# Function to display dates when the student was present using a calendar
def display_present_dates():
    present_dates = []

    # Fetch dates when the student was present from the Attendance11 table
    cursor.execute("SELECT DISTINCT date FROM Attendance11 WHERE svv_net_id = %s", (student_id,))
    rows = cursor.fetchall()

    for row in rows:
        present_dates.append(row[0].strftime("%Y-%m-%d"))

    # Create a new window to display the calendar
    present_dates_window = Toplevel(root)
    present_dates_window.title("Present Dates")

    cal = Calendar(present_dates_window, selectmode="none", date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)

    # Highlight the dates when the student was present
    for date_str in present_dates:
        year, month, day = map(int, date_str.split('-'))
        cal.calevent_create(datetime(year, month, day), "Present", "blue")

# Function to calculate the percentage of attendance for a specific month
def calculate_attendance_percentage():
    global selected_month, selected_year
    if selected_month is not None and selected_year is not None:
        attendance_count = 0
        total_days = 0

        # Fetch all dates for the specified month from the Attendance11 table
        cursor.execute("SELECT DISTINCT date FROM Attendance11 WHERE MONTH(date) = %s AND YEAR(date) = %s",
                       (selected_month, selected_year))
        rows = cursor.fetchall()

        present_dates = [row[0] for row in rows]

        # Calculate the total number of days in the month
        for date in range(1, 32):  # Assuming maximum days in a month is 31
            if datetime(selected_year, selected_month, date).month == selected_month:
                total_days += 1

        # Count the number of days the student was present in the specified month
        for date in range(1, total_days + 1):
            if datetime(selected_year, selected_month, date).strftime("%Y-%m-%d") in present_dates:
                attendance_count += 1

        # Calculate the attendance percentage
        if total_days > 0:
            attendance_percentage = (attendance_count / total_days) * 100
        else:
            attendance_percentage = 0

        messagebox.showinfo("Attendance Percentage", f"Attendance percentage for {selected_month}/{selected_year}: {attendance_percentage:.2f}%")
    else:
        messagebox.showwarning("Warning", "Please select a month and year.")

# GUI for selecting a month and year
def select_month_year():
    select_month_year_window = Toplevel(root)
    select_month_year_window.title("Select Month and Year")

    Label(select_month_year_window, text="Select Month and Year", font=('Arial', 12)).pack(pady=10)

    month_label = Label(select_month_year_window, text="Month:", font=('Arial', 10))
    month_label.pack(pady=5)
    month_spinbox = Spinbox(select_month_year_window, from_=1, to=12)
    month_spinbox.pack(pady=5)

    year_label = Label(select_month_year_window, text="Year:", font=('Arial', 10))
    year_label.pack(pady=5)
    year_spinbox = Spinbox(select_month_year_window, from_=1900, to=2100)
    year_spinbox.pack(pady=5)

    def submit_month_year():
        global selected_month, selected_year
        selected_month = int(month_spinbox.get())
        selected_year = int(year_spinbox.get())
        select_month_year_window.destroy()
        calculate_attendance_percentage()

    submit_button = Button(select_month_year_window, text="Submit", command=submit_month_year)
    submit_button.pack(pady=10)

# Main function to get student ID and display attendance options
def display_attendance_options():
    global student_id

    # Fetch student IDs from the database
    cursor.execute("SELECT svv_net_id FROM STUD1")
    students = cursor.fetchall()

    student_id_window = Toplevel(root)
    student_id_window.title("Select Student")

    Label(student_id_window, text="Select Student", font=('Arial', 12)).pack(pady=10)

    student_id_combobox = ttk.Combobox(student_id_window, values=students)
    student_id_combobox.pack(pady=5)

    def select_student():
        global student_id
        student_id = student_id_combobox.get()
        student_id_window.destroy()
        show_attendance_options()

    select_button = Button(student_id_window, text="Select", command=select_student)
    select_button.pack(pady=10)

# Function to display attendance options after selecting the student
def show_attendance_options():
    attendance_options_window = Toplevel(root)
    attendance_options_window.title("Attendance Options")

    Label(attendance_options_window, text="Attendance Options", font=('Arial', 12)).pack(pady=10)

    present_dates_button = Button(attendance_options_window, text="Display Present Dates",
                                  command=display_present_dates)
    present_dates_button.pack(pady=5)

    percentage_button = Button(attendance_options_window, text="Calculate Attendance Percentage",
                               command=select_month_year)
    percentage_button.pack(pady=5)

# Main GUI
root = Tk()
root.title("Attendance System")

display_attendance_options()

mainloop()
