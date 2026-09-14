from database.connection import get_db
from database.crud import delete_case, get_case_by_case_id


db = get_db()

try:
    deleted = delete_case(
        db=db,
        case_id="C001"
    )

    if deleted:
        print("\nCase deleted successfully!")

        case = get_case_by_case_id(
            db=db,
            case_id="C001"
        )

        if case is None:
            print("Delete verification successful!")
            print("Case C001 no longer exists.")
        else:
            print("Warning: Case still exists.")

    else:
        print("Case C001 not found.")

finally:
    db.close()