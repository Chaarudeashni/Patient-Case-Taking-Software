from datetime import date, datetime
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt

from backend.database.connection import create_tables, get_db
from backend.database.models import (
    User,
    Patient,
    Case,
    Complaint,
    PresentHistory,
    PastHistory,
    PersonalHistory,
    FamilyHistory,
    ReviewOfSystems,
    Document,
    ExtractedData,
    Examination,
    Assessment,
    Followup,
    AYUSHHistory,
    AISummary,
    Consent,
    Consultation,
    Appointment,
)


app = FastAPI(
    title="Patient Case Taking API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    create_tables()

    db = next(get_db())

    try:
        existing_user = (
            db.query(User)
            .filter(User.username == "demo_clinician")
            .first()
        )

        if not existing_user:
            password_hash = bcrypt.hashpw(
                b"demo123",
                bcrypt.gensalt()
            ).decode("utf-8")

            user = User(
                username="demo_clinician",
                email="demo_clinician@example.com",
                password_hash=password_hash,
                role="clinician"
            )

            db.add(user)
            db.commit()

            print("Default clinician created.")

    finally:
        db.close()


# ============================================================
# PATIENT SCHEMAS
# ============================================================

class PatientIn(BaseModel):
    patient_id: str = Field(min_length=1, max_length=50)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


# ============================================================
# COMPLETE CASE SCHEMA
# ============================================================

class CompleteCase(BaseModel):
    patient_id: int
    clinician_id: int = 1
    case_id: Optional[str] = None

    case_date: date = date.today()
    status: str = "active"

    # -------------------------
    # COMPLAINT
    # -------------------------
    chief_complaint: Optional[str] = None
    duration: Optional[str] = None
    duration_unit: Optional[str] = None
    additional_complaints: Optional[str] = None
    severity: Optional[str] = None
    complaint_notes: Optional[str] = None

    # -------------------------
    # PRESENT HISTORY
    # -------------------------
    history_present_illness: Optional[str] = None
    onset: Optional[str] = None
    course: Optional[str] = None
    associated_symptoms: Optional[str] = None
    aggravating_factors: Optional[str] = None
    relieving_factors: Optional[str] = None
    previous_treatment: Optional[str] = None
    history_notes: Optional[str] = None

    # -------------------------
    # PAST HISTORY
    # -------------------------
    past_medical_history: Optional[str] = None
    past_surgical_history: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    family_history: Optional[str] = None
    hospitalization_details: Optional[str] = None
    past_history_notes: Optional[str] = None

    # -------------------------
    # PERSONAL HISTORY
    # -------------------------
    diet: Optional[str] = None
    appetite: Optional[str] = None
    sleep: Optional[str] = None
    bowel: Optional[str] = None
    bladder: Optional[str] = None
    exercise: Optional[str] = None
    smoking: Optional[str] = None
    alcohol: Optional[str] = None
    personal_notes: Optional[str] = None

    # -------------------------
    # EXAMINATION
    # -------------------------
    temperature: Optional[str] = None
    pulse: Optional[str] = None
    respiratory_rate: Optional[str] = None
    blood_pressure: Optional[str] = None
    spo2: Optional[str] = None
    weight: Optional[str] = None
    height: Optional[str] = None
    general_examination: Optional[str] = None
    system_examination: Optional[str] = None

    # -------------------------
    # ASSESSMENT
    # -------------------------
    provisional_diagnosis: Optional[str] = None
    differential_diagnosis: Optional[str] = None
    clinical_assessment: Optional[str] = None
    treatment_plan: Optional[str] = None


# ============================================================
# FOLLOW-UP
# ============================================================

class FollowupIn(BaseModel):
    case_id: int
    visit_date: date
    symptoms: Optional[str] = None
    changes_since_last_visit: Optional[str] = None
    examination: Optional[str] = None
    treatment_response: Optional[str] = None
    medication_adherence: Optional[str] = None
    new_findings: Optional[str] = None
    plan: Optional[str] = None
    next_followup_date: Optional[date] = None


# ============================================================
# BASIC SERIALIZERS
# ============================================================

def patient_dict(p):
    return {
        "id": p.id,
        "patient_id": p.patient_id,
        "first_name": p.first_name,
        "last_name": p.last_name or "",
        "date_of_birth": p.date_of_birth,
        "gender": p.gender or "",
        "phone": p.phone or "",
        "email": p.email or "",
        "address": p.address or "",
    }


# ============================================================
# COMPLETE CASE SERIALIZER
# ============================================================

def case_dict(c, db=None):
    """
    Return the main case together with its related
    clinical history records.

    This is required by Clinical Records because the
    Case table itself only contains case metadata.
    """

    result = {
        "id": c.id,
        "case_id": c.case_id,
        "patient_id": c.patient_id,
        "clinician_id": c.clinician_id,
        "case_date": c.case_date,
        "status": c.status,
        "summary": c.summary or "",
    }

    # If no database session was supplied, return only
    # the basic case information.
    if db is None:
        return result

    # ========================================================
    # COMPLAINT
    # ========================================================

    complaint = (
        db.query(Complaint)
        .filter(Complaint.case_id == c.id)
        .first()
    )

    # ========================================================
    # PRESENT HISTORY
    # ========================================================

    present_history = (
        db.query(PresentHistory)
        .filter(PresentHistory.case_id == c.id)
        .first()
    )

    # ========================================================
    # PAST HISTORY
    # ========================================================

    past_history = (
        db.query(PastHistory)
        .filter(PastHistory.case_id == c.id)
        .first()
    )

    # ========================================================
    # PERSONAL HISTORY
    # ========================================================

    personal_history = (
        db.query(PersonalHistory)
        .filter(PersonalHistory.case_id == c.id)
        .first()
    )

    # ========================================================
    # FAMILY HISTORY
    # ========================================================

    family_history = (
        db.query(FamilyHistory)
        .filter(FamilyHistory.case_id == c.id)
        .first()
    )

    # ========================================================
    # EXAMINATION
    # ========================================================

    examination = (
        db.query(Examination)
        .filter(Examination.case_id == c.id)
        .first()
    )

    # ========================================================
    # ASSESSMENT
    # ========================================================

    assessment = (
        db.query(Assessment)
        .filter(Assessment.case_id == c.id)
        .first()
    )

    # ========================================================
    # BUILD COMPLAINT
    # ========================================================

    if complaint:
        result["complaint"] = {
            "complaint": complaint.complaint,
            "duration": complaint.duration,
            "onset": complaint.onset,
            "severity": complaint.severity,
            "associated_symptoms": complaint.associated_symptoms,
        }
    else:
        result["complaint"] = None

    # ========================================================
    # BUILD PRESENT HISTORY
    # ========================================================

    if present_history:
        result["present_history"] = {
            "history": present_history.history,
            "onset": present_history.onset,
            "progression": present_history.progression,
            "aggravating_factors": present_history.aggravating_factors,
            "relieving_factors": present_history.relieving_factors,
            "previous_treatment": present_history.previous_treatment,
        }
    else:
        result["present_history"] = None

    # ========================================================
    # BUILD PAST HISTORY
    # ========================================================

    if past_history:
        result["past_history"] = {
            "previous_illnesses": past_history.previous_illnesses,
            "hospitalizations": past_history.hospitalizations,
            "surgeries": past_history.surgeries,
            "medications": past_history.medications,
            "allergies": past_history.allergies,
        }
    else:
        result["past_history"] = None

    # ========================================================
    # BUILD PERSONAL HISTORY
    # ========================================================

    if personal_history:
        result["personal_history"] = {
            "diet": personal_history.diet,
            "appetite": personal_history.appetite,
            "sleep": personal_history.sleep,
            "bowel": personal_history.bowel,
            "bladder": personal_history.bladder,
            "lifestyle": personal_history.lifestyle,
            "other_details": personal_history.other_details,
        }
    else:
        result["personal_history"] = None

    # ========================================================
    # BUILD FAMILY HISTORY
    # ========================================================

    if family_history:
        result["family_history"] = {
            "details": family_history.details,
        }
    else:
        result["family_history"] = None

    # ========================================================
    # BUILD EXAMINATION
    # ========================================================

    if examination:
        result["examination"] = {
            "temperature": examination.temperature,
            "pulse": examination.pulse,
            "respiratory_rate": examination.respiratory_rate,
            "blood_pressure": examination.blood_pressure,
            "spo2": examination.spo2,
            "weight": examination.weight,
            "height": examination.height,
            "general_examination": examination.general_examination,
            "other_findings": examination.other_findings,
        }
    else:
        result["examination"] = None

    # ========================================================
    # BUILD ASSESSMENT
    # ========================================================

    if assessment:
        result["assessment"] = {
            "case_summary": assessment.case_summary,
            "clinical_impression": assessment.clinical_impression,
            "differential_diagnosis": assessment.differential_diagnosis,
            "management_plan": assessment.management_plan,
        }
    else:
        result["assessment"] = None

    return result


# ============================================================
# ROOT / HEALTH
# ============================================================

@app.get("/")
def root():
    return {
        "message": "Patient Case Taking API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# PATIENTS
# ============================================================

@app.get("/patients")
def list_patients(
    db: Session = Depends(get_db)
):
    return [
        patient_dict(p)
        for p in db.query(Patient)
        .order_by(Patient.id.desc())
        .all()
    ]


@app.get("/patients/{patient_id}")
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db)
):
    p = (
        db.query(Patient)
        .filter(Patient.patient_id == patient_id)
        .first()
    )

    if not p:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient_dict(p)


@app.post("/patients", status_code=201)
def create_patient(
    data: PatientIn,
    db: Session = Depends(get_db)
):
    if (
        db.query(Patient)
        .filter(Patient.patient_id == data.patient_id)
        .first()
    ):
        raise HTTPException(
            status_code=409,
            detail="Patient ID already exists"
        )

    p = Patient(**data.model_dump())

    db.add(p)

    try:
        db.commit()
        db.refresh(p)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Patient already exists"
        )

    return patient_dict(p)


@app.put("/patients/{patient_id}")
def update_patient(
    patient_id: str,
    data: PatientUpdate,
    db: Session = Depends(get_db)
):
    p = (
        db.query(Patient)
        .filter(Patient.patient_id == patient_id)
        .first()
    )

    if not p:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    for key, value in data.model_dump(
        exclude_unset=True
    ).items():
        setattr(p, key, value)

    db.commit()
    db.refresh(p)

    return patient_dict(p)


@app.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: str,
    db: Session = Depends(get_db)
):
    patient = (
        db.query(Patient)
        .filter(Patient.patient_id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    case_count = (
        db.query(Case)
        .filter(Case.patient_id == patient.id)
        .count()
    )

    if case_count > 0:
        raise HTTPException(
            status_code=409,
            detail="Patient cannot be deleted because cases are linked to this patient"
        )

    appointment_count = (
        db.query(Appointment)
        .filter(Appointment.patient_id == patient.id)
        .count()
    )

    if appointment_count > 0:
        raise HTTPException(
            status_code=409,
            detail="Patient cannot be deleted because appointments are linked to this patient"
        )

    db.delete(patient)
    db.commit()

    return {
        "message": "Patient deleted successfully",
        "patient_id": patient_id
    }


# ============================================================
# CASES
# ============================================================

@app.get("/cases")
def list_cases(
    db: Session = Depends(get_db)
):
    return [
        case_dict(c, db)
        for c in (
            db.query(Case)
            .order_by(Case.id.desc())
            .all()
        )
    ]


@app.get("/patients/{patient_id}/cases")
def patient_cases(
    patient_id: str,
    db: Session = Depends(get_db)
):
    p = (
        db.query(Patient)
        .filter(Patient.patient_id == patient_id)
        .first()
    )

    if not p:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    cases = (
        db.query(Case)
        .filter(Case.patient_id == p.id)
        .order_by(Case.case_date.desc())
        .all()
    )

    return [
        case_dict(c, db)
        for c in cases
    ]


@app.get("/cases/{case_id}")
def get_case(
    case_id: str,
    db: Session = Depends(get_db)
):
    c = (
        db.query(Case)
        .filter(Case.case_id == case_id)
        .first()
    )

    if not c:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return case_dict(c, db)


@app.delete("/cases/{case_id}")
def delete_case(
    case_id: str,
    db: Session = Depends(get_db)
):
    case = (
        db.query(Case)
        .filter(Case.case_id == case_id)
        .first()
    )

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    db.delete(case)
    db.commit()

    return {
        "message": "Case deleted successfully",
        "case_id": case_id
    }


# ============================================================
# COMPLETE CASE CREATION
# ============================================================

@app.post("/cases/complete", status_code=201)
def create_complete_case(
    data: CompleteCase,
    db: Session = Depends(get_db)
):

    # --------------------------------------------------------
    # PATIENT
    # --------------------------------------------------------

    patient = (
        db.query(Patient)
        .filter(Patient.id == data.patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # --------------------------------------------------------
    # CLINICIAN
    # --------------------------------------------------------

    clinician = (
        db.query(User)
        .filter(User.id == data.clinician_id)
        .first()
    )

    if not clinician:
        raise HTTPException(
            status_code=404,
            detail="Clinician not found"
        )

    # --------------------------------------------------------
    # CASE ID
    # --------------------------------------------------------

    case_id = (
        data.case_id
        or f"C{(db.query(Case).count() + 1):03d}"
    )

    while (
        db.query(Case)
        .filter(Case.case_id == case_id)
        .first()
    ):
        case_id = f"C{int(case_id[1:]) + 1:03d}"

    # --------------------------------------------------------
    # CREATE CASE
    # --------------------------------------------------------

    case = Case(
        case_id=case_id,
        patient_id=patient.id,
        clinician_id=clinician.id,
        case_date=data.case_date,
        status=data.status,
        summary=(
            data.clinical_assessment
            or data.provisional_diagnosis
        )
    )

    db.add(case)
    db.flush()

    # --------------------------------------------------------
    # COMPLAINT
    # --------------------------------------------------------

    duration = " ".join(
        x
        for x in [
            data.duration and str(data.duration),
            data.duration_unit
        ]
        if x
    )

    if data.chief_complaint:
        db.add(
            Complaint(
                case_id=case.id,
                complaint=data.chief_complaint,
                duration=duration or None,
                onset=data.onset,
                severity=data.severity,
                associated_symptoms="; ".join(
                    x
                    for x in [
                        data.additional_complaints,
                        data.associated_symptoms,
                        data.complaint_notes
                    ]
                    if x
                )
            )
        )

    # --------------------------------------------------------
    # PRESENT HISTORY
    # --------------------------------------------------------

    if any([
        data.history_present_illness,
        data.onset,
        data.course,
        data.aggravating_factors,
        data.relieving_factors,
        data.previous_treatment
    ]):
        db.add(
            PresentHistory(
                case_id=case.id,
                history=data.history_present_illness,
                onset=data.onset,
                progression=data.course,
                aggravating_factors=data.aggravating_factors,
                relieving_factors=data.relieving_factors,
                previous_treatment=data.previous_treatment
            )
        )

    # --------------------------------------------------------
    # PAST HISTORY
    # --------------------------------------------------------

    if any([
        data.past_medical_history,
        data.hospitalization_details,
        data.past_surgical_history,
        data.medications,
        data.allergies
    ]):
        db.add(
            PastHistory(
                case_id=case.id,
                previous_illnesses=data.past_medical_history,
                hospitalizations=data.hospitalization_details,
                surgeries=data.past_surgical_history,
                medications=data.medications,
                allergies=data.allergies
            )
        )

    # --------------------------------------------------------
    # PERSONAL HISTORY
    # --------------------------------------------------------

    lifestyle = "; ".join(
        f"{key}: {value}"
        for key, value in {
            "exercise": data.exercise,
            "smoking": data.smoking,
            "alcohol": data.alcohol
        }.items()
        if value
    )

    if any([
        data.diet,
        data.appetite,
        data.sleep,
        data.bowel,
        data.bladder,
        lifestyle,
        data.personal_notes
    ]):
        db.add(
            PersonalHistory(
                case_id=case.id,
                diet=data.diet,
                appetite=data.appetite,
                sleep=data.sleep,
                bowel=data.bowel,
                bladder=data.bladder,
                lifestyle=lifestyle or None,
                other_details=data.personal_notes
            )
        )

    # --------------------------------------------------------
    # FAMILY HISTORY
    # --------------------------------------------------------

    if data.family_history:
        db.add(
            FamilyHistory(
                case_id=case.id,
                details=data.family_history
            )
        )

    # --------------------------------------------------------
    # EXAMINATION
    # --------------------------------------------------------

    if any([
        data.temperature,
        data.pulse,
        data.respiratory_rate,
        data.blood_pressure,
        data.spo2,
        data.weight,
        data.height,
        data.general_examination,
        data.system_examination
    ]):
        db.add(
            Examination(
                case_id=case.id,
                temperature=(
                    str(data.temperature)
                    if data.temperature is not None
                    else None
                ),
                pulse=(
                    str(data.pulse)
                    if data.pulse is not None
                    else None
                ),
                respiratory_rate=(
                    str(data.respiratory_rate)
                    if data.respiratory_rate is not None
                    else None
                ),
                blood_pressure=data.blood_pressure,
                spo2=(
                    str(data.spo2)
                    if data.spo2 is not None
                    else None
                ),
                weight=(
                    str(data.weight)
                    if data.weight is not None
                    else None
                ),
                height=(
                    str(data.height)
                    if data.height is not None
                    else None
                ),
                general_examination=data.general_examination,
                other_findings=data.system_examination
            )
        )

    # --------------------------------------------------------
    # ASSESSMENT
    # --------------------------------------------------------

    if any([
        data.provisional_diagnosis,
        data.differential_diagnosis,
        data.clinical_assessment,
        data.treatment_plan
    ]):
        db.add(
            Assessment(
                case_id=case.id,
                case_summary=data.clinical_assessment,
                clinical_impression=data.provisional_diagnosis,
                differential_diagnosis=data.differential_diagnosis,
                management_plan=data.treatment_plan
            )
        )

    # --------------------------------------------------------
    # SAVE EVERYTHING
    # --------------------------------------------------------

    db.commit()
    db.refresh(case)

    return case_dict(case, db)


# ============================================================
# FOLLOW-UPS
# ============================================================

@app.get("/followups")
def list_followups(
    db: Session = Depends(get_db)
):
    followups = (
        db.query(Followup)
        .order_by(Followup.visit_date.desc())
        .all()
    )

    result = []

    for f in followups:
        case = (
            db.query(Case)
            .filter(Case.id == f.case_id)
            .first()
        )

        result.append({
            "id": f.id,
            "case_id": f.case_id,
            "case_code": case.case_id if case else "",
            "visit_date": f.visit_date,
            "symptoms": f.symptoms,
            "changes_since_last_visit": f.changes_since_last_visit,
            "examination": f.examination,
            "treatment_response": f.treatment_response,
            "medication_adherence": f.medication_adherence,
            "new_findings": f.new_findings,
            "plan": f.plan,
            "next_followup_date": f.next_followup_date
        })

    return result


@app.post("/followups", status_code=201)
def create_followup(
    data: FollowupIn,
    db: Session = Depends(get_db)
):
    if not db.query(Case).filter(
        Case.id == data.case_id
    ).first():
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    f = Followup(**data.model_dump())

    db.add(f)
    db.commit()
    db.refresh(f)

    return {
        "id": f.id,
        **data.model_dump()
    }


# ============================================================
# APPOINTMENTS
# ============================================================

@app.get("/appointments")
def list_appointments(
    db: Session = Depends(get_db)
):
    rows = (
        db.query(Appointment)
        .order_by(Appointment.appointment_date.desc())
        .all()
    )

    return [
        {
            "id": a.id,
            "appointment_id": a.appointment_id,
            "patient_id": a.patient_id,
            "clinician_id": a.clinician_id,
            "appointment_date": a.appointment_date,
            "appointment_time": a.appointment_time,
            "reason": a.reason or "",
            "notes": a.notes or "",
            "status": a.status
        }
        for a in rows
    ]


class AppointmentIn(BaseModel):
    patient_id: int
    clinician_id: Optional[int] = None
    appointment_date: date
    appointment_time: str
    reason: Optional[str] = None
    notes: Optional[str] = None
    status: str = "Scheduled"


@app.post("/appointments", status_code=201)
def create_appointment(
    data: AppointmentIn,
    db: Session = Depends(get_db)
):
    if not db.query(Patient).filter(
        Patient.id == data.patient_id
    ).first():
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    aid = f"A{(db.query(Appointment).count() + 1):03d}"

    a = Appointment(
        appointment_id=aid,
        **data.model_dump()
    )

    db.add(a)
    db.commit()
    db.refresh(a)

    return {
        "id": a.id,
        "appointment_id": a.appointment_id,
        **data.model_dump()
    }


@app.delete("/appointments/{appointment_id}")
def delete_appointment(
    appointment_id: str,
    db: Session = Depends(get_db)
):
    appointment = (
        db.query(Appointment)
        .filter(
            Appointment.appointment_id == appointment_id
        )
        .first()
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    db.delete(appointment)
    db.commit()

    return {
        "message": "Appointment deleted successfully",
        "appointment_id": appointment_id
    }


# ============================================================
# USERS / LOGIN
# ============================================================

@app.get("/users")
def list_users(
    db: Session = Depends(get_db)
):
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role
        }
        for u in db.query(User).all()
    ]


@app.post("/login")
def login(
    username: str,
    password: str,
    db: Session = Depends(get_db)
):
    u = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if not u:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not bcrypt.checkpw(
        password.encode("utf-8"),
        u.password_hash.encode("utf-8")
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "authenticated": True,
        "user_id": u.id,
        "username": u.username,
        "role": u.role
    }


# ============================================================
# REVIEW OF SYSTEMS
# ============================================================

class ReviewOfSystemsIn(BaseModel):
    case_id: int
    general: Optional[str] = None
    respiratory: Optional[str] = None
    cardiovascular: Optional[str] = None
    gastrointestinal: Optional[str] = None
    neurological: Optional[str] = None
    musculoskeletal: Optional[str] = None
    genitourinary: Optional[str] = None
    skin: Optional[str] = None
    other_systems: Optional[str] = None


@app.post("/cases/{case_id}/review-of-systems")
def create_review_of_systems(
    case_id: int,
    data: ReviewOfSystemsIn,
    db: Session = Depends(get_db),
):
    if case_id != data.case_id:
        raise HTTPException(
            status_code=400,
            detail=f"case_id mismatch: URL={case_id}, BODY={data.case_id}"
        )

    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    existing = (
        db.query(ReviewOfSystems)
        .filter(ReviewOfSystems.case_id == case_id)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Review of systems already exists for this case"
        )

    record = ReviewOfSystems(
        **data.model_dump()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.get("/cases/{case_id}/review-of-systems")
def get_review_of_systems(
    case_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(ReviewOfSystems)
        .filter(ReviewOfSystems.case_id == case_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Review of systems not found"
        )

    return record


@app.put("/cases/{case_id}/review-of-systems")
def update_review_of_systems(
    case_id: int,
    data: ReviewOfSystemsIn,
    db: Session = Depends(get_db),
):
    if case_id != data.case_id:
        raise HTTPException(
            status_code=400,
            detail="case_id mismatch"
        )

    record = (
        db.query(ReviewOfSystems)
        .filter(ReviewOfSystems.case_id == case_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Review of systems not found"
        )

    for key, value in data.model_dump(
        exclude={"case_id"}
    ).items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record


# ============================================================
# DOCUMENTS
# ============================================================

class DocumentIn(BaseModel):
    patient_id: int
    document_type: Optional[str] = None
    file_name: Optional[str] = None
    file_path: Optional[str] = None


@app.post("/patients/{patient_id}/documents")
def create_document(
    patient_id: int,
    data: DocumentIn,
    db: Session = Depends(get_db),
):
    if patient_id != data.patient_id:
        raise HTTPException(
            status_code=400,
            detail="patient_id mismatch"
        )

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    record = Document(
        **data.model_dump()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.get("/patients/{patient_id}/documents")
def get_patient_documents(
    patient_id: int,
    db: Session = Depends(get_db),
):
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return (
        db.query(Document)
        .filter(Document.patient_id == patient_id)
        .all()
    )


@app.get("/documents/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return record


@app.delete("/documents/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Document deleted successfully"
    }


# ============================================================
# EXTRACTED DATA
# ============================================================

class ExtractedDataIn(BaseModel):
    document_id: int
    data_type: Optional[str] = None
    extracted_text: Optional[str] = None
    structured_data: Optional[str] = None


@app.post("/documents/{document_id}/extracted-data")
def create_extracted_data(
    document_id: int,
    data: ExtractedDataIn,
    db: Session = Depends(get_db),
):
    if document_id != data.document_id:
        raise HTTPException(
            status_code=400,
            detail="document_id mismatch"
        )

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    record = ExtractedData(
        **data.model_dump()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.get("/documents/{document_id}/extracted-data")
def get_document_extracted_data(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return (
        db.query(ExtractedData)
        .filter(
            ExtractedData.document_id == document_id
        )
        .all()
    )


# ============================================================
# AYUSH HISTORY
# ============================================================

class AYUSHHistoryIn(BaseModel):
    case_id: int
    system: Optional[str] = None
    practitioner: Optional[str] = None
    treatment: Optional[str] = None
    medications: Optional[str] = None
    duration: Optional[str] = None
    response: Optional[str] = None
    details: Optional[str] = None


@app.post("/cases/{case_id}/ayush-history")
def create_ayush_history(
    case_id: int,
    data: AYUSHHistoryIn,
    db: Session = Depends(get_db),
):
    if case_id != data.case_id:
        raise HTTPException(
            status_code=400,
            detail="case_id mismatch"
        )

    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    existing = (
        db.query(AYUSHHistory)
        .filter(AYUSHHistory.case_id == case_id)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="AYUSH history already exists for this case"
        )

    record = AYUSHHistory(
        **data.model_dump()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.get("/cases/{case_id}/ayush-history")
def get_ayush_history(
    case_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(AYUSHHistory)
        .filter(AYUSHHistory.case_id == case_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="AYUSH history not found"
        )

    return record


@app.put("/cases/{case_id}/ayush-history")
def update_ayush_history(
    case_id: int,
    data: AYUSHHistoryIn,
    db: Session = Depends(get_db),
):
    if case_id != data.case_id:
        raise HTTPException(
            status_code=400,
            detail="case_id mismatch"
        )

    record = (
        db.query(AYUSHHistory)
        .filter(AYUSHHistory.case_id == case_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="AYUSH history not found"
        )

    for key, value in data.model_dump(
        exclude={"case_id"}
    ).items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record


# ============================================================
# AI SUMMARIES
# ============================================================

class AISummaryIn(BaseModel):
    case_id: int
    summary: Optional[str] = None
    key_findings: Optional[str] = None
    possible_assessment: Optional[str] = None
    recommendations: Optional[str] = None
    status: str = "draft"


@app.post("/cases/{case_id}/ai-summaries")
def create_ai_summary(
    case_id: int,
    data: AISummaryIn,
    db: Session = Depends(get_db),
):
    if case_id != data.case_id:
        raise HTTPException(
            status_code=400,
            detail="case_id mismatch"
        )

    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    record = AISummary(
        **data.model_dump()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.get("/cases/{case_id}/ai-summaries")
def get_ai_summaries(
    case_id: int,
    db: Session = Depends(get_db),
):
    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return (
        db.query(AISummary)
        .filter(AISummary.case_id == case_id)
        .all()
    )


@app.get("/ai-summaries/{summary_id}")
def get_ai_summary(
    summary_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(AISummary)
        .filter(AISummary.id == summary_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="AI summary not found"
        )

    return record


@app.put("/ai-summaries/{summary_id}")
def update_ai_summary(
    summary_id: int,
    data: AISummaryIn,
    db: Session = Depends(get_db),
):
    record = (
        db.query(AISummary)
        .filter(AISummary.id == summary_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="AI summary not found"
        )

    for key, value in data.model_dump(
        exclude={"case_id"}
    ).items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record


# ============================================================
# CONSENTS
# ============================================================

class ConsentIn(BaseModel):
    patient_id: int
    consent_type: str
    status: str
    consent_text: Optional[str] = None
    consented_at: Optional[datetime] = None


@app.post("/patients/{patient_id}/consents")
def create_consent(
    patient_id: int,
    data: ConsentIn,
    db: Session = Depends(get_db),
):
    if patient_id != data.patient_id:
        raise HTTPException(
            status_code=400,
            detail="patient_id mismatch"
        )

    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    record = Consent(
        **data.model_dump()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.get("/patients/{patient_id}/consents")
def get_patient_consents(
    patient_id: int,
    db: Session = Depends(get_db),
):
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return (
        db.query(Consent)
        .filter(Consent.patient_id == patient_id)
        .all()
    )


@app.put("/consents/{consent_id}")
def update_consent(
    consent_id: int,
    data: ConsentIn,
    db: Session = Depends(get_db),
):
    record = (
        db.query(Consent)
        .filter(Consent.id == consent_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Consent not found"
        )

    for key, value in data.model_dump(
        exclude={"patient_id"}
    ).items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record


# ============================================================
# CONSULTATIONS
# ============================================================

class ConsultationIn(BaseModel):
    patient_id: int
    clinician_id: Optional[int] = None
    case_id: Optional[int] = None
    ai_summary_id: Optional[int] = None
    consultation_date: Optional[datetime] = None
    consultation_type: Optional[str] = None
    status: str = "scheduled"
    notes: Optional[str] = None


@app.post("/consultations")
def create_consultation(
    data: ConsultationIn,
    db: Session = Depends(get_db),
):
    patient = (
        db.query(Patient)
        .filter(Patient.id == data.patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    if data.clinician_id is not None:
        clinician = (
            db.query(User)
            .filter(User.id == data.clinician_id)
            .first()
        )

        if not clinician:
            raise HTTPException(
                status_code=404,
                detail="Clinician not found"
            )

    if data.case_id is not None:
        case = (
            db.query(Case)
            .filter(Case.id == data.case_id)
            .first()
        )

        if not case:
            raise HTTPException(
                status_code=404,
                detail="Case not found"
            )

    if data.ai_summary_id is not None:
        summary = (
            db.query(AISummary)
            .filter(AISummary.id == data.ai_summary_id)
            .first()
        )

        if not summary:
            raise HTTPException(
                status_code=404,
                detail="AI summary not found"
            )

    record = Consultation(
        **data.model_dump()
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


@app.get("/consultations/{consultation_id}")
def get_consultation(
    consultation_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(Consultation)
        .filter(Consultation.id == consultation_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Consultation not found"
        )

    return record


@app.get("/patients/{patient_id}/consultations")
def get_patient_consultations(
    patient_id: int,
    db: Session = Depends(get_db),
):
    patient = (
        db.query(Patient)
        .filter(Patient.id == patient_id)
        .first()
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return (
        db.query(Consultation)
        .filter(Consultation.patient_id == patient_id)
        .all()
    )


@app.get("/cases/{case_id}/consultations")
def get_case_consultations(
    case_id: int,
    db: Session = Depends(get_db),
):
    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return (
        db.query(Consultation)
        .filter(Consultation.case_id == case_id)
        .all()
    )


@app.put("/consultations/{consultation_id}")
def update_consultation(
    consultation_id: int,
    data: ConsultationIn,
    db: Session = Depends(get_db),
):
    record = (
        db.query(Consultation)
        .filter(Consultation.id == consultation_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Consultation not found"
        )

    for key, value in data.model_dump().items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)

    return record


@app.delete("/consultations/{consultation_id}")
def delete_consultation(
    consultation_id: int,
    db: Session = Depends(get_db),
):
    record = (
        db.query(Consultation)
        .filter(Consultation.id == consultation_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=404,
            detail="Consultation not found"
        )

    db.delete(record)
    db.commit()

    return {
        "message": "Consultation deleted successfully"
    }
