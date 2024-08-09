import tkinter as tk
from tkinter import messagebox
import mysql.connector

global deptNum
deptNum = 0
def validate_ids(cursor, course_id, teacher_id, dept_id):
    try:

        cursor.execute("SELECT * FROM department WHERE deptId = %s", (dept_id,))
        department = cursor.fetchone()
        if not department:
            messagebox.showerror("Error", "Given departmentID doesn't exist.")
            return False
    
        cursor.execute("SELECT * FROM course WHERE courseId = %s AND deptNo = %s", (course_id, dept_id))
        course = cursor.fetchone()
        if not course:
            messagebox.showerror("Error", "Course ID does not exist in the specified department.")
            return False
        
        cursor.execute("SELECT * FROM professor WHERE empId = %s", (teacher_id,))
        teacher = cursor.fetchone()
        if not teacher:
            messagebox.showerror("Error", "Teacher ID does not exist.")
            return False
        
        cursor.execute("SELECT * FROM teaching WHERE empId = %s AND courseId = %s AND year = 2006 AND sem = 'even'", (teacher_id, course_id))
        course = cursor.fetchone()
        if course:
            messagebox.showerror("Error", "Course already exists for the year 2006, even semester.")
            return False
        
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Database error: {err}")
        return False

def add_course(mycursor, dept_id, course_id, teacher_id, class_room):
    global deptNum
    if validate_ids(mycursor, course_id, teacher_id, dept_id):
        try:
            deptNum = dept_id
            sql = "INSERT INTO teaching (empId, courseId, sem, year, classRoom) VALUES (%s, %s, %s, %s, %s)"
            val = (teacher_id, course_id, "even", 2006, class_room)
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo("Success", "Course added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err.msg}")

def validate_enrollment(mycursor, roll_no, course_id):
    global deptNum
    try:
        
        # Check if a course is added before enrollment
        print(deptNum)

        if deptNum == 0:
            messagebox.showerror("Error", "Please add a course before enrolling students.")
            return False
        
        # Check if the student exists in the student table
        mycursor.execute("SELECT * FROM student WHERE rollNo = %s", (roll_no,))
        student = mycursor.fetchone()
        if not student:
            messagebox.showerror("Error", "Student roll number does not exist.")
            return False
        
        # Check if the course exists in the course table with the global department number  
        mycursor.execute("SELECT * FROM course WHERE courseId = %s AND deptNo = %s", (course_id, deptNum))
        course = mycursor.fetchone()
        if not course:
            messagebox.showerror("Error", "Course ID does not match the department of the last added course.")
            return False
        
        mycursor.execute("SELECT * FROM teaching WHERE courseId = %s AND year = 2006 AND sem = 'even'", (course_id,))
        teaching = mycursor.fetchall()
        if not teaching:
            messagebox.showerror("Error", "This course is not taught in the even semester of 2006.")
            return False
                
        mycursor.execute("SELECT * FROM prerequisite WHERE courseId = %s", (course_id,))
        prerequisites = mycursor.fetchall()
        print(prerequisites)
        passed_all_prerequisites = True
        for prerequisite in prerequisites:
            mycursor.execute("SELECT * FROM enrollment WHERE rollNo = %s AND courseId = %s AND grade != 'U' AND grade != 'W' AND year < 2006 ", (roll_no, prerequisite[0]))
            if not mycursor.fetchone():
                passed_all_prerequisites = False
                break

        if not passed_all_prerequisites:
            messagebox.showerror("Error", "Student has not passed all prerequisites for this course.")
            return False
        
        mycursor.execute("SELECT * FROM enrollment WHERE rollNo = %s AND courseId = %s AND year <= 2006 AND grade != 'U' AND grade != 'W'", (roll_no, course_id))
        enrollment = mycursor.fetchone()
        if enrollment:
            messagebox.showerror("Error", "Student is already enrolled in this course for the even semester of 2006.")
            return False
        
        # Implement prerequisite checking logic here if needed
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"rtwt Database error: {err}")
        return False

def enroll_student(mycursor, roll_no, course_id):
    if validate_enrollment(mycursor, roll_no, course_id):
        try:
            sql = "INSERT INTO enrollment (rollNo, courseId, sem, year, grade) VALUES (%s, %s, 'even', 2006, NULL)"
            val = (roll_no, course_id)
            mycursor.execute(sql, val)
            mydb.commit()
            messagebox.showinfo("Success", "Student enrolled successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err.msg}")

# Set up MySQL connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="varshu",
    database="academic_insti"
)

mycursor = mydb.cursor()

# GUI Setup
root = tk.Tk()
root.title("Academic Institution Management")

def open_add_course_window():
    add_course_window = tk.Toplevel(root)
    add_course_window.title("Add Course")

    tk.Label(add_course_window, text="Department ID:").grid(row=0, column=0)
    department_entry = tk.Entry(add_course_window)
    department_entry.grid(row=0, column=1)

    tk.Label(add_course_window, text="Course ID:").grid(row=1, column=0)
    course_entry = tk.Entry(add_course_window)
    course_entry.grid(row=1, column=1)

    tk.Label(add_course_window, text="Teacher ID:").grid(row=2, column=0)
    teacher_entry = tk.Entry(add_course_window)
    teacher_entry.grid(row=2, column=1)

    tk.Label(add_course_window, text="Class Room:").grid(row=3, column=0)
    classroom_entry = tk.Entry(add_course_window)
    classroom_entry.grid(row=3, column=1)

    add_button = tk.Button(add_course_window, text="Add Course", command=lambda: add_course(mycursor, department_entry.get(), course_entry.get(), teacher_entry.get(), classroom_entry.get()))
    add_button.grid(row=4, column=0, columnspan=2)

    back_button = tk.Button(add_course_window, text="Back", command=add_course_window.destroy)
    back_button.grid(row=5, column=0, columnspan=2)

def open_enroll_student_window():
    enroll_window = tk.Toplevel(root)
    enroll_window.title("Enroll Student")

    tk.Label(enroll_window, text="Roll No:").grid(row=0, column=0)
    roll_entry = tk.Entry(enroll_window)
    roll_entry.grid(row=0, column=1)

    tk.Label(enroll_window, text="Course ID:").grid(row=1, column=0)
    course_id_entry = tk.Entry(enroll_window)
    course_id_entry.grid(row=1, column=1)

    enroll_button = tk.Button(enroll_window, text="Enroll Student", command=lambda: enroll_student(mycursor, roll_entry.get(), course_id_entry.get()))
    enroll_button.grid(row=2, column=0, columnspan=2)

    back_button = tk.Button(enroll_window, text="Back", command=enroll_window.destroy)
    back_button.grid(row=3, column=0, columnspan=2)

add_course_button = tk.Button(root, text="Add Course", command=open_add_course_window)
add_course_button.pack()

enroll_student_button = tk.Button(root, text="Enroll Student", command=open_enroll_student_window)
enroll_student_button.pack()

root.mainloop()

# Clean up
mycursor.close()
mydb.close()