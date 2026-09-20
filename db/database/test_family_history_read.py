from database.connection import get_db
from database.crud import get_family_history_by_case_id

db = get_db()

try:
    case_id = 1

    family_history = get_family_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if family_history is None:
        print("Family history not found!")
    else:
        print("\nFamily history retrieved successfully!")
        print("Database ID:", family_history.id)
        print("Case ID:", family_history.case_id)
        print("Family members:", family_history.family_members)
        print(
            "Relevant diseases:",
            family_history.relevant_diseases
        )
        print(
            "Hereditary conditions:",
            family_history.hereditary_conditions
        )
        print("Details:", family_history.details)

finally:
    db.close()