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


@app.get("/api/locations")
def locations():
    return sorted({j["location"] for j in JOBS if j.get("location")})


def _salary_midpoint(job: dict) -> float | None:
    lo, hi = job.get("salary_min"), job.get("salary_max")
    if lo and hi:
        return (lo + hi) / 2
    return lo or hi or None


# Scoped to Adzuna (SGD, Singapore) only: it's 59/63 of the salaried jobs
# anyway, and mixing in RemoteOK's handful of USD salaries as if the same
# currency would misrepresent both. Categories/locations here are almost
# entirely "IT Jobs"/"Singapore" too (no per-skill breakdown either, since
# Adzuna's free tier truncates description to 500 chars — too little text
# for reliable skill matching on this specific subset) so a distribution is
# the one honest chart this dataset supports beyond a single summary number.
#
# Converted to MYR (Jason's actual market) since the data itself is
# Singapore/SGD. Rate is a static snapshot, not a live lookup — this app has
# no other runtime external dependency and salary data doesn't need to track
# FX moment-to-moment. Fetched from open.er-api.com on 2026-09-07.
SALARY_CURRENCY = "MYR"
SGD_TO_MYR = 3.192
SALARIED_JOBS = [
    m * SGD_TO_MYR for j in JOBS if j.get("source") == "adzuna" and (m := _salary_midpoint(j)) is not None
]

BUCKET_SIZE = 100_000


@app.get("/api/salary/summary")
def salary_summary():
    if not SALARIED_JOBS:
        return {"count": 0, "avg": None, "min": None, "max": None, "currency": SALARY_CURRENCY}
    return {
        "count": len(SALARIED_JOBS),
        "avg": round(sum(SALARIED_JOBS) / len(SALARIED_JOBS)),
        "min": round(min(SALARIED_JOBS)),
        "max": round(max(SALARIED_JOBS)),
        "currency": SALARY_CURRENCY,
    }


@app.get("/api/salary/distribution")
def salary_distribution():
    buckets: dict[int, int] = {}
    for m in SALARIED_JOBS:
        bucket = int(m // BUCKET_SIZE)
        buckets[bucket] = buckets.get(bucket, 0) + 1
    return [
        {"range": f"{b * BUCKET_SIZE // 1000}k-{(b + 1) * BUCKET_SIZE // 1000}k", "count": count}
        for b, count in sorted(buckets.items())
    ]
