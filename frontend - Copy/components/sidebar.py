import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown(
            "<h4 style='margin: 0;'>Patient Case Taking Software</h4>",
            unsafe_allow_html=True
        )

        st.divider()

        if st.button("Dashboard", use_container_width=True):
            st.switch_page("pages/dashboard_page.py")

        if st.button("Patients", use_container_width=True):
            st.switch_page("pages/patients.py")

        if st.button("Clinical Records", use_container_width=True):
            st.switch_page("pages/clinical_records.py")

        st.divider()

        st.markdown("New Case")
        st.markdown("Follow Ups")
        st.markdown("Appointments")
        st.markdown("Reports")
        st.markdown("Settings")

        st.divider()

        st.markdown("User")

        if st.button("Logout", use_container_width=True):
            st.success("Logged out")