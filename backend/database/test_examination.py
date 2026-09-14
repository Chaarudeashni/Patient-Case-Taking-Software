from database.connection import get_db
from database.crud import create_examination

db = get_db()

try:
    case_id = 1

    examination = create_examination(
        db=db,
        case_id=case_id,
        temperature="98.6 F",
        pulse="78 bpm",
        respiratory_rate="18/min",
        blood_pressure="120/80 mmHg",
        spo2="98%",
        weight="65 kg",
        height="170 cm",
        general_examination="Patient conscious, oriented and cooperative",
        respiratory_examination="Air entry equal bilaterally",
        cardiovascular_examination="S1 and S2 normal",
        gastrointestinal_examination="Abdomen soft and non-tender",
        neurological_examination="No focal neurological deficit",
        other_findings="No other significant findings"
    )

    print("\nExamination created successfully!")
    print("Database ID:", examination.id)
    print("Case ID:", examination.case_id)
    print("Temperature:", examination.temperature)
    print("Pulse:", examination.pulse)
    print("Respiratory rate:", examination.respiratory_rate)
    print("Blood pressure:", examination.blood_pressure)
    print("SpO2:", examination.spo2)
    print("Weight:", examination.weight)
    print("Height:", examination.height)
    print("General examination:", examination.general_examination)
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