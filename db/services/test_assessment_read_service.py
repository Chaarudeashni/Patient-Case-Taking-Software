from database.connection import SessionLocal
from services.case_service import get_case_assessment


if __name__ == "__main__":
    db = SessionLocal()

    assessment = get_case_assessment(
        db=db,
        case_id=1
    )

    if assessment:
        print("Assessment retrieved successfully!")
        print("Database ID:", assessment.id)
        print("Case ID:", assessment.case_id)
        print("Case Summary:", assessment.case_summary)
        print("Clinical Impression:", assessment.clinical_impression)
        print("Differential Diagnosis:", assessment.differential_diagnosis)
        print("Investigations:", assessment.investigations)
        print("Management Plan:", assessment.management_plan)
        print("Advice:", assessment.advice)
    else:
        print("Assessment not found.")

    db.close()
