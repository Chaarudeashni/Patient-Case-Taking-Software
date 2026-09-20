import os
import requests

API_URL = os.getenv("PATIENT_API_URL", "http://127.0.0.1:8000")


def _request(method, path, **kwargs):
    try:
        r = requests.request(
            method,
            f"{API_URL}{path}",
            timeout=10,
            **kwargs
        )

        if not r.ok:
            try:
                detail = r.json().get("detail", r.text)
            except Exception:
                detail = r.text
            raise RuntimeError(str(detail))

        return r.json()

    except requests.RequestException as e:
        raise RuntimeError(
            f"Backend is not reachable at {API_URL}. "
            f"Start FastAPI first. ({e})"
        )


# ============================================================
# AUTHENTICATION / USERS
# ============================================================

def login(username, password):
    return _request(
        "POST",
        "/login",
        params={
            "username": username,
            "password": password
        }
    )


def get_users():
    return _request("GET", "/users")


# ============================================================
# PATIENTS
# ============================================================

def get_patients():
    return _request("GET", "/patients")


def create_patient(data):
    return _request("POST", "/patients", json=data)


def get_patient(patient_id):
    return _request("GET", f"/patients/{patient_id}")


def update_patient(patient_id, data):
    return _request("PUT", f"/patients/{patient_id}", json=data)


def delete_patient(patient_id):
    return _request("DELETE", f"/patients/{patient_id}")


# ============================================================
# CASES
# ============================================================

def get_cases():
    return _request("GET", "/cases")


def get_patient_cases(patient_id):
    return _request(
        "GET",
        f"/patients/{patient_id}/cases"
    )


def create_complete_case(data):
    return _request(
        "POST",
        "/cases/complete",
        json=data
    )


def delete_case(case_id):
    return _request(
        "DELETE",
        f"/cases/{case_id}"
    )


# ============================================================
# REVIEW OF SYSTEMS
# ============================================================

def get_review_of_systems(case_id):
    return _request(
        "GET",
        f"/cases/{case_id}/review-of-systems"
    )


def create_review_of_systems(case_id, data):
    return _request(
        "POST",
        f"/cases/{case_id}/review-of-systems",
        json=data
    )


# ============================================================
# DOCUMENTS
# ============================================================

def get_documents(patient_id):
    return _request(
        "GET",
        f"/patients/{patient_id}/documents"
    )


def create_document(data):
    return _request(
        "POST",
        "/documents",
        json=data
    )


# ============================================================
# EXTRACTED DATA
# ============================================================

def get_extracted_data(document_id):
    return _request(
        "GET",
        f"/documents/{document_id}/extracted-data"
    )


def create_extracted_data(document_id, data):
    return _request(
        "POST",
        f"/documents/{document_id}/extracted-data",
        json=data
    )


# ============================================================
# AYUSH HISTORY
# ============================================================

def get_ayush_history(case_id):
    return _request(
        "GET",
        f"/cases/{case_id}/ayush-history"
    )


def create_ayush_history(case_id, data):
    return _request(
        "POST",
        f"/cases/{case_id}/ayush-history",
        json=data
    )


# ============================================================
# AI SUMMARIES
# ============================================================

def get_ai_summaries(case_id):
    return _request(
        "GET",
        f"/cases/{case_id}/ai-summaries"
    )


def get_ai_summary(summary_id):
    return _request(
        "GET",
        f"/ai-summaries/{summary_id}"
    )


def create_ai_summary(case_id, data):
    return _request(
        "POST",
        f"/cases/{case_id}/ai-summaries",
        json=data
    )


# ============================================================
# CONSENTS
# ============================================================

def get_consents(patient_id):
    return _request(
        "GET",
        f"/patients/{patient_id}/consents"
    )


def create_consent(patient_id, data):
    return _request(
        "POST",
        f"/patients/{patient_id}/consents",
        json=data
    )


# ============================================================
# CONSULTATIONS
# ============================================================

def get_consultations(patient_id):
    return _request(
        "GET",
        f"/patients/{patient_id}/consultations"
    )


def create_consultation(data):
    return _request(
        "POST",
        "/consultations",
        json=data
    )


def get_consultation(consultation_id):
    return _request(
        "GET",
        f"/consultations/{consultation_id}"
    )


# ============================================================
# FOLLOW-UPS
# ============================================================

def get_followups():
    return _request("GET", "/followups")


def create_followup(data):
    return _request(
        "POST",
        "/followups",
        json=data
    )


# ============================================================
# APPOINTMENTS
# ============================================================

def get_appointments():
    return _request("GET", "/appointments")


def create_appointment(data):
    return _request(
        "POST",
        "/appointments",
        json=data
    )