import json
from datetime import datetime
import os
import tkinter as tk
from tkinter import simpledialog, scrolledtext

DATA_FILE = "students.json"
HISTORY_FILE = "history.txt"  # File to store history of added/deleted students in text format
PASSWORD_FILE = "password.txt"  # File to store the password


# Load and save students
def load_students():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_students(students):
    with open(DATA_FILE, "w") as file:
        json.dump(students, file, indent=4)


# Load password from file (for simplicity, we keep it in a text file)
def load_password():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            return file.read().strip()
    else:
        return None


# Set a new password (if necessary)
def set_password():
    new_password = simpledialog.askstring("Set Password", "Enter a new password:")
    if new_password:
        with open(PASSWORD_FILE, "w") as file:
            file.write(new_password)
        print("Password set successfully!")


# Log history to a separate text file
def log_history(action, student):
    """Log an action (add/delete) with student details to the history text file."""
    with open(HISTORY_FILE, "a") as file:
        action_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Action: {action}, Roll: {student['Roll']}, Name: {student['Name']}, Time: {action_time}\n")


# Functions to add, view, update, and delete students
def add_student(students):
    roll = input("Enter Roll Number: ")
    name = input("Enter Name: ")
    age = input("Enter Age: ")
    course = input("Enter Course: ")
    student = {"Roll": roll, "Name": name, "Age": age, "Course": course}
    students.append(student)
    print("Student added successfully!")
    log_history("ADD", student)


def view_students(students):
    if not students:
        print("No students found.")
    else:
        print(f"{'Roll':<10}{'Name':<20}{'Age':<10}{'Course':<10}")
        print("-" * 50)
        for student in students:
            print(f"{student['Roll']:<10}{student['Name']:<20}{student['Age']:<10}{student['Course']:<10}")


def search_student(students):
    roll = input("Enter Roll Number to search: ")
    for student in students:
        if student["Roll"] == roll:
            print("Student Found:")
            print(
                f"Roll: {student['Roll']}, Name: {student['Name']}, Age: {student['Age']}, Course: {student['Course']}")
            return
    print("Student not found.")


def update_student(students):
    roll = input("Enter Roll Number to update: ")
    for student in students:
        if student["Roll"] == roll:
            print("Enter new details (leave blank to keep current):")
            name = input(f"Name ({student['Name']}): ") or student["Name"]
            age = input(f"Age ({student['Age']}): ") or student["Age"]
            course = input(f"Course ({student['Course']}): ") or student["Course"]
            student.update({"Name": name, "Age": age, "Course": course})
            print("Student updated successfully!")
            return
    print("Student not found.")


def delete_student(students):
    roll = input("Enter Roll Number to delete: ")
    for student in students:
        if student["Roll"] == roll:
            students.remove(student)
            print("Student deleted successfully!")
            log_history("DELETE", student)
            return
    print("Student not found.")


# Tkinter function to view action history in a separate window
def view_history():
    """Display all the actions performed on the students data in a separate Tkinter window."""
    # Ask for the password before allowing access to history
    password = simpledialog.askstring("Password", "Enter the password to view action history:")
    if password != load_password():
        print("Incorrect password. Access denied.")
        return

    # Create the Tkinter window
    history_window = tk.Tk()
    history_window.title("Action History")

    # Create a scrolled text widget to display the history
    history_text = scrolledtext.ScrolledText(history_window, width=80, height=20)
    history_text.pack(padx=10, pady=10)

    try:
        # Read the history file and display its contents in the scrolled text widget
        with open(HISTORY_FILE, "r") as file:
            history = file.read()
            if history:
                history_text.insert(tk.END, history)
            else:
                history_text.insert(tk.END, "No history found.")
    except FileNotFoundError:
        history_text.insert(tk.END, "No history file found.")

    # Disable the text box so that it cannot be edited
    history_text.config(state=tk.DISABLED)

    # Add a button to close the window
    close_button = tk.Button(history_window, text="Close", command=history_window.destroy)
    close_button.pack(pady=5)

    # Run the Tkinter window
    history_window.mainloop()


def delete_selected_history(history, index):
    """Delete the selected action from the history and update the file."""
    if index is not None:
        # Remove the selected entry from the history
        deleted_action = history.pop(index)

        # Rewrite the history file without the deleted action
        with open(HISTORY_FILE, "w") as file:
            file.writelines(history)

        print(f"Deleted action: {deleted_action.strip()}")
        return True
    return False


def view_history():
    """Display all the actions performed on the students data in a separate Tkinter window."""
    # Ask for the password before allowing access to history
    password = simpledialog.askstring("Password", "Enter the password to view action history:")
    if password != load_password():
        print("Incorrect password. Access denied.")
        return

    # Create the Tkinter window
    history_window = tk.Tk()
    history_window.title("Action History")

    # Create a Listbox to display the history
    history_listbox = tk.Listbox(history_window, width=80, height=20)
    history_listbox.pack(padx=10, pady=10)

    try:
        # Read the history file
        with open(HISTORY_FILE, "r") as file:
            history = file.readlines()

        if history:
            # Insert all the history entries into the listbox
            for line in history:
                history_listbox.insert(tk.END, line.strip())
        else:
            history_listbox.insert(tk.END, "No history found.")

        # Define a function to delete the selected history item
        def delete_history_item():
            selected_index = history_listbox.curselection()  # Get the index of the selected item
            if selected_index:
                index = selected_index[0]
                if delete_selected_history(history, index):
                    # Update the Listbox after deletion
                    history_listbox.delete(index)

        # Add a delete button to delete the selected action
        delete_button = tk.Button(history_window, text="Delete Selected Action", command=delete_history_item)
        delete_button.pack(pady=5)

        # Add a close button to close the window
        close_button = tk.Button(history_window, text="Close", command=history_window.destroy)
        close_button.pack(pady=5)

        # Run the Tkinter window
        history_window.mainloop()

    except FileNotFoundError:
        print("No history file found.")


# Main function to control the menu
def main():
    students = load_students()

    # If no password is set, prompt to set a password
    if not load_password():
        set_password()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen (Windows or Unix-based)
        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Save & Exit")
        print(
            "7. View Action History (Password Required)")  # Option to view the history of actions with password protection
        choice = input("Enter your choice: ")

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            update_student(students)
        elif choice == "5":
            delete_student(students)
        elif choice == "6":
            save_students(students)
            print("Data saved. Exiting...")
            break
        elif choice == "7":
            view_history()  # View the action history in a separate window with password protection
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

