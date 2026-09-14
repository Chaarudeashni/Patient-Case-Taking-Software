from services.schemas import ExaminationCreateSchema


examination = ExaminationCreateSchema(
    case_id=1,
    temperature="98.6 F",
    pulse="72 bpm",
    respiratory_rate="16/min",
    blood_pressure="120/80 mmHg",
    spo2="98%",
    weight="65 kg",
    height="170 cm",
    general_examination="Patient appears comfortable.",
    respiratory_examination="Normal respiratory sounds.",
    cardiovascular_examination="Normal heart sounds.",
    gastrointestinal_examination="Abdomen soft and non-tender.",
    neurological_examination="Alert and oriented.",
    other_findings="No additional findings."
)

print("\nExamination validation successful!")
print(examination)