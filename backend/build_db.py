# build_db.py
import sqlite3
import json
from pathlib import Path

# Folder containing all generated JSON files
DATA_DIR = Path(__file__).resolve().parent / "data"

# Output DB file
DB_PATH = Path(__file__).resolve().parent / "company_questions.db"

# Create DB connection
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create table
c.execute("""
CREATE TABLE IF NOT EXISTS problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    title TEXT,
    difficulty TEXT,
    url TEXT,
    meta TEXT
)
""")
conn.commit()

# Loop through all JSON files (one per company)
for json_file in DATA_DIR.glob("*.json"):
    company = json_file.stem
    items = json.load(open(json_file, encoding='utf-8'))

    for it in items:
        title = it.get("Problem", it.get("Title", it.get("title", "")))
        difficulty = it.get("Difficulty", it.get("difficulty", ""))
        url = it.get("URL", it.get("Link", ""))

        meta = json.dumps(it, ensure_ascii=False)

        c.execute(
            "INSERT INTO problems (company, title, difficulty, url, meta) VALUES (?, ?, ?, ?, ?)",
            (company, title, difficulty, url, meta)
        )

conn.commit()
conn.close()

print("Database built successfully → company_questions.db")
