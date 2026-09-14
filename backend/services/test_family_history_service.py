from database.connection import SessionLocal
from services.case_service import create_new_family_history


if __name__ == "__main__":
    db = SessionLocal()

    history = create_new_family_history(
        db=db,
        case_id=1,
        family_members="Father, Mother",
        relevant_diseases="Hypertension in father",
        hereditary_conditions="No known hereditary conditions",
        details="No other significant family history"
    )

    print("Family history created successfully!")
    print("Database ID:", history.id)
    print("Case ID:", history.case_id)

    db.close()
