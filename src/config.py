from datetime import datetime, timedelta
import random

# ------------------------
# Global random seed
# ------------------------
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# ------------------------
# Time configuration
# ------------------------
NOW = datetime.now()
START_DATE = NOW - timedelta(days=180)

# ------------------------
# Scale configuration
# ------------------------
NUM_TEAMS = 12
NUM_USERS = 120
NUM_PROJECTS = 60

TASKS_PER_PROJECT_MIN = 20
TASKS_PER_PROJECT_MAX = 80

SUBTASK_PARENT_RATIO = 0.15  # 15% of tasks become parents

# ------------------------
# Behavioral probabilities
# ------------------------
UNASSIGNED_TASK_PROB = 0.15
BLOCKED_TASK_PROB = 0.05
