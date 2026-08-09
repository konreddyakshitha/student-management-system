import sqlite3

# ==============================
# DATABASE CONNECTION
# ==============================

connection = sqlite3.connect("students.db")
cursor = connection.cursor()

# Create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

connection.commit()


# ==============================
# ADD STUDENT
# ==============================

def add_student():

    # Validate name
    while True:
        name = input("Enter student name: ")

        if name.strip():
            break

        print("Name cannot be empty.")

    # Check student ID
    while True:
        student_id = input("Enter student ID: ")

        cursor.execute(
            "SELECT id FROM students WHERE id = ?",
            (student_id,)
        )

        existing_student = cursor.fetchone()

        if existing_student is None:
            break

        print("Student ID already exists. Please enter a different ID.")

    # Validate age
    while True:
        age = input("Enter student age: ")

        if age.isdigit():
            break

        print("Invalid age. Please enter a number.")

    # Insert student into database
    cursor.execute(
        "INSERT INTO students (id, name, age) VALUES (?, ?, ?)",
        (student_id, name, int(age))
    )

    connection.commit()

    print("Student added successfully!")


# ==============================
# VIEW STUDENTS
# ==============================

def view_students():

    print("\n===== Student Details =====")

    cursor.execute(
        "SELECT id, name, age FROM students"
    )

    students = cursor.fetchall()

    if not students:
        print("No students found.")
        return

    for student in students:
        print("Name:", student[1])
        print("ID:", student[0])
        print("Age:", student[2])
        print("------")


# ==============================
# SEARCH STUDENT
# ==============================

def search_student():

    student_id = input("Enter student ID to search: ")

    cursor.execute(
        "SELECT id, name, age FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student:
        print("\n===== Student Found! =====")
        print("Name:", student[1])
        print("ID:", student[0])
        print("Age:", student[2])
    else:
        print("Student not found.")


# ==============================
# UPDATE STUDENT
# ==============================

def update_student():
    student_id = input("Enter student ID to update: ")

    cursor.execute(
        "SELECT id, name, age FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student:
        print("\nStudent Found!")
        print("Current Name:", student[1])
        print("Current Age:", student[2])

        while True:
            new_name = input("Enter new name: ")

            if new_name.strip():
                break

            print("Name cannot be empty.")

        while True:
            new_age = input("Enter new age: ")

            if new_age.isdigit():
                break

            print("Invalid age. Please enter a number.")

        cursor.execute(
            """
            UPDATE students
            SET name = ?, age = ?
            WHERE id = ?
            """,
            (new_name, int(new_age), student_id)
        )

        connection.commit()

        print("Student updated successfully!")

    else:
        print("Student not found.")
# ==============================
# DELETE STUDENT
# ==============================

def delete_student():
    student_id = input("Enter student ID to delete: ")

    cursor.execute(
        "SELECT id, name, age FROM students WHERE id = ?",
        (student_id,)
    )

    student = cursor.fetchone()

    if student:
        print("\nStudent Found!")
        print("Name:", student[1])
        print("ID:", student[0])
        print("Age:", student[2])

        confirmation = input(
            "Are you sure you want to delete this student? (yes/no): "
        )

        if confirmation.lower() == "yes":
            cursor.execute(
                "DELETE FROM students WHERE id = ?",
                (student_id,)
            )

            connection.commit()

            print("Student deleted successfully!")

        else:
            print("Delete cancelled.")

    else:
        print("Student not found.")


# ==============================
# MAIN MENU
# ==============================

while True:

    print("\n===== Student Management System =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        search_student()

    elif choice == "4":
        update_student()

    elif choice == "5":
        delete_student()

    elif choice == "6":
        print("Thank you for using Student Management System!")
        break

    else:
        print("Invalid choice. Please try again.")


# Close database
connection.close()