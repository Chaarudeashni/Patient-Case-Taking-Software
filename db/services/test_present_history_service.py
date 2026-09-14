from database.connection import get_db
from services.case_service import create_new_present_history

db = get_db()

try:
    present_history = create_new_present_history(
        db=db,
        case_id=1,
        history="Headache started gradually and has been increasing over the last few days.",
        onset="Gradual",
        progression="Progressively increasing",
        aggravating_factors="Bright light and physical activity",
        relieving_factors="Rest and sleep",
        previous_treatment="No previous treatment"
    )

    print("\nPresent history service test successful!")
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

finally:
    db.close()