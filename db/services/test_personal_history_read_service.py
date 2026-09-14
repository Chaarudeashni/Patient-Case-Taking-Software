from database.connection import SessionLocal
from services.case_service import get_case_personal_history


if __name__ == "__main__":
    db = SessionLocal()

    history = get_case_personal_history(
        db=db,
        case_id=1
    )

    if history:
        print("Personal history retrieved successfully!")
        print("Database ID:", history.id)
        print("Case ID:", history.case_id)
        print("Diet:", history.diet)
        print("Appetite:", history.appetite)
        print("Sleep:", history.sleep)
        print("Bowel:", history.bowel)
        print("Bladder:", history.bladder)
        print("Lifestyle:", history.lifestyle)
        print("Other Details:", history.other_details)
    else:
        print("Personal history not found.")

    db.close()