from datetime import date
from database.connection import SessionLocal
from services.case_service import create_new_followup


if __name__ == "__main__":
    db = SessionLocal()

    followup = create_new_followup(
        db=db,
        case_id=1,
        visit_date=date.today(),
        symptoms="Symptoms improving",
        changes_since_last_visit="Reduced symptoms since previous visit",
        examination="Stable findings",
        treatment_response="Good response",
        medication_adherence="Good",
        new_findings="No new findings",
        plan="Continue current management",
        next_followup_date=date.today()
    )

    print("Follow-up created successfully!")
    print("Database ID:", followup.id)
    print("Case ID:", followup.case_id)

    db.close()
