from database.connection import SessionLocal
from services.case_service import remove_examination


if __name__ == "__main__":
    db = SessionLocal()

    deleted = remove_examination(
        db=db,
        case_id=1
    )

    if deleted:
        print("Examination deleted successfully!")
        print("Examination for Case ID 1 was deleted successfully.")
    else:
        print("Examination not found.")

    db.close()
