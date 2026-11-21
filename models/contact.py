class Contact:
    
    # this class stores the details of a trusted family member or friend then then dispatcher uses these contacts to send alerts when the patient is in an emergency. One patient can have multiple contacts.
    
    
    def __init__(self, patient_name, contact_name, contact_phone, relationship, contact_id=None):
        self.contact_id = contact_id
        self.patient_name = patient_name
        self.contact_name = contact_name
        self.contact_phone = contact_phone
        self.relationship = relationship

    def __str__(self):
        return f"{self.contact_name} ({self.relationship}) - {self.contact_phone}"

    def to_dict(self):
        return {
            "contact_id": self.contact_id,
            "patient_name": self.patient_name,
            "contact_name": self.contact_name,
            "contact_phone": self.contact_phone,
            "relationship": self.relationship
        }