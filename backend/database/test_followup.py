from datetime import date

from database.connection import get_db
from database.crud import create_followup
from database.models import Followup

db = get_db()

try:
    case_id = 1

    followup = create_followup(
        db=db,
        case_id=case_id,
        visit_date=date(2026, 9, 8),
        symptoms="Headache has reduced",
        changes_since_last_visit="Symptoms improved since previous visit",
        examination="Patient clinically stable",
        treatment_response="Good response to treatment",
        medication_adherence="Good",
        new_findings="No new significant findings",
        plan="Continue current management and monitor symptoms",
        next_followup_date=date(2026, 9, 22)
    )

    print("\nFollow-up created successfully!")
    print("Database ID:", followup.id)
    print("Case ID:", followup.case_id)
    print("Visit date:", followup.visit_date)
    print("Symptoms:", followup.symptoms)
    print(
        "Changes since last visit:",
        followup.changes_since_last_visit
    )
    print("Examination:", followup.examination)
    print("Treatment response:", followup.treatment_response)
    print("Medication adherence:", followup.medication_adherence)
    print("New findings:", followup.new_findings)
    print("Plan:", followup.plan)
    print("Next follow-up date:", followup.next_followup_date)

finally:
    db.close()

def get_followups_by_case_id(db, case_id):
    """
    Get all follow-up records for a case.
    """

    return (
        db.query(Followup)
        .filter(Followup.case_id == case_id)
        .order_by(Followup.visit_date.desc())
        .all()
    )