import tkinter as tk
from tkinter import messagebox
from Backend import save_user  # Import the save_user function

def open_sign_in(root):
    # Create a new Toplevel window for sign-in
    sign_in_window = tk.Toplevel(root)
    sign_in_window.title("Sign Up Page")
    sign_in_window.attributes('-fullscreen', True)

    # Labels and Entries dictionary to store references
    labels = [
        "First Name",
        "Last Name",
        "Phone Number",
        "Email address",
        "User Id",
        "Password",
        "Confirm Password"
    ]

    entries = {}  # Store entry widgets in a dictionary

    # Create a frame to hold the form
    form_frame = tk.Frame(sign_in_window, padx=20, pady=20)
    form_frame.pack(expand=True)

    # Create labels and entry fields
    for i, label_text in enumerate(labels):
        label = tk.Label(form_frame, text=label_text, font=("Arial", 14))
        label.grid(row=i, column=0, sticky="e", padx=10, pady=10)

        entry = tk.Entry(form_frame, font=("Arial", 14), show="*" if "Password" in label_text else "")
        entry.grid(row=i, column=1, padx=10, pady=10, sticky="we")
        entries[label_text] = entry

    # Function to check if all required fields are filled
    def check_entries():
        # Get the values from the entry fields
        if all(entries[label].get() for label in labels):
            create_account_button.config(state="normal")  # Enable the button
        else:
            create_account_button.config(state="disabled")  # Disable the button

    # Bind check_entries to all entry fields
    for entry in entries.values():
        entry.bind("<KeyRelease>", lambda event: check_entries())

    # Create Account button
    def create_account():
        # Get field values
        first_name = entries["First Name"].get()
        last_name = entries["Last Name"].get()
        phone_number = entries["Phone Number"].get()
        email_address = entries["Email address"].get()
        user_id = entries["User Id"].get()
        password = entries["Password"].get()
        confirm_password = entries["Confirm Password"].get()

        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Call save_user function to save data
        try:
            save_user(user_id, first_name, last_name, password, email_address, phone_number)
            sign_in_window.destroy()  # Close the sign-in window
            root.deiconify()  # Show the main page window again
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {e}")

    create_account_button = tk.Button(
        form_frame, text="Create Account", font=("Arial", 14), state="disabled", command=create_account
    )
    create_account_button.grid(row=len(labels), column=0, columnspan=2, pady=(20, 10))

    # Make columns responsive
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=2)

    # Hide the main window while the sign-in page is open
    root.withdraw()

    # Override the close button to properly quit or return
    def on_close():
        root.deiconify()
        sign_in_window.destroy()

    sign_in_window.protocol("WM_DELETE_WINDOW", on_close)

    # Run the sign-in window
    sign_in_window.mainloop()
