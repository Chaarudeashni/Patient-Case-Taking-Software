from database.connection import SessionLocal
from services.case_service import update_existing_examination


if __name__ == "__main__":
    db = SessionLocal()

    examination = update_existing_examination(
        db=db,
        case_id=1,
        temperature="99.0 F",
        pulse="76 bpm",
        respiratory_rate="18/min",
        blood_pressure="118/78 mmHg",
        spo2="99%",
        weight="66 kg",
        height="170 cm",
        general_examination="Patient conscious, oriented and comfortable",
        respiratory_examination="Clear",
        cardiovascular_examination="Normal",
        gastrointestinal_examination="Normal",
        neurological_examination="Normal",
        other_findings="Updated examination findings"
    )

    if examination:
        print("Examination updated successfully!")
        print("Database ID:", examination.id)
        print("Case ID:", examination.case_id)
        print("Temperature:", examination.temperature)
        print("Pulse:", examination.pulse)
        print("Blood Pressure:", examination.blood_pressure)
        print("Other Findings:", examination.other_findings)
    else:
        print("Examination not found.")

    db.close()
