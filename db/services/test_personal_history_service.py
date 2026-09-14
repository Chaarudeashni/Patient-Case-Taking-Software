from database.connection import SessionLocal
from services.case_service import create_new_personal_history


if __name__ == "__main__":
    db = SessionLocal()

    history = create_new_personal_history(
        db=db,
        case_id=1,
        diet="Mixed diet",
        appetite="Normal",
        sleep="7 hours",
        bowel="Regular",
        bladder="Normal",
        lifestyle="Moderately active",
        other_details="No other significant personal history"
    )

    print("Personal history created successfully!")
    print("Database ID:", history.id)
    print("Case ID:", history.case_id)

    db.close()