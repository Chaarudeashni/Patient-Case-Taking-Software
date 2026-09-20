from database.connection import SessionLocal
from services.case_service import create_new_examination


if __name__ == "__main__":
    db = SessionLocal()

    examination = create_new_examination(
        db=db,
        case_id=1,
        temperature="98.6 F",
        pulse="72 bpm",
        respiratory_rate="16/min",
        blood_pressure="120/80 mmHg",
        spo2="98%",
        weight="65 kg",
        height="170 cm",
        general_examination="Patient conscious and oriented",
        respiratory_examination="Normal",
        cardiovascular_examination="Normal",
        gastrointestinal_examination="Normal",
        neurological_examination="Normal",
        other_findings="No other significant findings"
    )

    print("Examination created successfully!")
    print("Database ID:", examination.id)
    print("Case ID:", examination.case_id)

    db.close()
