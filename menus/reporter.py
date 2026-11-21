from database import database as db

def update_circle_of_trust():
    # this function lets the reporter add emergency contacts for a specific patient.
    print("\nCIRCLE OF TRUST")
    
    # first we ask for the patients name so we know whose contacts these are
    patient_name = input("Enter the patient's full name (e.g., John Doe): ").strip()
    
    if not patient_name:
        print("Patient name cannot be empty. Returning to menu.")
        return

    while True:
        print(f"\nAdding contacts for: {patient_name}")
        contact_name = input("Contact Name (or type 'done' to finish): ").strip()
        
        if contact_name.lower() == 'done':
            break
            
        if not contact_name:
            print("Contact name cannot be empty. Try again.")
            continue

        contact_phone = input("Contact Phone (e.g., 0799888777): ").strip()
        relationship = input("Relationship (e.g., Mother, Brother): ").strip()
        
        # second we insert the data into the MySQL database
        try:
            query = """
                INSERT INTO contacts (patient_name, contact_name, contact_phone, relationship)
                VALUES (%s, %s, %s, %s)
            """
            values = (patient_name, contact_name, contact_phone, relationship)
            
            db.cursor.execute(query, values)
            db.connection.commit()
            print(f"Success! {contact_name} added to the Circle of Trust.")
            
        except Exception as e:
            print(f"Database Error: Could not save contact. {e}")
            
    print("\nReturning to Reporter Menu...")