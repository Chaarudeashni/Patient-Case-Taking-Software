from services.schemas import PastHistoryCreateSchema


history = PastHistoryCreateSchema(
    case_id=1,
    previous_illnesses="No significant previous illness",
    hospitalizations="None",
    surgeries="None",
    medications="Occasional paracetamol",
    allergies="No known allergies"
)

print("\nPast history validation successful!")
print(history)

class PersonalHistoryCreateSchema(BaseModel):
    """
    Validation schema for creating personal history.
    """

    case_id: int
    diet: str | None = None
    appetite: str | None = Field(default=None, max_length=100)
    sleep: str | None = None
    bowel: str | None = None
    bladder: str | None = None
    lifestyle: str | None = None
    other_details: str | None = None