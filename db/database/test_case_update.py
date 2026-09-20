from database.connection import get_db
from database.crud import update_case


db = get_db()

try:
    case = update_case(
        db=db,
        case_id="C001",
        status="completed",
        summary="Updated demo case summary"
    )

    if case is None:
        print("Case C001 not found.")
    else:
        print("\nCase updated successfully!")
        print("Case ID:", case.case_id)
        print("Case date:", case.case_date)
        print("Status:", case.status)
        print("Summary:", case.summary)

finally:
    db.close()