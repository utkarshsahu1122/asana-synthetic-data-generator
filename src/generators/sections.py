from utils.id_utils import generate_uuid

DEFAULT_SECTIONS = ["To Do", "In Progress", "Blocked", "Done"]

def generate_sections(projects):
    sections = []

    for project in projects:
        for idx, name in enumerate(DEFAULT_SECTIONS):
            sections.append({
                "section_id": generate_uuid(),
                "project_id": project["project_id"],
                "name": name,
                "position": idx
            })

    return sections
