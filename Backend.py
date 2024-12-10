import mysql.connector
from mysql.connector import errorcode
from tkinter import messagebox
import time
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'user': 'fatue2024bis698g6',
    'password': 'warm',
    'host': '141.209.241.91',
    'database': 'fatue2024bis698g6s',
}

# SQL commands to create tables
CREATE_TABLES_SQL = [
    """
    CREATE TABLE IF NOT EXISTS User (
        User_ID VARCHAR(50),
        FirstName VARCHAR(50),
        LastName VARCHAR(50),
        Password VARCHAR(50),
        Email VARCHAR(100),
        Phone VARCHAR(15),
        PRIMARY KEY (User_ID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Laundry_Machine (
        Machine_ID INT AUTO_INCREMENT,
        Status VARCHAR(20),
        Remaining_Time INT,
        PRIMARY KEY (Machine_ID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Reservation (
        Reservation_ID INT AUTO_INCREMENT,
        User_ID VARCHAR(50),
        Date DATE,
        Time VARCHAR(20),
        Machine_ID INT,
        PRIMARY KEY (Reservation_ID),
        FOREIGN KEY (User_ID) REFERENCES User(User_ID),
        FOREIGN KEY (Machine_ID) REFERENCES Laundry_Machine(Machine_ID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Laundry_Timeslot (
        ReservationItem_ID VARCHAR(255) PRIMARY KEY,
        Starting_time TIME,
        Ending_time TIME,
        Reservation_ID INT,
        Penalty_amount DECIMAL(10, 2),
        FOREIGN KEY (Reservation_ID) REFERENCES Reservation(Reservation_ID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Payment (
        Payment_ID INT AUTO_INCREMENT,
        Amount DECIMAL(10, 2),
        Card_Holder_Name VARCHAR(100),
        Phone_Number VARCHAR(15),
        Card_Number VARCHAR(16),
        Security_Code VARCHAR(4),
        Expiry_Date DATE,
        Reservation_ID INT,
        PRIMARY KEY (Payment_ID),
        FOREIGN KEY (Reservation_ID) REFERENCES Reservation(Reservation_ID)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Notification (
        Notification_ID INT AUTO_INCREMENT PRIMARY KEY,
        User_ID VARCHAR(50),
        Message TEXT,
        Notification_Type VARCHAR(255),
        Status VARCHAR(50) DEFAULT 'Unread',
        Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (User_ID) REFERENCES User(User_ID)
    );
    """
    """
    CREATE TABLE IF NOT EXISTS Penalty (
        penalty_id INT AUTO_INCREMENT PRIMARY KEY,
        User_id INT,
        penalty_reason TEXT,
        penalty_amount DECIMAL(10, 2),
        status VARCHAR(50) DEFAULT 'Unpaid',
        issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (User_id) REFERENCES User(User_ID)
    );
    """
]


def reserve_machine(machine_id):
    """
    Mark the machine as 'Running' when a reservation is made.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        update_query = "UPDATE Laundry_Machine SET Status = 'Running' WHERE Machine_ID = %s"
        cursor.execute(update_query, (machine_id,))
        conn.commit()

        print(f"Machine {machine_id} is now running.")
    except mysql.connector.Error as err:
        print(f"Database error while reserving machine: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def release_machine(machine_id):
    """
    Mark the machine as 'Empty' when the reservation ends.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        update_query = "UPDATE Laundry_Machine SET Status = 'Empty' WHERE Machine_ID = %s"
        cursor.execute(update_query, (machine_id,))
        conn.commit()

        print(f"Machine {machine_id} is now available.")
    except mysql.connector.Error as err:
        print(f"Database error while releasing machine: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def initialize_database():
    """Initializes the MySQL database and creates tables if not already created."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Create tables
        for sql in CREATE_TABLES_SQL:
            cursor.execute(sql)

        conn.commit()
        print("Database and tables initialized successfully.")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Invalid username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist. Please create the database first.")
        else:
            print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
def apply_penalty(user_id):
    """
    Check if a user exceeded their reserved time and apply a penalty.
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Fetch reservations where the machine was used beyond the reserved time
        query = """
        SELECT lt.ReservationItem_ID, lt.Ending_time, r.User_ID
        FROM Laundry_Timeslot lt
        JOIN Reservation r ON lt.Reservation_ID = r.Reservation_ID
        WHERE r.User_ID = %s AND TIMEDIFF(NOW(), lt.Ending_time) > 0;
        """
        cursor.execute(query, (user_id,))
        exceeded_reservations = cursor.fetchall()

        for reservation in exceeded_reservations:
            reservation_item_id, ending_time, user_id = reservation

            # Calculate exceeded hours
            exceeded_time = (datetime.now() - ending_time).total_seconds() / 3600
            exceeded_hours = int(exceeded_time)

            # Calculate penalty amount
            penalty_amount = exceeded_hours * 25

            # Insert penalty record
            penalty_query = """
            INSERT INTO Penalty (User_id, penalty_reason, penalty_amount)
            VALUES (%s, %s, %s);
            """
            penalty_reason = f"Exceeded reserved time by {exceeded_hours} hours."
            cursor.execute(penalty_query, (user_id, penalty_reason, penalty_amount))
            conn.commit()

            # Send penalty notification
            penalty_message = f"A penalty of ${penalty_amount:.2f} has been applied for exceeding the reserved time by {exceeded_hours} hours."
            send_notification(user_id, penalty_message, "Penalty Applied")

            print(f"Applied penalty of ${penalty_amount:.2f} for User_ID: {user_id}")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Database error while applying penalty: {err}")
    except Exception as e:
        print(f"Error applying penalty: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def fetch_machine_data():
    """
    Fetch the status and remaining time of all machines from the database.
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query = "SELECT Machine_ID, Status, Remaining_Time FROM Laundry_Machine"
        cursor.execute(query)
        machine_data = cursor.fetchall()

        cursor.close()
        connection.close()
        return machine_data
    except Exception as e:
        raise Exception(f"Error fetching machine data: {str(e)}")

def fetch_records(table_name, columns="*"):
    """Fetch records from a specified table."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT {columns} FROM {table_name}"
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as err:
        print(f"Error fetching records: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
def send_notification(user_id, message, notification_type='Payment Confirmation'):
    """Function to send a notification after a payment is successful."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Check if the user exists
        check_user_query = "SELECT User_ID FROM User WHERE User_ID = %s"
        cursor.execute(check_user_query, (user_id,))
        if not cursor.fetchone():
            raise Exception(f"User ID {user_id} does not exist. Cannot send notification.")

        # Insert the notification into the Notification table
        insert_notification = """
        INSERT INTO Notification (User_ID, Message, Notification_Type, Status)
        VALUES (%s, %s, %s, 'Unread');
        """
        cursor.execute(insert_notification, (user_id, message, notification_type))
        conn.commit()

        print("Notification sent successfully!")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def process_payment(user_id, amount, booking_id):
    """Function to process payment and send a notification."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Mark the payment as successful in the database
        update_payment = """
        UPDATE Payment SET Status = 'Paid' WHERE Reservation_ID = %s;
        """
        cursor.execute(update_payment, (booking_id,))
        conn.commit()

        # Send a notification
        message = f"Your payment of ${amount} for laundry slot {booking_id} is successful. Thank you!"
        send_notification(user_id, message)

        print("Payment processed and notification sent!")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def save_payment_details(user_id, card_holder_name, card_number, security_code, expiry_date, amount):
    """Save payment details for a user."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Fetch reservation ID for the user
        reservation_query = """
        SELECT Reservation_ID 
        FROM Reservation 
        WHERE User_ID = %s 
        ORDER BY Reservation_ID DESC LIMIT 1
        """
        cursor.execute(reservation_query, (user_id,))
        reservation_result = cursor.fetchone()
        if not reservation_result:
            raise Exception("No reservation found for this user.")
        reservation_id = reservation_result[0]

        # Insert payment details into the Payment table
        payment_query = """
        INSERT INTO Payment (Amount, Card_Holder_Name, Card_Number, Security_Code, Expiry_Date, Reservation_ID)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(payment_query, (amount, card_holder_name, card_number, security_code, expiry_date, reservation_id))
        conn.commit()

        print(f"Payment details saved successfully for Reservation ID: {reservation_id}")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Database error while saving payment details: {err}")
    except Exception as e:
        print(f"Error saving payment details: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def save_user(user_id, first_name, last_name, password, email, phone):
    """Save user details."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
            INSERT INTO User (User_ID, FirstName, LastName, Password, Email, Phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, first_name, last_name, password, email, phone))
        conn.commit()

        messagebox.showinfo("Success", "Account created successfully!")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to save user: {err}")

def save_laundry_timeslot(reservationitem_id, starting_time, ending_time, reservation_id):
    """Save a laundry timeslot."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        INSERT INTO Laundry_Timeslot (ReservationItem_ID, Starting_time, Ending_time, Reservation_ID)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (reservationitem_id, starting_time, ending_time, reservation_id))
        conn.commit()

        print(f"Timeslot saved successfully for Reservation_ID: {reservation_id}")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Database error while saving timeslot: {err}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            
def generate_id(user_id):
    """Generate a unique ID by combining user_id and the current timestamp."""
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    return f"{user_id}_{timestamp}"  # Combine user_id and timestamp into a unique ID
 
def refresh_amount_on_signout(user_id):
    """
    Refresh unpaid reservations and reset the amount to zero for the user on sign-out.
    """
    try:
        # Apply penalties before refreshing amounts
        apply_penalty(user_id)

        # Proceed with the existing logic to reset unpaid amounts
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Fetch and reset unpaid amounts
        query = """
        SELECT COUNT(*) * 2.00 AS Amount
        FROM Laundry_Timeslot
        WHERE Reservation_ID IN (
            SELECT Reservation_ID FROM Reservation WHERE User_ID = %s AND Paid = FALSE
        )
        """
        cursor.execute(query, (user_id,))
        total_amount = cursor.fetchone()[0]
        print(f"DEBUG: Unpaid amount for user {user_id}: ${total_amount:.2f}")

        # Mark reservations as paid
        update_query = """
        UPDATE Reservation SET Paid = TRUE WHERE User_ID = %s AND Paid = FALSE;
        """
        cursor.execute(update_query, (user_id,))

        # Reset payment amounts
        reset_query = """
        UPDATE Payment
        SET Amount = 0.00
        WHERE Reservation_ID IN (
            SELECT Reservation_ID FROM Reservation WHERE User_ID = %s
        )
        """
        cursor.execute(reset_query, (user_id,))

        conn.commit()
        print(f"DEBUG: Refreshed unpaid reservations and reset amount to zero for user {user_id}.")
    except mysql.connector.Error as err:
        print(f"Error refreshing amount on sign-out: {err}")
        raise
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()



# Call the function to initialize the database
if __name__ == "_main_":
    initialize_database()