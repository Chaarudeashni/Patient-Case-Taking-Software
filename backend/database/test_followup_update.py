from datetime import date

from database.connection import get_db
from database.crud import update_followup

db = get_db()

try:
    followup_id = 1

    followup = update_followup(
        db=db,
        followup_id=followup_id,
        visit_date=date(2026, 9, 8),
        symptoms="Headache significantly improved",
        changes_since_last_visit="Marked improvement since previous visit",
        examination="Patient clinically stable and comfortable",
        treatment_response="Very good response to treatment",
        medication_adherence="Good",
        new_findings="No new significant findings",
        plan="Continue current management and review as scheduled",
        next_followup_date=date(2026, 9, 29)
    )

    if followup is None:
        print("Follow-up not found!")
    else:
        print("\nFollow-up updated successfully!")
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