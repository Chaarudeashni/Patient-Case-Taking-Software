import streamlit as st

st.set_page_config(
    page_title="Patient Case Taking Software",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

login_page = st.Page(
    "pages/login.py",
    title="Login",
)

home_page = st.Page(
    "pages/home.py",
    title="Home",
)

dashboard_page = st.Page(
    "pages/dashboard_page.py",
    title="Dashboard",
)

patients_page = st.Page(
    "pages/patients.py",
    title="Patients",
)

new_case_page = st.Page(
    "pages/new_case.py",
    title="New Case",
)

follow_ups_page = st.Page(
    "pages/follow_ups.py",
    title="Follow Ups",
)

appointments_page = st.Page(
    "pages/appointments.py",
    title="Appointments",
)

reports_page = st.Page(
    "pages/reports.py",
    title="Reports",
)

settings_page = st.Page(
    "pages/settings.py",
    title="Settings",
)

if not st.session_state.logged_in:

    pg = st.navigation(
        [login_page],
        position="hidden",
    )

    st.markdown(
        """
        <style>

        /* Hide sidebar on login page */
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        /* Login background */
        .stApp {
            background-color: #f5f7fb;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #f5f7fb;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    pg.run()

else:

    st.markdown(
        """
        <style>

        /* =================================================
           MAIN PAGE
           ================================================= */

        .stApp {
            background-color: #f5f7fb;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #f5f7fb;
        }

        [data-testid="stMain"] {
            background-color: #f5f7fb;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }


        /* =================================================
           MAIN PAGE HEADINGS
           ================================================= */

        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
            color: #172033 !important;
        }


        /* =================================================
           MAIN PAGE INPUTS
           ================================================= */

        input,
        textarea {
            color: #172033 !important;
            background-color: white !important;
        }

        [data-baseweb="select"] {
            background-color: white !important;
        }

        [data-baseweb="select"] * {
            color: #172033 !important;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            border: 1px solid #d5dbe7;
            border-radius: 8px;
        }


        /* =================================================
           MAIN PAGE BUTTONS
           ================================================= */

        .stButton > button {
            border-radius: 8px;
            min-height: 42px;
            font-weight: 600;
        }


        /* =================================================
           SIDEBAR BACKGROUND
           ================================================= */

        section[data-testid="stSidebar"] {
            background-color: #111827 !important;
        }

        section[data-testid="stSidebar"] > div {
            background-color: #111827 !important;
        }


        /* =================================================
           SIDEBAR CONTENT
           ================================================= */

        section[data-testid="stSidebar"] > div:first-child {
            padding-top: 22px !important;
            padding-left: 22px !important;
            padding-right: 22px !important;
            padding-bottom: 18px !important;
        }


        /* =================================================
           SIDEBAR TITLE
           ================================================= */

        section[data-testid="stSidebar"] h2 {
            color: #ffffff !important;

            font-size: 17px !important;
            font-weight: 700 !important;

            line-height: 1.2 !important;

            margin: 0 !important;
            padding: 0 !important;

            text-align: left !important;
        }

        /* =================================================
           SIDEBAR TEXT
           ================================================= */

        section[data-testid="stSidebar"] p {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] span {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] label {
            color: #ffffff !important;
        }


        /* =================================================
           SIDEBAR DIVIDER
           ================================================= */

        section[data-testid="stSidebar"] hr {
            border: none !important;

            border-top: 1px solid #374151 !important;

            margin-top: 0 !important;
            margin-bottom: 17px !important;
        }


        /* =================================================
           SIDEBAR MENU CONTAINER
           ================================================= */

        section[data-testid="stSidebar"] .stButton {
            width: 100% !important;

            margin: 0 !important;
            padding: 0 !important;
        }


        /* =================================================
           SIDEBAR MENU BUTTON
           ================================================= */

        section[data-testid="stSidebar"] .stButton > button {
            width: 100% !important;

            height: 40px !important;
            min-height: 40px !important;

            margin: 0 0 2px 0 !important;

            padding: 0 14px !important;

            background-color: transparent !important;

            border: none !important;
            border-radius: 8px !important;

            color: #ffffff !important;

            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;

            text-align: left !important;

            box-shadow: none !important;
        }


        /* =================================================
           FORCE BUTTON INNER CONTENT LEFT
           ================================================= */

        section[data-testid="stSidebar"] .stButton > button > div {
            width: 100% !important;

            display: flex !important;
            align-items: center !important;
            justify-content: flex-start !important;

            text-align: left !important;

            margin: 0 !important;
            padding: 0 !important;
        }


        /* =================================================
           FORCE TEXT LEFT
           ================================================= */

        section[data-testid="stSidebar"] .stButton > button p {
            width: auto !important;

            color: #ffffff !important;

            font-size: 14px !important;
            font-weight: 500 !important;

            line-height: 1 !important;

            margin: 0 !important;
            padding: 0 !important;

            text-align: left !important;
        }


        /* =================================================
           BUTTON SPAN
           ================================================= */

        section[data-testid="stSidebar"] .stButton > button span {
            color: #ffffff !important;
        }


        /* =================================================
           MENU HOVER
           ================================================= */

        section[data-testid="stSidebar"] .stButton > button:hover {
            background-color: #1f2937 !important;

            color: #ffffff !important;
        }


        /* =================================================
           USER DIVIDER
           ================================================= */

        section[data-testid="stSidebar"] .stDivider {
            margin-top: 19px !important;
            margin-bottom: 19px !important;
        }


        /* =================================================
           USERNAME
           ================================================= */

        section[data-testid="stSidebar"] .user-name {
            color: #ffffff !important;

            font-size: 15px !important;
            font-weight: 700 !important;

            line-height: 1.2 !important;

            margin: 0 0 12px 0 !important;
            padding: 0 !important;

            text-align: left !important;
        }


        /* =================================================
           LOGOUT
           ================================================= */

        section[data-testid="stSidebar"] .logout-button {
            color: #ffffff !important;

            text-align: left !important;
        }


        /* =================================================
           SIDEBAR CAPTION
           ================================================= */

        section[data-testid="stSidebar"] .stCaption,
        section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
            color: #cbd5e1 !important;
        }

        section[data-testid="stSidebar"]
        [data-testid="stCaptionContainer"] p {
            color: #cbd5e1 !important;
        }


        /* =================================================
           METRIC CARDS
           ================================================= */

        [data-testid="stMetric"] {
            background-color: white;
            border: 1px solid #e1e6ef;
            border-radius: 12px;
            padding: 18px;
        }

        [data-testid="stMetricLabel"] {
            color: #667085 !important;
        }

        [data-testid="stMetricValue"] {
            color: #172033 !important;
        }


        /* =================================================
           ALERTS
           ================================================= */

        [data-testid="stAlert"] {
            border-radius: 8px;
        }


        /* =================================================
           DATAFRAME
           ================================================= */

        [data-testid="stDataFrame"] {
            border-radius: 10px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    pg = st.navigation(
        [
            home_page,
            dashboard_page,
            patients_page,
            new_case_page,
            follow_ups_page,
            appointments_page,
            reports_page,
            settings_page,
        ],
        position="hidden",
    )


    with st.sidebar:

        st.markdown(
            "## Patient Case-Taking Software",
        )

        st.divider()

        if st.button(
            "Home",
            key="sidebar_home",
            use_container_width=True,
        ):
            st.switch_page(home_page)

        if st.button(
            "Dashboard",
            key="sidebar_dashboard",
            use_container_width=True,
        ):
            st.switch_page(dashboard_page)


        if st.button(
            "Patients",
            key="sidebar_patients",
            use_container_width=True,
        ):
            st.switch_page(patients_page)


        if st.button(
            "New Case",
            key="sidebar_new_case",
            use_container_width=True,
        ):
            st.switch_page(new_case_page)


        if st.button(
            "Follow Ups",
            key="sidebar_follow_ups",
            use_container_width=True,
        ):
            st.switch_page(follow_ups_page)


        if st.button(
            "Appointments",
            key="sidebar_appointments",
            use_container_width=True,
        ):
            st.switch_page(appointments_page)


        if st.button(
            "Reports",
            key="sidebar_reports",
            use_container_width=True,
        ):
            st.switch_page(reports_page)


        if st.button(
            "Settings",
            key="sidebar_settings",
            use_container_width=True,
        ):
            st.switch_page(settings_page)


        st.divider()

        st.markdown(
            '<div class="user-name">'
            + (
                st.session_state.username
                if st.session_state.username
                else "Frontend User"
            )
            + "</div>",
            unsafe_allow_html=True,
        )


        if st.button(
            "Logout",
            key="sidebar_logout",
            use_container_width=True,
        ):
            st.session_state.logged_in = False
            st.session_state.username = ""

            st.switch_page(login_page)

    pg.run()