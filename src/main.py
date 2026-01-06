from pathlib import Path
from db import execute_script, get_connection
from config import NUM_USERS, NUM_PROJECTS
from generators.organizations import generate_organization
from generators.teams import generate_teams
from generators.users import generate_users
from generators.team_memberships import generate_team_memberships
from generators.projects import generate_projects
from generators.sections import generate_sections

def insert_many(conn, table, rows):
    if not rows:
        return
    keys = rows[0].keys()
    cols = ", ".join(keys)
    placeholders = ", ".join("?" for _ in keys)
    values = [tuple(row[k] for k in keys) for row in rows]
    conn.executemany(
        f"INSERT INTO {table} ({cols}) VALUES ({placeholders})",
        values
    )

def main():
    Path("data").mkdir(exist_ok=True)
    execute_script("docs/schema.sql")
    conn = get_connection()

    org = generate_organization()
    insert_many(conn, "organizations", [org])

    teams = generate_teams(org["org_id"])
    insert_many(conn, "teams", teams)

    users = generate_users(org["org_id"], org["domain"], NUM_USERS)
    insert_many(conn, "users", users)

    memberships = generate_team_memberships(teams, users)
    insert_many(conn, "team_memberships", memberships)

    projects = generate_projects(org["org_id"], teams, NUM_PROJECTS)
    insert_many(conn, "projects", projects)

    sections = generate_sections(projects)
    insert_many(conn, "sections", sections)

    conn.commit()
    conn.close()

    print("Core entities generated successfully.")

if __name__ == "__main__":
    main()
