from database.connection import get_db
from database.crud import (
    create_complaint,
    get_complaints_by_case_id,
    update_complaint,
    delete_complaint
)

db = get_db()

try:
    # Use the test case
    case_id = 1

    # -----------------------------
    # CREATE
    # -----------------------------
    complaint = create_complaint(
        db=db,
        case_id=case_id,
        complaint="Headache",
        duration="3 days",
        onset="Gradual",
        location="Frontal region",
        severity="Moderate",
        associated_symptoms="Mild nausea"
    )

    print("\nComplaint created successfully!")
    print("Complaint ID:", complaint.id)

    # -----------------------------
    # READ
    # -----------------------------
    complaints = get_complaints_by_case_id(
        db=db,
        case_id=case_id
    )

    print("\nComplaints retrieved successfully!")
    print("Number of complaints:", len(complaints))

    for item in complaints:
        print("\nComplaint ID:", item.id)
        print("Case ID:", item.case_id)
        print("Complaint:", item.complaint)
        print("Duration:", item.duration)
        print("Onset:", item.onset)
        print("Location:", item.location)
        print("Severity:", item.severity)
        print("Associated symptoms:", item.associated_symptoms)

    # -----------------------------
    # UPDATE
    # -----------------------------
    updated_complaint = update_complaint(
        db=db,
        complaint_id=complaint.id,
        complaint="Severe Headache",
        duration="5 days",
        severity="Severe",
        associated_symptoms="Nausea and dizziness"
    )

    if updated_complaint is None:
        print("\nComplaint was not found.")
    else:
        print("\nComplaint updated successfully!")
        print("Complaint ID:", updated_complaint.id)
        print("Complaint:", updated_complaint.complaint)
        print("Duration:", updated_complaint.duration)
        print("Severity:", updated_complaint.severity)
        print(
            "Associated symptoms:",
            updated_complaint.associated_symptoms
        )

    # -----------------------------
    # DELETE
    # -----------------------------
    deleted = delete_complaint(
        db=db,
        complaint_id=complaint.id
    )

    if deleted:
        print("\nComplaint deleted successfully!")
    else:
        print("\nComplaint was not found.")

    # -----------------------------
    # VERIFY DELETE
    # -----------------------------
    remaining_complaints = get_complaints_by_case_id(
        db=db,
        case_id=case_id
    )

    complaint_exists = any(
        item.id == complaint.id
        for item in remaining_complaints
    )

    if not complaint_exists:
        print("Delete verification successful!")
    else:
        print("Delete verification failed!")

finally:
    db.close()