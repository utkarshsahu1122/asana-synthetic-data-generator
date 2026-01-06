from pathlib import Path
from db import execute_script

def main():
    Path("data").mkdir(exist_ok=True)

    print("Initializing database...")
    execute_script("docs/schema.sql")

    print("Schema created.")
    print("Data generation coming next...")

if __name__ == "__main__":
    main()
