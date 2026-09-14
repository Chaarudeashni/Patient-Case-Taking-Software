import streamlit as st
from pathlib import Path
from utils.api import login

st.markdown(
    """
    <style>

        .stApp {
            background: #ffffff;
        }

        [data-testid="stAppViewContainer"] {
            background: #ffffff;
        }

        [data-testid="stMain"] {
            background: #ffffff;
        }

        section[data-testid="stSidebar"] {
            display: none;
        }

        .block-container {
            max-width: 1300px;
            padding-top: 4rem;
            padding-bottom: 3rem;
        }

        /* Login heading */
        .login-heading {
            color: #102f63;
            font-size: 30px;
            font-weight: 700;
            line-height: 1.25;
            margin-top: 20px;
            margin-bottom: 8px;
        }

        /* Login description */
        .login-description {
            color: #667085;
            font-size: 15px;
            line-height: 1.5;
            margin-bottom: 28px;
        }

        /* Input labels */
        div[data-testid="stTextInput"] label {
            color: #102f63 !important;
            font-weight: 600 !important;
        }

        /* Input boxes */
        div[data-baseweb="input"] {
            border: 1px solid #d6dce5;
            border-radius: 8px;
            background: #ffffff;
        }

        div[data-baseweb="input"]:focus-within {
            border-color: #102f63;
            box-shadow: 0 0 0 1px #102f63;
        }

        input {
            color: #172b4d !important;
        }

        /* Remember me */
        div[data-testid="stCheckbox"] label {
            color: #344054 !important;
            font-weight: 400 !important;
        }

        /* Sign in button */
        div[data-testid="stButton"] > button[kind="primary"] {
            background-color: #102f63;
            border: 1px solid #102f63;
            border-radius: 8px;
            height: 48px;
            color: #ffffff;
            font-size: 16px;
            font-weight: 600;
        }

        div[data-testid="stButton"] > button[kind="primary"]:hover {
            background-color: #163d73;
            border-color: #163d73;
        }

        /* Forgot password */
        div[data-testid="stButton"] > button[kind="secondary"] {
            background: transparent;
            border: none;
            color: #174a8b;
            font-size: 14px;
        }

        div[data-testid="stButton"] > button[kind="secondary"]:hover {
            background: transparent;
            color: #102f63;
        }

        /* Image */
        img {
            border-radius: 14px;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

image_path = Path(__file__).parent.parent / "assets" / "login_image.png"

with st.container(border=True):

    image_column, login_column = st.columns(
        [1.05, 0.95],
        gap="large",
    )

    with image_column:

        st.write("")

        if image_path.exists():

            st.image(
    str(image_path),
    use_container_width=True,
)

        else:

            st.error(
                "Login image not found."
            )
    with login_column:

        st.markdown(
            '<div class="login-heading">'
            'Patient Case Taking Software'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="login-description">'
            'Sign in to access the patient management system'
            '</div>',
            unsafe_allow_html=True,
        )
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )
        remember_me = st.checkbox(
            "Remember me",
            key="login_remember_me",
        )

        st.write("")
        if st.button(
            "Sign In",
            type="primary",
            use_container_width=True,
            key="login_button",
        ):

            if not username.strip():

                st.error(
                    "Please enter your username."
                )

            elif not password.strip():

                st.error(
                    "Please enter your password."
                )

            else:

                try:
                    user = login(username.strip(), password)
                    st.session_state.logged_in = True
                    st.session_state.username = user["username"]
                    st.session_state.user_id = user["user_id"]
                    st.session_state.role = user["role"]
                    st.rerun()
                except RuntimeError as e:
                    st.error(str(e))

        st.write("")
        if st.button(
            "Forgot Password?",
            key="forgot_password_button",
        ):

            st.info(
                "Password recovery will be connected "
                "when authentication is implemented."
            )

        st.write("")
