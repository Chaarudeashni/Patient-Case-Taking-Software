from datetime import date
from database.connection import SessionLocal
from services.case_service import update_existing_followup


if __name__ == "__main__":
    db = SessionLocal()

    followup = update_existing_followup(
        db=db,
        followup_id=1,
        visit_date=date.today(),
        symptoms="Symptoms significantly improved",
        changes_since_last_visit="Further improvement since last visit",
        examination="Stable examination findings",
        treatment_response="Very good response",
        medication_adherence="Good",
        new_findings="No new findings",
        plan="Continue current management",
        next_followup_date=date.today()
    )

    if followup:
        print("Follow-up updated successfully!")
        print("Database ID:", followup.id)
        print("Case ID:", followup.case_id)
        print("Symptoms:", followup.symptoms)
        print("Treatment Response:", followup.treatment_response)
        print("Plan:", followup.plan)
    else:
        print("Follow-up not found.")

    db.close()
