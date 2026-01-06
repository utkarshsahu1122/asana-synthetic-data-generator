import random
from datetime import timedelta
from utils.id_utils import generate_uuid


COMMENT_TEMPLATES = [
    "Started working on this.",
    "Blocked due to dependency.",
    "Fix pushed, needs review.",
    "Waiting for clarification.",
    "Completed as discussed.",
]


def generate_comments(tasks, users):
    comments = []

    for task in tasks:
        num_comments = 0

        if task["status"] == "blocked":
            num_comments = random.randint(1, 3)
        elif task["completed"]:
            num_comments = random.randint(1, 4)
        else:
            num_comments = random.randint(0, 2)

        for _ in range(num_comments):
            user = random.choice(users)
            comments.append({
                "comment_id": generate_uuid(),
                "task_id": task["task_id"],
                "user_id": user["user_id"],
                "body": random.choice(COMMENT_TEMPLATES),
                "created_at": task["created_at"],
            })

    return comments
