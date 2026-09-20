from database.connection import SessionLocal
from services.case_service import get_case_family_history


if __name__ == "__main__":
    db = SessionLocal()

    history = get_case_family_history(
        db=db,
        case_id=1
    )

    if history:
        print("Family history retrieved successfully!")
        print("Database ID:", history.id)
        print("Case ID:", history.case_id)
        print("Family Members:", history.family_members)
        print("Relevant Diseases:", history.relevant_diseases)
        print("Hereditary Conditions:", history.hereditary_conditions)
        print("Details:", history.details)
    else:
        print("Family history not found.")

    db.close()
