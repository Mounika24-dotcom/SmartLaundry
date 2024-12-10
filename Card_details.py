import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
from db_config import DB_CONFIG
from Backend import save_payment_details

def validate_payment_details(entries):
    """
    Validates the payment details entered by the user.
    """
    card_number = entries[1].get()
    security_code = entries[2].get()

    if not card_number.isdigit() or len(card_number) != 16:
        messagebox.showerror("Error", "Card Number must be a 16-digit number.")
        return False
    if not security_code.isdigit() or len(security_code) != 3:
        messagebox.showerror("Error", "CVV must be a 3-digit number.")
        return False
    return True

from Backend import send_notification  # Ensure send_notification is imported

from Backend import send_notification  # Ensure send_notification is imported

def save_payment_to_db(entries, user_id):
    try:
        card_holder_name = entries[0].get()
        card_number = entries[1].get()
        security_code = entries[2].get()
        expiry_date = entries[3].get()

        # Convert expiry date format
        try:
            formatted_expiry_date = datetime.strptime(expiry_date, "%m/%y").strftime("%Y-%m-01")
        except ValueError:
            messagebox.showerror("Error", "Invalid expiry date format. Use MM/YY format.")
            return False

        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Fetch the number of slots booked for unpaid reservations
        slots_query = """
        SELECT COUNT(*)
        FROM Laundry_Timeslot
        WHERE Reservation_ID IN (
            SELECT Reservation_ID
            FROM Reservation
            WHERE User_ID = %s AND Paid = 0
        )
        """
        cursor.execute(slots_query, (user_id,))
        slots_booked = cursor.fetchone()[0]

        if slots_booked == 0:
            messagebox.showinfo("Info", "No unpaid reservations found.")
            cursor.close()
            connection.close()
            return False

        # Calculate amount
        amount = slots_booked * 2.00

        # Save payment details
        save_payment_details(user_id, card_holder_name, card_number, security_code, formatted_expiry_date, amount)

        # Mark reservations as paid
        update_query = """
        UPDATE Reservation
        SET Paid = 1
        WHERE User_ID = %s AND Paid = 0
        """
        cursor.execute(update_query, (user_id,))
        connection.commit()

        # Send notification
        notification_message = f"Payment of ${amount:.2f} has been successfully processed for your reservations."
        send_notification(user_id, notification_message, "Payment Confirmation")

        # Display notification directly
        messagebox.showinfo("Notification", notification_message)

        # Close the connection
        cursor.close()
        connection.close()

        # Show success message
        messagebox.showinfo("Success", f"Payment successfull!")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Payment failed: {str(e)}")
        return False


def make_payment(entries, user_id, amount_label_var):
    """
    Handles the payment process when the 'Make Payment' button is clicked.
    Updates the amount to zero upon success.
    """
    if not validate_payment_details(entries):
        return

    if save_payment_to_db(entries, user_id):
        # Update amount to zero
        amount_label_var.set("Amount to be Charged: $0.00")

def show_notifications(user_id):
    """
    Fetch and display notifications for the user.
    """
    from Backend import fetch_records  # Ensure the function to fetch records is imported

    notifications = fetch_records("Notification", columns="Message, Created_At")
    if not notifications:
        messagebox.showinfo("Notifications", "No new notifications.")
        return

    # Create a string to display notifications
    notification_text = "\n".join(
        [f"{n['Created_At']}: {n['Message']}" for n in notifications]
    )
    messagebox.showinfo("Notifications", notification_text)

def open_card_details(user_id=None):
    """
    Opens the payment details window with dynamic amount and payment processing in full-screen mode.
    """
    def fetch_and_display_amount():
        """
        Fetch the latest amount dynamically for unpaid reservations and update the display.
        """
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            cursor = connection.cursor()

            slots_query = """
            SELECT COUNT(*)
            FROM Laundry_Timeslot
            WHERE Reservation_ID IN (
                SELECT Reservation_ID
                FROM Reservation
                WHERE User_ID = %s AND Paid = 0
            )
            """
            cursor.execute(slots_query, (user_id,))
            slots_booked = cursor.fetchone()[0]

            cursor.close()
            connection.close()

            amount = slots_booked * 2.00
            amount_label_var.set(f"Amount to be Charged: ${amount:.2f}")
        except Exception as e:
            amount_label_var.set("Error fetching amount.")
            print(f"Error fetching amount: {str(e)}")

    def validate_fields(*args):
        """
        Enable the Save button only when all fields are filled.
        """
        if all(entry.get().strip() for entry in entries):
            save_button.config(state=tk.NORMAL)
        else:
            save_button.config(state=tk.DISABLED)

    # Create card details window
    card_details_window = tk.Toplevel()
    card_details_window.title("Credit Card Information")
    card_details_window.attributes('-fullscreen', True)  # Make the window full-screen

    # Add heading in the middle of the window
    heading_label = tk.Label(
        card_details_window,
        text="Card Details",
        font=("Arial", 24, "bold"),
        fg="blue"
    )
    heading_label.pack(pady=20)
    
    # Create form frame
    form_frame = tk.Frame(card_details_window, padx=20, pady=20)
    form_frame.pack(expand=True)

    # Labels and entry fields
    labels = ["Card Holder Name", "Card Number", "CVV", "Expiry Date (MM/YY)"]
    entries = []

    for i, label_text in enumerate(labels):
        tk.Label(form_frame, text=label_text, font=("Arial", 14)).grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entry = tk.Entry(form_frame, font=("Arial", 14))
        entry.grid(row=i, column=1, padx=10, pady=5, sticky='we')
        entries.append(entry)

        entry.bind("<KeyRelease>", validate_fields)

    amount_label_var = tk.StringVar(value="Fetching amount...")
    amount_label = tk.Label(form_frame, textvariable=amount_label_var, font=("Arial", 14), fg="green")
    amount_label.grid(row=len(labels), column=0, columnspan=2, pady=5)

    save_button = tk.Button(
        form_frame, text="Save", font=("Arial", 14),
        state=tk.DISABLED,
        command=lambda: save_payment_to_db(entries, user_id)
    )
    save_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

    back_button = tk.Button(
        form_frame, text="Back", font=("Arial", 14),
        command=card_details_window.destroy
    )
    back_button.grid(row=len(labels) + 2, column=0, columnspan=2, pady=10)


    make_payment_button = tk.Button(
        form_frame, text="Make Payment", font=("Arial", 14),
        command=lambda: make_payment(entries, user_id, amount_label_var)
    )
    make_payment_button.grid(row=len(labels) + 3, column=0, columnspan=2, pady=10)

    fetch_and_display_amount()
