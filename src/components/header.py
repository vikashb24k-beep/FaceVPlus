
import streamlit as st


def header_home():
    st.markdown(
        "<h1 style='text-align:center; color:#E0E3FF;'>"
        "🛡️ FaceVPlus</h1>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<p style='text-align:center; color:#C7D2FE;'>"
        "Smart Face &amp; Voice Recognition</p>",
        unsafe_allow_html=True,
    )



def header_dashboard():
    col1, col2 = st.columns(
        [1, 4],
        vertical_alignment="center"
    )

    with col1:
        st.markdown(
            "<span style='font-size:60px; color:#5865F2;'>"
            ":material/dictionary:"
            "</span>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <h2 style="
                color: #5865F2;
                margin: 0;
                font-size: 32px;
                line-height: 1.2;
            ">FaceVPlus</h2>
            """,
            unsafe_allow_html=True
        )