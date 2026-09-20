from database.connection import get_db
from database.crud import get_examination_by_case_id

db = get_db()

try:
    case_id = 1

    examination = get_examination_by_case_id(
        db=db,
        case_id=case_id
    )

    if examination is None:
        print("Examination not found!")
    else:
        print("\nExamination retrieved successfully!")
        print("Database ID:", examination.id)
        print("Case ID:", examination.case_id)
        print("Temperature:", examination.temperature)
        print("Pulse:", examination.pulse)
        print("Respiratory rate:", examination.respiratory_rate)
        print("Blood pressure:", examination.blood_pressure)
        print("SpO2:", examination.spo2)
        print("Weight:", examination.weight)
        print("Height:", examination.height)
        print(
            "General examination:",
            examination.general_examination
        )
        print(
            "Respiratory examination:",
            examination.respiratory_examination
        )
        print(
            "Cardiovascular examination:",
            examination.cardiovascular_examination
        )
        print(
            "Gastrointestinal examination:",
            examination.gastrointestinal_examination
        )
        print(
            "Neurological examination:",
            examination.neurological_examination
        )
        print("Other findings:", examination.other_findings)

finally:
    db.close()