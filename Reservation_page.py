import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime

# Dictionary to track reserved slots
reserved_slots = {"Today": [], "Tomorrow": []}

# Function to open reservation page
def open_reservation():
    # Create a new Tk window for the reservation page
    reservation_window = tk.Tk()
    reservation_window.title("Laundry Slot Reservation")

    # Full-screen settings
    reservation_window.attributes('-fullscreen', True)

    # Sidebar frame (navigation bar)
    sidebar = tk.Frame(reservation_window, width=250, height=500)
    sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

    # Function to toggle the menu visibility
    def toggle_menu():
        if menu_frame.winfo_ismapped():
            menu_frame.grid_forget()  # Hide menu
        else:
            menu_frame.grid(row=1, column=0, sticky="ns")  # Show menu

    # Frame for the dropdown menu (hidden initially)
    menu_frame = tk.Frame(sidebar)
    menu_frame.grid(row=1, column=0, sticky="ns")
    menu_frame.grid_forget()  # Initially hide the menu

    # Function for "Contact Us"
    def contact_us():
        messagebox.showinfo("Contact Us", "You can contact us at support@laundry.com.")

    # Function for "Sign Out"
    def sign_out():
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            reservation_window.destroy()  # Close the application

    # Sidebar buttons (hidden initially)
    contact_button = tk.Button(menu_frame, text="Contact Us", command=contact_us, font=("Arial", 12), width=20, anchor="w")
    contact_button.grid(row=0, column=0, padx=10, pady=10)

    sign_out_button = tk.Button(menu_frame, text="Sign Out", command=sign_out, font=("Arial", 12), width=20, anchor="w")
    sign_out_button.grid(row=1, column=0, padx=10, pady=10)

    # Hamburger button to toggle the menu
    hamburger_button = tk.Button(sidebar, text="☰", font=("Arial", 20), bg="lightgray", command=toggle_menu)
    hamburger_button.grid(row=0, column=0, padx=10, pady=10)

    # Time slots as a grid
    time_slots = [
        ["1AM - 2AM", "2AM - 3AM", "3AM - 4AM", "4AM - 5AM", "5AM - 6AM", "6AM - 7AM"],
        ["7AM - 8AM", "8AM - 9AM", "9AM - 10AM", "10AM - 11AM", "11AM - 12AM", "12PM- 1PM"],
        ["1PM - 2PM", "2PM - 3PM", "3PM - 4PM", "4PM - 5PM", "5PM - 6PM", "6PM - 7PM"],
        ["7PM - 8PM", "8PM - 9PM", "9PM - 10PM", "10PM - 11PM", "11PM - 12PM", "12AM - 1AM"],
    ]

    # Frame for Today and Tomorrow buttons
    buttons_frame = tk.Frame(reservation_window)
    buttons_frame.grid(row=0, column=1, padx=20, pady=10)

    # Dynamic frame for dropdown (for time slots)
    dynamic_frame = tk.Frame(reservation_window)
    dynamic_frame.grid(row=1, column=1, padx=30, pady=30)

    def reserve_slot(day, time):
        # Show a popup to confirm the reservation
        confirm = messagebox.askyesno("Confirm Reservation", f"Do you want to reserve the slot at {time} on {day}?")
        if confirm:
            reserved_slots[day].append(time)
            # Show a message thanking the user
            messagebox.showinfo("Reservation Confirmed", f"Thank you! Your slot at {time} on {day} has been reserved.")
            show_slots(day)

    def show_slots(day):
        # Clear the frame
        for widget in dynamic_frame.winfo_children():
            widget.destroy()

        # Add label with date
        date_text = f"{day}: {datetime.date.today() if day == 'Today' else datetime.date.today() + datetime.timedelta(days=1)}"
        section_label = tk.Label(dynamic_frame, text=date_text, font=("Arial", 16, "bold"), pady=10)
        section_label.pack()

        # Add dropdown menu for time slots
        dropdown_frame = tk.Frame(dynamic_frame)
        dropdown_frame.pack()

        for row in time_slots:
            row_frame = tk.Frame(dropdown_frame)
            row_frame.pack()
            for time in row:
                if time in reserved_slots[day]:
                    # Reserved slot
                    time_button = ttk.Button(row_frame, text="❌", width=15, state="disabled")
                else:
                    # Available slot
                    time_button = ttk.Button(row_frame, text=time, width=15, command=lambda t=time: reserve_slot(day, t))
                time_button.pack(side="left", padx=10, pady=10)

    def handle_today():
        show_slots("Today")

    def handle_tomorrow():
        show_slots("Tomorrow")

    # Today and Tomorrow buttons
    today_button = ttk.Button(buttons_frame, text="Today to Reserve", command=handle_today)
    today_button.pack(side="left", padx=20)

    tomorrow_button = ttk.Button(buttons_frame, text="Tomorrow to Reserve", command=handle_tomorrow)
    tomorrow_button.pack(side="left", padx=20)

    # Frame for the Back button at the bottom
    back_frame = tk.Frame(reservation_window)
    back_frame.grid(row=2, column=1, pady=10, sticky="s")

    # Function for the Back button
    def go_back():
        if messagebox.askyesno("Back", "Do you want to go back to the main page?"):
            reservation_window.destroy()  # Close the reservation window

    # Back button
    back_button = ttk.Button(back_frame, text="Back", command=go_back)
    back_button.pack(pady=10)

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

# Uncomment the next line to test the reservation page
if __name__ == "__main__":
    open_reservation()
