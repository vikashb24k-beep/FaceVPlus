import streamlit as st
import time
import numpy as np
import pandas as pd
from datetime import datetime
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photoes_dialog
from src.database.config import supabase
from src.pipelines.face_pipeline import predict_attendance 
from src.components.dialog_attendance_result import attendance_result_dialog 
from src.components.dialog_voice_attendance import voice_attendance_dialog
from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subjects
)



def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.subheader(f"Welcome, {teacher_data['name']}")

    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Logout",
            type="secondary",
            key="teacher_logout_btn",
            shortcut="control+backspace"
        ):
            st.session_state.pop("teacher_data", None)
            st.session_state["is_logged_in"] = False
            st.session_state.pop("current_teacher_tab", None)
            st.session_state["teacher_login_type"] = "login"
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = (
            "primary"
            if st.session_state.current_teacher_tab == "take_attendance"
            else "tertiary"
        )

        if st.button(
            "Take Attendance",
            type=type1,
            width="stretch",
            icon=":material/ar_on_you:"
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = (
            "primary"
            if st.session_state.current_teacher_tab == "manage_subjects"
            else "tertiary"
        )

        if st.button(
            "Manage Subjects",
            type=type2,
            width="stretch",
            icon=":material/book_ribbon:"
        ):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = (
            "primary"
            if st.session_state.current_teacher_tab == "attendance_records"
            else "tertiary"
        )

        if st.button(
            "Attendance Records",
            type=type3,
            width="stretch",
            icon=":material/cards_stack:"
        ):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    st.header("Take AI Attendance")

    teacher_id = st.session_state.teacher_data['teacher_id']

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning("You don't have any subjects yet!")
        return

    subject_options = {
        f"{s['name']}-{s['subject_code']}": s['subject_id']
        for s in subjects
    }

    col1, col2 = st.columns([3, 1])

    with col1:
        selected_subject_label = st.selectbox(
            'Select subjects',
            options=list(subject_options.keys()),
            key='attendance_subject_select'
        )

    with col2:
        if st.button(
            'Add Photos',
            icon=':material/exposure_plus_1:',
            width='stretch',
            key='add_attendance_photos'
        ):
            add_photoes_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    # Display added photos
    if st.session_state.attendance_images:
        st.header("Added Photos")
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(
                    img,
                    width='stretch',
                    caption=f'Photo {idx + 1}'
                )

    has_photos = bool(st.session_state.attendance_images)

    c1, c2, c3 = st.columns(3)

    # Clear photos
    with c1:
        if st.button(
            'Clear All Photos',
            type='tertiary',
            width='stretch',
            icon=':material/delete:',
            disabled=not has_photos,
            key='clear_attendance_photos'
        ):
            st.session_state.attendance_images = []
            st.rerun()

    # Run face analysis
    with c2:
        if st.button(
            'Run Face Analysis',
            type='secondary',
            width='stretch',
            icon=':material/analytics:',
            disabled=not has_photos,
            key='run_face_analysis'
        ):
            with st.spinner('Analyzing faces...'):

                # Store detected student IDs and photo sources
                all_detected_ids = {}

                for idx, img in enumerate(
                    st.session_state.attendance_images
                ):
                    img_np = np.array(img.convert('RGB'))

                    detected, _, _ = predict_attendance(img_np)

                    if detected:
                        for sid in detected:
                            detected_student_id = int(sid)

                            all_detected_ids.setdefault(
                                detected_student_id, []
                            ).append(f'Photo {idx + 1}')

                # Get students enrolled in the selected subject
                enrolled_res = (
                    supabase.table('subject_students')
                    .select('*,students(*)')
                    .eq('subject_id', selected_subject_id)
                    .execute()
                )

                enrolled_students = enrolled_res.data or []

                if not enrolled_students:
                    st.warning("No students in this course.")

                else:
                    results = []
                    attendance_to_log = []

                    current_timestamp = (
                        datetime.now().astimezone().isoformat()
                    )

                    for node in enrolled_students:
                        student = node.get('students')

                        if not student:
                            continue

                        # FIX: Access the dictionary using its actual key
                        student_id = int(student['student_id'])

                        sources = all_detected_ids.get(
                            student_id, []
                        )

                        is_present = len(sources) > 0

                        results.append({
                            'Name': student['name'],
                            'ID': student['student_id'],
                            'Source': (
                                ', '.join(sources)
                                if is_present else '-'
                            ),
                            'Status': (
                                'Present' if is_present else 'Absent'
                            )
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                    if results:
                        attendance_result_dialog(
                            pd.DataFrame(results),
                            attendance_to_log
                        )
                    else:
                        st.warning(
                            "No valid enrolled student records found."
                        )

    # Voice attendance
    with c3:
        if st.button(
            "Use Voice Attendance",
            type='primary',
            width='stretch',
            icon=':material/mic:',
            key='use_voice_attendance'
        ):
            st.header('Voice Attendance')
            voice_attendance_dialog(selected_subject_id) 


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1, col2 = st.columns(2)

    with col1:
        st.header('Manage Subjects')

    with col2:
        if st.button('Create New Subject', width='stretch'):
            create_subject_dialog(teacher_id)

    # LIST all SUBJECTS
    subjects = get_teacher_subjects(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            def share_btn(
                subject_code=sub['subject_code'],
                subject_name=sub['name']
            ):
                if st.button(
                    f"Share Code: {subject_code}",
                    key=f"share_{subject_name}",
                    icon=":material/share:"
                ):
                    share_subject_dialog(subject_code, subject_name)

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn
            )

    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")

def teacher_tab_attendance_records():
    st.header("Attendance Records")
    


def login_teacher(username, password):
    if not username.strip() or not password:
        return False

    teacher = teacher_login(username, password)

    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True

    return False


# Login screen
def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="teacher_login_back_btn",
            shortcut="control+backspace"
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Login using password", text_alignment="center")
    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="vikash"
    )

    teacher_pass = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter password"
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

            elif login_teacher(teacher_username, teacher_pass):
                st.toast("Welcome back!", icon="👋")
                time.sleep(1)
                st.rerun()

            else:
                st.error("Invalid username or password.")

    with btnc2:
        if st.button(
            "Register Instead",
            type="primary",
            icon=":material/passkey:",
            width="stretch"
        ):
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


# Registration validation
def register_teacher(
    teacher_username,
    teacher_name,
    teacher_pass,
    teacher_pass_confirm
):
    if not all([
        teacher_username.strip(),
        teacher_name.strip(),
        teacher_pass,
        teacher_pass_confirm
    ]):
        return False, "All fields are required."

    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords do not match."

    try:
        if check_teacher_exists(teacher_username.strip()):
            return False, "Username already taken."

        create_teacher(
            teacher_username.strip(),
            teacher_pass,
            teacher_name.strip()
        )

        return True, "Account created successfully. Please log in."

    except Exception as e:
        print(f"Teacher registration error: {e}")
        return False, "Registration failed. Please try again."


# Registration screen
def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="teacher_register_back_btn",
            shortcut="control+backspace"
        ):
            st.session_state["login_type"] = None
            st.session_state.teacher_login_type = "login"
            st.rerun()

    st.header("Register your teacher profile")
    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="vikash"
    )

    teacher_name = st.text_input(
        "Enter name",
        placeholder="vikkash kumar"
    )

    teacher_pass = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter password"
    )

    teacher_pass_confirm = st.text_input(
        "Confirm your password",
        type="password",
        placeholder="Confirm password"
    )

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        if st.button(
            "Register now",
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
                st.session_state.teacher_login_type = "login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button(
            "Login Instead",
            type="primary",
            icon=":material/passkey:",
            width="stretch"
        ):
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()