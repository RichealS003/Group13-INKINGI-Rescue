from utils.validators import get_menu_choice, get_yes_and_no_choice, get_phone_number, get_place_text
from models.emergency import Emergency, insert_emergency, get_last_emergency_number

emergency_types_dict = {
    1: "Road Accident", 
    2: "Medical Emergency",
    3: "Fire",
    4: "Other"
}

severity_levels = {
    1: "Low", 
    2: "Medium", 
    3: "High", 
    4: "Critical"
}

#HELPER FUNCTIONS
def report_summary(emergency_type, district, landmark, severity, phone_number):
    print("\n---------------Confirm Report---------------")
    print(f"Emergency type: {emergency_type}")
    print(f"Location: {district} near {landmark}")
    print(f"Severity: {severity}")
    print(f"Phone Number: {phone_number}")

#REPORTER MENU LOGIC

def report_emergency():
    print("\n--------------------Report Emergency--------------------")

    #Getting emergency type
    emergency_type_input = get_menu_choice("1. What type of emergency are you reporting""\n1. Road accident \n2.Medical emergency \n3. Fire \n4. Other", 1, 4)
    emergency_type = emergency_types_dict[emergency_type_input]

    #Getting district
    district = get_place_text("2. Which district did the emergency occur in? (eg: Gasabo) ")

    #Getting landmark
    landmark = get_place_text("3. What is the nearest landmark? (eg: Simba Supermarket)")

    #Getting severity level
    severity_input = get_menu_choice("What is the severity level? ""\n1. Low \n2. Medium \n3. High \n4. Critical", 1,4)
    severity = severity_levels[severity_input]

    #Getting phone number
    phone_number = get_phone_number("What is your phone number? ")

    #Confirmation of report
    report_summary()
    user_confirmation = get_yes_and_no_choice("Do you want to proceed with the report? (y/n)")
    if not user_confirmation:
        print("Confirmation re")

    #insert the emergency into sql database

#MAIN REPORTER MENU

def reporter_menu():
    print("\n--------------------Reporter Screen--------------------")
    print("What are we doing today?")
    print("1. Report a new emergency")
    print("2. Update circle of trust contacts")
    print("0. Return to main menu")
    print("")

    user_input = get_menu_choice("Type a number between 0-2: ",0, 2)
    #! Call the functions
    if user_input == 1:
        pass 
    elif user_input == 2:
        pass
    else:
        print("Returning to main menu")
        return