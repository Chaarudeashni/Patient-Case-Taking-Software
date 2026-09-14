import streamlit as st

if "settings_saved" not in st.session_state:
    st.session_state.settings_saved = False


st.title("Settings")
st.write("Manage application preferences and frontend settings.")


tab1, tab2, tab3 = st.tabs(
    [
        "Profile",
        "Appearance",
        "Notifications",
    ]
)


with tab1:

    st.subheader("User Profile")
    st.write("Update the information displayed for the current user.")

    col1, col2 = st.columns(2)

    with col1:
        first_name = st.text_input(
            "First Name",
            value="Frontend",
            placeholder="Enter first name",
        )

    with col2:
        last_name = st.text_input(
            "Last Name",
            value="User",
            placeholder="Enter last name",
        )

    email = st.text_input(
        "Email Address",
        value="frontend@example.com",
        placeholder="Enter email address",
    )

    role = st.selectbox(
        "Role",
        [
            "Doctor",
            "Nurse",
            "Receptionist",
            "Administrator",
            "Frontend Demo User",
        ],
        index=4,
    )

    st.divider()

    if st.button(
        "Save Profile",
        type="primary",
        use_container_width=False,
    ):
        if not first_name.strip():
            st.error("Please enter your first name.")
        elif not last_name.strip():
            st.error("Please enter your last name.")
        elif not email.strip():
            st.error("Please enter your email address.")
        else:
            st.session_state.settings_saved = True
            st.success("Profile settings saved successfully.")


with tab2:

    st.subheader("Appearance")
    st.write("Customize how the application looks.")


    if "theme" not in st.session_state:
        st.session_state.theme = "Light"

    if "sidebar_style" not in st.session_state:
        st.session_state.sidebar_style = "Expanded"

    if "compact_mode" not in st.session_state:
        st.session_state.compact_mode = False


    theme = st.radio(
        "Theme",
        [
            "Light",
            "Dark",
            "System Default",
        ],
        index=[
            "Light",
            "Dark",
            "System Default"
        ].index(st.session_state.theme),
        horizontal=True,
        key="theme_selection",
    )

    st.session_state.theme = theme


    sidebar_style = st.selectbox(
        "Sidebar Style",
        [
            "Expanded",
            "Collapsed",
        ],
        index=[
            "Expanded",
            "Collapsed"
        ].index(st.session_state.sidebar_style),
        key="sidebar_selection",
    )

    st.session_state.sidebar_style = sidebar_style


    compact_mode = st.checkbox(
        "Enable compact layout",
        value=st.session_state.compact_mode,
        key="compact_selection",
    )

    st.session_state.compact_mode = compact_mode

    if theme == "Dark":

        st.markdown(
            """
            <style>

            /* Main page */
            .stApp {
                background-color: #111827;
                color: #f9fafb;
            }

            /* Text */
            .stApp p,
            .stApp label,
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp h4,
            .stApp h5,
            .stApp h6 {
                color: #f9fafb !important;
            }

            /* Input boxes */
            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox div[data-baseweb="select"],
            .stNumberInput input {
                background-color: #1f2937 !important;
                color: #f9fafb !important;
            }

            /* Sidebar */
            section[data-testid="stSidebar"] {
                background-color: #0f172a;
            }

            /* Divider */
            hr {
                border-color: #374151;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )

    elif theme == "Light":

        st.markdown(
            """
            <style>

            .stApp {
                background-color: #ffffff;
                color: #111827;
            }

            .stApp p,
            .stApp label,
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp h4,
            .stApp h5,
            .stApp h6 {
                color: #111827 !important;
            }

            section[data-testid="stSidebar"] {
                background-color: #0f172a;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <style>

            .stApp {
                background-color: inherit;
                color: inherit;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )

    if sidebar_style == "Collapsed":

        st.markdown(
            """
            <style>

            section[data-testid="stSidebar"] {
                min-width: 80px !important;
                width: 80px !important;
            }

            section[data-testid="stSidebar"] > div {
                width: 80px !important;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <style>

            section[data-testid="stSidebar"] {
                min-width: 260px !important;
                width: 260px !important;
            }

            section[data-testid="stSidebar"] > div {
                width: 260px !important;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )

    if compact_mode:

        st.markdown(
            """
            <style>

            .block-container {
                padding-top: 1rem !important;
                padding-bottom: 1rem !important;
            }

            div[data-testid="stVerticalBlock"] {
                gap: 0.35rem !important;
            }

            </style>
            """,
            unsafe_allow_html=True,
        )


    st.divider()

    if st.button(
        "Save Appearance",
        type="primary",
        use_container_width=False,
    ):
        st.success("Appearance preferences saved successfully.")


with tab3:

    st.subheader("Notifications")
    st.write("Choose which notifications should be enabled.")

    follow_up_notifications = st.toggle(
        "Follow-up reminders",
        value=True,
    )

    appointment_notifications = st.toggle(
        "Appointment reminders",
        value=True,
    )

    case_notifications = st.toggle(
        "New case notifications",
        value=True,
    )

    report_notifications = st.toggle(
        "Report ready notifications",
        value=True,
    )

    st.divider()

    notification_method = st.selectbox(
        "Notification Method",
        [
            "In-app notifications",
            "Email",
            "SMS",
            "In-app + Email",
        ],
    )

    st.divider()

    st.info(
        "Notification preferences are currently stored only "
        "during this frontend session."
    )

    if st.button(
        "Save Notifications",
        type="primary",
        use_container_width=False,
    ):
        st.success("Notification preferences saved successfully.")


