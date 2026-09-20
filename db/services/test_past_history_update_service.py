from database.connection import SessionLocal
from services.case_service import update_existing_past_history


if __name__ == "__main__":
    db = SessionLocal()

    updated_history = update_existing_past_history(
        db=db,
        case_id=1,
        previous_illnesses="History of seasonal allergy",
        hospitalizations="None",
        surgeries="Appendectomy in 2020",
        medications="Cetirizine when required",
        allergies="No known drug allergies"
    )

    if updated_history:
        print("Past history update service test successful!")
        print("Database ID:", updated_history.id)
        print("Case ID:", updated_history.case_id)
        print("Previous illnesses:", updated_history.previous_illnesses)
        print("Hospitalizations:", updated_history.hospitalizations)
        print("Surgeries:", updated_history.surgeries)
        print("Medications:", updated_history.medications)
        print("Allergies:", updated_history.allergies)
    else:
        print("Past history not found")

    db.close()