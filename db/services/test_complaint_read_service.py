from database.connection import get_db
from services.case_service import get_case_complaints

db = get_db()

try:
    case_id = 1

    complaints = get_case_complaints(
        db=db,
        case_id=case_id
    )

    print("\nComplaint read service test successful!")
    print("Number of complaints:", len(complaints))

    for complaint in complaints:
        print("\n--- Complaint ---")
        print("Database ID:", complaint.id)
        print("Case ID:", complaint.case_id)
        print("Complaint:", complaint.complaint)
        print("Duration:", complaint.duration)
        print("Onset:", complaint.onset)
        print("Location:", complaint.location)
        print("Severity:", complaint.severity)
        print(
            "Associated symptoms:",
            complaint.associated_symptoms
        )

finally:
    db.close()