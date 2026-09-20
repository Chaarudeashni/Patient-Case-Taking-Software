from database.connection import SessionLocal
from services.case_service import remove_followup


if __name__ == "__main__":
    db = SessionLocal()

    deleted = remove_followup(
        db=db,
        followup_id=1
    )

    if deleted:
        print("Follow-up deleted successfully!")
        print("Follow-up ID 1 was deleted successfully.")
    else:
        print("Follow-up not found.")

    db.close()
