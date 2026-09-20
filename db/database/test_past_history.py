from database.connection import get_db
from database.crud import (
    get_past_history_by_case_id,
    delete_past_history
)

db = get_db()

try:
    # Use the existing test case
    case_id = 1

    # Check that the record exists before deleting
    past_history = get_past_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if past_history is None:
        print("\nPast history was not found.")
    else:
        print("\nPast history found!")
        print("Database ID:", past_history.id)
        print("Case ID:", past_history.case_id)

        # DELETE
        deleted = delete_past_history(
            db=db,
            case_id=case_id
        )

        if deleted:
            print("\nPast history deleted successfully!")
        else:
            print("\nPast history deletion failed!")

        # VERIFY DELETE
        remaining_history = get_past_history_by_case_id(
            db=db,
            case_id=case_id
        )

        if remaining_history is None:
            print("Delete verification successful!")
        else:
            print("Delete verification failed!")

finally:
    db.close()