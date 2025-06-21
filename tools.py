import streamlit as st
import openai
from field_map import FIELD_MAP
import re
import requests
import docx
from PyPDF2 import PdfReader

def collect_fields(keys=None):
    if keys is None:
        keys = [f["key"] for f in FIELD_MAP]
    return {key: st.session_state.get(key, "") for key in keys}

def show_adjustable_output(
    output,
    regen_prompt_func,
    extra_context=None,
    output_label="Output",
    prompt_instruction="Add your feedback or edit below and regenerate:"
):
    st.markdown(f"#### {output_label}")
    adjusted = st.text_area("Edit directly", value=output, height=300, key="edit_"+output_label)
    feedback = st.text_area(
        "Feedback (add info, rephrase, change style, ...)",
        placeholder="E.g., make shorter, add more about remote work...",
        key="feedback_"+output_label
    )
    if st.button("Regenerate", key="regen_"+output_label):
        prompt = regen_prompt_func(adjusted, feedback, extra_context)
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        st.markdown("#### Adjusted Output")
        st.markdown(response.choices[0].message.content.strip())
    st.caption("Edit the text or provide feedback, then regenerate.")

def jobad_regen_prompt(adjusted, feedback, data):
    return f"""Rewrite the following job ad with these user requests:\n\n{feedback}\n\nHere is the latest user-edited text:\n{adjusted}\n\nOriginal vacancy context (for reference):\n{data}\nReturn Markdown only."""

def generate_job_ad():
    keys = [
        "job_title", "role_purpose", "employment_type", "seniority_level", "company_name", "company_size", "industry",
        "work_location_city", "department_name", "primary_responsibilities", "hard_skills", "soft_skills",
        "salary_currency", "salary_range_min", "salary_range_max", "recruiter_email"
    ]
    data = collect_fields(keys)
    prompt = f"""
Write a concise, attractive job ad (Markdown) for the following vacancy. Use job title, role, skills, salary, location, company and recruiter contact.
{data}
"""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    jobad = response.choices[0].message.content.strip()
    show_adjustable_output(jobad, jobad_regen_prompt, extra_context=data, output_label="Job Ad")

def boolean_regen_prompt(adjusted, feedback, data):
    return f"""Rewrite this Boolean search string for the job, using user feedback:\n{feedback}\nUser's adjusted search:\n{adjusted}\nOriginal context:\n{data}\nReturn only the search string."""

def generate_boolean_search():
    keys = ["job_title", "hard_skills", "work_location_city", "industry"]
    data = collect_fields(keys)
    prompt = f"""
As a sourcing expert, write an advanced Boolean search string for this role, with title, must-have skills, city, and industry. Output only the search string.
{data}
"""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    search = response.choices[0].message.content.strip()
    show_adjustable_output(search, boolean_regen_prompt, extra_context=data, output_label="Boolean String")

def interview_regen_prompt(adjusted, feedback, data):
    return f"""Rewrite this interview sheet with user feedback:\n{feedback}\nUser's adjusted text:\n{adjusted}\nContext:\n{data}\nMarkdown only."""

def generate_interview_prep_sheet():
    keys = ["job_title", "hard_skills", "soft_skills", "primary_responsibilities", "company_name", "department_name"]
    data = collect_fields(keys)
    prompt = f"""
Create a line manager/HR interview prep sheet (Markdown) for this role, including suggested questions for all must-have skills.
{data}
"""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    sheet = response.choices[0].message.content.strip()
    show_adjustable_output(sheet, interview_regen_prompt, extra_context=data, output_label="Interview Prep Sheet")

def email_regen_prompt(adjusted, feedback, data):
    return f"""Rewrite this recruiting email with user feedback:\n{feedback}\nAdjusted text:\n{adjusted}\nContext:\n{data}\nOutput only the email."""

def draft_contact_email():
    contact_target = st.selectbox("Contact Target", ["Candidate", "Line Manager", "HR", "Finance"])
    keys = ["job_title", "company_name", "department_name", "recruiter_email"]
    data = collect_fields(keys)
    prompt = f"""
Draft a businesslike email for the {contact_target} about this vacancy: {data}. Subject and signature included. Use recruiter email if present.
"""
    if st.button("Generate Email"):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        email = response.choices[0].message.content.strip()
        show_adjustable_output(email, email_regen_prompt, extra_context=data, output_label="Contact Email")

def persona_regen_prompt(adjusted, feedback, data):
    return f"""Rewrite this candidate persona with feedback:\n{feedback}\nUser-edited version:\n{adjusted}\nContext:\n{data}\nMarkdown only."""

def generate_candidate_persona():
    keys = ["job_title", "hard_skills", "soft_skills", "company_name", "industry"]
    data = collect_fields(keys)
    prompt = f"""
Write a short, vivid candidate persona for this vacancy, summarizing background, motivators, where to source, what attracts.
{data}
"""
    if st.button("Generate Persona"):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        persona = response.choices[0].message.content.strip()
        show_adjustable_output(persona, persona_regen_prompt, extra_context=data, output_label="Candidate Persona")

def export_vacancy_markdown():
    if st.button("Export Vacancy Profile as Markdown"):
        data = collect_fields()
        prompt = f"""
Write a Markdown vacancy profile for documentation or sharing, using all available fields:\n{data}
"""
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        md = response.choices[0].message.content.strip()
        st.download_button("Download Markdown", md, file_name="vacancy_profile.md")

# extractors


# ---------- PDF & DOCX TEXT EXTRACTORS ----------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_text_from_url(url):
    r = requests.get(url)
    return r.text  # For advanced use, use readability-lxml to grab only article body.

# ---------- REGEX PATTERNS ----------
# Tweak/add per field and target language/format
REGEX_PATTERNS = {
    "job_title":  r"(?:Job\s*Title|Position)\s*:?\s*(?P<job_title>[^\n,]+)",
    "company_name": r"(?:Company|Employer)\s*:?\s*(?P<company_name>[^\n,]+)",
    "work_location_city": r"(?:Location|Work City|Ort)\s*:?\s*(?P<work_location_city>[^\n,]+)",
    "employment_type": r"(?:Employment Type|Vertragsart)\s*:?\s*(?P<employment_type>Permanent|Fixed-term|Internship|Freelance|Working Student)",
    "seniority_level": r"(?:Seniority Level|Karrierelevel)\s*:?\s*(?P<seniority_level>Intern|Junior|Mid|Senior|Lead|Head|Director)",
    "salary_range_min": r"(?:Salary|Gehalt|Vergütung)[^\d]*(?P<salary_range_min>\d{4,6})\s*(?:-|to|–)\s*\d{4,6}",
    "salary_range_max": r"(?:Salary|Gehalt|Vergütung)[^\d]*\d{4,6}\s*(?:-|to|–)\s*(?P<salary_range_max>\d{4,6})",
    "languages_required": r"(?:Languages Required|Sprachen)[^\n:]*:\s*(?P<languages_required>.+)",
    "application_deadline": r"(?:Application Deadline|Bewerbungsfrist)[^\n:]*:\s*(?P<application_deadline>[^\n,]+)",
    # Add more per FIELD_MAP!
}

def extract_with_regex(text):
    result = {}
    for key, pattern in REGEX_PATTERNS.items():
        m = re.search(pattern, text, re.IGNORECASE)
        if m and m.group(key):
            val = m.group(key).strip()
            if key == "languages_required":
                val = [lang.strip() for lang in re.split(",|/|und|and", val)]
            result[key] = val
    return result

# ---------- AI Fallback ----------
def ai_extract_fields(text, field_map):
    # Prepare extraction schema for GPT
    fields = "\n".join(f"- {f['label']} ({f['key']})" for f in field_map)
    prompt = f"""Extract the following fields from this job ad (if not present, leave empty):
{fields}

Return a valid JSON object with each key. 
Job Ad:
{text}
"""
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    import json
    raw = response.choices[0].message.content.strip()
    # Remove code block if needed
    if raw.startswith("```"):
        raw = raw.strip("```").strip("json").strip()
    try:
        return json.loads(raw)
    except Exception:
        return {}

def extract_all_fields(text, field_map):
    regex_data = extract_with_regex(text)
    # Only extract via AI for missing/ambiguous fields
    missing_keys = [f["key"] for f in field_map if f["key"] not in regex_data]
    if missing_keys:
        ai_data = ai_extract_fields(text, [f for f in field_map if f["key"] in missing_keys])
        regex_data.update(ai_data)
    return regex_data

# ----------- PRO-TIPS -----------
# - Regex is best for highly structured data (headline: Job Title, etc.).
# - Always sanitize PDF/DOCX/HTML to pure text before extraction.
# - Provide clear mapping in prompt for GPT.
# - Present the extraction results for user correction (no blind autofill!).
