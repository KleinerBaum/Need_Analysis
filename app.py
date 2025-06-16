import streamlit as st
from agents.file_agent import extract_text_from_pdf
from functions.field_extraction import extract_job_fields
from functions.boolean_search import generate_boolean_search

st.set_page_config(page_title="Vacalyser FC2 Demo", layout="wide")
st.title("📄 Vacalyser – Function Calling Demo (Option 1+2)")

# Mode-Auswahl: Option 1 oder 2
mode = st.radio(
    "Extraction Mode",
    options=["Function Calling (ChatCompletion)", "Responses API (Tool Loop)"],
    index=0,
    help="Option 1: Direktes Function Calling / Option 2: Responses API Tool Loop",
)

uploaded_file = st.file_uploader("Upload Job Ad (PDF)", type=["pdf"])
language = st.selectbox("Sprache der Anzeige", ["de", "en"], index=0)

if uploaded_file:
    st.subheader("📃 Extracted Text")
    text = extract_text_from_pdf(uploaded_file)
    st.text_area("Raw Text", text, height=300)

    st.subheader("🧠 Structured Job Fields")
    with st.spinner("Extrahiere strukturierte Daten ..."):
        extracted = extract_job_fields(text, language, mode)
    st.json(extracted)

    st.subheader("🔍 Boolean Search String")
    boolean_string = generate_boolean_search(extracted)
    st.code(boolean_string, language="text")
