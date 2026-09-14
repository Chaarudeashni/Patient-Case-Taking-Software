from database.connection import get_db
from database.crud import get_patient_by_patient_id


db = get_db()

try:
    patient = get_patient_by_patient_id(
        db=db,
        patient_id="P001"
    )

    if patient:
        print("Patient still exists.")
    else:
        print("Patient deletion verified successfully!")

finally:
    db.close()