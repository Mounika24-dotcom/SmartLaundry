import tkinter as tk
from tkinter import messagebox

# Function to open the sign-in page
def open_sign_in(root):
    # Create a new Toplevel window for sign-in
    sign_in_window = tk.Toplevel(root)
    sign_in_window.title("Sign Up Page")

    # Set the window to start maximized for Windows
    #sign_in_window.state("zoomed")
    
    # For macOS and Linux, set to full-screen
    sign_in_window.attributes('-fullscreen', True)

    # Labels and Entries dictionary to store references
    labels = [
        "First Name",
        "Last Name",
        "Phone Number",
        "Email Id",
        "User Id",
        "Password",
        "Confirm Password"
    ]

    # Store entry widgets in a dictionary
    entries = {}

    # Create a frame to hold the form
    form_frame = tk.Frame(sign_in_window, padx=20, pady=20)
    form_frame.pack(expand=True)

    # Create labels on the left and entry fields on the right
    for i, label_text in enumerate(labels):
        label = tk.Label(form_frame, text=label_text, font=("Arial", 14))
        label.grid(row=i, column=0, sticky="e", padx=10, pady=10)

        entry = tk.Entry(form_frame, font=("Arial", 14), show="*" if "Password" in label_text else "")
        entry.grid(row=i, column=1, padx=10, pady=10, sticky="we")
        entries[label_text] = entry

    # Function to check if all required fields are filled
    def check_entries():
        # Get the values from the entry fields
        first_name = entries["First Name"].get()
        last_name = entries["Last Name"].get()
        phone_number = entries["Phone Number"].get()
        email_id = entries["Email address"].get()
        user_id = entries["User Id"].get()
        password = entries["Password"].get()
        confirm_password = entries["Confirm Password"].get()

        # Enable or disable the Create Account button based on entry validation
        if first_name and last_name and phone_number and email_id and user_id and password and confirm_password:
            create_account_button.config(state="normal")  # Enable the button
        else:
            create_account_button.config(state="disabled")  # Disable the button

    # Call check_entries when either entry field changes
    for entry in entries.values():
        entry.bind("<KeyRelease>", lambda event: check_entries())

    # Create Account button (Initially disabled)
    def create_account():
        # Print or process entries here
        for field, entry in entries.items():
            print(f"{field}: {entry.get()}")
        messagebox.showinfo("Account Created", "Account has been created successfully!")
        sign_in_window.destroy()  # Close the sign-in window
        root.deiconify()  # Show the main page window again

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
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            root.destroy()
            sign_in_window.destroy()

    sign_in_window.protocol("WM_DELETE_WINDOW", on_close)

    # Run the sign-in window
    sign_in_window.mainloop()