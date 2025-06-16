# utils_jobinfo.py
"""Utility functions for job data extraction and session management."""

from __future__ import annotations

import base64
import re
from typing import Dict, Optional

import docx
import fitz  # PyMuPDF
import streamlit as st


def extract_text_from_pdf(file) -> str:
    """Return plain text from a PDF file."""
    doc = fitz.open(stream=file, filetype="pdf")
    return "".join(page.get_text() for page in doc)


def extract_text_from_docx(file) -> str:
    """Return text from a DOCX file."""
    doc = docx.Document(file)
    return "\n".join(para.text for para in doc.paragraphs)


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
    """Naive regex extraction of some fields from text."""
    fields: Dict[str, str] = {}
    job_title = re.search(r"(?i)(Stellenbezeichnung|Jobtitel|Position):?\s*(.+)", text)
    if job_title:
        fields["job_title"] = job_title.group(2).strip()
    company_name = re.search(r"(?i)(Unternehmen|Company|Firma):?\s*(.+)", text)
    if company_name:
        fields["company_name"] = company_name.group(2).strip()
    return fields


def save_fields_to_session(fields: Dict[str, str]) -> None:
    """Persist fields in Streamlit session state."""
    st.session_state.setdefault("job_fields", {}).update(fields)


def display_fields_editable() -> None:
    """Show all stored fields as editable inputs."""
    fields = st.session_state.get("job_fields", {})
    st.markdown("### Extrahierte Jobdaten / Extracted Job Info")
    for key, value in fields.items():
        st.text_input(key.replace("_", " ").title(), value, key=f"edit_{key}")


def export_fields_as_markdown() -> None:
    """Provide a download link for the stored fields as Markdown."""
    fields = st.session_state.get("job_fields", {})
    md = "\n".join(
        f"**{k.replace('_', ' ').capitalize()}:** {v}" for k, v in fields.items()
    )
    b64 = base64.b64encode(md.encode()).decode()
    href = (
        f'<a href="data:text/markdown;base64,{b64}" download="jobinfo.md">'
        "Markdown herunterladen / Download Markdown</a>"
    )
    st.markdown(href, unsafe_allow_html=True)


def display_all_fields_multiline_copy() -> None:
    """Show fields as multiline text areas."""
    fields = st.session_state.get("job_fields", {})
    st.markdown("### Alle Felder / All Fields")
    for key, value in fields.items():
        st.text_area(key.replace("_", " ").title(), value, key=f"multi_{key}")
