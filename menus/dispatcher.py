from database import database as db

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