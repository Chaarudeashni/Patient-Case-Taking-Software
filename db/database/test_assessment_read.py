from database.connection import get_db
from database.crud import get_assessment_by_case_id

db = get_db()

try:
    case_id = 1

    assessment = get_assessment_by_case_id(
        db=db,
        case_id=case_id
    )

    if assessment is None:
        print("Assessment not found!")
    else:
        print("\nAssessment retrieved successfully!")
        print("Database ID:", assessment.id)
        print("Case ID:", assessment.case_id)
        print("Case summary:", assessment.case_summary)
        print(
            "Clinical impression:",
            assessment.clinical_impression
        )
        print(
            "Differential diagnosis:",
            assessment.differential_diagnosis
        )
        print("Investigations:", assessment.investigations)
        print("Management plan:", assessment.management_plan)
        print("Advice:", assessment.advice)

finally:
    db.close()