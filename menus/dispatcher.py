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




def view_response_time_report():
    db.cursor.execute("""
    SELECT emergency_id, time_reported, arrival_time
    FROM emergencies
    WHERE status = 'RESOLVED' AND arrival_time IS NOT NULL
""")
    resolved_emergencies = db.cursor.fetchall()

    if not resolved_emergencies:
        print("No resolved emergencies with recorded arrival times were found.")
        return

    #This will hold the running total of the response times for all the resolved emergencies.
    total_response_time = 0
    print("*"*50)
    print(f"INKINGI RESCUE - RESPONSE TIME REPORT.")
    print("*"*50)
    for emergency in resolved_emergencies:
        emergency_id, time_reported, arrival_time = emergency
        response_time = arrival_time - time_reported
        response_minutes = response_time.total_seconds()/60
        print(f"Emergency ID: {emergency_id}.\n Response Time: {response_minutes:.2f} minutes.")
        total_response_time += response_minutes
    average_response_time = total_response_time/len(resolved_emergencies)
    print(f"The Average Response Time is: {average_response_time:.2f} minutes.")
        
