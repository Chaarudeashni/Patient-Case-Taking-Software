from database.connection import SessionLocal
from services.case_service import get_case_examination


if __name__ == "__main__":
    db = SessionLocal()

    examination = get_case_examination(
        db=db,
        case_id=1
    )

    if examination:
        print("Examination retrieved successfully!")
        print("Database ID:", examination.id)
        print("Case ID:", examination.case_id)
        print("Temperature:", examination.temperature)
        print("Pulse:", examination.pulse)
        print("Respiratory Rate:", examination.respiratory_rate)
        print("Blood Pressure:", examination.blood_pressure)
        print("SpO2:", examination.spo2)
        print("Weight:", examination.weight)
        print("Height:", examination.height)
        print("General Examination:", examination.general_examination)
        print("Respiratory Examination:", examination.respiratory_examination)
        print("Cardiovascular Examination:", examination.cardiovascular_examination)
        print("Gastrointestinal Examination:", examination.gastrointestinal_examination)
        print("Neurological Examination:", examination.neurological_examination)
        print("Other Findings:", examination.other_findings)
    else:
        print("Examination not found.")

    db.close()
