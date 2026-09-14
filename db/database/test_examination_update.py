from database.connection import get_db
from database.crud import update_examination

db = get_db()

try:
    case_id = 1

    examination = update_examination(
        db=db,
        case_id=case_id,
        temperature="99.1 F",
        pulse="82 bpm",
        respiratory_rate="20/min",
        blood_pressure="122/82 mmHg",
        spo2="97%",
        weight="64.5 kg",
        height="170 cm",
        general_examination="Patient conscious, oriented and cooperative",
        respiratory_examination="Air entry equal bilaterally; no added sounds",
        cardiovascular_examination="S1 and S2 normal",
        gastrointestinal_examination="Abdomen soft and non-tender",
        neurological_examination="No focal neurological deficit",
        other_findings="Mild increase in temperature noted"
    )

    if examination is None:
        print("Examination not found!")
    else:
        print("\nExamination updated successfully!")
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
            "Respiratory examination:",
            examination.respiratory_examination
        )
        print("Other findings:", examination.other_findings)

finally:
    db.close()