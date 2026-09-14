from services.case_service import get_case


from database.connection import get_db


db = get_db()

try:
    case = get_case(
        db=db,
        case_id="C001"
    )

    if case is None:
        print("Case C001 not found.")
    else:
        print("\nCase service is working!")
        print("Case ID:", case.case_id)
        print("Status:", case.status)
        print("Summary:", case.summary)

finally:
    db.close()