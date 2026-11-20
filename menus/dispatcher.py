from database import database as db
import datetime







#This is the function for marking an emergency as resolved. 
# Dispatcher menu option 4.
def resolve_emergency():
    emergency_input = input("Enter the Emergency ID for the emergency you want to resolve:").strip()
    db.cursor.execute("SELECT * FROM emergencies WHERE emergency_id = %s", (emergency_input, ))
    emergency = db.cursor.fetchone()

    if emergency is None:
        print("Emergency ID not found. Please check and try again.")
        return
    else:
        #This is based on the current order in the emergency table
        current_status = emergency[6].upper()

    if current_status == "RESOLVED":
        print("This emergency has already been resolved.")
        return
    #An emergency cann only be marked as resolved when the ambulance has been dispatched and arrives at the location.
    if current_status != "DISPATCHED":
        print("This emergency cannot be resolved because an ambulance has not yet been dispatched for it.")
        return

    confirmation = input("Has the ambulance arrived at the location? (Yes/No)").strip().lower()
    if confirmation == "yes" or confirmation == "y":
        arrival_time = datetime.datetime.now()
    elif confirmation == "no" or confirmation == "n":
        print("The ambulance has not arrived yet.")
        return
    else:
        print("Invalid choice. Please try again.")
        return

    db.cursor.execute("UPDATE emergencies SET status = %s, arrival_time = %s WHERE emergency_id = %s", ("RESOLVED", arrival_time, emergency_input))
    db.connection.commit()
    print("Emergency successfully marked as RESOLVED. Arrival time recorded.")

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

