import streamlit as st
from datetime import date, datetime

from utils.api import (
    get_patients,
    get_patient_cases,
    get_users,
    get_documents,
    create_document,
    get_extracted_data,
    create_extracted_data,
    get_ayush_history,
    create_ayush_history,
    get_ai_summaries,
    create_ai_summary,
    get_consents,
    create_consent,
    get_consultations,
    create_consultation,
)


st.title("Clinical Records")
st.caption(
    "Manage patient documents, extracted data, AYUSH history, "
    "AI summaries, consent, and consultations."
)


# ============================================================
# LOAD PATIENTS
# ============================================================

try:
    patients = get_patients()
except RuntimeError as e:
    st.error(str(e))
    patients = []


if not patients:
    st.warning("No patients found. Please register a patient first.")
    st.stop()


# ============================================================
# PATIENT SELECTION
# ============================================================

patient_options = {
    f"{p['patient_id']} — {p['first_name']} {p['last_name']}": p
    for p in patients
}

selected_patient_label = st.selectbox(
    "Select Patient",
    list(patient_options.keys()),
)

patient = patient_options[selected_patient_label]

patient_db_id = patient["id"]
display_patient_id = patient["patient_id"]

st.info(
    f"Patient: {patient['first_name']} {patient['last_name']} "
    f"| Patient ID: {display_patient_id}"
)


# ============================================================
# CASE SELECTION
# ============================================================

try:
    cases = get_patient_cases(display_patient_id)
except RuntimeError as e:
    st.error(str(e))
    cases = []


if not cases:
    st.warning("No cases found for this patient.")
    st.stop()


case_options = {
    f"{c['case_id']} — {c['case_date']}": c
    for c in cases
}

selected_case_label = st.selectbox(
    "Select Case",
    list(case_options.keys()),
)

case = case_options[selected_case_label]

case_db_id = case["id"]


st.divider()


# ============================================================
# DOCUMENTS
# ============================================================

st.header("Documents")

try:
    documents = get_documents(patient_db_id)
except RuntimeError as e:
    st.error(str(e))
    documents = []


if documents:
    for doc in documents:
        st.write(
            f"**{doc.get('file_name', 'Unnamed document')}** "
            f"| Type: {doc.get('document_type', 'N/A')} "
            f"| ID: {doc.get('id')}"
        )
else:
    st.info("No documents available yet.")


with st.expander("Add Document"):
    with st.form("add_document_form"):
        document_type = st.selectbox(
            "Document Type",
            [
                "Lab Report",
                "Prescription",
                "Medical Report",
                "Imaging Report",
                "Other",
            ],
        )

        file_name = st.text_input(
            "File Name",
            placeholder="example.pdf",
        )

        file_path = st.text_input(
            "File Path",
            placeholder="uploads/example.pdf",
        )

        save_document = st.form_submit_button(
            "Save Document",
            use_container_width=True,
        )

    if save_document:
        if not file_name.strip():
            st.error("File name is required.")
        else:
            try:
                create_document(
                    {
                        "patient_id": patient_db_id,
                        "document_type": document_type,
                        "file_name": file_name.strip(),
                        "file_path": file_path.strip() or None,
                    }
                )

                st.success("Document saved successfully.")
                st.rerun()

            except RuntimeError as e:
                st.error(str(e))


# ============================================================
# EXTRACTED DATA
# ============================================================

st.divider()
st.header("Extracted Data")


if documents:

    document_options = {
        f"{d['id']} — {d.get('file_name', 'Unnamed')}": d
        for d in documents
    }

    selected_document_label = st.selectbox(
        "Select Document",
        list(document_options.keys()),
    )

    selected_document = document_options[selected_document_label]
    document_id = selected_document["id"]

    try:
        extracted_records = get_extracted_data(document_id)
    except RuntimeError:
        extracted_records = []

    if extracted_records:
        for record in extracted_records:
            st.write(
                f"**Type:** {record.get('data_type', 'N/A')}"
            )

            if record.get("extracted_text"):
                st.write(
                    f"**Extracted Text:** "
                    f"{record['extracted_text']}"
                )

            if record.get("structured_data"):
                st.write(
                    f"**Structured Data:** "
                    f"{record['structured_data']}"
                )

            st.divider()
    else:
        st.info("No extracted data available yet.")

    with st.expander("Add Extracted Data"):
        with st.form("add_extracted_data_form"):

            data_type = st.text_input(
                "Data Type",
                value="Lab Results",
            )

            extracted_text = st.text_area(
                "Extracted Text",
                placeholder="Enter extracted report text...",
            )

            structured_data = st.text_area(
                "Structured Data",
                placeholder="Optional JSON/text",
            )

            save_extracted = st.form_submit_button(
                "Save Extracted Data",
                use_container_width=True,
            )

        if save_extracted:
            try:
                create_extracted_data(
                    document_id,
                    {
                        "document_id": document_id,
                        "data_type": data_type or None,
                        "extracted_text": extracted_text or None,
                        "structured_data": structured_data or None,
                    },
                )

                st.success("Extracted data saved successfully.")
                st.rerun()

            except RuntimeError as e:
                st.error(str(e))

else:
    st.info("Add a document first.")


# ============================================================
# AYUSH HISTORY
# ============================================================

st.divider()
st.header("AYUSH History")

try:
    ayush = get_ayush_history(case_db_id)
except RuntimeError as e:
    # A 404 simply means there is no AYUSH record yet.
    ayush = None


if ayush:
    st.success("AYUSH history available.")

    st.write(f"**System:** {ayush.get('system', 'N/A')}")
    st.write(f"**Practitioner:** {ayush.get('practitioner', 'N/A')}")
    st.write(f"**Treatment:** {ayush.get('treatment', 'N/A')}")
    st.write(f"**Medications:** {ayush.get('medications', 'N/A')}")
    st.write(f"**Duration:** {ayush.get('duration', 'N/A')}")
    st.write(f"**Response:** {ayush.get('response', 'N/A')}")
    st.write(f"**Details:** {ayush.get('details', 'N/A')}")

else:
    st.info("No AYUSH history available yet.")


with st.expander("Add AYUSH History"):

    with st.form("add_ayush_form"):

        system = st.selectbox(
            "System",
            ["Ayurveda", "Yoga", "Unani", "Siddha", "Homoeopathy", "Other"],
        )

        practitioner = st.text_input("Practitioner")

        treatment = st.text_input("Treatment")

        medications = st.text_input("Medications")

        duration = st.text_input("Duration")

        response = st.text_input("Response")

        details = st.text_area("Details")

        save_ayush = st.form_submit_button(
            "Save AYUSH History",
            use_container_width=True,
        )

    if save_ayush:

        try:
            create_ayush_history(
                case_db_id,
                {
                    "case_id": case_db_id,
                    "system": system,
                    "practitioner": practitioner or None,
                    "treatment": treatment or None,
                    "medications": medications or None,
                    "duration": duration or None,
                    "response": response or None,
                    "details": details or None,
                },
            )

            st.success("AYUSH history saved successfully.")
            st.rerun()

        except RuntimeError as e:
            st.error(str(e))


# ============================================================
# AI SUMMARY
# ============================================================

st.divider()
st.header("AI Summary")

try:
    ai_summaries = get_ai_summaries(case_db_id)
except RuntimeError as e:
    st.error(str(e))
    ai_summaries = []


if ai_summaries:

    for summary in ai_summaries:

        st.write(f"**Summary:** {summary.get('summary', 'N/A')}")

        st.write(
            f"**Key Findings:** "
            f"{summary.get('key_findings', 'N/A')}"
        )

        st.write(
            f"**Possible Assessment:** "
            f"{summary.get('possible_assessment', 'N/A')}"
        )

        st.write(
            f"**Recommendations:** "
            f"{summary.get('recommendations', 'N/A')}"
        )

        st.write(
            f"**Status:** "
            f"{summary.get('status', 'draft')}"
        )

else:
    st.info("No AI summary available yet.")


with st.expander("Add AI Summary"):

    with st.form("add_ai_summary_form"):

        summary_text = st.text_area("Summary")

        key_findings = st.text_area("Key Findings")

        possible_assessment = st.text_area(
            "Possible Assessment"
        )

        recommendations = st.text_area(
            "Recommendations"
        )

        summary_status = st.selectbox(
            "Status",
            ["draft", "reviewed", "final"],
        )

        save_summary = st.form_submit_button(
            "Save AI Summary",
            use_container_width=True,
        )

    if save_summary:

        try:
            create_ai_summary(
                case_db_id,
                {
                    "case_id": case_db_id,
                    "summary": summary_text or None,
                    "key_findings": key_findings or None,
                    "possible_assessment": possible_assessment or None,
                    "recommendations": recommendations or None,
                    "status": summary_status,
                },
            )

            st.success("AI summary saved successfully.")
            st.rerun()

        except RuntimeError as e:
            st.error(str(e))


# ============================================================
# CONSENT
# ============================================================

st.divider()
st.header("Patient Consent")

try:
    consents = get_consents(patient_db_id)
except RuntimeError as e:
    st.error(str(e))
    consents = []


if consents:

    for consent in consents:

        st.write(
            f"**Consent Type:** "
            f"{consent.get('consent_type', 'N/A')}"
        )

        st.write(
            f"**Status:** "
            f"{consent.get('status', 'N/A')}"
        )

        st.write(
            f"**Consent Text:** "
            f"{consent.get('consent_text', 'N/A')}"
        )

else:
    st.info("No consent records available yet.")


with st.expander("Add Consent"):

    with st.form("add_consent_form"):

        consent_type = st.text_input(
            "Consent Type",
            value="Clinical Data Processing",
        )

        consent_status = st.selectbox(
            "Status",
            ["granted", "pending", "withdrawn"],
        )

        consent_text = st.text_area(
            "Consent Text",
            value=(
                "Patient consents to the processing of "
                "clinical information for healthcare purposes."
            ),
        )

        save_consent = st.form_submit_button(
            "Save Consent",
            use_container_width=True,
        )

    if save_consent:

        try:
            create_consent(
                patient_db_id,
                {
                    "patient_id": patient_db_id,
                    "consent_type": consent_type,
                    "status": consent_status,
                    "consent_text": consent_text or None,
                    "consented_at": (
                        datetime.now().isoformat()
                        if consent_status == "granted"
                        else None
                    ),
                },
            )

            st.success("Consent saved successfully.")
            st.rerun()

        except RuntimeError as e:
            st.error(str(e))


# ============================================================
# CONSULTATION
# ============================================================

st.divider()
st.header("Consultation")

try:
    consultations = get_consultations(patient_db_id)
except RuntimeError as e:
    st.error(str(e))
    consultations = []


if consultations:

    for consultation in consultations:

        st.write(
            f"**Date:** "
            f"{consultation.get('consultation_date', 'N/A')}"
        )

        st.write(
            f"**Status:** "
            f"{consultation.get('status', 'N/A')}"
        )

        st.write(
            f"**Type:** "
            f"{consultation.get('consultation_type', 'N/A')}"
        )

        st.write(
            f"**Notes:** "
            f"{consultation.get('notes', 'N/A')}"
        )

        st.divider()

else:
    st.info("No consultation records available yet.")


# Load clinicians
try:
    clinicians = get_users()
except RuntimeError:
    clinicians = []


with st.expander("Add Consultation"):

    with st.form("add_consultation_form"):

        if clinicians:

            clinician_options = {
                f"{u['id']} — {u['username']}": u
                for u in clinicians
            }

            clinician_label = st.selectbox(
                "Clinician",
                list(clinician_options.keys()),
            )

            clinician = clinician_options[clinician_label]

            clinician_id = clinician["id"]

        else:

            clinician_id = None
            st.info("No clinician list available.")

        consultation_date = st.date_input(
            "Consultation Date",
            value=date.today(),
        )

        consultation_type = st.text_input(
            "Consultation Type",
            value="Initial Consultation",
        )

        consultation_status = st.selectbox(
            "Status",
            ["scheduled", "completed", "cancelled"],
        )

        notes = st.text_area(
            "Notes",
            placeholder="Enter consultation notes...",
        )

        save_consultation = st.form_submit_button(
            "Save Consultation",
            use_container_width=True,
        )

    if save_consultation:

        try:

            create_consultation(
                {
                    "patient_id": patient_db_id,
                    "clinician_id": clinician_id,
                    "case_id": case_db_id,
                    "ai_summary_id": None,
                    "consultation_date": (
                        datetime.combine(
                            consultation_date,
                            datetime.min.time(),
                        ).isoformat()
                    ),
                    "consultation_type": (
                        consultation_type or None
                    ),
                    "status": consultation_status,
                    "notes": notes or None,
                }
            )

            st.success("Consultation saved successfully.")
            st.rerun()

        except RuntimeError as e:
            st.error(str(e))