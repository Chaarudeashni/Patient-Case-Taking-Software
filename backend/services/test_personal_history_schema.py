from services.schemas import PersonalHistoryCreateSchema


history = PersonalHistoryCreateSchema(
    case_id=1,
    diet="Mixed diet",
    appetite="Normal",
    sleep="7 hours per night",
    bowel="Regular",
    bladder="Normal",
    lifestyle="Moderately active",
    other_details="No additional details"
)

print("\nPersonal history validation successful!")
print(history)