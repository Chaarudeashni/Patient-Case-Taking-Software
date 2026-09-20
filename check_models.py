from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False, default="clinician")
    created_at = Column(DateTime, default=datetime.utcnow)


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(String(50), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    date_of_birth = Column(Date)
    gender = Column(String(20))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False
    )

    clinician_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    case_date = Column(Date, nullable=False)

    status = Column(
        String(30),
        nullable=False,
        default="active"
    )

    summary = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False,
        index=True
    )

    complaint = Column(String(255), nullable=False)
    duration = Column(String(100))
    onset = Column(String(100))
    location = Column(String(255))
    severity = Column(String(50))
    associated_symptoms = Column(Text)


class PresentHistory(Base):
    __tablename__ = "present_histories"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False,
        unique=True,
        index=True
    )

    history = Column(Text)
    onset = Column(String(100))
    progression = Column(Text)
    aggravating_factors = Column(Text)
    relieving_factors = Column(Text)
    previous_treatment = Column(Text)


class PastHistory(Base):
    __tablename__ = "past_histories"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False,
        unique=True,
        index=True
    )

    previous_illnesses = Column(Text)
    hospitalizations = Column(Text)
    surgeries = Column(Text)
    medications = Column(Text)
    allergies = Column(Text)


class PersonalHistory(Base):
    __tablename__ = "personal_histories"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False,
        unique=True,
        index=True
    )

    diet = Column(Text)
    appetite = Column(String(100))
    sleep = Column(Text)
    bowel = Column(Text)
    bladder = Column(Text)
    lifestyle = Column(Text)
    other_details = Column(Text)


class FamilyHistory(Base):
    __tablename__ = "family_histories"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False,
        unique=True,
        index=True
    )

    family_members = Column(Text)
    relevant_diseases = Column(Text)
    hereditary_conditions = Column(Text)
    details = Column(Text)


class ReviewOfSystems(Base):
    __tablename__ = "review_of_systems"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False,
        unique=True,
        index=True
    )

    general = Column(Text)
    respiratory = Column(Text)
    cardiovascular = Column(Text)
    gastrointestinal = Column(Text)
    neurological = Column(Text)
    musculoskeletal = Column(Text)
    genitourinary = Column(Text)
    skin = Column(Text)
    other_systems = Column(Text)


class Examination(Base):
    __tablename__ = "examinations"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False,
        unique=True,
        index=True
    )

    temperature = Column(String(50))
    pulse = Column(String(50))
    respiratory_rate = Column(String(50))
    blood_pressure = Column(String(50))
    spo2 = Column(String(50))
    weight = Column(String(50))
    height = Column(String(50))

    general_examination = Column(Text)
    respiratory_examination = Column(Text)
    cardiovascular_examination = Column(Text)
    gastrointestinal_examination = Column(Text)
    neurological_examination = Column(Text)
    other_findings = Column(Text)


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False,
        unique=True,
        index=True
    )

    case_summary = Column(Text)
    clinical_impression = Column(Text)
    differential_diagnosis = Column(Text)
    investigations = Column(Text)
    management_plan = Column(Text)
    advice = Column(Text)


class Followup(Base):
    __tablename__ = "followups"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False,
        index=True
    )

    visit_date = Column(Date, nullable=False)
    symptoms = Column(Text)
    changes_since_last_visit = Column(Text)
    examination = Column(Text)
    treatment_response = Column(Text)
    medication_adherence = Column(Text)
    new_findings = Column(Text)
    plan = Column(Text)
    next_followup_date = Column(Date)


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    appointment_id = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    clinician_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(String(20), nullable=False)
    reason = Column(Text)
    notes = Column(Text)
    status = Column(
        String(30),
        nullable=False,
        default="Scheduled"
    )


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    document_type = Column(String(100))
    file_name = Column(String(255))
    file_path = Column(Text)
    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class ExtractedData(Base):
    __tablename__ = "extracted_data"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
        index=True
    )

    data_type = Column(String(100))
    extracted_text = Column(Text)
    structured_data = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class AYUSHHistory(Base):
    __tablename__ = "ayush_histories"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False,
        unique=True,
        index=True
    )

    system = Column(String(50))
    practitioner = Column(Text)
    treatment = Column(Text)
    medications = Column(Text)
    duration = Column(String(100))
    response = Column(Text)
    details = Column(Text)


class AISummary(Base):
    __tablename__ = "ai_summaries"

    id = Column(Integer, primary_key=True, index=True)

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=False,
        index=True
    )

    summary = Column(Text)
    key_findings = Column(Text)
    possible_assessment = Column(Text)
    recommendations = Column(Text)

    status = Column(
        String(30),
        nullable=False,
        default="draft"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class Consent(Base):
    __tablename__ = "consents"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    consent_type = Column(String(100), nullable=False)
    status = Column(String(30), nullable=False)
    consent_text = Column(Text)

    consented_at = Column(DateTime)
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    clinician_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    case_id = Column(
        Integer,
        ForeignKey("cases.id"),
        nullable=True,
        index=True
    )

    ai_summary_id = Column(
        Integer,
        ForeignKey("ai_summaries.id"),
        nullable=True
    )

    consultation_date = Column(
        DateTime,
        default=datetime.utcnow
    )

    consultation_type = Column(String(50))
    status = Column(String(30), default="scheduled")
    notes = Column(Text)