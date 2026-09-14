from database.connection import SessionLocal
from services.case_service import remove_past_history


if __name__ == "__main__":
    db = SessionLocal()

    deleted_history = remove_past_history(
        db=db,
        case_id=1
    )

    if deleted_history:
        print("Past history delete service test successful!")
        print("Past history for Case ID 1 was deleted successfully.")
    else:
        print("Past history not found")

    db.close()