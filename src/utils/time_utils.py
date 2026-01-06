import random
from datetime import datetime, timedelta

# Relative acceptance weights for task creation/update times.
# Encodes typical human work intensity across the week.
# Values are heuristic, ordered, and intentionally non-zero for weekends.
WEEKDAY_WEIGHTS = {
    0: 1.2,  # Monday
    1: 1.2,
    2: 1.1,
    3: 1.0,
    4: 0.9,
    5: 0.2,  # Saturday
    6: 0.2,  # Sunday
}

def random_datetime(start: datetime, end: datetime) -> datetime:
    delta = end - start
    seconds = delta.total_seconds()
    while True:
        dt = start + timedelta(seconds=random.uniform(0, seconds))
        if random.random() < WEEKDAY_WEIGHTS[dt.weekday()]:
            return dt

def random_due_date(created_at: datetime) -> datetime | None:
    r = random.random()

    if r < 0.10:
        return None
    elif r < 0.35:
        return created_at + timedelta(days=random.randint(1, 7))
    elif r < 0.75:
        return created_at + timedelta(days=random.randint(8, 30))
    elif r < 0.95:
        return created_at + timedelta(days=random.randint(31, 90))
    else:
        return created_at - timedelta(days=random.randint(1, 14))
