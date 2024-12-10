import mysql.connector
from mysql.connector import errorcode
import mysql.connector
from tkinter import messagebox
from db_config import DB_CONFIG
import time

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
        Phone VARCHAR(15)
    )
   """,
    """
    CREATE TABLE IF NOT EXISTS Laundry_Machine (
      Machine_ID INT,
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
      ReservationItem_ID VARCHAR(255),
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
    """
]

def initialize_database():
    """Initializes the MySQL database and creates tables if not already created."""
    try:
        # Connect to the MySQL server
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
            
def save_laundry_timeslot(reservation_item_id, starting_time, ending_time, reservation_id, penalty_amount=0.0):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Debug: Print the values being inserted
        print(f"Inserting timeslot: ReservationItem_ID={reservation_item_id}, Starting={starting_time}, Ending={ending_time}, Reservation_ID={reservation_id}, Penalty={penalty_amount}")

        query = """
            INSERT INTO Laundry_Timeslot 
            (ReservationItem_ID, Starting_time, Ending_time, Reservation_ID, Penalty_amount)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (reservation_item_id, starting_time, ending_time, reservation_id, penalty_amount))
        connection.commit()

        print(f"Laundry timeslot saved successfully: {reservation_item_id}")
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Failed to save laundry timeslot: {str(e)}")
        raise


def save_user(user_id, first_name, last_name, password, email, phone):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = """
            INSERT INTO User (User_ID, FirstName, LastName, Password, Email, Phone)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, first_name, last_name, password, email, phone))
        connection.commit()

        messagebox.showinfo("Success", "Account created successfully!")
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to save user: {err}")
        
def generate_id(user_id):
    """Generate a unique ID by combining user_id and the current timestamp."""
    timestamp = int(time.time() * 1000)  # Current timestamp in milliseconds
    return f"{user_id}_{timestamp}"  # Combine user_id and timestamp into a unique ID


def fetch_records(table_name, columns="*"):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT {columns} FROM {table_name}"
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    except mysql.connector.Error as err:
        print(f"Error fetching records: {err}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def save_payment_details(user_id, card_holder_name, card_number, security_code, expiry_date):
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        # Calculate slots booked
        slots_query = """
        SELECT COUNT(*) 
        FROM Reservation 
        WHERE User_ID = %s
        """
        cursor.execute(slots_query, (user_id,))
        slots_booked = cursor.fetchone()[0]
        if slots_booked == 0:
            raise Exception("No reservations found for this user.")

        # Calculate the amount based on slots booked
        amount = slots_booked * 2.00

        # Fetch the latest reservation ID for the user
        reservation_query = """
        SELECT Reservation_ID 
        FROM Reservation 
        WHERE User_ID = %s 
        ORDER BY Reservation_ID DESC LIMIT 1
        """
        cursor.execute(reservation_query, (user_id,))
        reservation_id = cursor.fetchone()[0]

        # Insert the payment details into the Payment table
        payment_query = """
        INSERT INTO Payment (Amount, Card_Holder_Name, Card_Number, Security_Code, Expiry_Date, Reservation_ID)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(payment_query, (amount, card_holder_name, card_number, security_code, expiry_date, reservation_id))
        connection.commit()

        cursor.close()
        connection.close()

    except Exception as e:
        raise Exception(f"Error saving payment details: {str(e)}")

# Call the function to initialize the database
if __name__ == "__main__":
    initialize_database()
    
    
