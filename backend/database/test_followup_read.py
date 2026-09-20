from database.connection import get_db
from database.crud import get_followups_by_case_id

db = get_db()

try:
    case_id = 1

    followups = get_followups_by_case_id(
        db=db,
        case_id=case_id
    )

    if not followups:
        print("No follow-up records found!")
    else:
        print("\nFollow-ups retrieved successfully!")
        print("Number of follow-ups:", len(followups))

        for followup in followups:
            print("\n--- Follow-up ---")
            print("Database ID:", followup.id)
            print("Case ID:", followup.case_id)
            print("Visit date:", followup.visit_date)
            print("Symptoms:", followup.symptoms)
            print(
                "Changes since last visit:",
                followup.changes_since_last_visit
            )
            print("Examination:", followup.examination)
            print(
                "Treatment response:",
                followup.treatment_response
            )
            print(
                "Medication adherence:",
                followup.medication_adherence
            )
            print("New findings:", followup.new_findings)
            print("Plan:", followup.plan)
            print(
                "Next follow-up date:",
                followup.next_followup_date
            )

finally:
    db.close()