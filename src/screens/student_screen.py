import streamlit as st
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard


def student_screen():
    style_background_dashboard()
    style_base_layout()
    c1, c2 = st.columns(2, gap="small", vertical_alignment="center")
    with c1:
        header_dashboard()
    with c2:
        if st.button(
            "Go back to Home",
        type="secondary",
                key="loginbackbtn",
                shortcut="control+backspace"
            ):
                st.session_state["login_type"] = None
                st.rerun()
    
    st.header("Login using face id", text_alignment="center")
    st.space()
    st.space() 
    st.camera_input("Position your face in the center")
    footer_dashboard()