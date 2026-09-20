from database.connection import SessionLocal
from services.case_service import remove_assessment


if __name__ == "__main__":
    db = SessionLocal()

    deleted = remove_assessment(
        db=db,
        case_id=1
    )

    if deleted:
        print("Assessment deleted successfully!")
        print("Assessment for Case ID 1 was deleted successfully.")
    else:
        print("Assessment not found.")

    db.close()
