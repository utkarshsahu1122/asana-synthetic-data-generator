from datetime import datetime
from utils.id_utils import generate_uuid

TEAM_NAMES = [
    "Engineering",
    "Platform",
    "Infrastructure",
    "Data",
    "Growth",
    "Marketing",
    "Operations",
    "Product"
]

def generate_teams(org_id):
    teams = []
    for name in TEAM_NAMES:
        teams.append({
            "team_id": generate_uuid(),
            "org_id": org_id,
            "name": name,
            "description": f"{name} team",
            "created_at": datetime.now().isoformat()
        })
    return teams
