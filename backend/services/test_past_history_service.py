from database.connection import SessionLocal
from services.case_service import create_new_past_history


if __name__ == "__main__":
    db = SessionLocal()

    history = create_new_past_history(
        db=db,
        case_id=1,
        previous_illnesses="No major previous illness",
        hospitalizations="None",
        surgeries="None",
        medications="Paracetamol when required",
        allergies="No known drug allergies"
    )

    print("Past history created successfully!")
    print("Database ID:", history.id)
    print("Case ID:", history.case_id)

    db.close()