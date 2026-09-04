import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from skills import count_skills

app = FastAPI(title="Job Market Analyzer API")

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://job-market-analyzer.vercel.app",  # update to your real Vercel URL after deploy
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
