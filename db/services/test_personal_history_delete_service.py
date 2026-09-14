from database.connection import SessionLocal
from services.case_service import remove_personal_history


if __name__ == "__main__":
    db = SessionLocal()

    deleted = remove_personal_history(
        db=db,
        case_id=1
    )

    if deleted:
        print("Personal history deleted successfully!")
        print("Personal history for Case ID 1 was deleted successfully.")
    else:
        print("Personal history not found.")

    db.close()
