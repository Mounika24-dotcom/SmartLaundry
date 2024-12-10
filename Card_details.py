import tkinter as tk
import Backend
from Backend import initialize_database   
from tkinter import messagebox
from Backend import save_payment_details

def save_payment_to_db(entries, user_id):
    try:
        # Extract data from form
        card_holder_name = entries[0].get()
        card_number = entries[1].get()
        security_code = entries[2].get()
        expiry_date = entries[3].get()

        # Call the backend function to save payment details
        save_payment_details(user_id, card_holder_name, card_number, security_code, expiry_date)

        # Show success message
        messagebox.showinfo("Success", "Payment details saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save payment details: {str(e)}")


def validate_payment_details(entries):
    card_number = entries[1].get()
    security_code = entries[2].get()

    if not card_number.isdigit() or len(card_number) != 16:
        messagebox.showerror("Error", "Card Number must be a 16-digit number.")
        return False
    if not security_code.isdigit() or len(security_code) != 3:
        messagebox.showerror("Error", "CVV must be a 3-digit number.")
        return False
    return True

def open_card_details(user_id=None):
    # Create the card details window
    card_details_window = tk.Toplevel()
    card_details_window.title("Credit Card Information")
    card_details_window.attributes('-fullscreen', True)

    # Create a frame for the form
    form_frame = tk.Frame(card_details_window, padx=20, pady=20)
    form_frame.pack(expand=True)

    # Define Labels and Entry fields
    labels = [
        "Card Holder Name",
        "Card Number",
        "CVV",
        "Expiry Date"
    ]
    entries = []

    for i, label_text in enumerate(labels):
        tk.Label(form_frame, text=label_text, font=("Arial", 14)).grid(row=i, column=0, padx=10, pady=5, sticky='e')
        entry = tk.Entry(form_frame, font=("Arial", 14))
        entry.grid(row=i, column=1, padx=10, pady=5, sticky='we')
        entries.append(entry)

    # Submit button
    submit_button = tk.Button(
        form_frame, text="Save", font=("Arial", 14),
        command=lambda: save_payment_to_db(entries, user_id)
    )
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    # Make form responsive
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=2)
