import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Card_details # Assuming this is the file where the card details page is defined

# Function to open reservation page
def open_reservation():
    # Create a new Tk window for the reservation page
    reservation_window = tk.Tk()
    reservation_window.title("Laundry Slot Reservation")

    # Full-screen settings
    #reservation_window.state("zoomed")  # Maximized for Windows
    reservation_window.attributes('-fullscreen', True)  # Full-screen for macOS/Linux

    # Sidebar frame (navigation bar)
    sidebar = tk.Frame(reservation_window, width=250, bg="#f0f0f0")
    sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

    # Menu items (initially hidden)
    menu_frame = tk.Frame(sidebar, bg="#f0f0f0")
    menu_frame.grid(row=1, column=0, sticky="ns")
    menu_frame.grid_forget()

    def open_card_details():
        Card_details.open_card_details()  # Assuming you have a function like this in card_details.py

    # Function for "Contact Us"
    def contact_us():
        messagebox.showinfo("Contact Us", "You can contact us at support@laundry.com.")

    # Function for "Sign Out"
    def sign_out():
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            reservation_window.destroy()  # Close the reservation window

    # Function to open card details page
    
    card_details_button = tk.Button(menu_frame, text="Card Details", command=open_card_details, font=("Arial", 12), width=20, anchor="w")
    card_details_button.grid(row=0, column=0, padx=10, pady=10)  # Add this button

    # Sidebar buttons (hidden initially)
    contact_button = tk.Button(menu_frame, text="Contact Us", command=contact_us, font=("Arial", 12), width=20, anchor="w")
    contact_button.grid(row=1, column=0, padx=10, pady=10)

    sign_out_button = tk.Button(menu_frame, text="Sign Out", command=sign_out, font=("Arial", 12), width=20, anchor="w")
    sign_out_button.grid(row=2, column=0, padx=10, pady=10)

    

    # Hamburger menu button (to show/hide the menu)
    def toggle_menu():
        if menu_frame.winfo_ismapped():
            menu_frame.grid_forget()  # Hide menu
        else:
            menu_frame.grid(row=1, column=0, sticky="ns")  # Show menu

    hamburger_button = tk.Button(sidebar, text="☰", font=("Arial", 20), command=toggle_menu)
    hamburger_button.grid(row=0, column=0, padx=10, pady=10)

    # Time slots as a grid
    time_slots = [
        ["1AM", "2AM", "3AM", "4AM", "5AM", "6AM"],
        ["7AM", "8AM", "9AM", "10AM", "11AM", "12PM"],
        ["1PM", "2PM", "3PM", "4PM", "5PM", "6PM"],
        ["7PM", "8PM", "9PM", "10PM", "11PM", "12AM"],
    ]

    # Frame for Today and Tomorrow buttons
    buttons_frame = tk.Frame(reservation_window)
    buttons_frame.grid(row=0, column=1, padx=20, pady=10)

    # Dynamic frame for dropdown (for time slots)
    dynamic_frame = tk.Frame(reservation_window)
    dynamic_frame.grid(row=1, column=1, padx=20, pady=20)

    def show_dropdown(label_text, time_slots):
        # Clear the frame
        for widget in dynamic_frame.winfo_children():
            widget.destroy()

        # Add label
        section_label = tk.Label(dynamic_frame, text=label_text, font=("Arial", 16, "bold"), pady=10)
        section_label.pack()

        # Add dropdown menu for time slots
        dropdown_frame = tk.Frame(dynamic_frame)
        dropdown_frame.pack()

        for row in time_slots:
            row_frame = tk.Frame(dropdown_frame)
            row_frame.pack()
            for time in row:
                time_button = ttk.Button(row_frame, text=time, width=8)
                time_button.pack(side="left", padx=5, pady=5)

    def handle_today():
        show_dropdown("Today to Reserve", time_slots)

    def handle_tomorrow():
        show_dropdown("Tomorrow to Reserve", time_slots)

    # Today and Tomorrow buttons
    today_button = ttk.Button(buttons_frame, text="Today to Reserve", command=handle_today)
    today_button.pack(side="left", padx=20)

    tomorrow_button = ttk.Button(buttons_frame, text="Tomorrow to Reserve", command=handle_tomorrow)
    tomorrow_button.pack(side="left", padx=20)

    # Make layout responsive
    reservation_window.grid_columnconfigure(1, weight=1)
    reservation_window.grid_rowconfigure(1, weight=1)
    dynamic_frame.grid_columnconfigure(0, weight=1)

    # Override the close button to confirm exit
    def on_close():
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            reservation_window.destroy()

    reservation_window.protocol("WM_DELETE_WINDOW", on_close)

    # Run the reservation window
    reservation_window.mainloop()

# Uncomment the next line if you want to test the reservation window directly
#open_reservation()