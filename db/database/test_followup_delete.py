from database.connection import get_db
from database.crud import (
    get_followups_by_case_id,
    delete_followup
)

db = get_db()

try:
    case_id = 1
    followup_id = 1

    followups = get_followups_by_case_id(
        db=db,
        case_id=case_id
    )

    followup = next(
        (item for item in followups if item.id == followup_id),
        None
    )

    if followup is None:
        print("Follow-up not found!")
    else:
        print("Follow-up found!")
        print("Database ID:", followup.id)
        print("Case ID:", followup.case_id)

        deleted = delete_followup(
            db=db,
            followup_id=followup_id
        )

        if deleted:
            print("Follow-up deleted successfully!")
        else:
            print("Follow-up deletion failed!")

        remaining_followups = get_followups_by_case_id(
            db=db,
            case_id=case_id
        )

        deleted_record = next(
            (
                item
                for item in remaining_followups
                if item.id == followup_id
            ),
            None
        )

        if deleted_record is None:
            print("Delete verification successful!")
        else:
            print("Delete verification failed!")

finally:
    db.close()