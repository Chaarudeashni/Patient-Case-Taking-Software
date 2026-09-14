from services.schemas import FamilyHistoryCreateSchema


history = FamilyHistoryCreateSchema(
    case_id=1,
    family_members="Father, mother, and one sibling",
    relevant_diseases="No significant family history",
    hereditary_conditions="None reported",
    details="No known hereditary conditions"
)

print("\nFamily history validation successful!")
print(history)
