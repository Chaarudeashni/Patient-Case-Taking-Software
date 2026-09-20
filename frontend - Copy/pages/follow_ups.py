import streamlit as st
from datetime import date
from utils.api import get_cases, get_followups, create_followup
st.title("Follow Ups")
try: cases=get_cases(); followups=get_followups()
except RuntimeError as e: st.error(str(e)); cases=[]; followups=[]
with st.form("followup_form"):
    if cases:
        labels={f"{c['case_id']} — Patient DB ID {c['patient_id']}":c for c in cases}; label=st.selectbox("Case *",list(labels)); case=labels[label]
        visit=st.date_input("Visit Date",date.today()); symptoms=st.text_area("Symptoms"); changes=st.text_area("Changes Since Last Visit"); exam=st.text_area("Examination"); response=st.text_area("Treatment Response"); adherence=st.text_area("Medication Adherence"); findings=st.text_area("New Findings"); plan=st.text_area("Plan"); nxt=st.date_input("Next Follow-up Date",date.today())
        save=st.form_submit_button("Save Follow-up",use_container_width=True)
    else: st.info("Create a case before adding a follow-up."); save=False; case=None
if save:
    try:
        create_followup({"case_id":case["id"],"visit_date":visit.isoformat(),"symptoms":symptoms or None,"changes_since_last_visit":changes or None,"examination":exam or None,"treatment_response":response or None,"medication_adherence":adherence or None,"new_findings":findings or None,"plan":plan or None,"next_followup_date":nxt.isoformat()})
        st.success("Follow-up saved to the database."); st.rerun()
    except RuntimeError as e: st.error(str(e))
st.divider(); st.subheader("Follow-up Records")
for f in followups: st.write(f"**Case {f['case_id']}** · Visit: {f['visit_date']} · Next: {f.get('next_followup_date') or '-'}")
