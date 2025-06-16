"""Streamlit entry point for the Vacalyser wizard."""

from __future__ import annotations

import requests
import streamlit as st

from utils.utils_jobinfo import (
    basic_field_extraction,
    display_all_fields_multiline_copy,
    display_fields_editable,
    export_fields_as_markdown,
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

# --- Sidebar: Datei-Upload und (optional) URL -----------------------------
st.sidebar.header("1. Jobbeschreibung hochladen / Upload Job Description")
uploaded_file = st.sidebar.file_uploader(
    "W\u00e4hle eine Datei (PDF, DOCX, TXT) / Choose a file (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"],
)
url_input = st.sidebar.text_input("...oder gib eine URL ein / ...or enter a URL")

# --- Extraktion und Speicherung -------------------------------------------
if uploaded_file or url_input:
    if (
        uploaded_file
        and "last_uploaded" not in st.session_state
        or (
            uploaded_file
            and uploaded_file.name != st.session_state.get("last_uploaded", None)
        )
    ):
        text = extract_text(uploaded_file)
        fields = basic_field_extraction(text)
        save_fields_to_session(fields)
        st.session_state["last_uploaded"] = uploaded_file.name

    if url_input and url_input != st.session_state.get("last_url", ""):
        try:  # pragma: no cover - network
            response = requests.get(url_input, timeout=10)
            response.raise_for_status()
            text = response.text
            fields = basic_field_extraction(text)
            save_fields_to_session(fields)
            st.session_state["last_url"] = url_input
        except Exception as exc:  # pragma: no cover - network
            st.error(f"Fehler beim Laden der URL: {exc}")

# Initialisiere job_fields, falls noch nicht vorhanden
if "job_fields" not in st.session_state:
    st.session_state["job_fields"] = {}

# --- Wizard-Step Navigation ----------------------------------------------
st.sidebar.header("2. Schrittwahl / Choose Step")
wizard_steps = [
    ("Grunddaten / Basic Data", wizard_step_1_basic),
    ("Unternehmen / Company Info", wizard_step_2_company),
    ("Abteilung / Department", wizard_step_3_department),
    ("Rolle / Role", wizard_step_4_role),
    ("Aufgaben / Tasks", wizard_step_5_tasks),
    ("Skills / Kompetenzen", wizard_step_6_skills),
    ("Verg\u00fctung / Compensation", wizard_step_7_compensation),
    ("Recruiting-Prozess / Recruitment", wizard_step_8_recruitment),
]
step_labels = [label for label, _ in wizard_steps]
step_idx = st.sidebar.radio(
    "Schritt ausw\u00e4hlen / Select Step",
    list(range(len(step_labels))),
    format_func=lambda i: step_labels[i],
)

# --- Wizard-Ansicht -------------------------------------------------------
st.title("Recruitment Need Analysis Wizard")
st.info(
    "Alle extrahierten Daten werden bei jedem Schritt als Standardwert vorgeschlagen. / All extracted data will be pre-filled in each step."
)

wizard_steps[step_idx][1]()

# --- Utility-Optionen nach dem Wizard ------------------------------------
st.markdown("---")
st.header("Extras & Export")
st.subheader("1. Editierbare Felder / Editable Fields")
display_fields_editable()
st.subheader("2. Export als Markdown")
export_fields_as_markdown()
st.subheader("3. Mehrzeilige Ansicht (Copy & Paste)")
display_all_fields_multiline_copy()

if st.sidebar.checkbox("Session State anzeigen / Show Session State [DEV]"):
    st.write(st.session_state)
