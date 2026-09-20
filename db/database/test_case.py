from datetime import date

from database.connection import get_db
from database.crud import create_case, create_patient, create_user


db = get_db()

try:
    # Create a demo patient
    patient = create_patient(
        db=db,
        patient_id="P004",
        first_name="Demo",
        last_name="Patient",
        date_of_birth=date(1990, 1, 10),
        gender="Female",
        phone="9000000001",
        email="demo.patient@example.com",
        address="Demo Address"
    )

    # Create a demo clinician
    user = create_user(
        db=db,
        username="demo_clinician_3",
        email="demo.clinician.2@example.com",
        password_hash="demo_password_hash",
        role="clinician"
    )

    # Create a case for the patient
    case = create_case(
        db=db,
        case_id="C002",
        patient_id=patient.id,
        clinician_id=user.id,
        case_date=date.today(),
        status="active",
        summary="Initial demo case"
    )

    print("\nCase created successfully!")
    print("Case database ID:", case.id)
    print("Case ID:", case.case_id)
    print("Patient database ID:", case.patient_id)
    print("Clinician database ID:", case.clinician_id)
    print("Case date:", case.case_date)
    print("Status:", case.status)
    print("Summary:", case.summary)

finally:
    db.close()