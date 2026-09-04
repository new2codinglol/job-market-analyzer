"""One-off script: fetch job postings from Adzuna, write backend/data/seed_jobs.json.
Run locally only, never deployed. Requires ADZUNA_APP_ID and ADZUNA_APP_KEY in backend/.env.
"""
import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

APP_ID = os.environ["ADZUNA_APP_ID"]
APP_KEY = os.environ["ADZUNA_APP_KEY"]
COUNTRY = "us"
PAGES = 10  # ~20 results per page -> ~200 jobs
QUERY = "software engineer"

OUT_PATH = Path(__file__).parent.parent / "data" / "seed_jobs.json"


def fetch_page(page: int) -> list[dict]:
    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": 20,
        "what": QUERY,
        "content-type": "application/json",
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json().get("results", [])


def main():
    jobs = []
    for page in range(1, PAGES + 1):
        results = fetch_page(page)
        if not results:
            break
        for r in results:
            jobs.append({
                "id": r.get("id"),
                "title": r.get("title"),
                "company": (r.get("company") or {}).get("display_name"),
                "location": (r.get("location") or {}).get("display_name"),
                "description": r.get("description"),
                "salary_min": r.get("salary_min"),
                "salary_max": r.get("salary_max"),
                "category": (r.get("category") or {}).get("label"),
                "created": r.get("created"),
                "redirect_url": r.get("redirect_url"),
            })

    OUT_PATH.write_text(json.dumps(jobs, indent=2), encoding="utf-8")
    print(f"Wrote {len(jobs)} jobs to {OUT_PATH}")


if __name__ == "__main__":
    main()
