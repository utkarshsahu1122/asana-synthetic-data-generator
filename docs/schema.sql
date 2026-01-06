-- Asana-like relational schema
-- Target DB: SQLite
-- Design goals:
-- 1. Relational consistency
-- 2. Realistic task hierarchies
-- 3. Extensibility for analytics
-- 4. Support for custom fields

PRAGMA foreign_keys = ON;

CREATE TABLE organizations (
    org_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    domain TEXT,
    created_at TIMESTAMP
);

CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT UNIQUE,
    role TEXT,
    created_at TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

CREATE TABLE team_memberships (
    membership_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    role TEXT,
    joined_at TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    org_id TEXT NOT NULL,
    team_id TEXT,
    name TEXT NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP,
    project_type TEXT,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    position INTEGER,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT,
    section_id TEXT,
    parent_task_id TEXT,
    name TEXT,
    description TEXT,
    assignee_id TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    due_date DATE,
    completed BOOLEAN DEFAULT 0,
    completed_at TIMESTAMP,
    priority TEXT,
    estimate_hours REAL,
    status TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id)
);

CREATE TABLE subtasks (
    subtask_id TEXT PRIMARY KEY,
    parent_task_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);

CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT,
    body TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE custom_field_definitions (
    custom_field_id TEXT PRIMARY KEY,
    org_id TEXT,
    name TEXT,
    field_type TEXT,
    enum_options TEXT,
    applies_to TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

CREATE TABLE custom_field_values (
    id TEXT PRIMARY KEY,
    custom_field_id TEXT NOT NULL,
    object_type TEXT,
    object_id TEXT,
    value_text TEXT,
    value_number REAL,
    value_bool BOOLEAN,
    value_date DATE,
    created_at TIMESTAMP,
    FOREIGN KEY (custom_field_id) REFERENCES custom_field_definitions(custom_field_id)
);

CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    org_id TEXT,
    name TEXT,
    color TEXT,
    created_at TIMESTAMP,
    FOREIGN KEY (org_id) REFERENCES organizations(org_id)
);

CREATE TABLE task_tags (
    id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);
