from datetime import datetime, timedelta
from utils.id_utils import generate_uuid
import random

PROJECT_TYPES = ["Engineering", "Marketing", "Ops", "Research"]

def generate_projects(org_id, teams, num_projects):
    projects = []

    for i in range(num_projects):
        team = random.choice(teams)
        start = datetime.now() - timedelta(days=random.randint(30, 180))

        projects.append({
            "project_id": generate_uuid(),
            "org_id": org_id,
            "team_id": team["team_id"],
            "name": f"{team['name']} Project {i+1}",
            "description": f"Project focused on {team['name'].lower()} initiatives",
            "start_date": start.date().isoformat(),
            "end_date": None,
            "created_at": start.isoformat(),
            "project_type": random.choice(PROJECT_TYPES)
        })

    return projects
