import os
import logging
import requests
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout="wide")
SideBarLinks()

st.title("Game Administration Page")
st.write("\n\n")
st.write("Options")

# ---- API location ----
API_ROOT   = os.getenv("API_ROOT", "http://web-api:4000")  # or http://localhost:4000 if running locally
API_PREFIX = os.getenv("API_PREFIX", "")                   # e.g. "/api" if you used a prefix when registering the blueprint
GAMES_URL  = f"{API_ROOT}{API_PREFIX}/games"


# ---- Add Game form ----
with st.form("add_game_form", clear_on_submit=True):
    new_game_name = st.text_input("Name of Game to Add", placeholder="e.g., Chess")
    submitted = st.form_submit_button("Add Game")
    if submitted:
        name = (new_game_name or "").strip()
        if not name:
            st.warning("Please enter a game name.")
        else:
            try:
                r = requests.post(GAMES_URL, json={"name": name}, timeout=8)
                r.raise_for_status()
                st.success(f"Game '{name}' created!")
                st.rerun()  # reload the table with new data
            except requests.RequestException as e:
                st.error(f"Error creating game: {e}")

st.divider()

# ---- Fetch and display games ----
def normalize_games(raw):
    if not raw:
        return []
    first = raw[0]
    if isinstance(first, dict):
        return [{"ID": g.get("gameID"), "Name": g.get("name")} for g in raw]
    if isinstance(first, (list, tuple)):
        return [{"ID": g[0] if len(g) > 0 else None,
                 "Name": g[1] if len(g) > 1 else None} for g in raw]
    return []

games = []
try:
    with st.spinner("Loading games..."):
        resp = requests.get(GAMES_URL, timeout=8)
        resp.raise_for_status()
        games = normalize_games(resp.json())
except requests.RequestException as e:
    st.error(f"Error loading games: {e}")

if games:
    games_sorted = sorted(games, key=lambda g: (g["ID"] is None, g["ID"]))
    st.table(games_sorted)
else:
    st.info("No games found.")

if st.button("⬅ Back to Admin Home"):
    st.switch_page("pages/17_Jordan_Lee_home.py")
