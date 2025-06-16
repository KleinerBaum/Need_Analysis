# utils_jobinfo.py
"""Utility functions for job data extraction and session management."""

from __future__ import annotations

import base64
import re
from typing import Dict, Optional

from utils.i18n import tr

import docx
import fitz  # PyMuPDF
import streamlit as st


def extract_text_from_pdf(file) -> str:
    """Return plain text from a PDF file."""
    file.seek(0)
    data = file.read()
    doc = fitz.open(stream=data, filetype="pdf")
    return "".join(page.get_text() for page in doc)


def extract_text_from_docx(file) -> str:
    """Return text from a DOCX file including tables."""

    doc = docx.Document(file)
    lines = [para.text for para in doc.paragraphs]

    # Include table cell text (if any). Some job ad templates store
    # important fields like the job title in tables.
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if cell.text:
                    lines.append(cell.text)

    return "\n".join(lines)


def detect_file_type(file) -> Optional[str]:
    """Detect file type based on extension."""
    name = file.name.lower()
    if name.endswith(".pdf"):
        return "pdf"
    if name.endswith(".docx"):
        return "docx"
    if name.endswith(".txt"):
        return "txt"
    return None


def extract_text(file) -> str:
    """Extract content from a supported file."""
    filetype = detect_file_type(file)
    if filetype == "pdf":
        return extract_text_from_pdf(file)
    if filetype == "docx":
        return extract_text_from_docx(file)
    if filetype == "txt":
        return file.read().decode("utf-8")
    raise ValueError("Unsupported file type")


def basic_field_extraction(text: str) -> Dict[str, str]:
    """Naive regex extraction of some fields from raw job text.

    Besides ``job_title`` and ``company_name`` this function tries to detect
    simple skill statements like ``Proficiency in Python and ...``. Detected
    skills are stored comma separated in ``must_have_skills``.
    """

    fields: Dict[str, str] = {}

    job_title = re.search(
        r"(?im)^\s*(Stellenbezeichnung|Jobtitel|Position)\s*[:\-]\s*(.+)$",
        text,
    )
    if job_title:
        fields["job_title"] = job_title.group(2).strip()

    company_name = re.search(
        r"(?im)^\s*(Unternehmen|Company|Firma)\s*[:\-]\s*(.+)$",
        text,
    )
    if company_name:
        fields["company_name"] = company_name.group(2).strip()

    # --- very small skill extraction -------------------------------------
    cleaned_text = re.sub(r"e\.g\.,?", "", text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r"i\.e\.,?", "", cleaned_text, flags=re.IGNORECASE)
    skill_phrases = re.findall(
        r"(?i)(?:proficiency in|experience with|knowledge of|proficient in)\s+(.+?)(?:\.|\n)",
        cleaned_text,
    )
    skills: list[str] = []
    for phrase in skill_phrases:
        clean = re.sub(r"\(e\.g\.,?", "", phrase)
        clean = re.sub(r"[()]", ",", clean)
        clean = re.sub(r"[\.\n]", "", clean)
        clean = re.sub(r"\s+", " ", clean)
        parts = re.split(r",| and | und |&", clean)
        for part in parts:
            part = part.strip()
            if part and part not in skills:
                skills.append(part)
    if skills:
        fields["must_have_skills"] = ", ".join(skills)

    return fields


def save_fields_to_session(fields: Dict[str, str]) -> None:
    """Persist fields in Streamlit session state."""
    st.session_state.setdefault("job_fields", {}).update(fields)


def display_fields_summary() -> None:
    """Show extracted fields as two-line bullet points."""

    fields = st.session_state.get("job_fields", {})
    lang = st.session_state.get("lang", "de")

    st.markdown(tr("### Extrahierte Jobdaten / Extracted Job Info", lang))
    st.markdown("<style>.field-bullet{font-size:16px;}</style>", unsafe_allow_html=True)
    for key, value in fields.items():
        st.markdown(
            f"- **{key.replace('_', ' ').title()}**<br>{value}",
            unsafe_allow_html=True,
        )


def display_fields_editable(prefix: str = "edit_") -> None:
    """Show all stored fields as editable inputs.

    Args:
        prefix: Key prefix to differentiate multiple widget groups.
    """

    fields = st.session_state.get("job_fields", {})
    lang = st.session_state.get("lang", "de")

    # Track used widget keys to avoid StreamlitDuplicateElementKey errors.
    used_keys = st.session_state.setdefault("_used_widget_keys", set())

    st.markdown(tr("### Extrahierte Jobdaten / Extracted Job Info", lang))
    for key, value in fields.items():
        widget_key = f"{prefix}{key}"
        if widget_key in used_keys:
            suffix = 1
            while f"{widget_key}_{suffix}" in used_keys:
                suffix += 1
            widget_key = f"{widget_key}_{suffix}"
        used_keys.add(widget_key)
        st.text_input(key.replace("_", " ").title(), value, key=widget_key)


def export_fields_as_markdown() -> None:
    """Provide a download link for the stored fields as Markdown."""
    fields = st.session_state.get("job_fields", {})
    lang = st.session_state.get("lang", "de")
    md = "\n".join(
        f"**{k.replace('_', ' ').capitalize()}:** {v}" for k, v in fields.items()
    )
    b64 = base64.b64encode(md.encode()).decode()
    href = (
        f'<a href="data:text/markdown;base64,{b64}" download="jobinfo.md">'
        f"{tr('Markdown herunterladen / Download Markdown', lang)}</a>"
    )
    st.markdown(href, unsafe_allow_html=True)


def display_all_fields_multiline_copy() -> None:
    """Show fields as multiline text areas."""
    fields = st.session_state.get("job_fields", {})
    lang = st.session_state.get("lang", "de")
    st.markdown(tr("### Alle Felder / All Fields", lang))
    for key, value in fields.items():
        st.text_area(key.replace("_", " ").title(), value, key=f"multi_{key}")
