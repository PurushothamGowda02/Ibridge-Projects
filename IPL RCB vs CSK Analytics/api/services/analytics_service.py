from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Dict, List

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

DATA_DIR = Path("data")
MATCHES_FILE = DATA_DIR / "matches.csv"
DELIVERIES_FILE = DATA_DIR / "deliveries.csv"
IPL_COMBINED_FILE = DATA_DIR / "ipl.csv"

RCB_ALIASES = {
    "Royal Challengers Bangalore",
    "Royal Challengers Bengaluru",
    "RCB",
}
CSK_ALIASES = {
    "Chennai Super Kings",
    "CSK",
}


def _canon_team(name: str) -> str:
    if name in RCB_ALIASES:
        return "RCB"
    if name in CSK_ALIASES:
        return "CSK"
    return name


def _winner_label(name: str) -> str:
    if name in RCB_ALIASES:
        return "RCB"
    if name in CSK_ALIASES:
        return "CSK"
    return "No Result"


@lru_cache(maxsize=1)
def load_matches() -> pd.DataFrame:
    if MATCHES_FILE.exists():
        df = pd.read_csv(MATCHES_FILE)
    elif IPL_COMBINED_FILE.exists():
        raw = pd.read_csv(IPL_COMBINED_FILE, low_memory=False)
        required_combined_cols = ["match_id", "season", "date", "team1", "team2", "winner", "venue"]
        missing_combined = [c for c in required_combined_cols if c not in raw.columns]
        if missing_combined:
            raise ValueError(f"ipl.csv missing required columns: {missing_combined}")

        optional_cols = [c for c in ["toss_winner"] if c in raw.columns]
        keep_cols = required_combined_cols + optional_cols
        df = raw[keep_cols].drop_duplicates(subset=["match_id"]).copy()
        df = df.rename(columns={"match_id": "id"})
    else:
        raise FileNotFoundError(
            f"Missing dataset file: {MATCHES_FILE} or {IPL_COMBINED_FILE}. Add one inside data/."
        )

    required_cols = ["id", "season", "date", "team1", "team2", "winner", "venue"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"matches.csv missing required columns: {missing}")

    df["team1_c"] = df["team1"].astype(str).map(_canon_team)
    df["team2_c"] = df["team2"].astype(str).map(_canon_team)

    h2h = df[
        ((df["team1_c"] == "RCB") & (df["team2_c"] == "CSK"))
        | ((df["team1_c"] == "CSK") & (df["team2_c"] == "RCB"))
    ].copy()

    h2h["season"] = h2h["season"].astype(str)
    h2h["date"] = pd.to_datetime(h2h["date"], errors="coerce")
    h2h["winner_label"] = h2h["winner"].astype(str).map(_winner_label)

    return h2h.sort_values("date")


@lru_cache(maxsize=1)
def load_deliveries() -> pd.DataFrame | None:
    if not DELIVERIES_FILE.exists():
        if IPL_COMBINED_FILE.exists():
            df = pd.read_csv(IPL_COMBINED_FILE, low_memory=False)
            if "match_id" not in df.columns:
                return None
            return df
        return None
    else:
        df = pd.read_csv(DELIVERIES_FILE)
        if "match_id" not in df.columns:
            return None
        return df


def summary() -> Dict:
    df = load_matches()
    total = len(df)
    rcb_wins = int((df["winner_label"] == "RCB").sum())
    csk_wins = int((df["winner_label"] == "CSK").sum())
    no_result = total - rcb_wins - csk_wins

    first_match = df["date"].min()
    last_match = df["date"].max()

    return {
        "total_matches": total,
        "rcb_wins": rcb_wins,
        "csk_wins": csk_wins,
        "no_result": no_result,
        "rcb_win_pct": round((rcb_wins / total) * 100, 2) if total else 0,
        "csk_win_pct": round((csk_wins / total) * 100, 2) if total else 0,
        "first_match_date": first_match.strftime("%Y-%m-%d") if pd.notna(first_match) else None,
        "last_match_date": last_match.strftime("%Y-%m-%d") if pd.notna(last_match) else None,
    }


def season_wise() -> List[Dict]:
    df = load_matches().copy()
    grouped = (
        df.groupby(["season", "winner_label"], dropna=False)
        .size()
        .reset_index(name="wins")
        .sort_values("season")
    )
    pivot = grouped.pivot(index="season", columns="winner_label", values="wins").fillna(0)
    pivot = pivot.rename(columns={"RCB": "rcb_wins", "CSK": "csk_wins", "No Result": "no_result"})

    for col in ["rcb_wins", "csk_wins", "no_result"]:
        if col not in pivot.columns:
            pivot[col] = 0

    pivot = pivot.reset_index()
    pivot["total"] = pivot["rcb_wins"] + pivot["csk_wins"] + pivot["no_result"]

    return pivot.to_dict(orient="records")


def venue_stats() -> List[Dict]:
    df = load_matches().copy()
    venue_grp = (
        df.groupby(["venue", "winner_label"], dropna=False)
        .size()
        .reset_index(name="wins")
    )
    return venue_grp.sort_values(["venue", "winner_label"]).to_dict(orient="records")


def toss_impact() -> Dict:
    df = load_matches().copy()

    if "toss_winner" not in df.columns:
        return {"available": False, "message": "toss_winner column missing in matches.csv"}

    toss_win_and_match_win = (df["toss_winner"].astype(str) == df["winner"].astype(str)).sum()
    total = len(df)

    return {
        "available": True,
        "same_team_won_toss_and_match": int(toss_win_and_match_win),
        "percentage": round((toss_win_and_match_win / total) * 100, 2) if total else 0,
    }


def top_performers(limit: int = 10) -> Dict:
    matches_df = load_matches()
    deliveries_df = load_deliveries()

    if deliveries_df is None:
        return {
            "available": False,
            "message": "deliveries.csv missing or invalid. Top performers need ball-by-ball data.",
            "top_batters": [],
            "top_bowlers": [],
        }

    valid_match_ids = set(matches_df["id"].tolist())
    d = deliveries_df[deliveries_df["match_id"].isin(valid_match_ids)].copy()

    if "batter" in d.columns and "batsman_runs" in d.columns:
        bat_col = "batter"
        runs_col = "batsman_runs"
    elif "batter" in d.columns and "runs_scored" in d.columns:
        bat_col = "batter"
        runs_col = "runs_scored"
    elif "batsman" in d.columns and "batsman_runs" in d.columns:
        bat_col = "batsman"
        runs_col = "batsman_runs"
    else:
        bat_col = None
        runs_col = None

    if bat_col and runs_col:
        top_batters = (
            d.groupby(bat_col)[runs_col]
            .sum()
            .sort_values(ascending=False)
            .head(limit)
            .reset_index()
        )
        top_batters.columns = ["player", "runs"]
        top_batters = top_batters.to_dict(orient="records")
    else:
        top_batters = []

    wicket_col = None
    for col in ["is_wicket", "player_dismissed", "player_out"]:
        if col in d.columns:
            wicket_col = col
            break

    top_bowlers = []
    if "bowler" in d.columns and wicket_col:
        if wicket_col == "is_wicket":
            wickets_df = d[d["is_wicket"] == 1]
        elif wicket_col == "player_dismissed":
            wickets_df = d[d["player_dismissed"].notna() & (d["player_dismissed"].astype(str) != "")]
        else:
            wickets_df = d[d["player_out"].notna() & (d["player_out"].astype(str) != "")]

        top_bowlers = (
            wickets_df.groupby("bowler")
            .size()
            .sort_values(ascending=False)
            .head(limit)
            .reset_index(name="wickets")
            .rename(columns={"bowler": "player"})
            .to_dict(orient="records")
        )

    return {
        "available": True,
        "top_batters": top_batters,
        "top_bowlers": top_bowlers,
    }


@lru_cache(maxsize=1)
def train_winner_model():
    df = load_matches().copy()
    if "toss_winner" not in df.columns:
        raise ValueError("toss_winner column missing in matches.csv")

    model_df = df[df["winner_label"].isin(["RCB", "CSK"])].copy()
    if len(model_df) < 8:
        raise ValueError("Not enough historical matches to train ML model.")

    model_df["toss_winner_c"] = model_df["toss_winner"].astype(str).map(_canon_team)
    model_df["season"] = model_df["season"].astype(str)
    model_df["venue"] = model_df["venue"].astype(str)

    x = model_df[["season", "venue", "toss_winner_c"]]
    y = model_df["winner_label"]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["season", "venue", "toss_winner_c"])
        ]
    )
    clf = RandomForestClassifier(n_estimators=300, random_state=42)
    model = Pipeline([("prep", preprocessor), ("clf", clf)])
    model.fit(x, y)
    return model


def prediction_inputs() -> Dict:
    df = load_matches().copy()
    seasons = sorted(df["season"].dropna().astype(str).unique().tolist())
    venues = sorted(df["venue"].dropna().astype(str).unique().tolist())
    return {"seasons": seasons, "venues": venues, "teams": ["RCB", "CSK"]}


def predict_winner(season: str, venue: str, toss_winner: str) -> Dict:
    model = train_winner_model()
    toss_winner = _canon_team(toss_winner)
    if toss_winner not in {"RCB", "CSK"}:
        raise ValueError("toss_winner must be RCB or CSK")

    x_pred = pd.DataFrame(
        [{"season": str(season), "venue": str(venue), "toss_winner_c": toss_winner}]
    )
    probs = model.predict_proba(x_pred)[0]
    labels = list(model.classes_)
    prob_map = {labels[i]: round(float(probs[i]) * 100, 2) for i in range(len(labels))}

    predicted = max(prob_map, key=prob_map.get)
    return {
        "predicted_winner": predicted,
        "probabilities": {"RCB": prob_map.get("RCB", 0.0), "CSK": prob_map.get("CSK", 0.0)},
        "note": "Educational ML prediction based on historical RCB vs CSK matches.",
    }
