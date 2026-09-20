from services.schemas import ComplaintCreateSchema


complaint = ComplaintCreateSchema(
    case_id=1,
    complaint="Headache",
    duration="3 days",
    onset="Gradual",
    location="Frontal region",
    severity="Moderate",
    associated_symptoms="Mild nausea"
)

print("\nComplaint validation successful!")
print(complaint)