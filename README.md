# Scaler Program Evaluator & Sales Decision Engine

An academic fit and retention intelligence platform for edtech sales counselors. Built on empirical cohort data from **13,180 enrolled learners**, the engine computes optimal program and track placements, forecasts retention vs. refund risk, and arms counselors with spoken conversational teleprompter scripts.

---

## Key Capabilities

- **Dual-Channel Lead Ingestion**: Real-time sync from CRM/Metabase and drag-and-drop bulk CSV processing.
- **Academic Degree Prerequisite Gate**: Automatically prevents placement-track enrollment for candidates without a Bachelor's degree, protecting candidates from recruiter screening rejections.
- **Track-Level Calibration**: Accurately places learners into Beginner (15 Mos), Intermediate (12 Mos), or Advanced (9 Mos) pacing.
- **Visual Retention vs. Refund Meter**: Displays cohort completion with an 80% benchmark target line.
- **Sequential Spoken Teleprompter**: 3-stage phone script (Discovery Hook, Value Pitch, and Inbound Objection Rebuttal).

---

## Tech Stack

- **Backend**: Python 3.11, FastAPI, Uvicorn, Pandas
- **Frontend**: HTML5, Vanilla CSS3, JavaScript (Single-Page App, zero build step)
- **Database**: Embedded SQLite with WAL mode (`output/leads_store.db`)
- **Deployment**: Docker, Railway, Render, or any Linux/Windows server

---

## Quick Start (Local Run)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server**:
   ```bash
   python run_app.py
   ```

3. Open **`http://localhost:8000`** in your browser.

---

## Deployment to Railway

1. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO>.git
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app) and click **New Project** -> **Deploy from GitHub repo**.
   - Select this repository.
   - (Optional) Add a Persistent Volume mounted to `/app/output`.
   - Railway will build the Docker container and provide a live HTTPS link!

---

## Project Structure

```
.
├── Dockerfile              # Production container definition
├── docker-compose.yml      # 1-command local container runner
├── requirements.txt        # Python production dependencies
├── metabase_config.json    # CRM / Metabase connection settings
├── run_app.py              # Application launcher
├── src/                    # Backend API and evaluation logic
│   ├── evaluator.py        # Core evaluation brain & script generator
│   ├── server.py           # FastAPI web & API server
│   ├── lead_store.py       # Embedded SQLite WAL storage
│   ├── matrix_engine.py    # Historical learner cohort matching
│   └── metabase_client.py  # Metabase / CRM query client
├── web/                    # Counselor desk frontend
│   └── index.html          # Single-Page UI
└── output/                 # Precomputed cohort matrix
    ├── retention_matrix.json
    └── empirical_persona_matrix.csv
```
