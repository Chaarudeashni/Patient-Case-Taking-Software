from database.connection import get_db
from services.case_service import update_existing_complaint

db = get_db()

try:
    complaint_id = 5

    updated_complaint = update_existing_complaint(
        db=db,
        complaint_id=complaint_id,
        complaint="Updated service layer complaint",
        duration="4 days",
        onset="Sudden",
        location="Temporal region",
        severity="Mild",
        associated_symptoms="No associated symptoms"
    )

    if updated_complaint:
        print("\nComplaint update service test successful!")
        print("Database ID:", updated_complaint.id)
        print("Case ID:", updated_complaint.case_id)
        print("Complaint:", updated_complaint.complaint)
        print("Duration:", updated_complaint.duration)
        print("Onset:", updated_complaint.onset)
        print("Location:", updated_complaint.location)
        print("Severity:", updated_complaint.severity)
        print(
            "Associated symptoms:",
            updated_complaint.associated_symptoms
        )
    else:
        print("\nComplaint not found.")

finally:
    db.close()