import streamlit as st

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
