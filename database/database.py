import mysql.connector

from database.config import db_config, DATABASE_NAME

# Shared connection and cursor for the whole app and project.
# They start as None and are filled in by initialize().

# GUYS, FOR HOW TO USE IN YOUR FILE:
#     from database import database as db
#
#     db.cursor.execute("SELECT * FROM ambulances")
#     rows = db.cursor.fetchall()
#     db.connection.commit()   # after INSERT / UPDATE / DEL\

connection = None
cursor = None


def connect_to_db():
    """Connect to the MySQL server. Returns True if it worked."""
    global connection, cursor
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        print("Connected to the database server")
        return True
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return False


def create_database():
    """Create our database if it is missing, then switch to it."""
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    cursor.execute(f"USE {DATABASE_NAME}")


def create_tables():
    """Create the 4 tables if they do not exist yet."""

    # ambulances comes first because emergencies and dispatch_log point to it
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ambulances (
            ambulance_id INT AUTO_INCREMENT PRIMARY KEY,
            plate_number VARCHAR(20) NOT NULL UNIQUE,
            district     VARCHAR(50) NOT NULL,
            status       VARCHAR(20) NOT NULL DEFAULT 'AVAILABLE'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emergencies (
            emergency_id  INT AUTO_INCREMENT PRIMARY KEY,
            type          VARCHAR(50)  NOT NULL,
            district      VARCHAR(50)  NOT NULL,
            landmark      VARCHAR(100),
            severity      VARCHAR(20)  NOT NULL,
            caller_number VARCHAR(15)  NOT NULL,
            status        VARCHAR(20)  NOT NULL DEFAULT 'REPORTED',
            ambulance_id  INT,
            arrival_time  DATETIME,
            time_reported DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ambulance_id) REFERENCES ambulances(ambulance_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            contact_id    INT AUTO_INCREMENT PRIMARY KEY,
            patient_name  VARCHAR(100) NOT NULL,
            contact_name  VARCHAR(100) NOT NULL,
            contact_phone VARCHAR(15)  NOT NULL,
            relationship  VARCHAR(50)  NOT NULL

        )
    """)

    # One row every time an emergency changes status (REPORTED -> DISPATCHED
    # -> ARRIVED ...). The timestamps here are used for response-time stats.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dispatch_log (
            log_id       INT AUTO_INCREMENT PRIMARY KEY,
            emergency_id INT NOT NULL,
            ambulance_id INT,
            status       VARCHAR(20) NOT NULL,
            logged_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (emergency_id) REFERENCES emergencies(emergency_id),
            FOREIGN KEY (ambulance_id) REFERENCES ambulances(ambulance_id)
        )
    """)

    connection.commit()


def seed_ambulances():
    """Add some sample ambulances so the app can be tested right away."""

    # (plate_number, district) - status is AVAILABLE by default
    sample_ambulances = [
        ("RAD 101 A", "Gasabo"),
        ("RAD 102 A", "Gasabo"),
        ("RAD 103 A", "Gasabo"),
        ("RAD 201 B", "Kicukiro"),
        ("RAD 202 B", "Kicukiro"),
        ("RAD 301 C", "Nyarugenge"),
        ("RAD 302 C", "Nyarugenge"),
    ]

    # INSERT IGNORE skips a plate number that is already in the table,
    # so running this every time the app starts will not make duplicates
    cursor.executemany(
        "INSERT IGNORE INTO ambulances (plate_number, district) VALUES (%s, %s)",
        sample_ambulances
    )
    connection.commit()


def initialize():
    """Connect, make sure the database and tables exist, and get ready to use.
    Call this once at the start of the program. Returns True if it worked."""
    if not connect_to_db():
        return False
    try:
        create_database()
        create_tables()
        seed_ambulances()
        print("Database is ready")
        return True
    except mysql.connector.Error as err:
        print(f"Error setting up the database: {err}")
        return False


def close_db_connection():
    """Close the cursor and connection. Call this when the program exits."""
    global connection, cursor
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    cursor = None
    connection = None
    print("Database connection closed")
