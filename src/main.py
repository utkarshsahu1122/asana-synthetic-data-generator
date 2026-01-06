from pathlib import Path

from config import NUM_USERS, NUM_PROJECTS
from db import (
    initialize_schema,
    get_connection,
    DB_PATH,
    table_has_rows,
)

from generators.tasks import generate_tasks
from generators.comments import generate_comments
from generators.organizations import generate_organization
from generators.teams import generate_teams
from generators.users import generate_users
from generators.team_memberships import generate_team_memberships
from generators.projects import generate_projects
from generators.sections import generate_sections

# --------------------------------
# Run configuration
# --------------------------------
RESET_DB = False  # set True only if you want a fresh DB


# --------------------------------
# Helper functions
# --------------------------------
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


def fetch_all_as_dicts(conn, table):
    cursor = conn.execute(f"SELECT * FROM {table}")
    col_names = [description[0] for description in cursor.description]
    return [dict(zip(col_names, row)) for row in cursor.fetchall()]


# --------------------------------
# Main pipeline
# --------------------------------
def main():
    Path("data").mkdir(exist_ok=True)

    if RESET_DB and DB_PATH.exists():
        DB_PATH.unlink()

    initialize_schema("docs/schema.sql")
    conn = get_connection()

    # -----------------------
    # Organization
    # -----------------------
    if not table_has_rows(conn, "organizations"):
        org = generate_organization()
        insert_many(conn, "organizations", [org])
    else:
        org = fetch_all_as_dicts(conn, "organizations")[0]

    # -----------------------
    # Teams
    # -----------------------
    if not table_has_rows(conn, "teams"):
        teams = generate_teams(org["org_id"])
        insert_many(conn, "teams", teams)
    else:
        teams = fetch_all_as_dicts(conn, "teams")

    # -----------------------
    # Users
    # -----------------------
    if not table_has_rows(conn, "users"):
        users = generate_users(org["org_id"], org["domain"], NUM_USERS)
        insert_many(conn, "users", users)
    else:
        users = fetch_all_as_dicts(conn, "users")

    # -----------------------
    # Team memberships
    # -----------------------
    if not table_has_rows(conn, "team_memberships"):
        memberships = generate_team_memberships(teams, users)
        insert_many(conn, "team_memberships", memberships)

    # -----------------------
    # Projects
    # -----------------------
    if not table_has_rows(conn, "projects"):
        projects = generate_projects(org["org_id"], teams, NUM_PROJECTS)
        insert_many(conn, "projects", projects)
    else:
        projects = fetch_all_as_dicts(conn, "projects")

    # -----------------------
    # Sections
    # -----------------------
    if not table_has_rows(conn, "sections"):
        sections = generate_sections(projects)
        insert_many(conn, "sections", sections)
    else:
        sections = fetch_all_as_dicts(conn, "sections")
        
    # -----------------------
    # Tasks (append-only)
    # -----------------------
    tasks = generate_tasks(projects, sections, users)
    insert_many(conn, "tasks", tasks)

    # -----------------------
    # Comments (append-only)
    # -----------------------
    comments = generate_comments(tasks, users)
    insert_many(conn, "comments", comments)

    conn.commit()
    conn.close()

    print("Core entities generated successfully.")


if __name__ == "__main__":
    main()
