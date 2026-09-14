from database.connection import SessionLocal
from services.case_service import remove_family_history


if __name__ == "__main__":
    db = SessionLocal()

    deleted = remove_family_history(
        db=db,
        case_id=1
    )

    if deleted:
        print("Family history deleted successfully!")
        print("Family history for Case ID 1 was deleted successfully.")
    else:
        print("Family history not found.")

    db.close()
