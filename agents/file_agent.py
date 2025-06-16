import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    # Reset file pointer (important for Streamlit)
    uploaded_file.seek(0)
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    return "\n".join([page.get_text() for page in doc])
