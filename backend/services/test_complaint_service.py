print("TEST FILE IS RUNNING")
from database.connection import get_db
from services.case_service import create_new_complaint

db = get_db()

try:
    complaint = create_new_complaint(
        db=db,
        case_id=1,
        complaint="Service layer test complaint",
        duration="2 days",
        onset="Gradual",
        location="Head",
        severity="Moderate",
        associated_symptoms="Mild dizziness"
    )

    print("\nComplaint service test successful!")
    print("Database ID:", complaint.id)
    print("Case ID:", complaint.case_id)
    print("Complaint:", complaint.complaint)
    print("Duration:", complaint.duration)
    print("Severity:", complaint.severity)

finally:
    db.close()