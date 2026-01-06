from utils.id_utils import generate_uuid
from datetime import datetime
import random

def generate_team_memberships(teams, users):
    memberships = []

    for user in users:
        assigned_teams = random.sample(teams, k=random.randint(1, 2))
        for team in assigned_teams:
            memberships.append({
                "membership_id": generate_uuid(),
                "team_id": team["team_id"],
                "user_id": user["user_id"],
                "role": "Member",
                "joined_at": datetime.now().isoformat()
            })

    return memberships
