def generate_boolean_search(fields):
    skills = fields.get("required_skills", [])
    location = fields.get("location", "")
    job_title = fields.get("job_title", "")

    if not skills or not job_title:
        return "# Nicht genug Daten für Boolean-String"

    skill_part = " OR ".join([f'"{skill}"' for skill in skills])
    query = f'({skill_part}) AND "{job_title}" AND {location}'
    return query
