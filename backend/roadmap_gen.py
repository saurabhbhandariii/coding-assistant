# roadmap_gen.py
from dotenv import load_dotenv
load_dotenv()

import os
import json
import sqlite3
from pathlib import Path
import openai

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt template file
PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "roadmap_prompt.txt"


def get_company_problems(company, limit=200):
    """Fetch problems from SQLite DB for a company."""
    db_path = Path(__file__).resolve().parent / "company_questions.db"

    if not db_path.exists():
        raise RuntimeError("ERROR: company_questions.db not found. Run build_db.py first.")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute(
        "SELECT title, difficulty, url, meta FROM problems WHERE company = ? LIMIT ?",
        (company, limit)
    )

    rows = c.fetchall()
    conn.close()

    return [
        {
            "title": r[0],
            "difficulty": r[1],
            "url": r[2],
            "meta": json.loads(r[3]) if r[3] else {}
        }
        for r in rows
    ]


def build_prompt(company, user_level="intermediate", weeks=8):
    """Builds the full roadmap prompt including company problems."""
    problems = get_company_problems(company, limit=200)
    sample = "\n".join([f"- {p['title']} ({p['difficulty']})" for p in problems[:50]])

    tpl = PROMPT_PATH.read_text(encoding="utf-8")

    return tpl.format(
        company=company,
        sample_problems=sample or "No problems found",
        user_level=user_level,
        goal=f"prepare for {company} interviews within {weeks} weeks",
        weeks=weeks
    )


def generate_roadmap(company, user_level="intermediate", weeks=8, model="gpt-4o-mini"):
    """Calls OpenAI API to generate a full roadmap."""
    if not openai.api_key:
        raise RuntimeError("ERROR: CHAT_GPT_API_Key not set in environment (.env file).")

    prompt = build_prompt(company, user_level, weeks)

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a concise coding mentor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1500
    )

    text = response.choices[0].message["content"]
    return text


if __name__ == "__main__":
    # For testing
    print(generate_roadmap("google", "intermediate", 8))
