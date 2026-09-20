from database.connection import get_db
from services.case_service import get_case_present_history

db = get_db()

try:
    case_id = 1

    present_history = get_case_present_history(
        db=db,
        case_id=case_id
    )

    if present_history:
        print("\nPresent history read service test successful!")
        print("Database ID:", present_history.id)
        print("Case ID:", present_history.case_id)
        print("History:", present_history.history)
        print("Onset:", present_history.onset)
        print("Progression:", present_history.progression)
        print(
            "Aggravating factors:",
            present_history.aggravating_factors
        )
        print(
            "Relieving factors:",
            present_history.relieving_factors
        )
        print(
            "Previous treatment:",
            present_history.previous_treatment
        )
    else:
        print("\nPresent history not found.")

finally:
    db.close()