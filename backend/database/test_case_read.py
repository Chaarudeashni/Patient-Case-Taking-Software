from database.connection import get_db
from database.crud import get_case_by_case_id


db = get_db()

try:
    case = get_case_by_case_id(
        db=db,
        case_id="C001"
    )

    if case is None:
        print("Case not found.")
    else:
        print("\nCase retrieved successfully!")
        print("Database ID:", case.id)
        print("Case ID:", case.case_id)
        print("Patient ID:", case.patient_id)
        print("Clinician ID:", case.clinician_id)
        print("Case date:", case.case_date)
        print("Status:", case.status)
        print("Summary:", case.summary)

finally:
    db.close()