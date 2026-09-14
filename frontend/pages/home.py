import streamlit as st
from pathlib import Path
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

        .block-container {
            max-width: 1300px;
            margin-left: auto;
            margin-right: auto;
            padding-top: 4rem;
            padding-bottom: 3rem;
        }

        /* About heading */
        .about-heading {
            color: #102f63;
            font-size: 32px;
            font-weight: 700;
            line-height: 1.25;
            margin-top: 45px;
            margin-bottom: 20px;
        }

        /* About text */
        .about-text {
            color:#0e1012;
            font-size: 16px;
            line-height: 1.7;
            margin-bottom: 18px;
        }

        /* Image */
        .home-image img {
            border-radius: 16px;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

image_path = Path(__file__).parent.parent / "assets" / "home_image.png"

about_column, image_column = st.columns(
    [1, 1],
    gap="large",
)

with about_column:

    st.markdown(
        """
        <div class="about-heading">
            Patient Case Taking Software
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="about-text">
            Welcome to the Patient Case Taking Software.
        </div>

        <div class="about-text">
            This software helps manage patient case information
            in an organized and efficient way.
        </div>

        <div class="about-text">
            It helps healthcare professionals record and manage
            patient details, symptoms, diagnosis, and other
            important case information in one place.
        </div>

        <div class="about-text">
            The system provides an easy-to-use interface for
            managing patient cases efficiently.
        </div>
        """,
        unsafe_allow_html=True,
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
            "Home image not found. "
            "Place home_image.png inside frontend/assets/"
        )
