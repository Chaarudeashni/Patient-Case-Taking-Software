import os
import requests

API_URL = os.getenv("PATIENT_API_URL", "http://127.0.0.1:8000")

def _request(method, path, **kwargs):
    try:
        r=requests.request(method, f"{API_URL}{path}", timeout=60, **kwargs)
        if not r.ok:
            try: detail=r.json().get("detail", r.text)
            except Exception: detail=r.text
            raise RuntimeError(str(detail))
        return r.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Backend is not reachable at {API_URL}. Start FastAPI first. ({e})")

def get_patients(): return _request("GET","/patients")
def create_patient(data): return _request("POST","/patients",json=data)
def get_cases(): return _request("GET","/cases")
def get_patient_cases(patient_id): return _request("GET",f"/patients/{patient_id}/cases")
def create_complete_case(data): return _request("POST","/cases/complete",json=data)
def get_followups(): return _request("GET","/followups")
def create_followup(data): return _request("POST","/followups",json=data)
def get_users(): return _request("GET","/users")
def login(username,password): return _request("POST","/login",params={"username":username,"password":password})
def get_appointments(): return _request("GET","/appointments")
def create_appointment(data): return _request("POST","/appointments",json=data)
