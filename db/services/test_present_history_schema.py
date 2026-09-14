from services.schemas import PresentHistoryCreateSchema


history = PresentHistoryCreateSchema(
    case_id=1,
    history="Patient reports headache for the past three days.",
    onset="Gradual",
    progression="Symptoms increased gradually.",
    aggravating_factors="Lack of sleep",
    relieving_factors="Rest",
    previous_treatment="Paracetamol"
)

print("\nPresent history validation successful!")
print(history)