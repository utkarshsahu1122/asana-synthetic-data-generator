import random
from datetime import timedelta

from utils.id_utils import generate_uuid
from utils.time_utils import random_datetime, random_due_date
from utils.sampling import probability_event
from config import (
    START_DATE,
    NOW,
    TASKS_PER_PROJECT_MIN,
    TASKS_PER_PROJECT_MAX,
    SUBTASK_PARENT_RATIO,
    UNASSIGNED_TASK_PROB,
    BLOCKED_TASK_PROB,
)

TASK_PRIORITIES = ["Low", "Medium", "High", "Critical"]
TASK_STATUSES = ["todo", "in_progress", "blocked", "done"]


def generate_tasks(projects, sections, users):
    tasks = []

    users_by_id = {u["user_id"]: u for u in users}
    sections_by_project = {}
    for sec in sections:
        sections_by_project.setdefault(sec["project_id"], []).append(sec)

    for project in projects:
        num_tasks = random.randint(
            TASKS_PER_PROJECT_MIN, TASKS_PER_PROJECT_MAX
        )

        project_sections = sections_by_project[project["project_id"]]

        for _ in range(num_tasks):
            created_at = random_datetime(START_DATE, NOW)
            due_date = random_due_date(created_at)

            completed = probability_event(0.6)
            completed_at = None
            status = random.choice(TASK_STATUSES[:-1])

            if completed:
                completed_at = created_at + timedelta(
                    days=random.randint(1, 20)
                )
                status = "done"

            assignee = None
            if not probability_event(UNASSIGNED_TASK_PROB):
                assignee = random.choice(users)["user_id"]

            task = {
                "task_id": generate_uuid(),
                "project_id": project["project_id"],
                "section_id": random.choice(project_sections)["section_id"],
                "parent_task_id": None,
                "name": f"{project['project_type']} task",
                "description": None,
                "assignee_id": assignee,
                "created_at": created_at.isoformat(),
                "updated_at": created_at.isoformat(),
                "due_date": due_date.isoformat() if due_date else None,
                "completed": completed,
                "completed_at": completed_at.isoformat() if completed_at else None,
                "priority": random.choice(TASK_PRIORITIES),
                "estimate_hours": round(random.uniform(1, 16), 1),
                "status": status,
            }

            if probability_event(BLOCKED_TASK_PROB):
                task["status"] = "blocked"

            tasks.append(task)

    # -----------------------
    # Subtasks
    # -----------------------
    parent_tasks = random.sample(
        tasks,
        int(len(tasks) * SUBTASK_PARENT_RATIO),
    )

    for parent in parent_tasks:
        num_subtasks = random.randint(1, 3)
        for _ in range(num_subtasks):
            subtask = parent.copy()
            subtask["task_id"] = generate_uuid()
            subtask["parent_task_id"] = parent["task_id"]
            subtask["estimate_hours"] = round(
                parent["estimate_hours"] * random.uniform(0.3, 0.7), 1
            )
            tasks.append(subtask)

    return tasks
