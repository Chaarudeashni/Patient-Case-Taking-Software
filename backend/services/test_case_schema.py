from datetime import date

from services.schemas import CaseCreateSchema


case = CaseCreateSchema(
    case_id="C100",
    patient_id=1,
    clinician_id=1,
    case_date=date.today(),
    status="active",
    summary="Initial consultation"
)

print("\nCase validation successful!")
print(case)