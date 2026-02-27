# sync_repo.py
import os
import subprocess
from pathlib import Path
import csv
import json

REPO_URL = "https://github.com/liquidslr/leetcode-company-wise-problems.git"


LOCAL_DIR = Path(__file__).resolve().parent.parent / "data_repo"


OUTPUT_DIR = Path(__file__).resolve().parent / "data"


def git_clone_or_pull():
    """Clone repo if not present, otherwise pull updates."""
    LOCAL_DIR.parent.mkdir(parents=True, exist_ok=True)

    if LOCAL_DIR.exists():
        print("Pulling latest...")
        subprocess.run(["git", "-C", str(LOCAL_DIR), "pull"], check=False)
    else:
        print("Cloning repository...")
        subprocess.run(["git", "clone", REPO_URL, str(LOCAL_DIR)], check=True)


def parse_companies_to_json(output_dir=OUTPUT_DIR):
    """Parse all company CSV files into JSON."""
    companies_dir = LOCAL_DIR / "companies"

    output_dir.mkdir(exist_ok=True)

    if not companies_dir.exists():
        raise RuntimeError("Error: 'companies' folder not found in cloned repo.")

    for csv_path in companies_dir.glob("*.csv"):
        company = csv_path.stem
        rows = []

        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for r in reader:
                rows.append(r)

        out_path = output_dir / f"{company}.json"

        with open(out_path, "w", encoding="utf-8") as fo:
            json.dump(rows, fo, indent=2, ensure_ascii=False)

        print(f"Saved {company}: {len(rows)} problems → {out_path}")


if __name__ == "__main__":
    git_clone_or_pull()
    parse_companies_to_json()
