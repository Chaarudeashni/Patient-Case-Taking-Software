from database.connection import get_db
from database.crud import create_family_history

db = get_db()

try:
    # Use the existing test case
    case_id = 1

    family_history = create_family_history(
        db=db,
        case_id=case_id,
        family_members="Father, mother and one sibling",
        relevant_diseases="Father has hypertension",
        hereditary_conditions="No known hereditary conditions",
        details="No significant family history otherwise"
    )

    print("\nFamily history created successfully!")
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