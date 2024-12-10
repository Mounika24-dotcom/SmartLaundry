import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Backend import save_laundry_timeslot, generate_id
from datetime import timedelta
from Card_details import open_card_details
import mysql
import Backend
from Backend import initialize_database
from db_config import DB_CONFIG, get_db_connection
from datetime import datetime, date

def parse_time(time_str):
    """Convert time strings like '3AM' into MySQL TIME format (HH:MM:SS)."""
    return datetime.strptime(time_str, "%I%p").time()  # Parse 12-hour format with AM/PM

# Dictionary to track reserved slots
reserved_slots = {"Today": [], "Tomorrow": []}


def fetch_reservation_from_db():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query to fetch reservations for today and tomorrow
        query = "SELECT Date, TIME_FORMAT(Starting_time, '%l%p - %l%p') AS TimeRange FROM Laundry_Timeslot JOIN Reservation ON Laundry_Timeslot.Reservation_ID = Reservation.Reservation_ID"
        cursor.execute(query)
        rows = cursor.fetchall()

        connection.close()

        # Populate reserved_slots dictionary
        today = date.today()
        tomorrow = today + timedelta(days=1)

        reserved_slots["Today"].clear()
        reserved_slots["Tomorrow"].clear()

        for row in rows:
            reservation_date, time_range = row
            print(f"Fetched from DB: Date={reservation_date}, TimeRange={time_range}")  # Debugging
            if reservation_date == today:
                reserved_slots["Today"].append(time_range)
            elif reservation_date == tomorrow:
                reserved_slots["Tomorrow"].append(time_range)

        print(f"Reserved Slots After Fetching: {reserved_slots}")  # Debugging
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch reservation: {str(e)}")


def user_exists(user_id):
    """Check if a user exists in the User table."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM User WHERE User_ID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return result > 0
    except Exception as e:
        raise Exception(f"Error checking user existence: {str(e)}")


def save_reservation_to_db(day, user_id, machine_id=None):
    if not user_exists(user_id):
        raise Exception(f"User_ID '{user_id}' does not exist. Please add the user first.")

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        reservation_date = date.today() if day == "Today" else date.today() + timedelta(days=1)

        query = "INSERT INTO Reservation (User_ID, Date, Machine_ID) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, reservation_date, machine_id))
        connection.commit()

        reservation_id = cursor.lastrowid

        cursor.close()
        connection.close()
        return reservation_id
    except Exception as e:
        raise Exception(f"Failed to save reservation: {str(e)}")



# Function to open reservation page
def open_reservation(user_id):
    # Fetch reservations from the database
    fetch_reservation_from_db()
    
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
    # Card Details button
    card_details_button = tk.Button(menu_frame, text="Card Details", command=lambda: open_card_details(user_id), font=("Arial", 12), width=20, anchor="w")
    card_details_button.grid(row=0, column=0, padx=10, pady=10)
    
    contact_button = tk.Button(menu_frame, text="Contact Us", command=contact_us, font=("Arial", 12), width=20, anchor="w")
    contact_button.grid(row=1, column=0, padx=10, pady=10)

    sign_out_button = tk.Button(menu_frame, text="Sign Out", command=sign_out, font=("Arial", 12), width=20, anchor="w")
    sign_out_button.grid(row=2, column=0, padx=10, pady=10)

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

    def reserve_slot(day, time_range, user_id):
        # Split the time range into starting and ending times
        starting_time_str, ending_time_str = time_range.split(" - ")

        # Convert the times into MySQL TIME format
        starting_time = parse_time(starting_time_str)  # Converts '3AM' to '03:00:00'
        ending_time = parse_time(ending_time_str)      # Converts '4AM' to '04:00:00'

        # Format times to 12-hour format with AM/PM for display
        formatted_starting_time = starting_time.strftime("%I:%M %p")  # Example: '04:00 AM'
        formatted_ending_time = ending_time.strftime("%I:%M %p")      # Example: '05:00 AM'

        confirm = messagebox.askyesno(
            "Confirm Reservation",
            f"Do you want to reserve the slot from {formatted_starting_time} to {formatted_ending_time} on {day}?"
    )

        if confirm:
            try:
                # Step 1: Insert into Reservation table
                reservation_id = save_reservation_to_db(day, user_id)

                # Step 2: Generate a unique ID for the Laundry_Timeslot
                reservation_item_id = generate_id(user_id)

                # Step 3: Insert into Laundry_Timeslot table
                save_laundry_timeslot(
                    reservation_item_id=reservation_item_id,
                    starting_time=starting_time,
                    ending_time=ending_time,
                    reservation_id=reservation_id,
            )

                # Step 4: Add the slot to reserved_slots
                reserved_slots[day].append(time_range)

                # Step 5: Confirmation message and refresh UI
                messagebox.showinfo(
                    "Reservation Confirmed",
                    f"Your slot from {formatted_starting_time} to {formatted_ending_time} on {day} has been reserved."
            )
                show_slots(day)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to reserve slot: {str(e)}")


    def show_slots(day):
        # Clear the frame
        for widget in dynamic_frame.winfo_children():
            widget.destroy()

        # Add label with date
        date_text = f"{day}: {date.today() if day == 'Today' else date.today() + timedelta(days=1)}"
        section_label = tk.Label(dynamic_frame, text=date_text, font=("Arial", 16, "bold"), pady=10)
        section_label.pack()

        print(f"Displaying slots for {day}: {reserved_slots[day]}")  # Debugging

        # Add dropdown menu for time slots
        dropdown_frame = tk.Frame(dynamic_frame)
        dropdown_frame.pack()

        for row in time_slots:
            row_frame = tk.Frame(dropdown_frame)
            row_frame.pack()
            for time_range in row:
                if time_range in reserved_slots[day]:
                    # Reserved slot
                    time_button = ttk.Button(row_frame, text="❌", width=15, state="disabled")
                else:
                    # Available slot
                    time_button = ttk.Button(row_frame, text=time_range, width=15, 
                                         command=lambda t=time_range: reserve_slot(day, t, user_id))
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

    dynamic_frame = tk.Frame(reservation_window)
    dynamic_frame.grid(row=1, column=1, padx=30, pady=30)


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