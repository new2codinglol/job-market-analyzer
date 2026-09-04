import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from skills import KNOWN_SKILLS, count_skills, job_has_skill

app = FastAPI(title="Job Market Analyzer API")

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://job-market-analyzer-xi.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).parent / "data" / "seed_jobs.json"
JOBS = json.loads(DATA_PATH.read_text(encoding="utf-8"))
SKILL_COUNTS = count_skills(JOBS)


@app.get("/api/skills/top")
def top_skills(n: int = 10):
    return [{"skill": skill, "count": count} for skill, count in SKILL_COUNTS.most_common(n)]


@app.get("/api/skills/list")
def skills_list():
    return KNOWN_SKILLS


@app.get("/api/jobs")
def list_jobs(location: str = "", skill: str = "", limit: int = 100):
    results = JOBS
    if location:
        results = [j for j in results if location.lower() in (j.get("location") or "").lower()]
    if skill:
        results = [j for j in results if job_has_skill(j, skill)]
    return results[:limit]
