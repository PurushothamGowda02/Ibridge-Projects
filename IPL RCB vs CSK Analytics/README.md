# IPL RCB vs CSK Analytics (BCA Final Year Project)

A complete analytics project with:
- `FastAPI` backend (acts as API service)
- `Streamlit` frontend dashboard
- Analysis of **RCB vs CSK** matches from IPL 2008 to latest season in your dataset

## 1) Project Structure

```text
IPL RCB vs CSK Analytics/
  api/
    main.py
    routes/analytics.py
    services/analytics_service.py
  frontend/
    app.py
  data/
    matches.csv                <- add full dataset here
    deliveries.csv             <- optional (for top performers)
    matches_sample.csv
  requirements.txt
```

## 2) Dataset Format

### Required file
- `data/matches.csv`

Required columns:
- `id`
- `season`
- `date`
- `team1`
- `team2`
- `winner`
- `venue`

Optional but recommended:
- `toss_winner`

### Optional file
- `data/deliveries.csv`

Needed for top performers. Common columns used:
- `match_id`
- `batter` or `batsman`
- `batsman_runs`
- `bowler`
- `is_wicket` or `player_dismissed`

## 3) Install and Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Start API
```bash
uvicorn api.main:app --reload
```
API docs: `http://127.0.0.1:8000/docs`

### Start Streamlit frontend
```bash
streamlit run frontend/app.py
```
Frontend URL usually: `http://localhost:8501`

## 4) API Endpoints

- `GET /api/health`
- `GET /api/summary`
- `GET /api/season-wise`
- `GET /api/venue-stats`
- `GET /api/toss-impact`
- `GET /api/top-performers?limit=10`
- `GET /api/prediction-inputs`
- `GET /api/predict-winner?season=2024&venue=M%20Chinnaswamy%20Stadium&toss_winner=RCB`

## 5) Suggested BCA Report Sections

1. Problem Statement: RCB vs CSK rivalry trend analysis.
2. Objectives: season-wise, venue-wise, toss impact, top players.
3. Tech Stack: Python, FastAPI, Pandas, Streamlit, Plotly.
4. Methodology: data cleaning, alias normalization, filtering H2H matches.
5. Results and Insights.
6. Limitations and Future Scope (predictive modeling, win probability).

## 6) Notes

- Team aliases are normalized (`Royal Challengers Bangalore` and `Royal Challengers Bengaluru` both treated as `RCB`).
- If `deliveries.csv` is missing, project still runs but top performers section is disabled.

## 7) Next Improvements

- Add machine learning model for winner prediction.
- Add player-vs-player matchups.
- Deploy API and frontend on cloud (Render + Streamlit Community Cloud).

## 8) ML Winner Prediction (Added)

- Uses historical RCB vs CSK matches.
- Model: `RandomForestClassifier` with one-hot encoded categorical features.
- Features used:
  - `season`
  - `venue`
  - `toss_winner`
- Target:
  - Match winner (`RCB` or `CSK`)

This is designed for academic demonstration, not betting or professional forecasting.
