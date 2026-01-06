from faker import Faker
from datetime import datetime
from utils.id_utils import generate_uuid
import random

fake = Faker()

def generate_users(org_id, domain, num_users):
    users = []
    email_counter = {}

    for _ in range(num_users):
        first = fake.first_name().lower()
        last = fake.last_name().lower()
        base_email = f"{first}.{last}@{domain}"

        if base_email not in email_counter:
            email_counter[base_email] = 1
            email = base_email
        else:
            email_counter[base_email] += 1
            email = f"{first}.{last}{email_counter[base_email]}@{domain}"

        users.append({
            "user_id": generate_uuid(),
            "org_id": org_id,
            "first_name": first.capitalize(),
            "last_name": last.capitalize(),
            "email": email,
            "role": random.choice(["IC", "Manager", "Lead"]),
            "created_at": datetime.now().isoformat(),
            "is_active": True
        })

    return users
