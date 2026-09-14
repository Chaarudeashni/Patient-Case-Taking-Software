from datetime import date

from services.schemas import PatientCreateSchema


patient = PatientCreateSchema(
    patient_id="P100",
    first_name="Validation",
    last_name="Test",
    date_of_birth=date(1995, 5, 15),
    gender="Female",
    phone="9000000000",
    email="validation.test@example.com",
    address="Demo Address"
)

print("\nPatient validation successful!")
print(patient)