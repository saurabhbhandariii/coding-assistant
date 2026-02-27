# app.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from roadmap_gen import generate_roadmap, get_company_problems
import openai
import os
from pathlib import Path

# -----------------------------
# CREATE APP FIRST (IMPORTANT)
# -----------------------------
app = FastAPI(title="AI Coding Mentor API")

# -----------------------------
# ENABLE CORS (FOR CHROME EXTENSIONS)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROADMAP REQUEST BODY MODEL
# -----------------------------
class RoadmapReq(BaseModel):
    company: str
    weeks: int = 8
    user_level: str = "intermediate"

# -----------------------------
# HINT REQUEST MODEL
# -----------------------------
class HintReq(BaseModel):
    problem_title: str
    description: str = ""
    user_code: str = ""

# -----------------------------
# ENDPOINTS
# -----------------------------

@app.post("/roadmap")
def roadmap(req: RoadmapReq):
    """Generate a coding roadmap."""
    try:
        text = generate_roadmap(req.company, req.user_level, req.weeks)
        problems = get_company_problems(req.company, limit=50)

        return {
            "roadmap_text": text,
            "problems_sample": problems[:20]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/hint")
def hint(req: HintReq):
    """Generate hints for a LeetCode problem."""
    try:
        prompt_path = Path(__file__).resolve().parent / "prompts" / "hint_prompt.txt"

        if not prompt_path.exists():
            raise RuntimeError("hint_prompt.txt not found")

        prompt_template = prompt_path.read_text()

        prompt = (
            prompt_template
            .replace("[PROBLEM_TITLE]", req.problem_title)
            .replace("[DESCRIPTION]", req.description or "No description")
            .replace("[USER_CODE]", req.user_code or "No user code")
        )

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=600
        )

        return {"hint_text": response.choices[0].message["content"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/companies")
def companies():
    """Return all supported companies."""
    data_dir = Path(__file__).resolve().parent / "data"
    names = [p.stem for p in data_dir.glob("*.json")]
    return {"companies": names}

