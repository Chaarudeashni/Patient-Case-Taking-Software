from database.connection import get_db
from database.crud import (
    get_family_history_by_case_id,
    delete_family_history
)

db = get_db()

try:
    case_id = 1

    # Check that the record exists
    family_history = get_family_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if family_history is None:
        print("Family history not found!")
    else:
        print("Family history found!")
        print("Database ID:", family_history.id)

        # Delete the record
        deleted = delete_family_history(
            db=db,
            case_id=case_id
        )

        if deleted:
            print("Family history deleted successfully!")
        else:
            print("Family history deletion failed!")

        # Verify deletion
        deleted_record = get_family_history_by_case_id(
            db=db,
            case_id=case_id
        )

        if deleted_record is None:
            print("Delete verification successful!")
        else:
            print("Delete verification failed!")

finally:
    db.close()