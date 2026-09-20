from database.connection import get_db
from database.crud import (
    get_examination_by_case_id,
    delete_examination
)

db = get_db()

try:
    case_id = 1

    examination = get_examination_by_case_id(
        db=db,
        case_id=case_id
    )

    if examination is None:
        print("Examination not found!")
    else:
        print("Examination found!")
        print("Database ID:", examination.id)

        deleted = delete_examination(
            db=db,
            case_id=case_id
        )

        if deleted:
            print("Examination deleted successfully!")
        else:
            print("Examination deletion failed!")

        deleted_record = get_examination_by_case_id(
            db=db,
            case_id=case_id
        )

        if deleted_record is None:
            print("Delete verification successful!")
        else:
            print("Delete verification failed!")

finally:
    db.close()