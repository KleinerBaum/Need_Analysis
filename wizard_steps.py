"""Streamlit wizard steps for job data collection."""

from __future__ import annotations

import requests
import streamlit as st

from utils.utils_jobinfo import (
    basic_field_extraction,
    display_fields_editable,
    extract_text,
    save_fields_to_session,
)


def wizard_step_1_basic() -> None:
    """Step 1: capture basic job data."""
    st.header("1. Grunddaten / Basic Data")
    st.subheader(
        "Das Tool hilft Linemanagern, Informationsverluste im Recruiting zu vermeiden "
        "und den besten Kandidaten langfristig zu binden."
    )
    fields = st.session_state.get("job_fields", {})
    job_title = st.text_input("Jobtitel / Job Title *", fields.get("job_title", ""))
    url = st.text_input("Job Ad URL", fields.get("job_url", ""))
    uploaded = st.file_uploader("Job Ad File", type=["pdf", "docx", "txt"])

    text = ""
    if uploaded is not None:
        text = extract_text(uploaded)
    elif url:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            text = response.text
        except Exception as exc:  # pragma: no cover - network
            st.error(f"Fehler beim Laden der URL: {exc}")

    if text:
        extracted = basic_field_extraction(text)
        save_fields_to_session(extracted)
        display_fields_editable()

    if not job_title:
        st.warning("Bitte Jobtitel eingeben. / Please enter job title.")

    fields["job_title"] = job_title
    fields["job_url"] = url
    st.session_state["job_fields"] = fields


def wizard_step_2_company() -> None:
    """Step 2: company information."""
    fields = st.session_state.get("job_fields", {})
    st.header(f"2. Unternehmensdaten / Company Info – {fields.get('company_name', '')}")
    st.subheader(
        "Transparente Unternehmensinfos erleichtern Kandidaten die Entscheidung."
    )
    display_fields_editable()
    fields["company_name"] = st.text_input(
        "Unternehmen / Company Name *", fields.get("company_name", "")
    )
    fields["city"] = st.text_input("Stadt / City *", fields.get("city", ""))
    with st.expander("Weitere Angaben / More"):
        fields["headquarters_location"] = st.text_input(
            "Hauptsitz / Headquarters Location", fields.get("headquarters_location", "")
        )
        fields["company_website"] = st.text_input(
            "Unternehmenswebsite / Company Website", fields.get("company_website", "")
        )
    st.session_state["job_fields"] = fields


def wizard_step_3_department() -> None:
    """Step 3: department and team."""
    fields = st.session_state.get("job_fields", {})
    st.header("3. Abteilung & Team / Department and Team Info")
    display_fields_editable()
    with st.expander("Team/Abteilung (optional)"):
        fields["brand_name"] = st.text_input("Markenname / Brand Name", fields.get("brand_name", ""))
        fields["team_structure"] = st.text_area(
            "Teamstruktur / Team Structure", fields.get("team_structure", "")
        )
    st.session_state["job_fields"] = fields


def wizard_step_4_role() -> None:
    """Step 4: role definition."""
    fields = st.session_state.get("job_fields", {})
    st.header("4. Rollen-Definition / Role Definition")
    display_fields_editable()
    fields["job_type"] = st.selectbox(
        "Jobart / Job Type *",
        ["Vollzeit / Full-Time", "Teilzeit / Part-Time", "Praktikum / Internship", "Freelance"],
        index=0,
    )
    fields["contract_type"] = st.selectbox(
        "Vertragstyp / Contract Type *",
        ["Unbefristet / Permanent", "Befristet / Fixed-term", "Werkvertrag / Contract for Work"],
        index=0,
    )
    fields["job_level"] = st.selectbox(
        "Karrierelevel / Job Level *",
        ["Junior", "Mid", "Senior", "Lead", "Management"],
        index=0,
    )
    fields["role_description"] = st.text_area(
        "Rollenbeschreibung / Role Description *", fields.get("role_description", "")
    )
    fields["role_type"] = st.text_input("Rollentyp / Role Type *", fields.get("role_type", ""))
    with st.expander("Weitere Optionen / More Options"):
        fields["date_of_employment_start"] = st.date_input(
            "Startdatum / Start Date", fields.get("date_of_employment_start", None)
        )
        fields["role_performance_metrics"] = st.text_area(
            "Leistungskennzahlen / Performance Metrics", fields.get("role_performance_metrics", "")
        )
        fields["role_priority_projects"] = st.text_area(
            "Prioritätsprojekte / Priority Projects", fields.get("role_priority_projects", "")
        )
        fields["travel_requirements"] = st.text_input(
            "Reisebereitschaft / Travel Requirements", fields.get("travel_requirements", "")
        )
        fields["work_schedule"] = st.text_input(
            "Arbeitszeiten / Work Schedule", fields.get("work_schedule", "")
        )
        fields["role_keywords"] = st.text_input(
            "Schlüsselwörter / Role Keywords", fields.get("role_keywords", "")
        )
        fields["decision_making_authority"] = st.text_input(
            "Entscheidungskompetenz / Decision Making Authority", fields.get("decision_making_authority", "")
        )
    with st.expander("Fortgeschritten / Advanced", expanded=False):
        fields["reports_to"] = st.text_input("Berichtet an / Reports To", fields.get("reports_to", ""))
        fields["supervises"] = st.text_input("Führungsspanne / Supervises", fields.get("supervises", ""))
    st.session_state["job_fields"] = fields


def wizard_step_5_tasks() -> None:
    """Step 5: tasks and responsibilities."""
    fields = st.session_state.get("job_fields", {})
    st.header("5. Aufgaben & Verantwortlichkeiten / Tasks & Responsibilities")
    display_fields_editable()
    fields["task_list"] = st.text_area("Aufgabenliste / Task List *", fields.get("task_list", ""))
    with st.expander("Weitere Aufgaben / More Tasks"):
        fields["key_responsibilities"] = st.text_area(
            "Hauptverantwortlichkeiten / Key Responsibilities", fields.get("key_responsibilities", "")
        )
        fields["technical_tasks"] = st.text_area(
            "Technische Aufgaben / Technical Tasks", fields.get("technical_tasks", "")
        )
        fields["managerial_tasks"] = st.text_area(
            "Managementaufgaben / Managerial Tasks", fields.get("managerial_tasks", "")
        )
        fields["administrative_tasks"] = st.text_area(
            "Administrative Aufgaben / Administrative Tasks", fields.get("administrative_tasks", "")
        )
        fields["customer_facing_tasks"] = st.text_area(
            "Kundenkontakt / Customer Facing Tasks", fields.get("customer_facing_tasks", "")
        )
        fields["internal_reporting_tasks"] = st.text_area(
            "Reporting intern / Internal Reporting Tasks", fields.get("internal_reporting_tasks", "")
        )
        fields["performance_tasks"] = st.text_area(
            "Performance-Aufgaben / Performance Tasks", fields.get("performance_tasks", "")
        )
        fields["innovation_tasks"] = st.text_area(
            "Innovationsaufgaben / Innovation Tasks", fields.get("innovation_tasks", "")
        )
        fields["task_prioritization"] = st.text_area(
            "Aufgabenpriorisierung / Task Prioritization", fields.get("task_prioritization", "")
        )
    st.session_state["job_fields"] = fields


def wizard_step_6_skills() -> None:
    """Step 6: required skills."""
    fields = st.session_state.get("job_fields", {})
    st.header("6. Skills & Kompetenzen / Skills & Competencies")
    display_fields_editable()
    fields["must_have_skills"] = st.text_area("Must-have Skills *", fields.get("must_have_skills", ""))
    with st.expander("Weitere Skills / More Skills"):
        fields["hard_skills"] = st.text_area("Hard Skills", fields.get("hard_skills", ""))
        fields["soft_skills"] = st.text_area("Soft Skills", fields.get("soft_skills", ""))
        fields["nice_to_have_skills"] = st.text_area(
            "Nice-to-have Skills", fields.get("nice_to_have_skills", "")
        )
        fields["certifications_required"] = st.text_area(
            "Zertifikate / Certifications Required", fields.get("certifications_required", "")
        )
        fields["language_requirements"] = st.text_area(
            "Sprachkenntnisse / Language Requirements", fields.get("language_requirements", "")
        )
        fields["tool_proficiency"] = st.text_area("Toolkenntnisse / Tool Proficiency", fields.get("tool_proficiency", ""))
        fields["technical_stack"] = st.text_area("Technischer Stack / Technical Stack", fields.get("technical_stack", ""))
        fields["domain_expertise"] = st.text_area("Fachexpertise / Domain Expertise", fields.get("domain_expertise", ""))
        fields["leadership_competencies"] = st.text_area(
            "Leadership-Kompetenzen / Leadership Competencies", fields.get("leadership_competencies", "")
        )
        fields["industry_experience"] = st.text_area(
            "Branchenerfahrung / Industry Experience", fields.get("industry_experience", "")
        )
        fields["analytical_skills"] = st.text_area(
            "Analytische Fähigkeiten / Analytical Skills", fields.get("analytical_skills", "")
        )
        fields["communication_skills"] = st.text_area(
            "Kommunikationsfähigkeiten / Communication Skills", fields.get("communication_skills", "")
        )
        fields["project_management_skills"] = st.text_area(
            "Projektmanagement / Project Management Skills", fields.get("project_management_skills", "")
        )
        fields["soft_requirement_details"] = st.text_area(
            "Details zu Soft Requirements", fields.get("soft_requirement_details", "")
        )
        fields["visa_sponsorship"] = st.text_input("Visa Sponsorship", fields.get("visa_sponsorship", ""))
    st.session_state["job_fields"] = fields


def wizard_step_7_compensation() -> None:
    """Step 7: compensation and benefits."""
    fields = st.session_state.get("job_fields", {})
    st.header("7. Vergütung & Benefits / Compensation & Benefits")
    display_fields_editable()
    fields["salary_range"] = st.text_input("Gehaltsrange / Salary Range *", fields.get("salary_range", ""))
    fields["currency"] = st.selectbox("Währung / Currency *", ["EUR", "CHF", "GBP", "USD", "other"], index=0)
    fields["pay_frequency"] = st.selectbox(
        "Auszahlungsrhythmus / Pay Frequency *",
        ["Monatlich / Monthly", "Jährlich / Annually", "Wöchentlich / Weekly"],
        index=0,
    )
    with st.expander("Weitere Benefits / More Benefits"):
        fields["bonus_scheme"] = st.text_area("Bonusregelung / Bonus Scheme", fields.get("bonus_scheme", ""))
        fields["commission_structure"] = st.text_area(
            "Provisionsmodell / Commission Structure", fields.get("commission_structure", "")
        )
        fields["vacation_days"] = st.text_input("Urlaubstage / Vacation Days", fields.get("vacation_days", ""))
        fields["remote_work_policy"] = st.text_area("Remote-Regelung / Remote Work Policy", fields.get("remote_work_policy", ""))
        fields["flexible_hours"] = st.text_input("Flexible Arbeitszeiten / Flexible Hours", fields.get("flexible_hours", ""))
        fields["relocation_assistance"] = st.text_area("Umzugshilfe / Relocation Assistance", fields.get("relocation_assistance", ""))
        fields["childcare_support"] = st.text_area("Kinderbetreuung / Childcare Support", fields.get("childcare_support", ""))
    st.session_state["job_fields"] = fields


def wizard_step_8_recruitment() -> None:
    """Step 8: recruitment process."""
    fields = st.session_state.get("job_fields", {})
    st.header("8. Bewerbungsprozess / Recruitment Process")
    display_fields_editable()
    fields["recruitment_contact_email"] = st.text_input(
        "Recruiting-Kontakt E-Mail * / Contact Email *", fields.get("recruitment_contact_email", "")
    )
    with st.expander("Weitere Angaben / More Options"):
        fields["recruitment_steps"] = st.text_area(
            "Prozessschritte / Recruitment Steps", fields.get("recruitment_steps", "")
        )
        fields["recruitment_timeline"] = st.text_input(
            "Zeitleiste / Recruitment Timeline", fields.get("recruitment_timeline", "")
        )
        fields["number_of_interviews"] = st.text_input(
            "Anzahl Interviews / Number of Interviews", fields.get("number_of_interviews", "")
        )
        fields["interview_format"] = st.text_input("Interviewformat / Interview Format", fields.get("interview_format", ""))
        fields["assessment_tests"] = st.text_area("Assessment-Tests", fields.get("assessment_tests", ""))
        fields["onboarding_process_overview"] = st.text_area(
            "Onboarding-Prozess / Onboarding Process", fields.get("onboarding_process_overview", "")
        )
        fields["recruitment_contact_phone"] = st.text_input(
            "Telefon Recruiting-Kontakt / Contact Phone", fields.get("recruitment_contact_phone", "")
        )
        fields["application_instructions"] = st.text_area(
            "Bewerbungsanweisungen / Application Instructions", fields.get("application_instructions", "")
        )
    st.session_state["job_fields"] = fields
