from database.connection import SessionLocal
from services.case_service import create_new_assessment


if __name__ == "__main__":
    db = SessionLocal()

    assessment = create_new_assessment(
        db=db,
        case_id=1,
        case_summary="Patient presents with mild symptoms",
        clinical_impression="Stable clinical condition",
        differential_diagnosis="To be considered based on further evaluation",
        investigations="Routine investigations advised",
        management_plan="Supportive management and observation",
        advice="Follow prescribed advice and return if symptoms worsen"
    )

    print("Assessment created successfully!")
    print("Database ID:", assessment.id)
    print("Case ID:", assessment.case_id)

    db.close()
