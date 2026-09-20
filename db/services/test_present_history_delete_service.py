from database.connection import SessionLocal
from services.case_service import remove_present_history


if __name__ == "__main__":
    db = SessionLocal()

    deleted_history = remove_present_history(
        db=db,
        case_id=1
    )

    if deleted_history:
        print("Present history delete service test successful!")
        print("Present history for Case ID 1 was deleted successfully.")
    else:
        print("Present history delete service test failed!")

    db.close()