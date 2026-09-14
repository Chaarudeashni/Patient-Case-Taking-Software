import streamlit as st
from utils.api import get_patients, get_cases

st.title("Reports")
try: patients=get_patients(); cases=get_cases()
except RuntimeError as e: st.error(str(e)); patients=[]; cases=[]
patient_map={p['id']:p for p in patients}
st.metric("Case Reports",len(cases))
st.divider()
for c in cases:
    p=patient_map.get(c['patient_id'],{})
    name=f"{p.get('first_name','')} {p.get('last_name','')}".strip() or "Unknown patient"
    with st.container(border=True):
        st.subheader(f"{c['case_id']} — {name}")
        st.write(f"Patient ID: {p.get('patient_id','-')}")
        st.write(f"Case date: {c['case_date']} · Status: {c['status']}")
        st.write(c.get('summary') or "No summary recorded.")
        st.download_button("Download summary",f"Case: {c['case_id']}\nPatient: {name}\nPatient ID: {p.get('patient_id','-')}\nDate: {c['case_date']}\nStatus: {c['status']}\nSummary: {c.get('summary','')}",file_name=f"{c['case_id']}.txt",key=f"report_{c['id']}")
