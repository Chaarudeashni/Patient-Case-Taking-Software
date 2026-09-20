import streamlit as st
from utils.api import get_patients, get_cases, get_followups
st.markdown(
    """
    <style>

    /* Main page */
    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Main heading */
    .dashboard-title {
        font-size: 38px;
        font-weight: 700;
        color: #14213d;
        margin-bottom: 5px;
    }

    .dashboard-subtitle {
        font-size: 16px;
        color: #6b7280;
        margin-bottom: 28px;
    }

    /* Metric cards */
    .section-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 10px 14px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}

    .metric-label {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 12px;
        font-weight: 500;
    }

    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: #14213d;
    }

    /* Section cards */
    .section-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 10px 14px;
    margin-bottom: 18px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03);
}

    .section-title {
    font-size: 19px;
    font-weight: 650;
    color: #14213d;
    margin-bottom: 8px;
}

    /* Recent item */
    .recent-item {
        padding: 7px 0;
        border-bottom: 1px solid #edf2f7;
        font-size: 14px;
        color: #475569;
    }

    .recent-item:last-child {
        border-bottom: none;
    }

    .item-main {
        font-weight: 600;
        color: #14213d;
    }

    .item-secondary {
        color: #64748b;
    }

    /* Status */
    .status-active {
        display: inline-block;
        padding: 4px 9px;
        border-radius: 20px;
        background: #ecfdf5;
        color: #047857;
        font-size: 12px;
        font-weight: 600;
    }

    /* Empty state */
    .empty-state {
        color: #94a3b8;
        font-size: 14px;
        padding: 8px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    '<div class="dashboard-title">Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Overview of your patient case management'
    '</div>',
    unsafe_allow_html=True
)
try:

    patients = get_patients()
    cases = get_cases()
    followups = get_followups()

    pending = sum(
        1 for f in followups
        if f.get("next_followup_date")
    )
except RuntimeError as e:
    st.error(str(e))
    patients = []
    cases = []
    followups = []
    pending = 0

c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Patients</div>
            <div class="metric-value">{len(patients)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Cases</div>
            <div class="metric-value">{len(cases)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with c3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Pending Follow Ups</div>
            <div class="metric-value">{pending}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
st.write("")
st.markdown(
    """
    <div class="section-card">
        <div class="section-title">Recent Patients</div>
    """,
    unsafe_allow_html=True
)

if patients:

    for p in patients[:5]:

        first_name = p.get("first_name", "")
        last_name = p.get("last_name", "")
        patient_id = p.get("patient_id", "")
        phone = p.get("phone") or "No phone"

        full_name = f"{first_name} {last_name}".strip()

        st.markdown(
            f"""
            <div class="recent-item">
                <span class="item-main">
                    {patient_id} — {full_name}
                </span>
                <span class="item-secondary">
                    &nbsp; · &nbsp; {phone}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.markdown(
        '<div class="empty-state">No patients found.</div>',
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-card">
        <div class="section-title">Recent Cases</div>
    """,
    unsafe_allow_html=True
)

if cases:

    # Patient lookup using database ID
    patient_lookup = {
        p.get("id"): p
        for p in patients
    }

    for c in cases[:5]:

        case_id = c.get("case_id", "")
        patient_db_id = c.get("patient_id")
        case_date = c.get("case_date", "")
        status = c.get("status", "")

        patient = patient_lookup.get(patient_db_id)

        if patient:

            patient_code = patient.get("patient_id", "")
            first_name = patient.get("first_name", "")
            last_name = patient.get("last_name", "")

            full_name = f"{first_name} {last_name}".strip()

            if status.lower() == "active":

                status_html = (
                    '<span class="status-active">Active</span>'
                )

            else:

                status_html = status

            st.markdown(
                f"""
                <div class="recent-item">
                    <span class="item-main">
                        {case_id}
                    </span>
                    <span class="item-secondary">
                        &nbsp; · &nbsp;
                        {patient_code} — {full_name}
                        &nbsp; · &nbsp;
                        {case_date}
                        &nbsp; · &nbsp;
                    </span>
                    {status_html}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="recent-item">
                    <span class="item-main">
                        {case_id}
                    </span>
                    <span class="item-secondary">
                        &nbsp; · &nbsp;
                        Patient DB ID: {patient_db_id}
                        &nbsp; · &nbsp;
                        {case_date}
                        &nbsp; · &nbsp;
                        {status}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

else:

    st.markdown(
        '<div class="empty-state">No cases found.</div>',
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="section-card">
        <div class="section-title">Recent Follow-ups</div>
    """,
    unsafe_allow_html=True
)

if followups:

    for f in followups[:5]:

        case_id = f.get("case_code") or f.get("case_id", "")
        visit_date = f.get("visit_date", "")
        next_date = f.get("next_followup_date", "")

        st.markdown(
            f"""
            <div class="recent-item">
                <span class="item-main">
                    Case {case_id}
                </span>
                <span class="item-secondary">
                    &nbsp; · &nbsp;
                    Visit: {visit_date}
                    &nbsp; · &nbsp;
                    Next: {next_date}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.markdown(
        '<div class="empty-state">No follow-ups found.</div>',
        unsafe_allow_html=True
    )

st.markdown("</div>", unsafe_allow_html=True)