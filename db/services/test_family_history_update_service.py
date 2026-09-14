from database.connection import SessionLocal
from services.case_service import update_existing_family_history


if __name__ == "__main__":
    db = SessionLocal()

    history = update_existing_family_history(
        db=db,
        case_id=1,
        family_members="Father, Mother, Brother",
        relevant_diseases="Hypertension in father",
        hereditary_conditions="No known hereditary conditions",
        details="Updated family history details"
    )

    if history:
        print("Family history updated successfully!")
        print("Database ID:", history.id)
        print("Case ID:", history.case_id)
        print("Family Members:", history.family_members)
        print("Relevant Diseases:", history.relevant_diseases)
        print("Hereditary Conditions:", history.hereditary_conditions)
        print("Details:", history.details)
    else:
        print("Family history not found.")

    db.close()
