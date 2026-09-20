from database.connection import SessionLocal
from services.case_service import update_existing_assessment


if __name__ == "__main__":
    db = SessionLocal()

    assessment = update_existing_assessment(
        db=db,
        case_id=1,
        case_summary="Updated patient case summary",
        clinical_impression="Updated clinical impression",
        differential_diagnosis="Updated differential diagnosis",
        investigations="Updated investigation plan",
        management_plan="Updated management plan",
        advice="Updated patient advice"
    )

    if assessment:
        print("Assessment updated successfully!")
        print("Database ID:", assessment.id)
        print("Case ID:", assessment.case_id)
        print("Case Summary:", assessment.case_summary)
        print("Clinical Impression:", assessment.clinical_impression)
        print("Management Plan:", assessment.management_plan)
        print("Advice:", assessment.advice)
    else:
        print("Assessment not found.")

    db.close()
