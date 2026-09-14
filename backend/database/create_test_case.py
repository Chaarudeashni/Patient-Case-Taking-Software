from database.connection import get_db
from database.models import Patient, User
from database.crud import create_case

db = get_db()

try:
    # Get an existing synthetic patient
    patient = db.query(Patient).first()

    # Get an existing synthetic clinician
    clinician = db.query(User).first()

    if patient is None:
        print("No patient found in the database.")
    elif clinician is None:
        print("No user found in the database.")
    else:
        case = create_case(
            db=db,
            case_id="C002",
            patient_id=patient.id,
            clinician_id=clinician.id,
            status="active",
            summary="Synthetic test case for complaint CRUD"
        )

        print("\nTest case created successfully!")
        print("Database ID:", case.id)
        print("Case ID:", case.case_id)
        print("Patient ID:", case.patient_id)
        print("Clinician ID:", case.clinician_id)
        print("Status:", case.status)
        print("Summary:", case.summary)

finally:
    db.close()