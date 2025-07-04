# utils/field_map.py
from enum import Enum

class WizardStep(Enum):
    BASIC_DATA = 1
    COMPANY_INFO = 2
    DEPARTMENT_TEAM_INFO = 3
    ROLE_DEFINITION = 4
    TASKS_RESPONSIBILITIES = 5
    SKILLS_COMPETENCIES = 6
    COMPENSATION_BENEFITS = 7
    RECRUITMENT_PROCESS = 8
    LANGUAGE_PUBLICATION = 9
# Unified field definitions for Vacalyser wizard
field_map = {
    # Step 1: Basic Data
    "job_title": {
        "step": 1,
        "widget": "text_input",
        "label": "Stellentitel / Job Title",
        "help": "Official role title for the position.",
        "required": True,
        "source": "extracted"  # Often auto-detected from JD text
    },
    "input_url": {
        "step": 1,
        "widget": "text_input",
        "label": "JD-URL / Job Description URL",
        "help": "Optional URL of an online job description to import.",
        "required": False,
        "source": "user"
    },
    "uploaded_file": {
        "step": 1,
        "widget": "file_uploader",
        "label": "Stellenbeschreibung hochladen / Upload Job Description",
        "help": "Upload a PDF or DOCX of the job description for AI extraction.",
        "required": False,
        "source": "user"
    },
    # (parsed_data_raw is internal storage for extracted text; not an input field)

    # Step 2: Company Info
    "company_name": {
        "step": 2,
        "widget": "text_input",
        "label": "Unternehmensname / Company Name",
        "help": "Name of the hiring company/organization.",
        "required": True,
        "source": "extracted"
    },
    "city": {
        "step": 2,
        "widget": "text_input",
        "label": "Standort (Stadt) / Job Location (City)",
        "help": "Primary city or location for the job (leave blank if remote).",
        "required": True,
        "source": "extracted"
    },
    "headquarters_location": {
        "step": 2,
        "widget": "text_input",
        "label": "Hauptsitz / Headquarters Location",
        "help": "Company headquarters (if different from job location).",
        "required": False,
        "source": "extracted"
    },
    "company_website": {
        "step": 2,
        "widget": "text_input",
        "label": "Webseite / Company Website",
        "help": "Official website of the company (for reference or display).",
        "required": False,
        "source": "user"
    },

    # Step 3: Department and Team Info
    "brand_name": {
        "step": 3,
        "widget": "text_input",
        "label": "Marke/Abteilung / Brand or Department",
        "help": "Specific brand, division, or department (if applicable).",
        "required": False,
        "source": "user"
    },
    "team_structure": {
        "step": 3,
        "widget": "text_area",
        "label": "Team & Struktur / Team Structure",
        "help": "Brief description of the team and its structure (who the role reports to, team size, etc.).",
        "required": False,
        "source": "user"
    },

    # Step 4: Role Definition
    "date_of_employment_start": {
        "step": 4,
        "widget": "date_input",
        "label": "Startdatum / Start Date",
        "help": "Planned start date of employment.",
        "required": False,
        "source": "extracted"
    },
    "job_type": {
        "step": 4,
        "widget": "selectbox",
        "label": "Beschäftigungsart / Employment Type",
        "options": ["Vollzeit (Full-time)", "Teilzeit (Part-time)", "Freelance", "Werkstudent (Working Student)"],
        "help": "Type of employment in terms of hours or commitment.",
        "required": True,
        "source": "extracted"
    },
    "contract_type": {
        "step": 4,
        "widget": "selectbox",
        "label": "Vertragsart / Contract Type",
        "options": ["Unbefristet (Permanent)", "Befristet (Temporary)", "Praktikum (Internship)", "Freier Mitarbeiter (Contract)"],
        "help": "Type of contract for the role.",
        "required": True,
        "source": "extracted"
    },
    "job_level": {
        "step": 4,
        "widget": "selectbox",
        "label": "Karrierestufe / Seniority Level",
        "options": ["Einsteiger (Entry)", "Junior", "Mid-Level", "Senior", "Lead", "Direktor (Director)"],
        "help": "Seniority or career level required for the role.",
        "required": True,
        "source": "extracted"
    },
    "role_description": {
        "step": 4,
        "widget": "text_area",
        "label": "Rollenbeschreibung / Role Description",
        "help": "Overview paragraph describing the role's purpose and impact.",
        "required": True,
        "source": "llm"  # Can be AI-generated summary of the role
    },
    "role_type": {
        "step": 4,
        "widget": "multiselect",
        "label": "Rollentyp / Role Type",
        "options": ["Technisch (Technical)", "Führungsposition (Managerial)", "Administrativ (Administrative)"],
        "help": "Nature of the role (select one or multiple categories).",
        "required": True,
        "source": "extracted"
    },
    "reports_to": {
        "step": 4,
        "widget": "text_input",
        "label": "Berichtet an / Reports To",
        "help": "The position or person this role reports to (e.g. Manager or Team Lead).",
        "required": False,
        "source": "user"
    },
    "supervises": {
        "step": 4,
        "widget": "text_input",
        "label": "Führt Aufsicht über / Supervises",
        "help": "If a managerial role, list positions or team this role oversees.",
        "required": False,
        "source": "user"
    },
    # (Additional optional fields like performance metrics, priority projects, travel_requirements, etc. can be included here as needed.)

    # Step 5: Tasks & Responsibilities
    "task_list": {
        "step": 5,
        "widget": "text_area",
        "label": "Aufgaben / Task List",
        "help": "List of main tasks and responsibilities (bullet points).",
        "required": True,
        "source": "extracted"
    },
    "key_responsibilities": {
        "step": 5,
        "widget": "text_area",
        "label": "Kernverantwortungen / Key Responsibilities",
        "help": "Key high-level responsibilities (if not evident from task list).",
        "required": False,
        "source": "user"
    },
    "technical_tasks": {
        "step": 5,
        "widget": "text_area",
        "label": "Technische Aufgaben / Technical Tasks",
        "help": "Specific technical duties (if applicable to the role).",
        "required": False,
        "source": "user"
    },
    "managerial_tasks": {
        "step": 5,
        "widget": "text_area",
        "label": "Leitungsaufgaben / Managerial Tasks",
        "help": "Managerial or leadership duties (for managerial roles).",
        "required": False,
        "source": "user"
    },
    "administrative_tasks": {
        "step": 5,
        "widget": "text_area",
        "label": "Administrative Aufgaben / Administrative Tasks",
        "help": "Administrative or support tasks (if applicable).",
        "required": False,
        "source": "user"
    },

    # Step 6: Skills & Competencies
    "must_have_skills": {
        "step": 6,
        "widget": "text_area",
        "label": "Erforderliche Fähigkeiten / Must-have Skills",
        "help": "Essential skills and qualifications candidates must possess.",
        "required": True,
        "source": "extracted"
    },
    "hard_skills": {
        "step": 6,
        "widget": "text_area",
        "label": "Fachliche Skills / Hard Skills",
        "help": "Technical or domain-specific skills required.",
        "required": False,
        "source": "user"
    },
    "soft_skills": {
        "step": 6,
        "widget": "text_area",
        "label": "Soft Skills",
        "help": "Soft skills or personal competencies needed (communication, teamwork, etc.).",
        "required": False,
        "source": "user"
    },
    "nice_to_have_skills": {
        "step": 6,
        "widget": "text_area",
        "label": "Pluspunkte / Nice-to-have Skills",
        "help": "Additional skills or experience that are beneficial but not mandatory.",
        "required": False,
        "source": "user"
    },
    "certifications_required": {
        "step": 6,
        "widget": "text_input",
        "label": "Zertifikate / Required Certifications",
        "help": "Professional certifications or licenses required (if any).",
        "required": False,
        "source": "user"
    },
    "language_requirements": {
        "step": 6,
        "widget": "text_input",
        "label": "Sprachkenntnisse / Language Requirements",
        "help": "Required language proficiencies for candidates (if any).",
        "required": False,
        "source": "user"
    },
    "tool_proficiency": {
        "step": 6,
        "widget": "text_input",
        "label": "Toolkenntnisse / Tool Proficiency",
        "help": "Software or tool proficiencies needed (e.g. Excel, SAP, programming languages).",
        "required": False,
        "source": "user"
    },
    "technical_stack": {
        "step": 6,
        "widget": "text_input",
        "label": "Tech-Stack / Technical Stack",
        "help": "Technologies and frameworks used (for tech roles, e.g. AWS, React, etc.).",
        "required": False,
        "source": "user"
    },

    # Step 7: Compensation & Benefits
    "salary_range": {
        "step": 7,
        "widget": "text_input",
        "label": "Gehaltsspanne / Salary Range",
        "help": "Expected salary range for the position (e.g. 50-60k).",
        "required": True,
        "source": "user"
    },
    "currency": {
        "step": 7,
        "widget": "selectbox",
        "label": "Währung / Currency",
        "options": ["EUR", "USD", "GBP", "CHF", "Other"],
        "help": "Currency of the salary (Euro, USD, etc.).",
        "required": True,
        "source": "user"
    },
    "pay_frequency": {
        "step": 7,
        "widget": "selectbox",
        "label": "Zahlungsfrequenz / Pay Frequency",
        "options": ["Jährlich (Yearly)", "Monatlich (Monthly)", "Stündlich (Hourly)"],
        "help": "Frequency of pay (annual salary, monthly, hourly rate, etc.).",
        "required": True,
        "source": "user"
    },
    "bonus_scheme": {
        "step": 7,
        "widget": "text_input",
        "label": "Bonusregelung / Bonus Scheme",
        "help": "Description of any bonus or incentive scheme (if applicable).",
        "required": False,
        "source": "user"
    },
    "commission_structure": {
        "step": 7,
        "widget": "text_input",
        "label": "Provision / Commission Structure",
        "help": "Details of commission (for sales roles, if applicable).",
        "required": False,
        "source": "user"
    },
    "vacation_days": {
        "step": 7,
        "widget": "number_input",
        "label": "Urlaubstage / Vacation Days",
        "help": "Number of annual vacation days offered.",
        "required": False,
        "source": "user"
    },
    "remote_work_policy": {
        "step": 7,
        "widget": "selectbox",
        "label": "Home-Office Möglichkeit / Remote Work",
        "options": ["Keine / None", "Teilweise remote / Hybrid", "Vollständig remote / Fully Remote"],
        "help": "Remote work options or policy (none, hybrid, or fully remote).",
        "required": False,
        "source": "user"
    },
    "flexible_hours": {
        "step": 7,
        "widget": "checkbox",
        "label": "Gleitzeit / Flexible Hours",
        "help": "Check if flexible working hours are offered.",
        "required": False,
        "source": "user"
    },
    "relocation_assistance": {
        "step": 7,
        "widget": "checkbox",
        "label": "Umzugsunterstützung / Relocation Assistance",
        "help": "Check if relocation support is provided for candidates.",
        "required": False,
        "source": "user"
    },
    "childcare_support": {
        "step": 7,
        "widget": "checkbox",
        "label": "Kinderbetreuung / Childcare Support",
        "help": "Check if childcare or family support benefits are offered.",
        "required": False,
        "source": "user"
    },

    # Step 8: Recruitment Process
    "recruitment_contact_email": {
        "step": 8,
        "widget": "text_input",
        "label": "Kontakt E-Mail / Contact Email",
        "help": "Email address for applications or inquiries.",
        "required": True,
        "source": "user"
    },
    "recruitment_steps": {
        "step": 8,
        "widget": "text_area",
        "label": "Bewerbungsprozess / Recruitment Steps",
        "help": "Outline of the recruitment process (interviews, tests, etc.).",
        "required": False,
        "source": "user"
    },
    "recruitment_timeline": {
        "step": 8,
        "widget": "text_input",
        "label": "Einstellungszeitplan / Timeline",
        "help": "Estimated timeline for the hiring process (e.g. 4 weeks).",
        "required": False,
        "source": "user"
    },
    "number_of_interviews": {
        "step": 8,
        "widget": "number_input",
        "label": "Anzahl Interviews / Number of Interviews",
        "help": "How many interview rounds are planned (if known).",
        "required": False,
        "source": "user"
    },
    "interview_format": {
        "step": 8,
        "widget": "text_input",
        "label": "Interviewformat / Interview Format",
        "help": "Format of interviews (phone, video, on-site, etc.).",
        "required": False,
        "source": "user"
    },
    "assessment_tests": {
        "step": 8,
        "widget": "text_input",
        "label": "Tests / Assessment Tests",
        "help": "Any assessment or coding tests involved in hiring.",
        "required": False,
        "source": "user"
    },
    "onboarding_process_overview": {
        "step": 8,
        "widget": "text_area",
        "label": "Onboarding / Onboarding Process",
        "help": "Brief overview of the onboarding process for the new hire.",
        "required": False,
        "source": "user"
    },
    "recruitment_contact_phone": {
        "step": 8,
        "widget": "text_input",
        "label": "Kontakt Telefon / Contact Phone",
        "help": "Contact phone number for queries (optional).",
        "required": False,
        "source": "user"
    },
    "application_instructions": {
        "step": 8,
        "widget": "text_area",
        "label": "Bewerbungshinweise / Application Instructions",
        "help": "Specific instructions on how to apply (e.g. apply via company portal).",
        "required": False,
        "source": "user"
    },

    # Step 9: Language & Publication
    "language_of_ad": {
        "step": 9,
        "widget": "selectbox",
        "label": "Anzeigesprache / Advertisement Language",
        "options": ["Deutsch", "English"],
        "help": "Language of the job ad content to finalize.",
        "required": True,
        "source": "user"
    },
    "translation_required": {
        "step": 9,
        "widget": "checkbox",
        "label": "Übersetzung benötigt? / Translation needed?",
        "help": "Check if the job ad needs to be translated to another language.",
        "required": False,
        "source": "user"
    },
    "desired_publication_channels": {
        "step": 9,
        "widget": "multiselect",
        "label": "Veröffentlichungskanäle / Publication Channels",
        "options": ["LinkedIn", "Indeed", "Company Website", "Internal Portal", "Others"],
        "help": "Where the job ad will be published (for planning purposes).",
        "required": False,
        "source": "user"
    }
}


def get_fields_by_group(step: WizardStep, prio_max: int = None):
    """
    Gruppiert die Felder eines WizardSteps (optional gefiltert nach Priorität).

    Hinweis: Aktuell ist keine Priorität im field_map definiert.
    Falls du Prioritäten nutzt, ergänze das Attribut 'prio' in field_map.
    """
    fields = {name: meta for name, meta in field_map.items() if meta["step"] == step}

    if prio_max is not None:
        fields = {
            name: meta for name, meta in fields.items()
            if meta.get("prio", prio_max) <= prio_max
        }

    return fields
    
# Helper: get all fields for a given step
def get_fields_for_step(step_number: int):
    return [name for name, meta in field_map.items() if meta["step"] == step_number]

# Precompute dictionary of fields grouped by step for convenience
fields_by_step = {}
for fname, meta in field_map.items():
    fields_by_step.setdefault(meta["step"], {})[fname] = meta
