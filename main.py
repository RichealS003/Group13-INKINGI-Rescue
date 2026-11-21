from database import database as db
from menus.reporter import reporter_menu 
from menus.dispatcher import dispatcher_menu

def display_main_menu():
    while True:
        print("="*85)
        print(f"{'WELCOME TO INKINGI RESCUE':>55}\n {'Emergency Dispatch Management.':>58}")        
        print("="*85) 

        print("Who are you? ")
        print("1. Reporter")
        print("2. Dispatcher")
        print("3. Exit")
        choice = (input("Please select one of the options (1-3): ")).strip()
        

        if choice == "1":
            reporter_menu()
        elif choice == "2":
            dispatcher_menu()
        elif choice == "3":
            print("Exiting the application...")
            break
        else:
            print("Invalid choice. Please select one of the options(1-3)")


def main():
    if not db.initialize():
        print("Could not set up the database. Exiting.")
        return

    try:
        #Removed this print statement to avoid duplicate printing of the welcome message.
        # print("Welcome to INKINGI Rescue")
        # menus will be called from here
        display_main_menu()
    finally:
        db.close_db_connection()


if __name__ == "__main__":
    main()
