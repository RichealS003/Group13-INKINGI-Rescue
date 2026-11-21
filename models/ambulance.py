from database import database as db
import mysql.connector
class Ambulance:
    def __init__(self, plate_number, district, ambulance_id=None,
                 status = "AVAILABLE",arrival_time=None):
        """ Initialize an Ambulance

        """
        self.ambulance_id = ambulance_id
        self.plate_number = plate_number
        self.district = district
        self.status = status
        self.arrival_time = arrival_time

    @classmethod
    def find_available(cls):
        """ Find available ambulances

        """
        try:
            sql_read_query = """
            SELECT ambulance_id, plate_number, district, status
            FROM ambulances WHERE status = %s
            """
            db.cursor.execute(sql_read_query, ("AVAILABLE",))
            print(f"Successful!")
            rows = db.cursor.fetchall()
            return [cls(plate_number, district,
            ambulance_id=a_id, status=status)
            for a_id, plate_number, district, status in rows]
        except mysql.connector.Error as err:
            print(f"Error retrieveing ambulances from the database: {err}")
            return []


    def update_status(self, new_status):
        """ Change the status of an ambulance

        """
        try:
            db.cursor.execute(
                "UPDATE ambulances SET status = %s WHERE ambulance_id = %s",
                 (new_status, self.ambulance_id)
            )
            db.connection.commit()
            if db.cursor.rowcount == 0:
                print(f"No ambulance found with ID {self.ambulance_id}")
                return False
            self.status = new_status
            print(f"Successful!")
            return True

        except mysql.connector.Error as err:
            print(f"Error updating ambulance table in the database: {err}")
            return False