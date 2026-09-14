from datetime import date

from database.connection import get_db
from services.case_service import (
    create_new_patient,
    get_patient,
)


db = get_db()

try:
    patient = create_new_patient(
        db=db,
        patient_id="P003",
        first_name="Service",
        last_name="Test",
        date_of_birth=date(1988, 3, 20),
        gender="Male",
        phone="9000000002",
        email="service.test@example.com",
        address="Demo Address"
    )

    print("\nPatient created through service layer!")
    print("Patient ID:", patient.patient_id)
    print("Name:", patient.first_name, patient.last_name)

    retrieved_patient = get_patient(
        db=db,
        patient_id="P003"
    )

    if retrieved_patient:
        print("\nPatient retrieved through service layer!")
        print("Patient ID:", retrieved_patient.patient_id)
        print("Name:", retrieved_patient.first_name, retrieved_patient.last_name)
    else:
        print("\nPatient could not be retrieved.")

finally:
    db.close()