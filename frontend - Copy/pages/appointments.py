import streamlit as st
from datetime import date
from utils.api import get_patients, get_appointments, create_appointment
st.title("Appointments")
try: patients=get_patients(); appointments=get_appointments()
except RuntimeError as e: st.error(str(e)); patients=[]; appointments=[]
with st.form("appointment"):
    if patients:
        labels={f"{p['patient_id']} — {p['first_name']} {p['last_name']}":p for p in patients}; label=st.selectbox("Patient *",list(labels)); p=labels[label]
        adate=st.date_input("Appointment Date",date.today()); atime=st.text_input("Appointment Time",placeholder="10:30 AM"); reason=st.text_input("Reason"); notes=st.text_area("Notes"); status=st.selectbox("Status",["Scheduled","Completed","Cancelled"]); save=st.form_submit_button("Save Appointment",use_container_width=True)
    else: st.info("Register a patient first."); save=False; p=None
if save:
    if not atime.strip(): st.error("Appointment time is required.")
    else:
        try: create_appointment({"patient_id":p["id"],"appointment_date":adate.isoformat(),"appointment_time":atime.strip(),"reason":reason or None,"notes":notes or None,"status":status}); st.success("Appointment saved."); st.rerun()
        except RuntimeError as e: st.error(str(e))
st.divider(); st.subheader("Appointment Records")
for a in appointments: st.write(f"**{a['appointment_id']}** · Patient DB ID {a['patient_id']} · {a['appointment_date']} {a['appointment_time']} · {a['status']}")
