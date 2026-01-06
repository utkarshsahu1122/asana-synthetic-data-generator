import random
from datetime import datetime, timedelta

# Probability of accepting a sampled timestamp by weekday.
# Encodes realistic human work intensity.
WEEKDAY_ACCEPT_PROB = {
    0: 0.30,  # Monday
    1: 0.30,
    2: 0.28,
    3: 0.25,
    4: 0.22,
    5: 0.05,  # Saturday
    6: 0.05,  # Sunday
}

def random_datetime(start: datetime, end: datetime) -> datetime:
    delta = end - start
    seconds = delta.total_seconds()
    while True:
        dt = start + timedelta(seconds=random.uniform(0, seconds))
        if random.random() < WEEKDAY_ACCEPT_PROB[dt.weekday()]:
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
