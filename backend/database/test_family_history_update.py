from database.connection import get_db
from database.crud import update_family_history

db = get_db()

try:
    case_id = 1

    family_history = update_family_history(
        db=db,
        case_id=case_id,
        family_members="Father, mother, one sibling and grandmother",
        relevant_diseases="Father has hypertension; grandmother had diabetes",
        hereditary_conditions="Possible family history of diabetes",
        details="Updated family history after detailed interview"
    )

    if family_history is None:
        print("Family history not found!")
    else:
        print("\nFamily history updated successfully!")
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