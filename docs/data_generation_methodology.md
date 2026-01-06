# Data Generation Methodology

This document describes how synthetic data is generated for each table and column
in the Asana-like schema. The goal is to balance realism, consistency, and scalability.

Guiding principles:
- Preserve relational integrity
- Model realistic temporal behavior
- Favor analytical usefulness over UI fidelity
- Use LLMs only where semantic richness matters


## Global Assumptions

- Time range: last 6 months
- Workdays: Monday–Friday
- Peak task creation: Monday–Wednesday
- Typical team size: 4–9 users
- Projects follow either sprint-based or continuous workflows
- Not all tasks are assigned
- Not all tasks have due dates
- Completion probability increases with task age


## organizations

| Column | Strategy |
|------|----------|
| org_id | UUIDv4 |
| name | Single realistic SaaS company name |
| domain | Derived from name |
| created_at | Fixed timestamp 6–12 months in the past |

Notes:
- Only one organization is required for this dataset
- Schema supports multiple organizations for extensibility


## teams

| Column | Strategy |
|------|----------|
| team_id | UUIDv4 |
| org_id | Always references existing organization |
| name | Predefined functional names (Engineering, Platform, Growth, Data, Infra) |
| description | Short template-based text |
| created_at | After organization creation |

Notes:
- Teams are reused across projects
- Team count scales with user count


## users

| Column | Strategy |
|------|----------|
| user_id | UUIDv4 |
| org_id | Single organization |
| first_name | Sampled from public name datasets |
| last_name | Sampled independently |
| email | `{first}.{last}@{domain}`, with numeric suffix if collision |
| role | Weighted choice (IC > Manager > Lead) |
| created_at | Uniformly distributed since org creation |
| is_active | 90–95% active |

Notes:
- Users can belong to multiple teams
- Names are decoupled from roles to avoid bias

Collision Handling:
- Emails are generated as `{first}.{last}@{domain}`
- If a collision occurs, append an incrementing numeric suffix:
  - rahul.sharma@company.com
  - rahul.sharma2@company.com
  - rahul.sharma3@company.com
- This preserves realism while maintaining uniqueness


## team_memberships

| Column | Strategy |
|------|----------|
| membership_id | UUIDv4 |
| team_id | Sample team |
| user_id | Sample user |
| role | Member / Lead |
| joined_at | After both user and team creation |

Notes:
- Users typically belong to 1–2 teams
- Team size capped to maintain realism


## projects

| Column | Strategy |
|------|----------|
| project_id | UUIDv4 |
| org_id | Organization |
| team_id | Optional; some projects cross-team |
| name | LLM-generated or template-based |
| description | LLM-generated |
| start_date | Random weekday |
| end_date | Optional; sprint projects end sooner |
| created_at | Near start_date |
| project_type | Engineering, Marketing, Ops, Research |

Notes:
- Project type influences task behavior
- Sprint projects typically last 2–6 weeks


## sections

| Column | Strategy |
|------|----------|
| section_id | UUIDv4 |
| project_id | Parent project |
| name | Standard workflow names |
| position | Integer ordering |

Notes:
- Most projects have 3–5 sections
- Section names influence task status


## tasks

Tasks are the central entity of the dataset and are generated with
temporal, relational, and behavioral realism.

Each task represents a unit of work with a lifecycle influenced by:
- Project type
- Task age
- Assignment status
- Hierarchical position (parent vs subtask)

> Identification & relationships

| Column | Strategy |
|------|----------|
| task_id | UUIDv4 |
| project_id | Sampled from existing projects; some tasks may be project-less (backlog) |
| section_id | Sampled from project sections with weighted probabilities |
| parent_task_id | Assigned for ~12–18% of tasks to create subtasks |

Notes:
- Subtasks inherit project and section context from parent
- Maximum hierarchy depth capped at 2 to avoid pathological trees

> Semantic content

| Column | Strategy |
|------|----------|
| name | LLM-generated or template-based short action phrases |
| description | LLM-generated; optional (20–30% empty) |

> Assignment & ownership

| Column | Strategy |
|------|----------|
| assignee_id | Sampled from users in the project’s team; 10–20% unassigned |

> Temporal fields

| Column | Strategy |
|------|----------|
| created_at | Sampled from last 6 months with weekday bias |
| updated_at | After created_at; reflects last activity |
| due_date | Optional; distributed relative to created_at |

> Completion modeling

| Column | Strategy |
|------|----------|
| completed | Probabilistic; depends on task age and project type |
| completed_at | If completed, sampled after created_at |

> Status & effort

| Column | Strategy |
|------|----------|
| priority | Weighted enum (Low, Medium, High, Critical) |
| estimate_hours | Numeric; skewed toward small values |
| status | Derived from section + completion |


## subtasks

Subtasks are generated by selecting a subset of tasks
and creating child tasks linked via parent_task_id.

Rules:
- 12–18% of tasks become parents
- Each parent has 1–4 subtasks
- Subtasks inherit assignee unless overridden
- Subtasks usually have shorter estimates and nearer due dates


## comments

| Column | Strategy |
|------|----------|
| comment_id | UUIDv4 |
| task_id | Parent task |
| user_id | Task assignee or collaborator |
| body | LLM-generated short text |
| created_at | Between task creation and completion |

Notes:
- Completed tasks tend to have more comments
- Blocked tasks include blocker-related comments
