from database.connection import get_db
from services.case_service import update_existing_present_history

db = get_db()

try:
    case_id = 1

    updated_history = update_existing_present_history(
        db=db,
        case_id=case_id,
        history="Headache has continued and is now more frequent.",
        onset="Gradual",
        progression="Intermittent with increasing frequency",
        aggravating_factors="Bright light, physical activity, and lack of sleep",
        relieving_factors="Rest, sleep, and a quiet environment",
        previous_treatment="Rest and over-the-counter medication"
    )

    if updated_history:
        print("\nPresent history update service test successful!")
        print("Database ID:", updated_history.id)
        print("Case ID:", updated_history.case_id)
        print("History:", updated_history.history)
        print("Onset:", updated_history.onset)
        print("Progression:", updated_history.progression)
        print(
            "Aggravating factors:",
            updated_history.aggravating_factors
        )
        print(
            "Relieving factors:",
            updated_history.relieving_factors
        )
        print(
            "Previous treatment:",
            updated_history.previous_treatment
        )
    else:
        print("\nPresent history not found.")

finally:
    db.close()