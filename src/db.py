import sqlite3
from pathlib import Path

DB_PATH = Path("data/asana_simulation.sqlite")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def execute_script(sql_path: str):
    conn = get_connection()
    with open(sql_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
