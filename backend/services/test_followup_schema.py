from datetime import date

from services.schemas import FollowupCreateSchema


followup = FollowupCreateSchema(
    case_id=1,
    visit_date=date.today(),
    symptoms="Headache has reduced.",
    changes_since_last_visit="Symptoms improved since previous visit.",
    examination="No new significant findings.",
    treatment_response="Good response to treatment.",
    medication_adherence="Taking medication as advised.",
    new_findings="None",
    plan="Continue current management.",
    next_followup_date=date.today()
)

print("\nFollow-up validation successful!")
print(followup)