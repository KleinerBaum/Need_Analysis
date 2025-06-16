"""Utilities for working with uploaded files."""

from __future__ import annotations

from typing import BinaryIO

import fitz  # PyMuPDF


def extract_text_from_pdf(uploaded_file: BinaryIO) -> str:
    """Return plain text from a PDF file.

    The uploaded file pointer is reset before reading to ensure the entire
    document is processed. All page texts are concatenated using newlines.

    Args:
        uploaded_file: File-like object containing the PDF data.

    Returns:
        Extracted text content from the PDF.
    """

    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)
