from tkinter import *
from tkinter import messagebox
import pymysql
from tkcalendar import Calendar
import qrcode
from PIL import Image, ImageTk
import tempfile
import os
# Color palette
bg_color = "#CAF0F8"
btn_color = "#00B4D8"
btn_fg_color = "white"
label_color = "#03045E"

# Font
font_style = ("Arial", 12)

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

def open_registration_page(user_type):
    registration_page = Toplevel(root)
    if user_type == "student":
        registration_page.title("Student Registration Form")
    elif user_type == "teacher":
        registration_page.title("Teacher Registration Form")
    registration_page.configure(bg=bg_color)  # Set background color

    # Define table creation functions
    def create_student_table():
        create_table_query = """
        CREATE TABLE IF NOT EXISTS STUD1 (
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            age INT,
            gender VARCHAR(10),
            course VARCHAR(50),
            svv_net_id VARCHAR(50) Primary Key,
            password VARCHAR(255)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()

    def create_teacher_table():
        create_table_query = """
        CREATE TABLE IF NOT EXISTS TEACH1 (
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            age INT,
            gender VARCHAR(10),
            course VARCHAR(50),
            subjects VARCHAR(255),
            svv_net_id VARCHAR(50) Primary Key,
            password VARCHAR(255)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()

    # Create tables if they don't exist
    create_student_table()
    create_teacher_table()

    # Define registration function
    def reg():
        if (Pass.get() == CNFPASS.get()):
            try:
                if user_type == "student":
                    insert_query = """
                    INSERT INTO STUD1 (first_name, last_name, age, gender, course, svv_net_id, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(insert_query, (
                        FName.get(), LName.get(), AGE.get(), GENDER.get(), COURSE.get(), NID.get(), Pass.get()))
                elif user_type == "teacher":
                    subjects = ', '.join(SUBJECTS)
                    insert_query = """
                    INSERT INTO TEACH1 (first_name, last_name, age, gender, course, subjects, svv_net_id, password)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """
                    cursor.execute(insert_query, (
                        FName.get(), LName.get(), AGE.get(), GENDER.get(), COURSE.get(), subjects, NID.get(), Pass.get()))
                connection.commit()
                messagebox.showinfo("Registration Successful", "Welcome " + FName.get())
            except Exception as e:
                messagebox.showerror("Error", "An error occurred while registering: " + str(e))
        else:
            messagebox.showerror("Incorrect Entry", "Please make sure to retype the same password")

    # Define reset function
    def reset():
        FName.set("")
        LName.set("")
        AGE.set("")
        COURSE.set("")
        NID.set("")
        GENDER.set("")
        Pass.set("")
        CNFPASS.set("")
        SUBJECTS.clear()  # Clear subject selections

    # Define variables
    FName = StringVar()
    LName = StringVar()
    AGE = IntVar()
    COURSE = StringVar()
    NID = StringVar()
    GENDER = StringVar()
    Pass = StringVar()
    CNFPASS = StringVar()
    SUBJECTS = []

    # Create registration form
    Label(registration_page, text="First Name", bg=bg_color, fg=label_color, font=font_style).grid(row=0, column=0,
                                                                                                   padx=10, pady=10)
    Entry(registration_page, textvariable=FName, bg=bg_color).grid(row=0, column=1, padx=10, pady=10)
    Label(registration_page, text="Last Name", bg=bg_color, fg=label_color, font=font_style).grid(row=1, column=0,
                                                                                                  padx=10, pady=10)
    Entry(registration_page, textvariable=LName, bg=bg_color).grid(row=1, column=1, padx=10, pady=10)
    Label(registration_page, text="Age", bg=bg_color, fg=label_color, font=font_style).grid(row=2, column=0, padx=10,
                                                                                            pady=10)
    Entry(registration_page, textvariable=AGE, bg=bg_color).grid(row=2, column=1, padx=10, pady=10)
    Label(registration_page, text="Gender", bg=bg_color, fg=label_color, font=font_style).grid(row=3, column=0, padx=10,
                                                                                               pady=10)
    Radiobutton(registration_page, text="Male", variable=GENDER, value="Male", bg=bg_color, fg=label_color,
                font=font_style).grid(row=3, column=1, padx=10, pady=10)
    Radiobutton(registration_page, text="Female", variable=GENDER, value="Female", bg=bg_color, fg=label_color,
                font=font_style).grid(row=3, column=2, padx=10, pady=10)
    Label(registration_page, text="Course", bg=bg_color, fg=label_color, font=font_style).grid(row=4, column=0, padx=10,
                                                                                               pady=10)
    if user_type == "student":
        Entry(registration_page, textvariable=COURSE, bg=bg_color).grid(row=4, column=1, padx=10, pady=10)
    elif user_type == "teacher":
        course_options = ["CS", "DS", "IT", "BCA"]
        OptionMenu(registration_page, COURSE, *course_options).grid(row=4, column=1, padx=10, pady=10)
    if user_type == "teacher":
        Label(registration_page, text="Subjects", bg=bg_color, fg=label_color, font=font_style).grid(row=5, column=0,
                                                                                                      padx=10,
                                                                                                      pady=10)
        subjects = ["Maths", "Python", "CN", "Data Science", "C++", "HTML"]
        for i, subject in enumerate(subjects):
            cb = Checkbutton(registration_page, text=subject, variable=lambda val=subject: update_subjects(val), onvalue=subject, offvalue="")
            cb.grid(row=5 + i // 2, column=i % 2 + 1, padx=10, pady=5, sticky=W)

    Label(registration_page, text="SVV NET ID", bg=bg_color, fg=label_color, font=font_style).grid(row=7, column=0,
                                                                                                   padx=10, pady=10)
    Entry(registration_page, textvariable=NID, bg=bg_color).grid(row=7, column=1, padx=10, pady=10)
    Label(registration_page, text="Password", bg=bg_color, fg=label_color, font=font_style).grid(row=8, column=0,
                                                                                                 padx=10, pady=10)
    Entry(registration_page, textvariable=Pass, show="*", bg=bg_color).grid(row=8, column=1, padx=10, pady=10)
    Label(registration_page, text="Confirm Password", bg=bg_color, fg=label_color, font=font_style).grid(row=9,
                                                                                                         column=0,
                                                                                                         padx=10,
                                                                                                         pady=10)
    Entry(registration_page, textvariable=CNFPASS, show="*", bg=bg_color).grid(row=9, column=1, padx=10, pady=10)
    Button(registration_page, text="Register", command=reg, bg=btn_color, fg=btn_fg_color, font=font_style).grid(row=10,
                                                                                                                 column=0,
                                                                                                                 padx=10,
                                                                                                                 pady=10,
                                                                                                                 sticky=E)
    Button(registration_page, text="Clear", command=reset, bg=btn_color, fg=btn_fg_color, font=font_style).grid(row=10,
                                                                                                                column=1,
                                                                                                                padx=10,
                                                                                                                pady=10,
                                                                                                                sticky=W)

    
def update_subjects(val):
    if val in SUBJECTS:
        SUBJECTS.remove(val)
    else:
        SUBJECTS.append(val)

def open_login_page(user_type):
    login_page = Toplevel(root)
    if user_type == "student":
        login_page.title("Student Login Form")
    elif user_type == "teacher":
        login_page.title("Teacher Login Form")
    login_page.configure(bg=bg_color)  # Set background color

    def login():
        username = Username.get()
        password = Password.get()

        try:
            if user_type == "student":
                cursor.execute("SELECT * FROM STUD1 WHERE svv_net_id=%s AND password=%s", (username, password))
            elif user_type == "teacher":
                cursor.execute("SELECT * FROM TEACH1 WHERE svv_net_id=%s AND password=%s", (username, password))
            user = cursor.fetchone()
            if user:
                messagebox.showinfo("Login Successful", "Welcome " + user[0])
                # Call function to open landing page with user details
                open_landing_page(user, user_type)
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while logging in: " + str(e))

    Username = StringVar()
    Password = StringVar()

    Label(login_page, text="Username", bg=bg_color, fg=label_color, font=font_style).grid(row=0, column=0, padx=10,
                                                                                          pady=10)
    Entry(login_page, textvariable=Username, bg=bg_color).grid(row=0, column=1, padx=10, pady=10)
    Label(login_page, text="Password", bg=bg_color, fg=label_color, font=font_style).grid(row=1, column=0, padx=10,
                                                                                          pady=10)
    Entry(login_page, textvariable=Password, show="*", bg=bg_color).grid(row=1, column=1, padx=10, pady=10)
    Button(login_page, text="Login", command=login, bg=btn_color, fg=btn_fg_color, font=font_style).grid(row=2,
                                                                                                          columnspan=2,
                                                                                                          padx=10,
                                                                                                          pady=10)


def open_landing_page(user, user_type):
    landing_page = Toplevel(root)
    if user_type == "student":
        landing_page.title("Student Landing Page")
    elif user_type == "teacher":
        landing_page.title("Teacher Landing Page")
    landing_page.configure(bg=bg_color)  # Set background color
    
    # Display user details
    details_label = Label(landing_page, text="User Details", bg=bg_color, fg=label_color, font=font_style)
    details_label.pack(pady=10)

    Label(landing_page, text="First Name: " + user[0], bg=bg_color, fg=label_color, font=font_style).pack(pady=5)
    Label(landing_page, text="Last Name: " + user[1], bg=bg_color, fg=label_color, font=font_style).pack(pady=5)
    Label(landing_page, text="Age: " + str(user[2]), bg=bg_color, fg=label_color, font=font_style).pack(pady=5)
    Label(landing_page, text="Gender: " + user[3], bg=bg_color, fg=label_color, font=font_style).pack(pady=5)
    Label(landing_page, text="Course: " + user[4], bg=bg_color, fg=label_color, font=font_style).pack(pady=5)
    if user_type == "teacher":
        Label(landing_page, text="Subjects: " + user[5], bg=bg_color, fg=label_color, font=font_style).pack(pady=5)
    Label(landing_page, text="SVV NET ID: " + user[6], bg=bg_color, fg=label_color, font=font_style).pack(pady=5)

    # Button to display calendar
    Button(landing_page, text="Show Attendance", command=show_attendance).pack(pady=10)
    if user_type == "teacher":
        # Buttons for teachers
        Button(landing_page, text="Generate QR", command=open_QR).pack(pady=5)
        Button(landing_page, text="View Students", command=disp).pack(pady=5)
        Button(landing_page, text="Mark Attendance", command=mark_attendance).pack(pady=10)


def show_attendance():
    import DispAt

def mark_attendance():
    import attendance_module    

def generate_qr(qr_data):
    data = qr_data.get()
    if data:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a temporary file
        temp_file_path = tempfile.mktemp(suffix='.png')
        img.save(temp_file_path)

        # Display the image using PhotoImage
        img_tk = ImageTk.PhotoImage(file=temp_file_path)

        # Display the image in a label
        qr_label.config(image=img_tk)
        qr_label.image = img_tk

        # Remove the temporary file
        os.remove(temp_file_path)

        messagebox.showinfo("QR Code Generated", "QR code generated successfully.")
    else:
        messagebox.showerror("Error", "Please enter some data for QR code generation.")

def open_qr_generation_page():
    qr_generation_page = Toplevel(root)
    qr_generation_page.title("QR Code Generation")
    qr_generation_page.configure(bg=bg_color)  # Set background color

    Label(qr_generation_page, text="QR Code Generation", bg=bg_color, fg=label_color, font=("Arial", 16, "bold")).pack(pady=10)

    Label(qr_generation_page, text="Enter data for QR code:", bg=bg_color, fg=label_color, font=font_style).pack(pady=5)
    qr_data_entry = Entry(qr_generation_page, textvariable=StringVar(), bg=bg_color)
    qr_data_entry.pack(pady=5)

    global qr_label
    qr_label = Label(qr_generation_page, bg=bg_color)
    qr_label.pack(pady=10)

    Button(qr_generation_page, text="Generate QR Code", command=lambda: generate_qr(qr_data_entry), bg=btn_color, fg=btn_fg_color, font=font_style).pack(pady=10)

def open_QR():
    root = Tk()
    root.title("Admin Page")
    root.configure(bg=bg_color)  # Set background color

    Label(root, text="Admin Page", bg=bg_color, fg=label_color, font=("Arial", 16, "bold")).pack(pady=10)

    Button(root, text="Generate QR Code", command=open_qr_generation_page, bg=btn_color, fg=btn_fg_color, font=font_style).pack(pady=20)

    root.mainloop()



    
    # Create logout button

def disp():
    try:
        # Connect to the database
        connection = pymysql.connect(**db_config)

        # Create a cursor object
        cursor = connection.cursor()

        # Execute SQL query to fetch students and their courses
        cursor.execute("SELECT * FROM STUD1")

        # Fetch all records
        students = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        connection.close()

        # Display student details in a new window
        display_window = Tk()
        display_window.title("Student List")
        display_window.geometry("400x300")

        # Create a text widget to display student details
        text_widget = Text(display_window)
        text_widget.pack(expand=YES, fill=BOTH)

        # Display student details in the text widget
        for student in students:
            text_widget.insert(END, f"Name: {student[0]} {student[1]}\n")
            text_widget.insert(END, f"Course: {student[4]}\n")
            text_widget.insert(END, "-" * 30 + "\n")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")    
    
root = Tk()
root.title("Login Page")
root.configure(bg=bg_color)  # Set background color

# Create buttons for login and registration

Button(root, text="Student Registration", command=lambda: open_registration_page("student"), bg=btn_color,
       fg=btn_fg_color, font=font_style).grid(row=0, column=0, padx=10, pady=10)
Button(root, text="Login as Student", command=lambda: open_login_page("student"), bg=btn_color, fg=btn_fg_color,
       font=font_style).grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Teacher Registration", command=lambda: open_registration_page("teacher"), bg=btn_color,
       fg=btn_fg_color, font=font_style).grid(row=1, column=0, padx=10, pady=10)
Button(root, text="Login as Teacher", command=lambda: open_login_page("teacher"), bg=btn_color, fg=btn_fg_color,
       font=font_style).grid(row=1, column=1, padx=10, pady=10)
root.mainloop()
