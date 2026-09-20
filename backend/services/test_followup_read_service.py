from database.connection import SessionLocal
from services.case_service import get_case_followups


if __name__ == "__main__":
    db = SessionLocal()

    followups = get_case_followups(
        db=db,
        case_id=1
    )

    if followups:
        print("Follow-ups retrieved successfully!")

        for followup in followups:
            print("\nDatabase ID:", followup.id)
            print("Case ID:", followup.case_id)
            print("Visit Date:", followup.visit_date)
            print("Symptoms:", followup.symptoms)
            print("Changes Since Last Visit:", followup.changes_since_last_visit)
            print("Examination:", followup.examination)
            print("Treatment Response:", followup.treatment_response)
            print("Medication Adherence:", followup.medication_adherence)
            print("New Findings:", followup.new_findings)
            print("Plan:", followup.plan)
            print("Next Follow-up Date:", followup.next_followup_date)
    else:
        print("No follow-ups found.")

    db.close()
