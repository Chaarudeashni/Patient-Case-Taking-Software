from datetime import date
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
def create_patient(
    db,
    patient_id,
    first_name,
    last_name=None,
    date_of_birth=None,
    gender=None,
    phone=None,
    email=None,
    address=None
):
    """
    Create a new patient and save it to the database.
    """

    patient = Patient(
        patient_id=patient_id,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=gender,
        phone=phone,
        email=email,
        address=address
    )

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient
def get_patient_by_patient_id(db, patient_id):
    """
    Find a patient using their unique patient ID.
    """

    return (
        db.query(Patient)
        .filter(Patient.patient_id == patient_id)
        .first()
    )
def update_patient(
    db,
    patient_id,
    first_name=None,
    last_name=None,
    date_of_birth=None,
    gender=None,
    phone=None,
    email=None,
    address=None
):
    """
    Update an existing patient's information.
    """

    patient = get_patient_by_patient_id(
        db=db,
        patient_id=patient_id
    )

    if patient is None:
        return None

    if first_name is not None:
        patient.first_name = first_name

    if last_name is not None:
        patient.last_name = last_name

    if date_of_birth is not None:
        patient.date_of_birth = date_of_birth

    if gender is not None:
        patient.gender = gender

    if phone is not None:
        patient.phone = phone

    if email is not None:
        patient.email = email

    if address is not None:
        patient.address = address

    db.commit()
    db.refresh(patient)

    return patient

def delete_patient(db, patient_id):
    """
    Delete a patient using their unique patient ID.
    """

    patient = get_patient_by_patient_id(
        db=db,
        patient_id=patient_id
    )

    if patient is None:
        return False

    db.delete(patient)
    db.commit()

    return True
def create_case(
    db,
    case_id,
    patient_id,
    clinician_id,
    case_date=None,
    status="active",
    summary=None
):
    """
    Create a new case for an existing patient.
    """

    if case_date is None:
        case_date = date.today()

    case = Case(
        case_id=case_id,
        patient_id=patient_id,
        clinician_id=clinician_id,
        case_date=case_date,
        status=status,
        summary=summary
    )

    db.add(case)
    db.commit()
    db.refresh(case)

    return case

def get_case_by_case_id(db, case_id):
    """
    Find a case using its unique case ID.
    """

    return (
        db.query(Case)
        .filter(Case.case_id == case_id)
        .first()
    )

def get_cases_by_patient_id(db, patient_id):
    """
    Retrieve all cases belonging to a patient.
    """

    return (
        db.query(Case)
        .filter(Case.patient_id == patient_id)
        .order_by(Case.case_date.desc())
        .all()
    )
def update_case(
    db,
    case_id,
    case_date=None,
    status=None,
    summary=None
):
    """
    Update an existing case using its unique case ID.
    """

    case = get_case_by_case_id(
        db=db,
        case_id=case_id
    )

    if case is None:
        return None

    if case_date is not None:
        case.case_date = case_date

    if status is not None:
        case.status = status

    if summary is not None:
        case.summary = summary

    db.commit()
    db.refresh(case)

    return case

def delete_case(db, case_id):
    """
    Delete a case using its unique case ID.
    """

    case = get_case_by_case_id(
        db=db,
        case_id=case_id
    )

    if case is None:
        return False

    db.delete(case)
    db.commit()

    return True
def create_user(
    db,
    username,
    email,
    password_hash,
    role="clinician"
):
    """
    Create a new user/clinician.
    """

    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def create_complaint(
    db,
    case_id,
    complaint,
    duration=None,
    onset=None,
    location=None,
    severity=None,
    associated_symptoms=None
):
    """
    Create a new complaint for a case.
    """

    complaint_record = Complaint(
        case_id=case_id,
        complaint=complaint,
        duration=duration,
        onset=onset,
        location=location,
        severity=severity,
        associated_symptoms=associated_symptoms
    )

    db.add(complaint_record)
    db.commit()
    db.refresh(complaint_record)

    return complaint_record
def get_complaints_by_case_id(db, case_id):
    """
    Get all complaints belonging to a case.
    """
    return (
        db.query(Complaint)
        .filter(Complaint.case_id == case_id)
        .order_by(Complaint.id.asc())
        .all()
    )

def update_complaint(
    db,
    complaint_id,
    complaint=None,
    duration=None,
    onset=None,
    location=None,
    severity=None,
    associated_symptoms=None
):
    """
    Update an existing complaint.
    """
    complaint_record = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if complaint_record is None:
        return None

    if complaint is not None:
        complaint_record.complaint = complaint

    if duration is not None:
        complaint_record.duration = duration

    if onset is not None:
        complaint_record.onset = onset

    if location is not None:
        complaint_record.location = location

    if severity is not None:
        complaint_record.severity = severity

    if associated_symptoms is not None:
        complaint_record.associated_symptoms = associated_symptoms

    db.commit()
    db.refresh(complaint_record)

    return complaint_record

def delete_complaint(db, complaint_id):
    """
    Delete an existing complaint.
    """
    complaint_record = (
        db.query(Complaint)
        .filter(Complaint.id == complaint_id)
        .first()
    )

    if complaint_record is None:
        return False

    db.delete(complaint_record)
    db.commit()

    return True

def create_present_history(
    db,
    case_id,
    history=None,
    onset=None,
    progression=None,
    aggravating_factors=None,
    relieving_factors=None,
    previous_treatment=None
):
    """
    Create present history for a case.
    """

    present_history = PresentHistory(
        case_id=case_id,
        history=history,
        onset=onset,
        progression=progression,
        aggravating_factors=aggravating_factors,
        relieving_factors=relieving_factors,
        previous_treatment=previous_treatment
    )

    db.add(present_history)
    db.commit()
    db.refresh(present_history)

    return present_history
def get_present_history_by_case_id(db, case_id):
    """
    Get present history for a specific case.
    """

    return (
        db.query(PresentHistory)
        .filter(PresentHistory.case_id == case_id)
        .first()
    )
def update_present_history(
    db,
    case_id,
    history=None,
    onset=None,
    progression=None,
    aggravating_factors=None,
    relieving_factors=None,
    previous_treatment=None
):
    """
    Update present history for a specific case.
    """

    present_history = get_present_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if present_history is None:
        return None

    if history is not None:
        present_history.history = history

    if onset is not None:
        present_history.onset = onset

    if progression is not None:
        present_history.progression = progression

    if aggravating_factors is not None:
        present_history.aggravating_factors = aggravating_factors

    if relieving_factors is not None:
        present_history.relieving_factors = relieving_factors

    if previous_treatment is not None:
        present_history.previous_treatment = previous_treatment

    db.commit()
    db.refresh(present_history)

    return present_history

def delete_present_history(db, case_id):
    """
    Delete present history for a specific case.
    """

    present_history = get_present_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if present_history is None:
        return False

    db.delete(present_history)
    db.commit()

    return True

def create_past_history(
    db,
    case_id,
    previous_illnesses=None,
    hospitalizations=None,
    surgeries=None,
    medications=None,
    allergies=None
):
    """
    Create past history for a case.
    """

    past_history = PastHistory(
        case_id=case_id,
        previous_illnesses=previous_illnesses,
        hospitalizations=hospitalizations,
        surgeries=surgeries,
        medications=medications,
        allergies=allergies
    )

    db.add(past_history)
    db.commit()
    db.refresh(past_history)

    return past_history

def get_past_history_by_case_id(db, case_id):
    """
    Get past history for a specific case.
    """

    return (
        db.query(PastHistory)
        .filter(PastHistory.case_id == case_id)
        .first()
    )

def update_past_history(
    db,
    case_id,
    previous_illnesses=None,
    hospitalizations=None,
    surgeries=None,
    medications=None,
    allergies=None
):
    """
    Update past history for a specific case.
    """

    past_history = get_past_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if past_history is None:
        return None

    if previous_illnesses is not None:
        past_history.previous_illnesses = previous_illnesses

    if hospitalizations is not None:
        past_history.hospitalizations = hospitalizations

    if surgeries is not None:
        past_history.surgeries = surgeries

    if medications is not None:
        past_history.medications = medications

    if allergies is not None:
        past_history.allergies = allergies

    db.commit()
    db.refresh(past_history)

    return past_history

def delete_past_history(db, case_id):
    """
    Delete past history for a specific case.
    """

    past_history = get_past_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if past_history is None:
        return False

    db.delete(past_history)
    db.commit()

    return True
def create_personal_history(
    db,
    case_id,
    diet=None,
    appetite=None,
    sleep=None,
    bowel=None,
    bladder=None,
    lifestyle=None,
    other_details=None
):
    """
    Create personal history for a case.
    """

    personal_history = PersonalHistory(
        case_id=case_id,
        diet=diet,
        appetite=appetite,
        sleep=sleep,
        bowel=bowel,
        bladder=bladder,
        lifestyle=lifestyle,
        other_details=other_details
    )

    db.add(personal_history)
    db.commit()
    db.refresh(personal_history)

    return personal_history

def get_personal_history_by_case_id(db, case_id):
    """
    Get personal history for a specific case.
    """

    return (
        db.query(PersonalHistory)
        .filter(PersonalHistory.case_id == case_id)
        .first()
    )

def update_personal_history(
    db,
    case_id,
    diet=None,
    appetite=None,
    sleep=None,
    bowel=None,
    bladder=None,
    lifestyle=None,
    other_details=None
):
    """
    Update personal history for a specific case.
    """

    personal_history = get_personal_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if personal_history is None:
        return None

    if diet is not None:
        personal_history.diet = diet

    if appetite is not None:
        personal_history.appetite = appetite

    if sleep is not None:
        personal_history.sleep = sleep

    if bowel is not None:
        personal_history.bowel = bowel

    if bladder is not None:
        personal_history.bladder = bladder

    if lifestyle is not None:
        personal_history.lifestyle = lifestyle

    if other_details is not None:
        personal_history.other_details = other_details

    db.commit()
    db.refresh(personal_history)

    return personal_history

def delete_personal_history(db, case_id):
    """
    Delete personal history for a specific case.
    """

    personal_history = get_personal_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if personal_history is None:
        return False

    db.delete(personal_history)
    db.commit()

    return True

def create_family_history(
    db,
    case_id,
    family_members=None,
    relevant_diseases=None,
    hereditary_conditions=None,
    details=None
):
    """
    Create family history for a case.
    """

    family_history = FamilyHistory(
        case_id=case_id,
        family_members=family_members,
        relevant_diseases=relevant_diseases,
        hereditary_conditions=hereditary_conditions,
        details=details
    )

    db.add(family_history)
    db.commit()
    db.refresh(family_history)

    return family_history

def get_family_history_by_case_id(db, case_id):
    """
    Get family history for a case.
    """

    return (
        db.query(FamilyHistory)
        .filter(FamilyHistory.case_id == case_id)
        .first()
    )

def update_family_history(
    db,
    case_id,
    family_members=None,
    relevant_diseases=None,
    hereditary_conditions=None,
    details=None
):
    """
    Update family history for a case.
    """

    family_history = get_family_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if family_history is None:
        return None

    if family_members is not None:
        family_history.family_members = family_members

    if relevant_diseases is not None:
        family_history.relevant_diseases = relevant_diseases

    if hereditary_conditions is not None:
        family_history.hereditary_conditions = hereditary_conditions

    if details is not None:
        family_history.details = details

    db.commit()
    db.refresh(family_history)

    return family_history

def delete_family_history(db, case_id):
    """
    Delete family history for a case.
    """

    family_history = get_family_history_by_case_id(
        db=db,
        case_id=case_id
    )

    if family_history is None:
        return False

    db.delete(family_history)
    db.commit()

    return True

def create_examination(
    db,
    case_id,
    temperature=None,
    pulse=None,
    respiratory_rate=None,
    blood_pressure=None,
    spo2=None,
    weight=None,
    height=None,
    general_examination=None,
    respiratory_examination=None,
    cardiovascular_examination=None,
    gastrointestinal_examination=None,
    neurological_examination=None,
    other_findings=None
):
    """
    Create examination details for a case.
    """

    examination = Examination(
        case_id=case_id,
        temperature=temperature,
        pulse=pulse,
        respiratory_rate=respiratory_rate,
        blood_pressure=blood_pressure,
        spo2=spo2,
        weight=weight,
        height=height,
        general_examination=general_examination,
        respiratory_examination=respiratory_examination,
        cardiovascular_examination=cardiovascular_examination,
        gastrointestinal_examination=gastrointestinal_examination,
        neurological_examination=neurological_examination,
        other_findings=other_findings
    )

    db.add(examination)
    db.commit()
    db.refresh(examination)

    return examination

def get_examination_by_case_id(db, case_id):
    """
    Get examination details for a case.
    """

    return (
        db.query(Examination)
        .filter(Examination.case_id == case_id)
        .first()
    )

def update_examination(
    db,
    case_id,
    temperature=None,
    pulse=None,
    respiratory_rate=None,
    blood_pressure=None,
    spo2=None,
    weight=None,
    height=None,
    general_examination=None,
    respiratory_examination=None,
    cardiovascular_examination=None,
    gastrointestinal_examination=None,
    neurological_examination=None,
    other_findings=None
):
    """
    Update examination details for a case.
    """

    examination = get_examination_by_case_id(
        db=db,
        case_id=case_id
    )

    if examination is None:
        return None

    if temperature is not None:
        examination.temperature = temperature

    if pulse is not None:
        examination.pulse = pulse

    if respiratory_rate is not None:
        examination.respiratory_rate = respiratory_rate

    if blood_pressure is not None:
        examination.blood_pressure = blood_pressure

    if spo2 is not None:
        examination.spo2 = spo2

    if weight is not None:
        examination.weight = weight

    if height is not None:
        examination.height = height

    if general_examination is not None:
        examination.general_examination = general_examination

    if respiratory_examination is not None:
        examination.respiratory_examination = respiratory_examination

    if cardiovascular_examination is not None:
        examination.cardiovascular_examination = cardiovascular_examination

    if gastrointestinal_examination is not None:
        examination.gastrointestinal_examination = gastrointestinal_examination

    if neurological_examination is not None:
        examination.neurological_examination = neurological_examination

    if other_findings is not None:
        examination.other_findings = other_findings

    db.commit()
    db.refresh(examination)

    return examination

def delete_examination(db, case_id):
    """
    Delete examination details for a case.
    """

    examination = get_examination_by_case_id(
        db=db,
        case_id=case_id
    )

    if examination is None:
        return False

    db.delete(examination)
    db.commit()

    return True

def create_assessment(
    db,
    case_id,
    case_summary=None,
    clinical_impression=None,
    differential_diagnosis=None,
    investigations=None,
    management_plan=None,
    advice=None
):
    """
    Create assessment details for a case.
    """

    assessment = Assessment(
        case_id=case_id,
        case_summary=case_summary,
        clinical_impression=clinical_impression,
        differential_diagnosis=differential_diagnosis,
        investigations=investigations,
        management_plan=management_plan,
        advice=advice
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment

def get_assessment_by_case_id(db, case_id):
    """
    Get assessment details for a case.
    """

    return (
        db.query(Assessment)
        .filter(Assessment.case_id == case_id)
        .first()
    )

def update_assessment(
    db,
    case_id,
    case_summary=None,
    clinical_impression=None,
    differential_diagnosis=None,
    investigations=None,
    management_plan=None,
    advice=None
):
    """
    Update assessment details for a case.
    """

    assessment = get_assessment_by_case_id(
        db=db,
        case_id=case_id
    )

    if assessment is None:
        return None

    if case_summary is not None:
        assessment.case_summary = case_summary

    if clinical_impression is not None:
        assessment.clinical_impression = clinical_impression

    if differential_diagnosis is not None:
        assessment.differential_diagnosis = differential_diagnosis

    if investigations is not None:
        assessment.investigations = investigations

    if management_plan is not None:
        assessment.management_plan = management_plan

    if advice is not None:
        assessment.advice = advice

    db.commit()
    db.refresh(assessment)

    return assessment

def delete_assessment(db, case_id):
    """
    Delete assessment details for a case.
    """

    assessment = get_assessment_by_case_id(
        db=db,
        case_id=case_id
    )

    if assessment is None:
        return False

    db.delete(assessment)
    db.commit()

    return True

def create_followup(
    db,
    case_id,
    visit_date,
    symptoms=None,
    changes_since_last_visit=None,
    examination=None,
    treatment_response=None,
    medication_adherence=None,
    new_findings=None,
    plan=None,
    next_followup_date=None
):
    """
    Create a follow-up record for a case.
    """

    followup = Followup(
        case_id=case_id,
        visit_date=visit_date,
        symptoms=symptoms,
        changes_since_last_visit=changes_since_last_visit,
        examination=examination,
        treatment_response=treatment_response,
        medication_adherence=medication_adherence,
        new_findings=new_findings,
        plan=plan,
        next_followup_date=next_followup_date
    )

    db.add(followup)
    db.commit()
    db.refresh(followup)

    return followup

def get_followups_by_case_id(db, case_id):
    """
    Get all follow-up records for a case.
    """

    return (
        db.query(Followup)
        .filter(Followup.case_id == case_id)
        .order_by(Followup.visit_date.desc())
        .all()
    )

def update_followup(
    db,
    followup_id,
    visit_date=None,
    symptoms=None,
    changes_since_last_visit=None,
    examination=None,
    treatment_response=None,
    medication_adherence=None,
    new_findings=None,
    plan=None,
    next_followup_date=None
):
    """
    Update a follow-up record.
    """

    followup = (
        db.query(Followup)
        .filter(Followup.id == followup_id)
        .first()
    )

    if followup is None:
        return None

    if visit_date is not None:
        followup.visit_date = visit_date

    if symptoms is not None:
        followup.symptoms = symptoms

    if changes_since_last_visit is not None:
        followup.changes_since_last_visit = changes_since_last_visit

    if examination is not None:
        followup.examination = examination

    if treatment_response is not None:
        followup.treatment_response = treatment_response

    if medication_adherence is not None:
        followup.medication_adherence = medication_adherence

    if new_findings is not None:
        followup.new_findings = new_findings

    if plan is not None:
        followup.plan = plan

    if next_followup_date is not None:
        followup.next_followup_date = next_followup_date

    db.commit()
    db.refresh(followup)

    return followup

def delete_followup(db, followup_id):
    """
    Delete a follow-up record.
    """

    followup = (
        db.query(Followup)
        .filter(Followup.id == followup_id)
        .first()
    )

    if followup is None:
        return False

    db.delete(followup)
    db.commit()

    return True

# ============================================================
# REVIEW OF SYSTEMS CRUD
# ============================================================

def create_review_of_systems(db, data):
    record = ReviewOfSystems(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_review_of_systems(db, case_id):
    return (
        db.query(ReviewOfSystems)
        .filter(ReviewOfSystems.case_id == case_id)
        .first()
    )


def update_review_of_systems(db, case_id, data):
    record = get_review_of_systems(db, case_id)

    if not record:
        return None

    for key, value in data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


def delete_review_of_systems(db, case_id):
    record = get_review_of_systems(db, case_id)

    if not record:
        return False

    db.delete(record)
    db.commit()
    return True


# ============================================================
# DOCUMENT CRUD
# ============================================================

def create_document(db, data):
    record = Document(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_document(db, document_id):
    return (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )


def get_documents_by_patient(db, patient_id):
    return (
        db.query(Document)
        .filter(Document.patient_id == patient_id)
        .all()
    )


def delete_document(db, document_id):
    record = get_document(db, document_id)

    if not record:
        return False

    db.delete(record)
    db.commit()
    return True


# ============================================================
# EXTRACTED DATA CRUD
# ============================================================

def create_extracted_data(db, data):
    record = ExtractedData(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_extracted_data(db, extracted_data_id):
    return (
        db.query(ExtractedData)
        .filter(ExtractedData.id == extracted_data_id)
        .first()
    )


def get_extracted_data_by_document(db, document_id):
    return (
        db.query(ExtractedData)
        .filter(ExtractedData.document_id == document_id)
        .all()
    )


def delete_extracted_data(db, extracted_data_id):
    record = get_extracted_data(db, extracted_data_id)

    if not record:
        return False

    db.delete(record)
    db.commit()
    return True


# ============================================================
# AYUSH HISTORY CRUD
# ============================================================

def create_ayush_history(db, data):
    record = AYUSHHistory(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_ayush_history(db, case_id):
    return (
        db.query(AYUSHHistory)
        .filter(AYUSHHistory.case_id == case_id)
        .first()
    )


def update_ayush_history(db, case_id, data):
    record = get_ayush_history(db, case_id)

    if not record:
        return None

    for key, value in data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


def delete_ayush_history(db, case_id):
    record = get_ayush_history(db, case_id)

    if not record:
        return False

    db.delete(record)
    db.commit()
    return True


# ============================================================
# AI SUMMARY CRUD
# ============================================================

def create_ai_summary(db, data):
    record = AISummary(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_ai_summary(db, summary_id):
    return (
        db.query(AISummary)
        .filter(AISummary.id == summary_id)
        .first()
    )


def get_ai_summaries_by_case(db, case_id):
    return (
        db.query(AISummary)
        .filter(AISummary.case_id == case_id)
        .all()
    )


def update_ai_summary(db, summary_id, data):
    record = get_ai_summary(db, summary_id)

    if not record:
        return None

    for key, value in data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


def delete_ai_summary(db, summary_id):
    record = get_ai_summary(db, summary_id)

    if not record:
        return False

    db.delete(record)
    db.commit()
    return True


# ============================================================
# CONSENT CRUD
# ============================================================

def create_consent(db, data):
    record = Consent(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_consent(db, consent_id):
    return (
        db.query(Consent)
        .filter(Consent.id == consent_id)
        .first()
    )


def get_consents_by_patient(db, patient_id):
    return (
        db.query(Consent)
        .filter(Consent.patient_id == patient_id)
        .all()
    )


def update_consent(db, consent_id, data):
    record = get_consent(db, consent_id)

    if not record:
        return None

    for key, value in data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


def delete_consent(db, consent_id):
    record = get_consent(db, consent_id)

    if not record:
        return False

    db.delete(record)
    db.commit()
    return True


# ============================================================
# CONSULTATION CRUD
# ============================================================

def create_consultation(db, data):
    record = Consultation(**data)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def get_consultation(db, consultation_id):
    return (
        db.query(Consultation)
        .filter(Consultation.id == consultation_id)
        .first()
    )


def get_consultations_by_patient(db, patient_id):
    return (
        db.query(Consultation)
        .filter(Consultation.patient_id == patient_id)
        .all()
    )


def get_consultations_by_case(db, case_id):
    return (
        db.query(Consultation)
        .filter(Consultation.case_id == case_id)
        .all()
    )


def update_consultation(db, consultation_id, data):
    record = get_consultation(db, consultation_id)

    if not record:
        return None

    for key, value in data.items():
        setattr(record, key, value)

    db.commit()
    db.refresh(record)
    return record


def delete_consultation(db, consultation_id):
    record = get_consultation(db, consultation_id)

    if not record:
        return False

    db.delete(record)
    db.commit()
    return True
