# Job Market Analyzer

Top in-demand tech skills and searchable job listings, extracted from real job postings (Singapore market — closest Adzuna coverage to the region; Malaysia isn't a supported Adzuna country).

## Live demo

- Frontend: https://job-market-analyzer-xi.vercel.app
- Backend API: https://job-market-analyzer-9s4i.onrender.com/api/skills/top (docs: /docs)

## Run locally

Backend:
```
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Frontend:
```
cd frontend
npm install
npm run dev
```
Open http://localhost:5173

## Populate real data

1. Get free API keys at https://developer.adzuna.com/signup
2. Copy `backend/.env.example` to `backend/.env`, fill in `ADZUNA_APP_ID` / `ADZUNA_APP_KEY`
3. `pip install -r requirements.txt` (includes requests/dotenv)
4. `python scripts/fetch_seed.py` — writes `backend/data/seed_jobs.json`

Until this is run, the app serves an empty skill/job list. `fetch_seed.py` currently pulls from Adzuna's `sg` (Singapore) market — edit `COUNTRY` in the script to change it, subject to Adzuna's supported country list.

## Deploy

- **Backend → Render**: Web Service, build `pip install -r requirements.txt`, start `uvicorn main:app --host 0.0.0.0 --port $PORT`. Free tier cold-starts after inactivity — first request may be slow.
- **Frontend → Vercel**: root `frontend/`, framework Vite, env var `VITE_API_URL` = your Render URL.
- Update `ALLOWED_ORIGINS` in `backend/main.py` with your real Vercel URL.
