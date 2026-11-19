from database import database as db


def main():
    if not db.initialize():
        print("Could not set up the database. Exiting.")
        return

    try:
        print("Welcome to INKINGI Rescue")
        # menus will be called from here
    finally:
        db.close_db_connection()


if __name__ == "__main__":
    main()
