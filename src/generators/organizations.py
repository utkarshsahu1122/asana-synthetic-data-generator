from datetime import datetime
from utils.id_utils import generate_uuid

def generate_organization():
    org = {
        "org_id": generate_uuid(),
        "name": "Acme Analytics",
        "domain": "acme.com",
        "created_at": datetime.now().isoformat()
    }
    return org
