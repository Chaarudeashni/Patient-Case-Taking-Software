from database.connection import SessionLocal
from services.case_service import get_case_past_history


if __name__ == "__main__":
    db = SessionLocal()

    history = get_case_past_history(
        db=db,
        case_id=1
    )

    if history:
        print("Past history read service test successful!")
        print("Database ID:", history.id)
        print("Case ID:", history.case_id)
        print("Previous illnesses:", history.previous_illnesses)
        print("Hospitalizations:", history.hospitalizations)
        print("Surgeries:", history.surgeries)
        print("Medications:", history.medications)
        print("Allergies:", history.allergies)
    else:
        print("Past history not found")

    db.close()