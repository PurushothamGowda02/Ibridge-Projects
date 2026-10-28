import os

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE_URL", "http://127.0.0.1:8000/api")

st.set_page_config(page_title="IPL RCB vs CSK Analytics", page_icon="??", layout="wide")
st.title("IPL Head-to-Head: RCB vs CSK (2008 to Present)")
st.caption("BCA Final Year Project Dashboard using FastAPI + Streamlit")


def get_json(endpoint: str):
    url = f"{API_BASE}/{endpoint.lstrip('/')}"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.json()


try:
    summary = get_json("summary")
except Exception as e:
    st.error(f"API or data error: {e}")
    st.stop()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Matches", summary["total_matches"])
c2.metric("RCB Wins", summary["rcb_wins"])
c3.metric("CSK Wins", summary["csk_wins"])
c4.metric("RCB Win %", f"{summary['rcb_win_pct']}%")
c5.metric("CSK Win %", f"{summary['csk_win_pct']}%")

st.write(
    f"Date Range: **{summary['first_match_date']}** to **{summary['last_match_date']}** | "
    f"No Result Matches: **{summary['no_result']}**"
)

st.subheader("Season-wise Head-to-Head")
season_data = get_json("season-wise")
season_df = pd.DataFrame(season_data)
if not season_df.empty:
    long_df = season_df.melt(
        id_vars=["season"],
        value_vars=["rcb_wins", "csk_wins", "no_result"],
        var_name="team",
        value_name="wins",
    )
    long_df["team"] = long_df["team"].replace(
        {"rcb_wins": "RCB", "csk_wins": "CSK", "no_result": "No Result"}
    )

    fig = px.bar(
        long_df,
        x="season",
        y="wins",
        color="team",
        barmode="group",
        title="Season-wise Wins",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No season-wise data available.")

st.subheader("Venue-wise Outcomes")
venue_data = get_json("venue-stats")
venue_df = pd.DataFrame(venue_data)
if not venue_df.empty:
    fig2 = px.bar(
        venue_df,
        x="venue",
        y="wins",
        color="winner_label",
        title="Wins by Venue",
    )
    fig2.update_layout(xaxis_tickangle=-40)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No venue data available.")

st.subheader("Toss Impact")
toss = get_json("toss-impact")
if toss.get("available"):
    st.write(
        f"In **{toss['same_team_won_toss_and_match']}** matches, the team that won the toss also won the match "
        f"(**{toss['percentage']}%**)."
    )
else:
    st.warning(toss.get("message", "Toss data unavailable."))

st.subheader("Top Performers in RCB vs CSK")
limit = st.slider("Top N Players", min_value=3, max_value=20, value=10)
performers = get_json(f"top-performers?limit={limit}")
if not performers.get("available"):
    st.warning(performers.get("message", "Top performer data unavailable."))
else:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Top Batters (Runs)**")
        batters_df = pd.DataFrame(performers.get("top_batters", []))
        st.dataframe(batters_df, use_container_width=True)

    with col2:
        st.markdown("**Top Bowlers (Wickets)**")
        bowlers_df = pd.DataFrame(performers.get("top_bowlers", []))
        st.dataframe(bowlers_df, use_container_width=True)

st.subheader("Winner Prediction (ML Demo)")
try:
    pred_inputs = get_json("prediction-inputs")
    seasons = pred_inputs.get("seasons", [])
    venues = pred_inputs.get("venues", [])
except Exception as e:
    st.warning(f"Prediction module unavailable: {e}")
    seasons, venues = [], []

if seasons and venues:
    p1, p2, p3 = st.columns(3)
    with p1:
        season_sel = st.selectbox("Season", seasons, index=len(seasons) - 1)
    with p2:
        venue_sel = st.selectbox("Venue", venues)
    with p3:
        toss_sel = st.selectbox("Toss Winner", ["RCB", "CSK"])

    if st.button("Predict Winner"):
        pred = get_json(
            f"predict-winner?season={season_sel}&venue={venue_sel}&toss_winner={toss_sel}"
        )
        st.success(f"Predicted Winner: {pred['predicted_winner']}")
        prob_df = pd.DataFrame(
            {
                "Team": ["RCB", "CSK"],
                "Probability (%)": [
                    pred["probabilities"].get("RCB", 0.0),
                    pred["probabilities"].get("CSK", 0.0),
                ],
            }
        )
        st.bar_chart(prob_df.set_index("Team"))
        st.caption(pred.get("note", ""))

st.divider()
st.caption("Developed for academic analytics and visualization of IPL rivalry trends.")
