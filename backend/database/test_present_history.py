from database.connection import get_db
from database.crud import (
    get_present_history_by_case_id,
    delete_present_history
)

db = get_db()

try:
    # Use the existing test case
    case_id = 1

    # Check that the record exists before deleting
    present_history = get_present_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if present_history is None:
        print("\nPresent history was not found.")
    else:
        print("\nPresent history found!")
        print("Database ID:", present_history.id)
        print("Case ID:", present_history.case_id)

        # DELETE
        deleted = delete_present_history(
            db=db,
            case_id=case_id
        )

        if deleted:
            print("\nPresent history deleted successfully!")
        else:
            print("\nPresent history deletion failed!")

        # VERIFY DELETE
        remaining_history = get_present_history_by_case_id(
            db=db,
            case_id=case_id
        )

        if remaining_history is None:
            print("Delete verification successful!")
        else:
            print("Delete verification failed!")

finally:
    db.close()