from database.crud import (
    create_case,
    get_case_by_case_id,
    get_cases_by_patient_id,
    update_case,
    delete_case,

    create_patient,
    get_patient_by_patient_id,
    update_patient,
    delete_patient,

    create_complaint,
    get_complaints_by_case_id,
    update_complaint,
    delete_complaint,

    create_present_history,
    get_present_history_by_case_id,
    update_present_history,
    delete_present_history,

    create_past_history,
    get_past_history_by_case_id,
    update_past_history,
    delete_past_history,

    create_personal_history,
    get_personal_history_by_case_id,
    update_personal_history,
    delete_personal_history,

    create_family_history,
    get_family_history_by_case_id,
    update_family_history,
    delete_family_history,

    create_examination,
    get_examination_by_case_id,
    update_examination,
    delete_examination,

    create_assessment,
    get_assessment_by_case_id,
    update_assessment,
    delete_assessment,

    create_followup,
    get_followups_by_case_id,
    update_followup,
    delete_followup,
)
def create_new_case(
    db,
    case_id,
    patient_id,
    clinician_id,
    case_date=None,
    status="active",
    summary=None
):
    """
    Service function for creating a new case.
    """

    return create_case(
        db=db,
        case_id=case_id,
        patient_id=patient_id,
        clinician_id=clinician_id,
        case_date=case_date,
        status=status,
        summary=summary
    )


def get_case(db, case_id):
    """
    Service function for retrieving a case.
    """

    return get_case_by_case_id(
        db=db,
        case_id=case_id
    )


def get_patient_cases(db, patient_id):
    """
    Service function for retrieving all cases of a patient.
    """

    return get_cases_by_patient_id(
        db=db,
        patient_id=patient_id
    )


def update_existing_case(
    db,
    case_id,
    case_date=None,
    status=None,
    summary=None
):
    """
    Service function for updating a case.
    """

    return update_case(
        db=db,
        case_id=case_id,
        case_date=case_date,
        status=status,
        summary=summary
    )


def remove_case(db, case_id):
    """
    Service function for deleting a case.
    """

    return delete_case(
        db=db,
        case_id=case_id
    )
def create_new_patient(
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
    Service function for creating a new patient.
    """

    return create_patient(
        db=db,
        patient_id=patient_id,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=gender,
        phone=phone,
        email=email,
        address=address
    )


def get_patient(db, patient_id):
    """
    Service function for retrieving a patient.
    """

    return get_patient_by_patient_id(
        db=db,
        patient_id=patient_id
    )


def update_existing_patient(
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
    Service function for updating a patient.
    """

    return update_patient(
        db=db,
        patient_id=patient_id,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=gender,
        phone=phone,
        email=email,
        address=address
    )


def remove_patient(db, patient_id):
    """
    Service function for deleting a patient.
    """

    return delete_patient(
        db=db,
        patient_id=patient_id
    )

def create_new_complaint(
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
    Create a new complaint through the service layer.
    """

    return create_complaint(
        db=db,
        case_id=case_id,
        complaint=complaint,
        duration=duration,
        onset=onset,
        location=location,
        severity=severity,
        associated_symptoms=associated_symptoms
    )

def get_case_complaints(db, case_id):
    """
    Get all complaints for a case through the service layer.
    """

    return get_complaints_by_case_id(
        db=db,
        case_id=case_id
    )

def update_existing_complaint(
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
    Update an existing complaint through the service layer.
    """

    return update_complaint(
        db=db,
        complaint_id=complaint_id,
        complaint=complaint,
        duration=duration,
        onset=onset,
        location=location,
        severity=severity,
        associated_symptoms=associated_symptoms
    )

def remove_complaint(db, complaint_id):
    """
    Delete an existing complaint through the service layer.
    """

    return delete_complaint(
        db=db,
        complaint_id=complaint_id
    )

def create_new_present_history(
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
    Create present history through the service layer.
    """

    return create_present_history(
        db=db,
        case_id=case_id,
        history=history,
        onset=onset,
        progression=progression,
        aggravating_factors=aggravating_factors,
        relieving_factors=relieving_factors,
        previous_treatment=previous_treatment
    )

def get_case_present_history(db, case_id):
    """
    Get the present history for a case through the service layer.
    """

    return get_present_history_by_case_id(
        db=db,
        case_id=case_id
    )

def update_existing_present_history(
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
    Update an existing present history through the service layer.
    """

    return update_present_history(
        db=db,
        case_id=case_id,
        history=history,
        onset=onset,
        progression=progression,
        aggravating_factors=aggravating_factors,
        relieving_factors=relieving_factors,
        previous_treatment=previous_treatment
    )

def remove_present_history(db, case_id):
    """
    Delete the present history for a case through the service layer.
    """

    return delete_present_history(
        db=db,
        case_id=case_id
    )

def create_new_past_history(
    db,
    case_id,
    previous_illnesses=None,
    hospitalizations=None,
    surgeries=None,
    medications=None,
    allergies=None
):
    """
    Create past history through the service layer.
    """

    return create_past_history(
        db=db,
        case_id=case_id,
        previous_illnesses=previous_illnesses,
        hospitalizations=hospitalizations,
        surgeries=surgeries,
        medications=medications,
        allergies=allergies
    )

def get_case_past_history(db, case_id):
    """
    Get the past history for a case through the service layer.
    """

    return get_past_history_by_case_id(
        db=db,
        case_id=case_id
    )

def update_existing_past_history(
    db,
    case_id,
    previous_illnesses=None,
    hospitalizations=None,
    surgeries=None,
    medications=None,
    allergies=None
):
    """
    Update the past history for a case through the service layer.
    """

    return update_past_history(
        db=db,
        case_id=case_id,
        previous_illnesses=previous_illnesses,
        hospitalizations=hospitalizations,
        surgeries=surgeries,
        medications=medications,
        allergies=allergies
    )

def remove_past_history(db, case_id):
    """
    Delete the past history for a case through the service layer.
    """

    return delete_past_history(
        db=db,
        case_id=case_id
    )

def create_new_personal_history(
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
    Create personal history through the service layer.
    """

    return create_personal_history(
        db=db,
        case_id=case_id,
        diet=diet,
        appetite=appetite,
        sleep=sleep,
        bowel=bowel,
        bladder=bladder,
        lifestyle=lifestyle,
        other_details=other_details
    )


def get_case_personal_history(db, case_id):
    """
    Get personal history for a case through the service layer.
    """

    return get_personal_history_by_case_id(
        db=db,
        case_id=case_id
    )


def update_existing_personal_history(
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
    Update personal history through the service layer.
    """

    return update_personal_history(
        db=db,
        case_id=case_id,
        diet=diet,
        appetite=appetite,
        sleep=sleep,
        bowel=bowel,
        bladder=bladder,
        lifestyle=lifestyle,
        other_details=other_details
    )


def remove_personal_history(db, case_id):
    """
    Delete personal history through the service layer.
    """

    return delete_personal_history(
        db=db,
        case_id=case_id
    )

# ============================================================
# FAMILY HISTORY SERVICE
# ============================================================

def create_new_family_history(
    db,
    case_id,
    family_members=None,
    relevant_diseases=None,
    hereditary_conditions=None,
    details=None
):
    return create_family_history(
        db=db,
        case_id=case_id,
        family_members=family_members,
        relevant_diseases=relevant_diseases,
        hereditary_conditions=hereditary_conditions,
        details=details
    )


def get_case_family_history(db, case_id):
    return get_family_history_by_case_id(
        db=db,
        case_id=case_id
    )


def update_existing_family_history(
    db,
    case_id,
    family_members=None,
    relevant_diseases=None,
    hereditary_conditions=None,
    details=None
):
    return update_family_history(
        db=db,
        case_id=case_id,
        family_members=family_members,
        relevant_diseases=relevant_diseases,
        hereditary_conditions=hereditary_conditions,
        details=details
    )


def remove_family_history(db, case_id):
    return delete_family_history(
        db=db,
        case_id=case_id
    )

# ============================================================
# EXAMINATION SERVICE
# ============================================================

def create_new_examination(
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
    return create_examination(
        db=db,
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


def get_case_examination(db, case_id):
    return get_examination_by_case_id(
        db=db,
        case_id=case_id
    )


def update_existing_examination(
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
    return update_examination(
        db=db,
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


def remove_examination(db, case_id):
    return delete_examination(
        db=db,
        case_id=case_id
    )

# ============================================================
# ASSESSMENT SERVICE
# ============================================================

def create_new_assessment(
    db,
    case_id,
    case_summary=None,
    clinical_impression=None,
    differential_diagnosis=None,
    investigations=None,
    management_plan=None,
    advice=None
):
    return create_assessment(
        db=db,
        case_id=case_id,
        case_summary=case_summary,
        clinical_impression=clinical_impression,
        differential_diagnosis=differential_diagnosis,
        investigations=investigations,
        management_plan=management_plan,
        advice=advice
    )


def get_case_assessment(db, case_id):
    return get_assessment_by_case_id(
        db=db,
        case_id=case_id
    )


def update_existing_assessment(
    db,
    case_id,
    case_summary=None,
    clinical_impression=None,
    differential_diagnosis=None,
    investigations=None,
    management_plan=None,
    advice=None
):
    return update_assessment(
        db=db,
        case_id=case_id,
        case_summary=case_summary,
        clinical_impression=clinical_impression,
        differential_diagnosis=differential_diagnosis,
        investigations=investigations,
        management_plan=management_plan,
        advice=advice
    )


def remove_assessment(db, case_id):
    return delete_assessment(
        db=db,
        case_id=case_id
    )

# ============================================================
# FOLLOW-UP SERVICE
# ============================================================

def create_new_followup(
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
    return create_followup(
        db=db,
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


def get_case_followups(db, case_id):
    return get_followups_by_case_id(
        db=db,
        case_id=case_id
    )


def update_existing_followup(
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
    return update_followup(
        db=db,
        followup_id=followup_id,
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


def remove_followup(db, followup_id):
    return delete_followup(
        db=db,
        followup_id=followup_id
    )