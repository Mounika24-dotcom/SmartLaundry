import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Backend import save_laundry_timeslot, generate_id, refresh_amount_on_signout
from datetime import timedelta
from Card_details import open_card_details
import mysql.connector
from Backend import initialize_database
from db_config import DB_CONFIG, get_db_connection
from datetime import datetime, date

def parse_time(time_str):
    """Convert time strings like '3AM' into MySQL TIME format (HH:MM:SS)."""
    return datetime.strptime(time_str, "%I%p").time()

# Dictionary to track reserved slots for all users
reserved_slots = {"Today": [], "Tomorrow": []}

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

def fetch_reservation_from_db():
    """Fetch all reservations and update the reserved_slots dictionary."""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Fetch reservations for all users
        query = """
        SELECT Date, TIME_FORMAT(Starting_time, '%l%p - %l%p') AS TimeRange
        FROM Laundry_Timeslot
        JOIN Reservation ON Laundry_Timeslot.Reservation_ID = Reservation.Reservation_ID
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        # Debugging: Print fetched rows
        print(f"DEBUG: Fetched reservations: {rows}")

        # Clear and update the reserved_slots dictionary
        reserved_slots["Today"].clear()
        reserved_slots["Tomorrow"].clear()

        today = date.today()
        tomorrow = today + timedelta(days=1)

        for row in rows:
            reservation_date, time_range = row
            if reservation_date == today:
                reserved_slots["Today"].append(time_range)
            elif reservation_date == tomorrow:
                reserved_slots["Tomorrow"].append(time_range)

        # Debugging: Print updated reserved slots
        print(f"DEBUG: Updated reserved_slots: {reserved_slots}")

        cursor.close()
        connection.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch reservations: {str(e)}")

def save_reservation_to_db(day, user_id, machine_id=None):
    """Save a reservation to the database."""
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

def open_reservation(user_id):
    """Open the reservation page for all users."""
    fetch_reservation_from_db()

    reservation_window = tk.Tk()
    reservation_window.title("Laundry Slot Reservation")
    reservation_window.attributes('-fullscreen', True)

    sidebar = tk.Frame(reservation_window, width=250, height=500)
    sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

    # Define a frame for the heading
    heading_frame = tk.Frame(reservation_window, padx=20, pady=10)
    heading_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

    # Add the heading label to the heading frame
    heading_label = tk.Label(
        heading_frame,
        text="Reservation of Time Slots",
        font=("Arial", 20, "bold"),
        fg="blue"
    )
    heading_label.pack()

    # Buttons frame for Today and Tomorrow buttons
    buttons_frame = tk.Frame(reservation_window)
    buttons_frame.grid(row=1, column=1, padx=20, pady=10, sticky="n")


    def toggle_menu():
        if menu_frame.winfo_ismapped():
            menu_frame.grid_forget()
        else:
            menu_frame.grid(row=1, column=0, sticky="ns")

    menu_frame = tk.Frame(sidebar)
    menu_frame.grid(row=1, column=0, sticky="ns")
    menu_frame.grid_forget()

    def contact_us():
        messagebox.showinfo("Contact Us", "You can contact us at support@laundry.com.")

    def sign_out():
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            try:
                refresh_amount_on_signout(user_id)
                messagebox.showinfo("Sign Out", " You are now signed out.")
                reservation_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to sign out: {str(e)}")

    card_details_button = tk.Button(menu_frame, text="Card Details", command=lambda: open_card_details(user_id), font=("Arial", 12), width=20, anchor="w")
    card_details_button.grid(row=0, column=0, padx=10, pady=10)

    contact_button = tk.Button(menu_frame, text="Contact Us", command=contact_us, font=("Arial", 12), width=20, anchor="w")
    contact_button.grid(row=1, column=0, padx=10, pady=10)

    sign_out_button = tk.Button(menu_frame, text="Sign Out", command=sign_out, font=("Arial", 12), width=20, anchor="w")
    sign_out_button.grid(row=2, column=0, padx=10, pady=10)

    hamburger_button = tk.Button(sidebar, text="☰", font=("Arial", 20), bg="lightgray", command=toggle_menu)
    hamburger_button.grid(row=0, column=0, padx=10, pady=10)

    buttons_frame = tk.Frame(reservation_window)
    buttons_frame.grid(row=0, column=1, padx=20, pady=10)

    # Today and Tomorrow buttons
    today_button = ttk.Button(
        buttons_frame,
        text="Today to Reserve",
        command=lambda: show_slots("Today")
    )
    today_button.pack(side="left", padx=20)

    tomorrow_button = ttk.Button(
        buttons_frame,
        text="Tomorrow to Reserve",
        command=lambda: show_slots("Tomorrow")
    )
    tomorrow_button.pack(side="left", padx=20)

    # Dynamic frame for displaying time slots
    dynamic_frame = tk.Frame(reservation_window)
    dynamic_frame.grid(row=2, column=1, padx=30, pady=30)

    
    # Time slots as a grid
    time_slots = [
        ["1AM - 2AM", "2AM - 3AM", "3AM - 4AM", "4AM - 5AM", "5AM - 6AM", "6AM - 7AM"],
        ["7AM - 8AM", "8AM - 9AM", "9AM - 10AM", "10AM - 11AM", "11AM - 12AM", "12PM- 1PM"],
        ["1PM - 2PM", "2PM - 3PM", "3PM - 4PM", "4PM - 5PM", "5PM - 6PM", "6PM - 7PM"],
        ["7PM - 8PM", "8PM - 9PM", "9PM - 10PM", "10PM - 11PM", "11PM - 12PM", "12AM - 1AM"],
    ]

    def reserve_slot(day, time_range, user_id):
        """Reserve a time slot and block it for all users."""
        starting_time_str, ending_time_str = time_range.split(" - ")
        starting_time = parse_time(starting_time_str)
        ending_time = parse_time(ending_time_str)

        formatted_starting_time = starting_time.strftime("%I:%M %p")
        formatted_ending_time = ending_time.strftime("%I:%M %p")

        if messagebox.askyesno("Confirm Reservation", f"Do you want to reserve the slot {formatted_starting_time} to {formatted_ending_time} on {day}?"):
            try:
                reservation_id = save_reservation_to_db(day, user_id)
                reservationitem_id = generate_id(user_id)
                save_laundry_timeslot(reservationitem_id, starting_time, ending_time, reservation_id)

                reserved_slots[day].append(time_range)

                # Inform the user and refresh the UI
                messagebox.showinfo("Success", f"Slot {time_range} reserved.")
                show_slots(day)  # Refresh UI to reflect reserved slots
            except Exception as e:
                messagebox.showerror("Error", f"Failed to reserve slot: {str(e)}")

    def show_slots(day):
        """Display time slots and mark reserved slots."""
        for widget in dynamic_frame.winfo_children():
            widget.destroy()

        date_text = f"{day}: {date.today() if day == 'Today' else date.today() + timedelta(days=1)}"
        section_label = tk.Label(dynamic_frame, text=date_text, font=("Arial", 16, "bold"), pady=10)
        section_label.pack()

        dropdown_frame = tk.Frame(dynamic_frame)
        dropdown_frame.pack()

        for row in time_slots:
            row_frame = tk.Frame(dropdown_frame)
            row_frame.pack()
            for time_range in row:
                if time_range in reserved_slots[day]:
                    time_button = ttk.Button(row_frame, text=f"❌ Reserved ({time_range})", width=20, state="disabled")
                else:
                    time_button = ttk.Button(row_frame, text=time_range, width=15, command=lambda t=time_range: reserve_slot(day, t, user_id))
                time_button.pack(side="left", padx=10, pady=10)

        # Debugging: Print current reserved slots
        print(f"DEBUG: Showing slots for {day}: {reserved_slots[day]}")


    def handle_today():
        show_slots("Today")

    def handle_tomorrow():
        show_slots("Tomorrow")
        
    

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
            
    reservation_window.protocol("WM_DELETE_WINDOW", reservation_window.destroy)
    reservation_window.mainloop()
    
if __name__ == "_main_":
    open_reservation()