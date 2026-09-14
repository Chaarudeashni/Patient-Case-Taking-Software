from database.connection import get_db
from database.crud import get_patient_by_patient_id, get_cases_by_patient_id


db = get_db()

try:
    # Find the patient using the unique patient ID
    patient = get_patient_by_patient_id(
        db=db,
        patient_id="P002"
    )

    if patient is None:
        print("Patient P002 not found.")
    else:
        print("\nPatient found successfully!")
        print("Patient database ID:", patient.id)
        print("Patient ID:", patient.patient_id)
        print("Name:", patient.first_name, patient.last_name)

        # Get all cases for this patient
        cases = get_cases_by_patient_id(
            db=db,
            patient_id=patient.id
        )

        print(f"\nNumber of cases found: {len(cases)}")

        for case in cases:
            print("\nCase")
            print("-----")
            print("Case ID:", case.case_id)
            print("Case date:", case.case_date)
            print("Status:", case.status)
            print("Summary:", case.summary)

finally:
    db.close()