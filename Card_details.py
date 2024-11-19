import tkinter as tk

def open_card_details():
    # Create the main window
    root = tk.Tk()
    root.title("Credit Card Information")

    #root.state("zoomed")  # Maximized for Windows
    root.attributes('-fullscreen', True)  

    # Create a frame for the form
    form_frame = tk.Frame(root, padx=20, pady=20)
    form_frame.pack(expand=True)  # Center the frame and make it responsive
    # Define Labels and Entry fields
    labels = [
        "Card Holder Name",
        "Card Number",
        "CVV",
        "Expiry Date"
    ]
    entries = []

    for i, label_text in enumerate(labels):
        tk.Label(form_frame, text=label_text, font=("Arial", 14)).grid(
            row=i, column=0, padx=10, pady=5, sticky='e'
        )
        entry = tk.Entry(form_frame, font=("Arial", 14))
        entry.grid(row=i, column=1, padx=10, pady=5, sticky='we')
        entries.append(entry)

    # Define the Submit Button
    submit_button = tk.Button(form_frame, text="Submit", font=("Arial", 14))
    submit_button.grid(row=len(labels), column=0, columnspan=2, pady=10)

    # Make columns responsive
    form_frame.grid_columnconfigure(0, weight=1)  # Label column adjusts to size
    form_frame.grid_columnconfigure(1, weight=2)  # Entry column takes more space

    # Run the application
    root.mainloop()