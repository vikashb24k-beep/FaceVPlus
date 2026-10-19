import streamlit as st
from src.database.db import enroll_student_to_subject
from src.database.config import supabase
from PIL import Image

import time


@st.dialog("Capture or upload photoes")
def add_photoes_dialog():
     
    st.write("Add classroom photoes to scan for attendance")

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab='camera'

    t1 , t2 = st.columns(2)

    with t1:
        type_camera = 'primary' if st.session_state.photo_tab=='camera'else "tertiary"
        if st.button("Camera",type=type_camera):
            st.session_state.photo_tab='camera'


    with t2:
        type_upload = 'primary' if st.session_state.photo_tab=='upload' else "tertiary"
        if st.button("Upload Photo",type=type_upload):
            st.session_state.photo_tab='upload'

    if st.session_state.photo_tab=='camera':
        cam_photo = st.camera_input("Take Photo",key='dialog_cam')
        if cam_photo:
            st.session_state.attendance_images.append(Image.open(cam_photo))
            st.toast("Photo Capture")
            st.rerun()
             

    if st.session_state.photo_tab=='upload':
        uploaded_files = st.file_uploader("'choose image files",type=['jpg','png','jpeg'],accept_multiple_files=True,key='dialog_upload')

        if uploaded_files:
            for f in uploaded_files:
                st.session_state.attendance_images.append(Image.open(f))
            st.toast("Photo Upload Sicessfully")
            st.rerun()
            
    st.divider()
    
    if st.button('Done',type='primary',width='stretch'):
        st.rerun()



        

    
    