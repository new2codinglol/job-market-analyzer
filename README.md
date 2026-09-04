# Job Market Analyzer

Top in-demand tech skills, extracted from real job postings.

## Live demo

_(add links after deploy)_

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

Until this is run, the app serves an empty skill list.

## Deploy

- **Backend → Render**: Web Service, build `pip install -r requirements.txt`, start `uvicorn main:app --host 0.0.0.0 --port $PORT`. Free tier cold-starts after inactivity — first request may be slow.
- **Frontend → Vercel**: root `frontend/`, framework Vite, env var `VITE_API_URL` = your Render URL.
- Update `ALLOWED_ORIGINS` in `backend/main.py` with your real Vercel URL.
