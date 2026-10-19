
import streamlit as st
import pandas as pd

from datetime import datetime

from src.pipelines.voice_pipeline import process_bulk_audio
from src.database.config import supabase
from src.components.dialog_attendance_result import show_attendance_result


@st.dialog('Voice Attendance')
def voice_attendance_dialog(selected_subject_id):

    st.write(
        "Record audio of students saying "
        "'I am present'. Then AI will recognize the students."
    )

    audio_data = st.audio_input(
        "Record classroom audio",
        key=f"voice_attendance_audio_{selected_subject_id}"
    )

    if st.button(
        'Analyze Audio',
        width='stretch',
        type='primary',
        key=f"analyze_voice_{selected_subject_id}"
    ):

        if audio_data is None:
            st.warning("Please record classroom audio first.")
            return

        with st.spinner('Processing audio data...'):

            enrolled_res = (
                supabase.table('subject_students')
                .select('*, students(*)')
                .eq('subject_id', selected_subject_id)
                .execute()
            )

            enrolled_students = enrolled_res.data or []

            if not enrolled_students:
                st.warning("No students enrolled in this course.")
                return

            candidates_dict = {
                node['students']['student_id']:
                    node['students']['voice_embedding']
                for node in enrolled_students
                if node.get('students')
                and node['students'].get('voice_embedding')
            }

            if not candidates_dict:
                st.error(
                    "No enrolled students have registered voice profiles."
                )
                return

            audio_bytes = audio_data.getvalue()

            detected_scores = process_bulk_audio(
                audio_bytes,
                candidates_dict
            )

            results = []
            attendance_to_log = []

            current_timestamp = (
                datetime.now().astimezone().isoformat()
            )

            for node in enrolled_students:

                student = node.get('students')

                if not student:
                    continue

                student_id = student['student_id']

                score = detected_scores.get(student_id, 0.0)

                # Assumes process_bulk_audio returns numeric scores
                is_present = score > 0

                results.append({
                    "Name": student['name'],
                    "ID": student_id,
                    "Source": score if is_present else "-",
                    "Status": "Present" if is_present else "Absent"
                })

                attendance_to_log.append({
                    'student_id': student_id,
                    'subject_id': selected_subject_id,
                    'timestamp': current_timestamp,
                    'is_present': bool(is_present)
                })

            if results:
                st.session_state.voice_attendance_results = (
                    selected_subject_id,
                    pd.DataFrame(results),
                    attendance_to_log
                )

    saved_results = st.session_state.get(
        'voice_attendance_results'
    )

    if (
        saved_results
        and saved_results[0] == selected_subject_id
    ):
        st.divider()

        _, df_results, logs = saved_results

        show_attendance_result(df_results, logs)

