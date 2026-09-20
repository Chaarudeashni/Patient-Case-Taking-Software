from database.connection import get_db
from database.models import Case

db = get_db()

try:
    cases = db.query(Case).order_by(Case.id.asc()).all()

    print("\nExisting cases:")

    if not cases:
        print("No cases found.")
    else:
        for case in cases:
            print(
                f"ID: {case.id} | "
                f"Case ID: {case.case_id} | "
                f"Patient ID: {case.patient_id} | "
                f"Clinician ID: {case.clinician_id}"
            )

finally:
    db.close()