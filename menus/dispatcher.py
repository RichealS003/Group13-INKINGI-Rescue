from database import database as db
from utils.validators import get_menu_choice, get_phone_number, get_place_text


def manage_circle_of_trust():
    # this funstion Lets the dispatcher view contacts and send simulated alerts.
    print("\nCIRCLE OF TRUST MANAGEMENT")
    
    # first we need to know which patient or emergency we are looking up
    patient_name = input("Enter the patient's full name to look up contacts: ").strip()
    
    if not patient_name:
        print("Patient name cannot be empty. Returning to menu.")
        return

    # then we try to fetch their contacts from the database
    try:
        query = "SELECT contact_name, contact_phone, relationship FROM contacts WHERE patient_name = %s"
        db.cursor.execute(query, (patient_name,))
        contacts = db.cursor.fetchall()
        
        if not contacts:
            print(f"\nNo contacts found for {patient_name} in the Circle of Trust.")
            return
            
        print(f"\nContacts for {patient_name}:")
        for index, contact in enumerate(contacts, start=1):
           
            print(f"{index}. {contact[0]} ({contact[2]}) - {contact[1]}")
            
    except Exception as e:
        print(f"Database Error: Could not fetch contacts. {e}")
        return

    # lastly we simulate sending an alert to everyone in the list
    print("\nSENDING EMERGENCY ALERTS...")
    for contact in contacts:
        contact_name = contact[0]
        phone = contact[1]
        print(f"Alert sent to {contact_name} at {phone}: Emergency reported for {patient_name}. Help is on the way.")

    print("\nAlerts completed. Returning to Dispatcher Menu...")


#This is the function for marking an emergency as resolved. 
# Dispatcher menu option 4.
def resolve_emergency():
    emergency_input = input("Enter the Emergency ID for the emergency you want to resolve: ").strip()
    db.cursor.execute("SELECT * FROM emergencies WHERE emergency_id = %s", (emergency_input, ))
    emergency = db.cursor.fetchone()

    if emergency is None:
        print(f"\nEmergency ID not found. Please check and try again.")
        return
    else:
        #This is based on the current order in the emergency table
        current_status = emergency[6].upper()
        ambulance_id = emergency[7]

    if current_status == "RESOLVED":
        print("This emergency has already been resolved.")
        return
    #An emergency can only be marked as resolved when the ambulance has been dispatched and arrives at the location.
    if current_status != "DISPATCHED":
        print("This emergency cannot be resolved because an ambulance has not yet been dispatched for it.")
        return

    confirmation = input("Has the ambulance arrived at the location? (Yes/No)").strip().lower()
    if confirmation == "no" or confirmation == "n":
        print("The ambulance has not arrived yet.")
        return
    elif confirmation != "yes" and confirmation != "y":
        print("Invalid choice. Please try again.")
        return

    try:
        #NOW() uses the database clock, the same clock that set time_reported.
        #Using Python's datetime.now() here would be 2 hours off (Kigali time vs the server's UTC).
        db.cursor.execute("UPDATE emergencies SET status = %s, arrival_time = NOW() WHERE emergency_id = %s", ("RESOLVED", emergency_input))
        #The ambulance is free again so it can be dispatched to the next emergency.
        db.cursor.execute("UPDATE ambulances SET status = %s WHERE ambulance_id = %s", ("AVAILABLE", ambulance_id))
        db.cursor.execute("INSERT INTO dispatch_log (emergency_id, ambulance_id, status) VALUES (%s, %s, %s)", (emergency_input, ambulance_id, "RESOLVED"))
        db.connection.commit()
    except Exception as e:
        #If something failed half way, we undo the changes so nothing is saved by mistake.
        db.connection.rollback()
        print(f"Database Error: Could not resolve the emergency. {e}")
        return

    print("Emergency successfully marked as RESOLVED. Arrival time recorded.")
    print("The ambulance is now AVAILABLE again.")


def view_response_time_report():
    db.cursor.execute("""
    SELECT emergency_id, time_reported, arrival_time
    FROM emergencies
    WHERE status = 'RESOLVED' AND arrival_time IS NOT NULL
""")
    resolved_emergencies = db.cursor.fetchall()

    if not resolved_emergencies:
        print("No resolved emergencies with recorded arrival times were found. Returning to menu...")
        return

    #This will hold the running total of the response times for all the resolved emergencies.
    total_response_time = 0
    print("*"*50)
    print("INKINGI RESCUE - RESPONSE TIME REPORT.")
    print("*"*50)
    for emergency in resolved_emergencies:
        emergency_id, time_reported, arrival_time = emergency
        response_time = arrival_time - time_reported
        response_minutes = response_time.total_seconds()/60
        print(f"Emergency ID: {emergency_id}.\n Response Time: {response_minutes:.2f} minutes.")
        total_response_time += response_minutes
    average_response_time = total_response_time/len(resolved_emergencies)
    print(f"\nThe Average Response Time is: {average_response_time:.2f} minutes.")
    print("Returning to the Dispatcher screen.")
        
#These are the same lists as the reporter menu so both menus save the same values.
emergency_types = {
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


#This is the function for reporting an emergency as a dispatcher.
#Dispatcher menu option 1.
def report_emergency():
    print("Report Emergency")

    
    print("Type of emergency:")
    for number in emergency_types:
        print(f"{number}. {emergency_types[number]}")
    type_choice = get_menu_choice("Choose the type of emergency (1-4): ", 1, 4)
    emergency_type = emergency_types[type_choice]


    district = get_place_text("Which district did it happen in? (e.g. Kicukiro): ")
    landmark = get_place_text("What is the nearest landmark? (e.g. Nyanza Bus park): ")


    print("Severity level:")
    for number in severity_levels:
        print(f"{number}. {severity_levels[number]}")
    severity_choice = get_menu_choice("Choose the severity level (1-4): ", 1, 4)
    severity = severity_levels[severity_choice]


    phone_number = get_phone_number("What is the caller's phone number? ")

    #Saving the emergency in the database. The ID and the time are made by the database.
    try:
        db.cursor.execute("INSERT INTO emergencies (type, district, landmark, severity, caller_number) VALUES (%s, %s, %s, %s, %s)", (emergency_type, district, landmark, severity, phone_number))
        db.connection.commit()
        emergency_id = db.cursor.lastrowid
    except Exception as e:
        print(f"Database Error: Could not save the emergency. {e}")
        return

    print("\nEmergency reported successfully.")
    print(f"Emergency ID: {emergency_id}")
    print(f"Emergency type: {emergency_type}")
    print(f"Location: {district} - near {landmark}")
    print(f"Severity: {severity}")
    print("Status: REPORTED")
    print("\nPlease keep the Emergency ID for reference.")


#This is the function for viewing the active emergencies.
#Dispatcher menu option 2.
def view_active_emergencies():
    print("Active Emergencies")

    #Only REPORTED and DISPATCHED emergencies are active, so RESOLVED and CANCELLED are left out.
    try:
        db.cursor.execute("SELECT emergency_id, severity, status, district, landmark FROM emergencies WHERE status IN ('REPORTED', 'DISPATCHED')")
        emergencies = db.cursor.fetchall()
    except Exception as e:
        print(f"Database Error: Could not fetch the emergencies. {e}")
        return

    if len(emergencies) == 0:
        print("No active or pending emergencies. It's all quiet here.")
        return

    for emergency in emergencies:
        print(f"ID: {emergency[0]} | Severity: {emergency[1]} | Status: {emergency[2]} | Location: {emergency[3]} - near {emergency[4]}")


#This is the function for dispatching an available ambulance.
#Dispatcher menu option 3.
def dispatch_ambulance():
    emergency_input = input("Enter the Emergency ID you want to dispatch an ambulance for: ").strip()

    try:
        db.cursor.execute("SELECT * FROM emergencies WHERE emergency_id = %s", (emergency_input, ))
        emergency = db.cursor.fetchone()

        if emergency is None:
            print("Emergency ID not found. Please check and try again.")
            return

        #This is based on the current order in the emergency table
        district = emergency[2]
        current_status = emergency[6]

        #An ambulance can only be dispatched for an emergency that is still waiting.
        if current_status != "REPORTED":
            print("This emergency is not waiting for an ambulance.")
            return

        #First we look for an available ambulance in the same district (the nearest one).
        db.cursor.execute("SELECT * FROM ambulances WHERE status = 'AVAILABLE' AND district = %s", (district, ))
        ambulances = db.cursor.fetchall()

        #If there is none there, we take any available ambulance.
        if len(ambulances) == 0:
            db.cursor.execute("SELECT * FROM ambulances WHERE status = 'AVAILABLE'")
            ambulances = db.cursor.fetchall()

        if len(ambulances) == 0:
            print("No available ambulances found.")
            return

        ambulance_id = ambulances[0][0]
        plate_number = ambulances[0][1]

        #Changing both statuses and saving the dispatch time in the dispatch log.
        db.cursor.execute("UPDATE emergencies SET status = %s, ambulance_id = %s WHERE emergency_id = %s", ("DISPATCHED", ambulance_id, emergency_input))
        db.cursor.execute("UPDATE ambulances SET status = %s WHERE ambulance_id = %s", ("BUSY", ambulance_id))
        db.cursor.execute("INSERT INTO dispatch_log (emergency_id, ambulance_id, status) VALUES (%s, %s, %s)", (emergency_input, ambulance_id, "DISPATCHED"))
        db.connection.commit()

    except Exception as e:
        #If something failed half way, we undo the changes so nothing is saved by mistake.
        db.connection.rollback()
        print(f"Database Error: Could not dispatch the ambulance. {e}")
        return

    print("Ambulance dispatched successfully.")
    print(f"Emergency ID: {emergency_input}")
    print(f"Ambulance ID: {ambulance_id} ({plate_number})")


#This is the dispatcher menu.
def dispatcher_menu():
    while True:
        print("\n--------------------Dispatcher Screen--------------------")
        print("What are we doing today?")
        print("1. Report a new emergency")
        print("2. View active emergencies")
        print("3. Dispatch an available ambulance")
        print("4. Update emergency status")
        print("5. Manage circle of trust contacts")
        print("6. View response time report")
        print("0. Return to main menu")
        print("")

        user_input = get_menu_choice("Type a number between 0-6: ", 0, 6)

        if user_input == 1:
            report_emergency()
        elif user_input == 2:
            view_active_emergencies()
        elif user_input == 3:
            dispatch_ambulance()
        elif user_input == 4:
            resolve_emergency()
        elif user_input == 5:
            manage_circle_of_trust()
        elif user_input == 6:
            view_response_time_report()
        else:
            print("Invalid Choice. Returning to main menu")
            return