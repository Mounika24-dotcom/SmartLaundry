import tkinter as tk
from tkinter import messagebox
from Sign_In import open_sign_in  # Import open_sign_in from Sign_In.py
from Reservation_page import open_reservation  # Import open_reservation from Reservation_page.py

# Initialize the main window
root = tk.Tk()
root.title("Smart Laundry System - Main Page")

# Set the window to start maximized for Windows
#root.state("zoomed")

# For macOS and Linux, set to full-screen
root.attributes('-fullscreen', True)

# Function for login action
def login():
    user_id = user_entry.get()
    password = password_entry.get()
    # Simple check for demonstration
    if user_id == "admin" and password == "password":
        messagebox.showinfo("Login Success", "Welcome!")
        root.destroy()  # Close the main window
        open_reservation()  # Open the reservation page
    else:
        messagebox.showerror("Login Failed", "Incorrect UserID or Password")

# Function to handle closing the main page
def on_close():
    if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
        root.destroy()  # Close the main window

# Create a main frame for better layout organization
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

# Title Label
title_label = tk.Label(main_frame, text="Smart Laundry System", font=("Arial", 24, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

# UserID label and entry
user_label = tk.Label(main_frame, text="UserID:", font=("Arial", 14))
user_label.grid(row=1, column=0, padx=10, pady=(10, 5), sticky="e")
user_entry = tk.Entry(main_frame, font=("Arial", 14))
user_entry.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="w")

# Password label and entry
password_label = tk.Label(main_frame, text="Password:", font=("Arial", 14))
password_label.grid(row=2, column=0, padx=10, pady=(10, 5), sticky="e")
password_entry = tk.Entry(main_frame, show="*", font=("Arial", 14))
password_entry.grid(row=2, column=1, padx=10, pady=(10, 5), sticky="w")

# Login button
login_button = tk.Button(main_frame, text="Login", font=("Arial", 14), command=login)
login_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))

# Sign In label and button for new users
new_user_label = tk.Label(main_frame, text="Not registered? Create an account below.", font=("Arial", 12))
new_user_label.grid(row=4, column=0, columnspan=2, pady=(10, 5))

sign_in_button = tk.Button(main_frame, text="Sign Up", font=("Arial", 14), command=lambda: open_sign_in(root))
sign_in_button.grid(row=5, column=0, columnspan=2, pady=(5, 20))

# Make columns and rows responsive
main_frame.grid_columnconfigure(0, weight=1)
main_frame.grid_columnconfigure(1, weight=1)

# Set up the on_close behavior when the user tries to close the window
root.protocol("WM_DELETE_WINDOW", on_close)

# Run the main loop
root.mainloop()