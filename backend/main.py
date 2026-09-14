from datetime import date
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt

from database.connection import create_tables, get_db
from database.models import (
    User, Patient, Case, Complaint, PresentHistory, PastHistory,
    PersonalHistory, FamilyHistory, Examination, Assessment, Followup, Appointment
)

app = FastAPI(title="Patient Case Taking API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    create_tables()

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

class CompleteCase(BaseModel):
    patient_id: int
    clinician_id: int = 1
    case_id: Optional[str] = None
    case_date: date = date.today()
    status: str = "active"
    chief_complaint: Optional[str] = None
    duration: Optional[str] = None
    duration_unit: Optional[str] = None
    additional_complaints: Optional[str] = None
    severity: Optional[str] = None
    complaint_notes: Optional[str] = None
    history_present_illness: Optional[str] = None
    onset: Optional[str] = None
    course: Optional[str] = None
    associated_symptoms: Optional[str] = None
    aggravating_factors: Optional[str] = None
    relieving_factors: Optional[str] = None
    previous_treatment: Optional[str] = None
    history_notes: Optional[str] = None
    past_medical_history: Optional[str] = None
    past_surgical_history: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    family_history: Optional[str] = None
    hospitalization_details: Optional[str] = None
    past_history_notes: Optional[str] = None
    diet: Optional[str] = None
    appetite: Optional[str] = None
    sleep: Optional[str] = None
    bowel: Optional[str] = None
    bladder: Optional[str] = None
    exercise: Optional[str] = None
    smoking: Optional[str] = None
    alcohol: Optional[str] = None
    personal_notes: Optional[str] = None
    temperature: Optional[str] = None
    pulse: Optional[str] = None
    respiratory_rate: Optional[str] = None
    blood_pressure: Optional[str] = None
    spo2: Optional[str] = None
    weight: Optional[str] = None
    height: Optional[str] = None
    general_examination: Optional[str] = None
    system_examination: Optional[str] = None
    provisional_diagnosis: Optional[str] = None
    differential_diagnosis: Optional[str] = None
    clinical_assessment: Optional[str] = None
    treatment_plan: Optional[str] = None

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


def patient_dict(p):
    return {"id": p.id, "patient_id": p.patient_id, "first_name": p.first_name, "last_name": p.last_name or "", "date_of_birth": p.date_of_birth, "gender": p.gender or "", "phone": p.phone or "", "email": p.email or "", "address": p.address or ""}

def case_dict(c):
    return {"id": c.id, "case_id": c.case_id, "patient_id": c.patient_id, "clinician_id": c.clinician_id, "case_date": c.case_date, "status": c.status, "summary": c.summary or ""}

@app.get("/")
def root(): return {"message": "Patient Case Taking API is running"}

@app.get("/health")
def health(): return {"status": "healthy"}

@app.get("/patients")
def list_patients(db: Session = Depends(get_db)):
    return [patient_dict(p) for p in db.query(Patient).order_by(Patient.id.desc()).all()]

@app.get("/patients/{patient_id}")
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    p = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not p: raise HTTPException(404, "Patient not found")
    return patient_dict(p)

@app.post("/patients", status_code=201)
def create_patient(data: PatientIn, db: Session = Depends(get_db)):
    if db.query(Patient).filter(Patient.patient_id == data.patient_id).first(): raise HTTPException(409, "Patient ID already exists")
    p = Patient(**data.model_dump())
    db.add(p)
    try: db.commit(); db.refresh(p)
    except IntegrityError: db.rollback(); raise HTTPException(409, "Patient already exists")
    return patient_dict(p)

@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, data: PatientUpdate, db: Session = Depends(get_db)):
    p = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not p: raise HTTPException(404, "Patient not found")
    for k,v in data.model_dump(exclude_unset=True).items(): setattr(p,k,v)
    db.commit(); db.refresh(p); return patient_dict(p)

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str, db: Session = Depends(get_db)):
    # Find patient
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

    # Check whether the patient has any cases
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

    # Check whether the patient has any appointments
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

    # Delete patient only when there are no linked records
    db.delete(patient)
    db.commit()

    return {
        "message": "Patient deleted successfully",
        "patient_id": patient_id
    }

@app.get("/cases")
def list_cases(db: Session = Depends(get_db)):
    return [case_dict(c) for c in db.query(Case).order_by(Case.id.desc()).all()]

@app.get("/patients/{patient_id}/cases")
def patient_cases(patient_id: str, db: Session = Depends(get_db)):
    p=db.query(Patient).filter(Patient.patient_id==patient_id).first()
    if not p: raise HTTPException(404,"Patient not found")
    return [case_dict(c) for c in db.query(Case).filter(Case.patient_id==p.id).order_by(Case.case_date.desc()).all()]

@app.get("/cases/{case_id}")
def get_case(case_id: str, db: Session = Depends(get_db)):
    c=db.query(Case).filter(Case.case_id==case_id).first()
    if not c: raise HTTPException(404,"Case not found")
    return case_dict(c)

@app.delete("/cases/{case_id}")
def delete_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.case_id == case_id).first()

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

@app.post("/cases/complete", status_code=201)
def create_complete_case(data: CompleteCase, db: Session = Depends(get_db)):
    patient=db.query(Patient).filter(Patient.id==data.patient_id).first()
    clinician=db.query(User).filter(User.id==data.clinician_id).first()
    if not patient: raise HTTPException(404,"Patient not found")
    if not clinician: raise HTTPException(404,"Clinician not found")
    case_id=data.case_id or f"C{(db.query(Case).count()+1):03d}"
    if db.query(Case).filter(Case.case_id==case_id).first(): raise HTTPException(409,"Case ID already exists")
    d=data.model_dump(); case=Case(case_id=case_id, patient_id=patient.id, clinician_id=clinician.id, case_date=data.case_date, status=data.status, summary=data.clinical_assessment or data.provisional_diagnosis)
    db.add(case); db.flush()
    duration = " ".join(x for x in [data.duration and str(data.duration), data.duration_unit] if x)
    if data.chief_complaint:
        db.add(Complaint(case_id=case.id, complaint=data.chief_complaint, duration=duration or None, onset=data.onset, severity=data.severity, associated_symptoms="; ".join(x for x in [data.additional_complaints,data.associated_symptoms,data.complaint_notes] if x)))
    if any([data.history_present_illness,data.onset,data.course,data.aggravating_factors,data.relieving_factors,data.previous_treatment]):
        db.add(PresentHistory(case_id=case.id, history=data.history_present_illness, onset=data.onset, progression=data.course, aggravating_factors=data.aggravating_factors, relieving_factors=data.relieving_factors, previous_treatment=data.previous_treatment))
    if any([data.past_medical_history,data.hospitalization_details,data.past_surgical_history,data.medications,data.allergies]):
        db.add(PastHistory(case_id=case.id, previous_illnesses=data.past_medical_history, hospitalizations=data.hospitalization_details, surgeries=data.past_surgical_history, medications=data.medications, allergies=data.allergies))
    lifestyle="; ".join(f"{k}: {v}" for k,v in {"exercise":data.exercise,"smoking":data.smoking,"alcohol":data.alcohol}.items() if v)
    if any([data.diet,data.appetite,data.sleep,data.bowel,data.bladder,lifestyle,data.personal_notes]):
        db.add(PersonalHistory(case_id=case.id, diet=data.diet, appetite=data.appetite, sleep=data.sleep, bowel=data.bowel, bladder=data.bladder, lifestyle=lifestyle or None, other_details=data.personal_notes))
    if data.family_history:
        db.add(FamilyHistory(case_id=case.id, details=data.family_history))
    if any([data.temperature,data.pulse,data.respiratory_rate,data.blood_pressure,data.spo2,data.weight,data.height,data.general_examination,data.system_examination]):
        db.add(Examination(case_id=case.id, temperature=str(data.temperature) if data.temperature is not None else None, pulse=str(data.pulse) if data.pulse is not None else None, respiratory_rate=str(data.respiratory_rate) if data.respiratory_rate is not None else None, blood_pressure=data.blood_pressure, spo2=str(data.spo2) if data.spo2 is not None else None, weight=str(data.weight) if data.weight is not None else None, height=str(data.height) if data.height is not None else None, general_examination=data.general_examination, other_findings=data.system_examination))
    if any([data.provisional_diagnosis,data.differential_diagnosis,data.clinical_assessment,data.treatment_plan]):
        db.add(Assessment(case_id=case.id, case_summary=data.clinical_assessment, clinical_impression=data.provisional_diagnosis, differential_diagnosis=data.differential_diagnosis, management_plan=data.treatment_plan))
    db.commit(); db.refresh(case)
    return case_dict(case)

@app.get("/followups")
def list_followups(db: Session = Depends(get_db)):
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
def create_followup(data: FollowupIn, db: Session=Depends(get_db)):
    if not db.query(Case).filter(Case.id==data.case_id).first(): raise HTTPException(404,"Case not found")
    f=Followup(**data.model_dump()); db.add(f); db.commit(); db.refresh(f); return {"id":f.id, **data.model_dump()}

@app.get("/appointments")
def list_appointments(db: Session=Depends(get_db)):
    rows=db.query(Appointment).order_by(Appointment.appointment_date.desc()).all()
    return [{"id":a.id,"appointment_id":a.appointment_id,"patient_id":a.patient_id,"clinician_id":a.clinician_id,"appointment_date":a.appointment_date,"appointment_time":a.appointment_time,"reason":a.reason or "","notes":a.notes or "","status":a.status} for a in rows]

class AppointmentIn(BaseModel):
    patient_id: int
    clinician_id: Optional[int] = None
    appointment_date: date
    appointment_time: str
    reason: Optional[str] = None
    notes: Optional[str] = None
    status: str = "Scheduled"

@app.post("/appointments", status_code=201)
def create_appointment(data: AppointmentIn, db: Session=Depends(get_db)):
    if not db.query(Patient).filter(Patient.id==data.patient_id).first(): raise HTTPException(404,"Patient not found")
    aid=f"A{(db.query(Appointment).count()+1):03d}"
    a=Appointment(appointment_id=aid, **data.model_dump()); db.add(a); db.commit(); db.refresh(a)
    return {"id":a.id,"appointment_id":a.appointment_id,**data.model_dump()}


@app.delete("/appointments/{appointment_id}")
def delete_appointment(appointment_id: str, db: Session = Depends(get_db)):
    appointment = (
        db.query(Appointment)
        .filter(Appointment.appointment_id == appointment_id)
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


@app.get("/users")
def list_users(db: Session=Depends(get_db)):
    return [{"id":u.id,"username":u.username,"email":u.email,"role":u.role} for u in db.query(User).all()]

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):

    u = db.query(User).filter(User.username == username).first()

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