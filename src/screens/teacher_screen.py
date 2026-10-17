
import streamlit as st
from src.ui.base_layout import style_base_layout, style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher, teacher_login
import time


def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if 'teacher_login_type' not in st.session_state or st.session_state['teacher_login_type'] == 'login':
        teacher_screen_login()
    elif st.session_state['teacher_login_type'] == 'register':
        teacher_screen_register()


# login
def teacher_screen_login():
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

    st.header("Login using password", text_alignment="center")
    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="vikashkumar"
    )

    teacher_pass = st.text_input(
        "Enter password",
        type="password",
        placeholder="password"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button(
            "Login",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch"
        ):
            if not teacher_username.strip() or not teacher_pass:
                st.warning("Please enter username and password.")

            elif teacher_login(teacher_username.strip(), teacher_pass):
                st.toast("Welcome back!", icon="👋")
                time.sleep(1)
                st.rerun()

            else:
                st.error("Invalid username or password!")

    with btnc2:
        if st.button(
            "Register Now",
            type="primary",
            icon=":material/passkey:",
            width="stretch"
        ):
            st.session_state['teacher_login_type'] = 'register'
            st.rerun()

    footer_dashboard()


def register_teacher(
    teacher_username,
    teacher_name,
    teacher_pass,
    teacher_pass_confirm
):
    # Validate all fields
    if not all([
        teacher_username.strip(),
        teacher_name.strip(),
        teacher_pass,
        teacher_pass_confirm
    ]):
        return False, "All fields are required!"

    # Validate password confirmation
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match!"

    try:
        # Check if username already exists
        if check_teacher_exists(teacher_username.strip()):
            return False, "Username already taken!"

        create_teacher(
            teacher_username.strip(),
            teacher_pass,
            teacher_name.strip()
        )

        return True, "Account created successfully! Please log in."

    except Exception as e:
        print(f"Teacher registration error: {e}")
        return False, "Registration failed. Please try again."


# signup
def teacher_screen_register():
    c1, c2 = st.columns(2, gap="small", vertical_alignment="center")

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="registerbackbtn",
            shortcut="control+backspace"
        ):
            st.session_state["login_type"] = None
            st.session_state["teacher_login_type"] = "login"
            st.rerun()

    st.header("Create Teacher Account", text_alignment="center")
    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="vikashkumar"
    )

    teacher_name = st.text_input(
        "Enter fullname",
        placeholder="vikash kumar"
    )

    teacher_pass = st.text_input(
        "Enter password",
        type="password",
        placeholder="password"
    )

    teacher_pass_confirm = st.text_input(
        "Confirm password",
        type="password",
        placeholder="Confirm password"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button(
            "Register Now",
            type="primary",
            icon=":material/passkey:",
            width="stretch"
        ):
            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_pass,
                teacher_pass_confirm
            )

            if success:
                st.success(message)
                time.sleep(2)
                st.session_state['teacher_login_type'] = 'login'
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button(
            "Login Instead",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch"
        ):
            st.session_state['teacher_login_type'] = 'login'
            st.rerun()

    footer_dashboard()
