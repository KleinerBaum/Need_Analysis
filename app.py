"""Streamlit entry point for the Vacalyser wizard."""

from __future__ import annotations

import streamlit as st

from utils.utils_jobinfo import (
    display_all_fields_multiline_copy,
    display_fields_editable,
)
from utils.i18n import tr
from wizard_steps import (
    wizard_step_1_basic,
    wizard_step_2_company,
    wizard_step_3_department,
    wizard_step_4_role,
    wizard_step_5_tasks,
    wizard_step_6_skills,
    wizard_step_7_compensation,
    wizard_step_8_recruitment,
    wizard_step_9_publication,
)

LOGO_PATH = "images/sthree.png"
BACKGROUND_PATH = "images/AdobeStock_506577005.jpeg"

st.set_page_config(page_title="Vacalyser Wizard", layout="wide")

st.image(LOGO_PATH, width=200)

# Reset widget key tracking each run to avoid stale keys
st.session_state["_used_widget_keys"] = set()

# --- Global language toggle ------------------------------------------------
if "lang" not in st.session_state:
    st.session_state["lang"] = "de"

col_space, col_toggle = st.columns([10, 1])
with col_toggle:
    toggle = st.toggle("English", value=st.session_state["lang"] == "en")
st.session_state["lang"] = "en" if toggle else "de"
lang = st.session_state["lang"]

st.markdown(
    f"""
    <style>
        .main {{
            background: linear-gradient(rgba(255,255,255,0.5), rgba(255,255,255,0.5)), url('{BACKGROUND_PATH}');
            background-size: cover;
            background-attachment: fixed;
        }}
        input, textarea {{border: 2px solid #5b031c !important;}}
        .stProgress > div > div > div > div {{background-color: #5b031c;}}
        h1, h2, h3 {{color: #5b031c;}}
    </style>
    """,
    unsafe_allow_html=True,
)


# Initialisiere job_fields, falls noch nicht vorhanden
if "job_fields" not in st.session_state:
    st.session_state["job_fields"] = {}

# --- Wizard-Step Navigation ----------------------------------------------
wizard_steps = [
    ("Grunddaten / Basic Data", wizard_step_1_basic),
    ("Unternehmen / Company Info", wizard_step_2_company),
    ("Abteilung / Department", wizard_step_3_department),
    ("Rolle / Role", wizard_step_4_role),
    ("Aufgaben / Tasks", wizard_step_5_tasks),
    ("Skills / Kompetenzen", wizard_step_6_skills),
    ("Verg\u00fctung / Compensation", wizard_step_7_compensation),
    ("Recruiting-Prozess / Recruitment", wizard_step_8_recruitment),
    ("Sprache & Veröffentlichung", wizard_step_9_publication),
]

if "step_idx" not in st.session_state:
    st.session_state["step_idx"] = 0

step_idx = st.session_state["step_idx"]
st.progress((step_idx + 1) / len(wizard_steps))

# --- Wizard-Ansicht -------------------------------------------------------
st.title("Recruitment Need Analysis Wizard")
st.info(
    tr(
        "Alle extrahierten Daten werden bei jedem Schritt als Standardwert vorgeschlagen. / All extracted data will be pre-filled in each step.",
        lang,
    )
)

wizard_steps[step_idx][1]()

col_prev, col_next = st.columns(2)
back_clicked = col_prev.button(tr("Zur\u00fcck / Back", lang), disabled=step_idx == 0)
next_clicked = col_next.button(
    tr("Weiter / Next", lang), disabled=step_idx == len(wizard_steps) - 1
)

if back_clicked:
    st.session_state["step_idx"] = max(0, step_idx - 1)
    st.rerun()
if next_clicked:
    st.session_state["step_idx"] = min(len(wizard_steps) - 1, step_idx + 1)
    st.rerun()

# --- Utility-Optionen nach dem Wizard ------------------------------------
st.markdown("---")
with st.expander(tr("Extras & Export", lang), expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(tr("1. Editierbare Felder / Editable Fields", lang))
        display_fields_editable()
    with col2:
        st.subheader(tr("3. Mehrzeilige Ansicht (Copy & Paste)", lang))
        display_all_fields_multiline_copy()

if st.checkbox(tr("Session State anzeigen / Show Session State [DEV]", lang)):
    st.write(st.session_state)
