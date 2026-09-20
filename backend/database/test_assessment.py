from database.connection import get_db
from database.crud import create_assessment

db = get_db()

try:
    case_id = 1

    assessment = create_assessment(
        db=db,
        case_id=case_id,
        case_summary="Patient presents with headache for 5 days.",
        clinical_impression="Acute headache requiring clinical evaluation.",
        differential_diagnosis="Tension headache; migraine.",
        investigations="Complete blood count and other investigations as clinically indicated.",
        management_plan="Supportive management and follow-up as advised by clinician.",
        advice="Maintain adequate hydration and return if symptoms worsen."
    )

    print("\nAssessment created successfully!")
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