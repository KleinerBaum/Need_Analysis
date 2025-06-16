"""Streamlit entry point for the Vacalyser wizard."""

from __future__ import annotations

import requests
import streamlit as st

from utils.utils_jobinfo import (
    basic_field_extraction,
    extract_text,
    save_fields_to_session,
)
from wizard_steps import (
    wizard_step_1_basic,
    wizard_step_2_company,
    wizard_step_3_department,
    wizard_step_4_role,
    wizard_step_5_tasks,
    wizard_step_6_skills,
    wizard_step_7_compensation,
    wizard_step_8_recruitment,
)

st.set_page_config(page_title="Vacalyser Wizard", layout="wide")

if "current_step" not in st.session_state:
    st.session_state.current_step = 0
if "job_fields" not in st.session_state:
    st.session_state.job_fields = {}

# --- Upload & automatic field extraction ---------------------------------
uploaded_file = st.file_uploader(
    "Jobbeschreibung hochladen / Upload Job Description",
    type=["pdf", "docx", "txt"],
)
url_input = st.text_input(
    "Job Ad URL",
    st.session_state.job_fields.get("job_url", ""),
)

text = ""
if uploaded_file is not None:
    text = extract_text(uploaded_file)
elif url_input:
    try:
        response = requests.get(url_input, timeout=10)
        response.raise_for_status()
        text = response.text
        st.session_state.job_fields["job_url"] = url_input
    except Exception as exc:  # pragma: no cover - network
        st.error(f"Fehler beim Laden der URL: {exc}")

if text:
    fields = basic_field_extraction(text)
    save_fields_to_session(fields)

steps = [
    wizard_step_1_basic,
    wizard_step_2_company,
    wizard_step_3_department,
    wizard_step_4_role,
    wizard_step_5_tasks,
    wizard_step_6_skills,
    wizard_step_7_compensation,
    wizard_step_8_recruitment,
]

steps[st.session_state.current_step]()

col_prev, col_next = st.columns(2)
with col_prev:
    if st.button("Zurück", disabled=st.session_state.current_step == 0):
        st.session_state.current_step = max(0, st.session_state.current_step - 1)
with col_next:
    if st.button("Weiter", key="next_btn"):
        if st.session_state.current_step < len(steps) - 1:
            st.session_state.current_step += 1
