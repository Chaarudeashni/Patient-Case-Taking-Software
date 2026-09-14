from datetime import date

from pydantic import BaseModel, EmailStr, Field


class PatientCreateSchema(BaseModel):
    """
    Validation schema for creating a patient.
    """

    patient_id: str = Field(min_length=1, max_length=50)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str | None = Field(default=None, max_length=100)
    date_of_birth: date | None = None
    gender: str | None = Field(default=None, max_length=20)
    phone: str | None = Field(default=None, max_length=20)
    email: EmailStr | None = Field(default=None)
    address: str | None = Field(default=None, max_length=200)

class CaseCreateSchema(BaseModel):
    """
    Validation schema for creating a case.
    """

    case_id: str = Field(min_length=1, max_length=50)
    patient_id: int
    clinician_id: int
    case_date: date
    status: str = Field(default="active", max_length=30)
    summary: str | None = None

class ComplaintCreateSchema(BaseModel):
    """
    Validation schema for creating a complaint.
    """

    case_id: int
    complaint: str = Field(min_length=1, max_length=255)
    duration: str | None = Field(default=None, max_length=100)
    onset: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, max_length=255)
    severity: str | None = Field(default=None, max_length=50)
    associated_symptoms: str | None = None
class PresentHistoryCreateSchema(BaseModel):
    """
    Validation schema for creating present history.
    """

    case_id: int
    history: str | None = None
    onset: str | None = Field(default=None, max_length=100)
    progression: str | None = None
    aggravating_factors: str | None = None
    relieving_factors: str | None = None
    previous_treatment: str | None = None

class PastHistoryCreateSchema(BaseModel):
    """
    Validation schema for creating past history.
    """

    case_id: int
    previous_illnesses: str | None = None
    hospitalizations: str | None = None
    surgeries: str | None = None
    medications: str | None = None
    allergies: str | None = None
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

class FamilyHistoryCreateSchema(BaseModel):
    """
    Validation schema for creating family history.
    """

    case_id: int
    family_members: str | None = None
    relevant_diseases: str | None = None
    hereditary_conditions: str | None = None
    details: str | None = None

class ExaminationCreateSchema(BaseModel):
    """
    Validation schema for creating an examination record.
    """

    case_id: int
    temperature: str | None = Field(default=None, max_length=50)
    pulse: str | None = Field(default=None, max_length=50)
    respiratory_rate: str | None = Field(default=None, max_length=50)
    blood_pressure: str | None = Field(default=None, max_length=50)
    spo2: str | None = Field(default=None, max_length=50)
    weight: str | None = Field(default=None, max_length=50)
    height: str | None = Field(default=None, max_length=50)
    general_examination: str | None = None
    respiratory_examination: str | None = None
    cardiovascular_examination: str | None = None
    gastrointestinal_examination: str | None = None
    neurological_examination: str | None = None
    other_findings: str | None = None

class AssessmentCreateSchema(BaseModel):
    """
    Validation schema for creating an assessment.
    """

    case_id: int
    case_summary: str | None = None
    clinical_impression: str | None = None
    differential_diagnosis: str | None = None
    investigations: str | None = None
    management_plan: str | None = None
    advice: str | None = None

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