from database.connection import get_db
from services.case_service import remove_complaint

db = get_db()

try:
    complaint_id = 5

    deleted_complaint = remove_complaint(
        db=db,
        complaint_id=complaint_id
    )

    if deleted_complaint:
        print("\nComplaint delete service test successful!")
        print("Deleted Database ID:", complaint_id)
    else:
        print("\nComplaint not found.")

finally:
    db.close()