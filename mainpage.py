import tkinter as tk
from tkinter import messagebox
from Backend import initialize_database, fetch_records, generate_id
from Sign_In import open_sign_in  # Import open_sign_in from Sign_In.py
from Reservation_page import open_reservation  # Import open_reservation from Reservation_page.py
import mysql.connector
from db_config import DB_CONFIG, get_db_connection

# Validate login credentials
import mysql.connector
from Backend import DB_CONFIG

def validate_login(user_id, password):
    try:
        # Connect to the database
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Query to check credentials
        query = "SELECT * FROM User WHERE User_ID = %s AND Password = %s"
        cursor.execute(query, (user_id, password))
        result = cursor.fetchone()

        # Debug: Print inputs and query results
        print(f"Debug: Checking credentials for User_ID={user_id}, Password={password}")
        print(f"Debug: Query Result: {result}")

        cursor.close()
        connection.close()

        return result is not None
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False


# Initialize the main window
root = tk.Tk()
root.title("Smart Laundry System - Main Page")
root.attributes('-fullscreen', True)  # Fullscreen mode

# Login action
def login():
    user_id = user_entry.get()
    password = password_entry.get()

    if validate_login(user_id, password):
        messagebox.showinfo("Login Success", "Welcome!")
        root.destroy()  # Close the main window
        open_reservation(user_id)  # Pass the User_ID to the reservation page
    else:
        messagebox.showerror("Login Failed", "Incorrect UserID or Password")

# Handle closing the main page
def on_close():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        root.destroy()

# UI Layout
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

# Title
title_label = tk.Label(main_frame, text="Smart Laundry System", font=("Arial", 24, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# User ID
user_label = tk.Label(main_frame, text="UserID:", font=("Arial", 14))
user_label.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="e")
user_entry = tk.Entry(main_frame, font=("Arial", 14))
user_entry.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="w")

# Password
password_label = tk.Label(main_frame, text="Password:", font=("Arial", 14))
password_label.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="e")
password_entry = tk.Entry(main_frame, show="*", font=("Arial", 14))
password_entry.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="w")

# Login Button
login_button = tk.Button(main_frame, text="Login", font=("Arial", 14), command=login)
login_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))

# Sign Up
new_user_label = tk.Label(main_frame, text="Not registered? Create an account below.", font=("Arial", 12))
new_user_label.grid(row=4, column=0, columnspan=2, pady=(10, 5))

sign_in_button = tk.Button(main_frame, text="Sign Up", font=("Arial", 14), command=lambda: open_sign_in(root))
sign_in_button.grid(row=5, column=0, columnspan=2, pady=(5, 20))

# Responsive Grid
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# On close behavior
root.protocol("WM_DELETE_WINDOW", on_close)

# Run the application
if __name__ == "__main__":
    initialize_database()  # Ensure tables are set up
    root.mainloop()
