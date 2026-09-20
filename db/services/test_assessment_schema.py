from services.schemas import AssessmentCreateSchema


assessment = AssessmentCreateSchema(
    case_id=1,
    case_summary="Patient presented with a three-day history of headache.",
    clinical_impression="Likely uncomplicated tension-type headache.",
    differential_diagnosis="Migraine, sinus-related headache.",
    investigations="No immediate investigation indicated in this demo case.",
    management_plan="Rest, hydration, and symptomatic management.",
    advice="Return if symptoms worsen or new symptoms develop."
)

print("\nAssessment validation successful!")
print(assessment)

class FollowupCreateSchema(BaseModel):
    """
    Validation schema for creating a follow-up record.
    """

    case_id: int
    visit_date: date
    symptoms: str | None = None
    changes_since_last_visit: str | None = None
    examination: str | None = None
    treatment_response: str | None = None
    medication_adherence: str | None = None
    new_findings: str | None = None
    plan: str | None = None
    next_followup_date: date | None = None