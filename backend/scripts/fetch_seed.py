"""One-off script: build backend/data/seed_jobs.json from Adzuna (API, needs
keys in backend/.env) plus RemoteOK and We Work Remotely (public feeds meant
for reuse, no keys needed). Run locally only, never deployed.
"""
import json
import os
import re
from pathlib import Path
from defusedxml import ElementTree

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

USER_AGENT = "job-market-analyzer-portfolio/1.0 (+https://github.com/new2codinglol/job-market-analyzer)"
HEADERS = {"User-Agent": USER_AGENT}

ADZUNA_COUNTRY = "sg"
ADZUNA_PAGES = 10  # ~20 results per page -> ~200 jobs
ADZUNA_QUERY = "software engineer"

OUT_PATH = Path(__file__).parent.parent / "data" / "seed_jobs.json"

TAG_RE = re.compile(r"<[^>]+>")


def strip_html(text: str) -> str:
    return TAG_RE.sub(" ", text or "").strip()


C1_CONTROL_RE = re.compile(r"[\x80-\x9f�]")


def fix_mojibake(text: str) -> str:
    # WWR's feed intermittently double-encodes non-ASCII text (real UTF-8
    # bytes get decoded as Latin-1 upstream, e.g. "BayamÃ³n"
    # instead of "Bayamón"). Round-tripping through latin-1->utf-8 only
    # succeeds when the text has exactly this signature, so it's a safe
    # no-op on already-correct text (ASCII round-trips to itself; real
    # multi-byte chars like Chinese aren't representable in latin-1 at all
    # and raise immediately).
    if not text:
        return text
    try:
        text = text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return text


def is_garbled(text: str) -> bool:
    # A few entries come through with worse (multi-step) corruption a single
    # round-trip can't undo, leaving stray control chars behind. Not worth
    # chasing for a handful of records — the caller drops these instead of
    # showing garbage.
    return bool(text) and bool(C1_CONTROL_RE.search(text))


# ponytail: Adzuna SG returns some salaries as monthly, some as annual, with
# no field to tell which. Observed a clean gap in this data (monthly maxes out
# ~3000, annual starts ~30000), so anything under this threshold gets
# annualized. Heuristic, not a guarantee — revisit if a job's real annual
# salary is genuinely below MONTHLY_SALARY_THRESHOLD.
MONTHLY_SALARY_THRESHOLD = 10_000


def annualize_sgd(salary_min, salary_max):
    if salary_min and salary_min < MONTHLY_SALARY_THRESHOLD:
        salary_min *= 12
    if salary_max and salary_max < MONTHLY_SALARY_THRESHOLD:
        salary_max *= 12
    return salary_min, salary_max


def fetch_adzuna() -> list[dict]:
    app_id = os.environ.get("ADZUNA_APP_ID")
    app_key = os.environ.get("ADZUNA_APP_KEY")
    if not app_id or not app_key:
        print("Skipping Adzuna: ADZUNA_APP_ID/ADZUNA_APP_KEY not set in backend/.env")
        return []

    jobs = []
    for page in range(1, ADZUNA_PAGES + 1):
        url = f"https://api.adzuna.com/v1/api/jobs/{ADZUNA_COUNTRY}/search/{page}"
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": 20,
            "what": ADZUNA_QUERY,
            "content-type": "application/json",
        }
        resp = requests.get(url, params=params, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        results = resp.json().get("results", [])
        if not results:
            break
        for r in results:
            salary_min, salary_max = annualize_sgd(r.get("salary_min"), r.get("salary_max"))
            jobs.append({
                "id": f"adzuna-{r.get('id')}",
                "title": r.get("title"),
                "company": (r.get("company") or {}).get("display_name"),
                "location": (r.get("location") or {}).get("display_name"),
                "description": r.get("description"),
                "salary_min": salary_min,
                "salary_max": salary_max,
                "category": (r.get("category") or {}).get("label"),
                "created": r.get("created"),
                "redirect_url": r.get("redirect_url"),
                "source": "adzuna",
            })
    print(f"Adzuna: {len(jobs)} jobs")
    return jobs


def fetch_remoteok() -> list[dict]:
    resp = requests.get("https://remoteok.com/api", headers=HEADERS, timeout=30)
    resp.raise_for_status()
    entries = resp.json()
    jobs = []
    for r in entries:
        if "id" not in r or "position" not in r:
            continue  # first entry is RemoteOK's API legal notice, not a job
        location = fix_mojibake(r.get("location")) or "Remote"
        if is_garbled(location):
            location = "Remote"
        jobs.append({
            "id": f"remoteok-{r['id']}",
            "title": fix_mojibake(r.get("position")),
            "company": fix_mojibake(r.get("company")),
            "location": location,
            "description": fix_mojibake(strip_html(r.get("description"))),
            "salary_min": r.get("salary_min"),
            "salary_max": r.get("salary_max"),
            "category": (r.get("tags") or [None])[0],
            "created": r.get("date"),
            "redirect_url": r.get("url"),
            "source": "remoteok",
        })
    print(f"RemoteOK: {len(jobs)} jobs")
    return jobs


WWR_CATEGORIES = ["remote-programming-jobs", "remote-devops-sysadmin-jobs"]


def fetch_weworkremotely() -> list[dict]:
    jobs = []
    for category in WWR_CATEGORIES:
        url = f"https://weworkremotely.com/categories/{category}.rss"
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        resp.encoding = "utf-8"  # feed is UTF-8; don't let requests guess wrong on a missing/odd charset
        root = ElementTree.fromstring(resp.text)
        for item in root.iter("item"):
            title = fix_mojibake((item.findtext("title") or "").strip())
            company, _, position = title.partition(": ")
            link = (item.findtext("link") or "").strip()
            location = fix_mojibake((item.findtext("region") or "Remote").strip())
            if is_garbled(location):
                location = "Remote"
            jobs.append({
                "id": f"wwr-{link.rsplit('/', 1)[-1]}",
                "title": position or title,
                "company": company if position else None,
                "location": location,
                "description": fix_mojibake(strip_html(item.findtext("description"))),
                "salary_min": None,
                "salary_max": None,
                "category": (item.findtext("category") or "").strip() or None,
                "created": (item.findtext("pubDate") or "").strip(),
                "redirect_url": link,
                "source": "weworkremotely",
            })
    print(f"We Work Remotely: {len(jobs)} jobs")
    return jobs


def dedupe(jobs: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for job in jobs:
        key = ((job.get("title") or "").strip().lower(), (job.get("company") or "").strip().lower())
        if key in seen:
            continue
        seen.add(key)
        unique.append(job)
    return unique


def main():
    jobs = fetch_adzuna() + fetch_remoteok() + fetch_weworkremotely()
    jobs = dedupe(jobs)
    OUT_PATH.write_text(json.dumps(jobs, indent=2), encoding="utf-8")
    print(f"Wrote {len(jobs)} jobs (after dedupe) to {OUT_PATH}")


if __name__ == "__main__":
    main()
