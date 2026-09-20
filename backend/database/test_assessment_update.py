from database.connection import get_db
from database.crud import update_assessment

db = get_db()

try:
    case_id = 1

    assessment = update_assessment(
        db=db,
        case_id=case_id,
        case_summary="Updated case summary after clinical evaluation.",
        clinical_impression="Updated clinical impression based on examination.",
        differential_diagnosis="Tension headache; migraine; other causes to be considered.",
        investigations="CBC and additional investigations as clinically indicated.",
        management_plan="Continue supportive management and monitor clinical progress.",
        advice="Maintain hydration, follow the treatment plan, and return for review if symptoms worsen."
    )

    if assessment is None:
        print("Assessment not found!")
    else:
        print("\nAssessment updated successfully!")
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