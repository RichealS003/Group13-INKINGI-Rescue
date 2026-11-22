#These are placeholder names for the actual names that will be used for the various functions
from database.database import initialize_database 
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
    initialize_database()
    display_main_menu()
    
if __name__ == "__main__":
    main()