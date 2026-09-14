from database.connection import get_db
from database.crud import (
    get_personal_history_by_case_id,
    delete_personal_history
)

db = get_db()

try:
    # Use the existing test case
    case_id = 1

    # Check that the record exists before deleting
    personal_history = get_personal_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if personal_history is None:
        print("\nPersonal history was not found.")
    else:
        print("\nPersonal history found!")
        print("Database ID:", personal_history.id)
        print("Case ID:", personal_history.case_id)

        # DELETE
        deleted = delete_personal_history(
            db=db,
            case_id=case_id
        )

        if deleted:
            print("\nPersonal history deleted successfully!")
        else:
            print("\nPersonal history deletion failed!")

        # VERIFY DELETE
        remaining_history = get_personal_history_by_case_id(
            db=db,
            case_id=case_id
        )

        if remaining_history is None:
            print("Delete verification successful!")
        else:
            print("Delete verification failed!")

finally:
    db.close()