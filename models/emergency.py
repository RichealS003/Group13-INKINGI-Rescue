from database import database as db
import mysql.connector
class Emergency:
    def __init__(self, emergency_type, district, landmark, severity, caller_number, emergency_id=None,
                 status="REPORTED", ambulance_id=None,time_reported=None,arrival_time=None ):
        """ Initalize an emergency

        """
        self.emergency_id = emergency_id
        self.emergency_type = emergency_type
        self.district = district
        self.landmark = landmark
        self.severity = severity
        self.caller_number = caller_number
        self.status = status
        self.ambulance_id = ambulance_id
        self.time_reported = time_reported
        self.arrival_time =  arrival_time

    def insert_emergencies(self):
        """Insert new emergencies

        """
        try:
            sql_insert_query = """
            INSERT INTO emergencies (emergency_type, district, landmark, severity,
            caller_number, status, ambulance_id, arrival_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            new_emergency = (self.emergency_type, self.district, self.landmark, self.severity,
                             self.caller_number, self.status, self.ambulance_id, self.arrival_time)
            db.cursor.execute(sql_insert_query, new_emergency)
            db.connection.commit()
            self.emergency_id = db.cursor.lastrowid
            print(f"Successful!")
            return True

        except mysql.connector.Error as err:
            print(f"Error adding emergency to the database: {err}")
            return False