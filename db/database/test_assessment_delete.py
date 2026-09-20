from database.connection import get_db
from database.crud import (
    get_assessment_by_case_id,
    delete_assessment
)

db = get_db()

try:
    case_id = 1

    assessment = get_assessment_by_case_id(
        db=db,
        case_id=case_id
    )

    if assessment is None:
        print("Assessment not found!")
    else:
        print("Assessment found!")
        print("Database ID:", assessment.id)

        deleted = delete_assessment(
            db=db,
            case_id=case_id
        )

        if deleted:
            print("Assessment deleted successfully!")
        else:
            print("Assessment deletion failed!")

        deleted_record = get_assessment_by_case_id(
            db=db,
            case_id=case_id
        )

        if deleted_record is None:
            print("Delete verification successful!")
        else:
            print("Delete verification failed!")

finally:
    db.close()