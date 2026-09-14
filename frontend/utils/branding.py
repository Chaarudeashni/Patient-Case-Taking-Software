import streamlit as st

def show_branding():
    st.markdown(
        """
        <div style="
            position: fixed;
            top: 5px;
            left: 5px;
            z-index: 999999;
            font-size: 12px;
            font-weight: 400;
            color: red;
            opacity: 1;
        ">
            MED QUEST TEST
        </div>
        """,
        unsafe_allow_html=True
    )