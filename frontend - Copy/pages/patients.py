import streamlit as st
from datetime import date
from utils.api import get_patients, create_patient

st.title("Patients")
st.write("Register, search and manage patient records.")
if "patient_view" not in st.session_state: st.session_state.patient_view="main"
if "selected_patient" not in st.session_state: st.session_state.selected_patient=None

def go(v): st.session_state.patient_view=v; st.rerun()

def load():
    try: return get_patients()
    except RuntimeError as e: st.error(str(e)); return []

patients=load()
if st.session_state.patient_view=="main":
    q=st.text_input("Search",placeholder="Search by patient name, patient ID or phone number")
    if q: patients=[p for p in patients if q.lower() in f"{p['first_name']} {p['last_name']} {p['patient_id']} {p['phone']}".lower()]
    st.button("Register New Patient",on_click=lambda: go("register"))
    st.divider()
    for p in patients:
        with st.container(border=True):
            c1,c2,c3=st.columns([3,2,1]); c1.write(f"**{p['first_name']} {p['last_name']}**"); c1.caption(f"Patient ID: {p['patient_id']}")
            c2.write(f"Phone: {p['phone'] or '-'}"); c2.write(f"Gender: {p['gender'] or '-'}")
            if c3.button("View",key=f"view_{p['patient_id']}"): st.session_state.selected_patient=p; go("view")
elif st.session_state.patient_view=="register":
    st.subheader("Register New Patient")
    with st.form("patient_registration"):
        c1,c2=st.columns(2); first=c1.text_input("First Name *"); last=c2.text_input("Last Name")
        c1,c2=st.columns(2); dob=c1.date_input("Date of Birth",value=date(2000,1,1),min_value=date(1900,1,1),max_value=date.today()); gender=c2.selectbox("Gender",["Select Gender","Male","Female","Other"])
        c1,c2=st.columns(2); phone=c1.text_input("Phone Number *"); email=c2.text_input("Email")
        address=st.text_area("Address"); submit=st.form_submit_button("Register Patient",use_container_width=True)
    if submit:
        if not first.strip() or not phone.isdigit() or len(phone)!=10 or gender=="Select Gender": st.error("Enter first name, valid 10-digit phone number and gender.")
        else:
            try:
                new_id=f"P{(max([int(p['patient_id'][1:]) for p in patients if p['patient_id'].startswith('P') and p['patient_id'][1:].isdigit()] or [0])+1):03d}"
                p=create_patient({"patient_id":new_id,"first_name":first.strip(),"last_name":last.strip() or None,"date_of_birth":dob.isoformat(),"gender":gender,"phone":phone.strip(),"email":email.strip() or None,"address":address.strip() or None})
                st.session_state.selected_patient=p; st.success("Patient registered successfully!"); st.session_state.patient_view="view"; st.rerun()
            except RuntimeError as e: st.error(str(e))
    if st.button("Cancel"): go("main")
else:
    p=st.session_state.selected_patient
    if not p: go("main")
    st.subheader(f"{p['first_name']} {p['last_name']}")
    st.write(f"**Patient ID:** {p['patient_id']}")
    c1,c2=st.columns(2); c1.write(f"Date of Birth: {p['date_of_birth'] or '-'}"); c1.write(f"Gender: {p['gender'] or '-'}"); c2.write(f"Phone: {p['phone'] or '-'}"); c2.write(f"Email: {p['email'] or '-'}"); c2.write(f"Address: {p['address'] or '-'}")
    if st.button("Back to Patients"): go("main")
