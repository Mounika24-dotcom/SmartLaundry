import mysql.connector
from mysql.connector import errorcode

# Database configuration
DB_CONFIG = {
    'user': 'fatue2024bis698g6',
    'password': 'warm',
    'host': '141.209.241.91',
    'database': 'fatue2024bis698g6s',
}

# Function to create a database connection
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        raise Exception(f"Database connection error: {err}")
