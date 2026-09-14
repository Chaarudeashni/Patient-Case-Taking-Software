from database.connection import SessionLocal
from services.case_service import update_existing_personal_history


if __name__ == "__main__":
    db = SessionLocal()

    history = update_existing_personal_history(
        db=db,
        case_id=1,
        diet="Vegetarian diet",
        appetite="Good",
        sleep="8 hours",
        bowel="Regular",
        bladder="Normal",
        lifestyle="Active",
        other_details="Updated personal history details"
    )

    if history:
        print("Personal history updated successfully!")
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