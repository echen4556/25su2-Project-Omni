# pages/20_Find_Player_And_Game.py

import os
import logging
import requests
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# ---------- Page setup ----------
st.set_page_config(layout="wide")
SideBarLinks()

st.title("Find Player by Game")
st.caption("Search for a user, then choose a game to view their info or stats.")

# ---------- API location ----------
API_ROOT = os.getenv("API_ROOT", "http://web-api:4000").rstrip("/")

# profiles blueprint has prefix + absolute routes -> /profiles/profiles [...]
PROFILES_URL = f"{API_ROOT}/profiles/profiles"           # list all profiles
PROFILE_GAMES = lambda pid: f"{API_ROOT}/games/profile/{pid}"  # list games for a profile

# ---------- Normalizers ----------
def normalize_profiles(raw):
    """
    Backend returns either dict rows or tuples in this order:
    (profileID, username, isAdmin, isPublic, isPremium)
    Normalize to: {"ID","Username","Admin","Public","Premium"}
    """
    if not raw:
        return []
    first = raw[0]
    if isinstance(first, dict):
        return [{
            "ID":        p.get("profileID"),
            "Username":  p.get("username"),
            "Admin":     p.get("isAdmin"),
            "Public":    p.get("isPublic"),
            "Premium":   p.get("isPremium"),
        } for p in raw]
    out = []
    for p in raw:
        pid    = p[0] if len(p) > 0 else None
        uname  = p[1] if len(p) > 1 else None
        admin  = p[2] if len(p) > 2 else None
        public = p[3] if len(p) > 3 else None
        prem   = p[4] if len(p) > 4 else None
        out.append({"ID": pid, "Username": uname, "Admin": admin, "Public": public, "Premium": prem})
    return out

def normalize_games(raw):
    """
    /games/profile/<id> returns either dicts {gameID,name} or tuples (gameID, name)
    Normalize to: {"ID","Name"}
    """
    if not raw:
        return []
    first = raw[0]
    if isinstance(first, dict):
        return [{"ID": g.get("gameID"), "Name": g.get("name")} for g in raw]
    out = []
    for g in raw:
        gid  = g[0] if len(g) > 0 else None
        name = g[1] if len(g) > 1 else None
        out.append({"ID": gid, "Name": name})
    return out

def dedupe_by_id(rows, id_key="ID"):
    seen, out = set(), []
    for r in rows:
        k = r.get(id_key)
        if k in seen:
            continue
        seen.add(k)
        out.append(r)
    return out

# ---------- Data fetchers (cached) ----------
@st.cache_data(ttl=30)
def fetch_all_profiles():
    r = requests.get(PROFILES_URL, timeout=8)
    r.raise_for_status()
    return normalize_profiles(r.json())

@st.cache_data(ttl=15)
def fetch_profile_games(profile_id: int):
    r = requests.get(PROFILE_GAMES(profile_id), timeout=8)
    r.raise_for_status()
    return normalize_games(r.json())

# ---------- UI: search ----------
col_q, col_btn = st.columns([3, 1])
with col_q:
    term = st.text_input("Username", value=st.session_state.pop("player_search_term", ""), placeholder="Start typing a username…").strip()
with col_btn:
    clear = st.button("Clear")
    if clear:
        term = ""
        st.session_state.pop("preselect_profile_id", None)

selected_profile = None
matches = []

if term:
    with st.spinner("Searching users..."):
        try:
            all_profiles = fetch_all_profiles()
            t = term.lower()
            matches = [p for p in all_profiles if t in (p["Username"] or "").lower()]
        except requests.RequestException as e:
            st.error(f"Error contacting server: {e}")
        except ValueError:
            st.error("Profiles endpoint did not return JSON")

# ---------- Choose exact user if needed ----------
pre_pid = st.session_state.pop("preselect_profile_id", None)

if matches:
    st.markdown("#### Matching Users")
    # Display quick table of matches for context
    st.table(pd.DataFrame(matches)[["ID", "Username"]].set_index("ID"))

    if pre_pid is not None:
        selected_profile = next((m for m in matches if m["ID"] == pre_pid), matches[0])
    elif len(matches) > 1:
        options = {f'{m["Username"]} (ID {m["ID"]})': m for m in matches}
        chosen = st.selectbox("Multiple matches — choose a profile:", list(options.keys()))
        selected_profile = options[chosen]
    else:
        selected_profile = matches[0]

# ---------- Show profile + game dropdown ----------
selected_game = None
if selected_profile:
    st.markdown("### Selected Profile")
    st.table(pd.DataFrame([selected_profile]).set_index("ID"))

    st.markdown("### Select Game")
    try:
        games = fetch_profile_games(selected_profile["ID"])
        games = dedupe_by_id(games, "ID")
        if games:
            gopts = {f'{g["Name"]} (ID {g["ID"]})': g for g in games}
            chosen_game = st.selectbox("Game", list(gopts.keys()))
            selected_game = gopts[chosen_game]
        else:
            st.info("This user has no linked games.")
    except requests.RequestException as e:
        st.error(f"Error loading games: {e}")

# ---------- Actions ----------
c1, c2 = st.columns(2)
if c1.button("Open Profile Page", disabled=not bool(selected_profile)):
    st.session_state["player_search_term"] = selected_profile["Username"]
    st.session_state["preselect_profile_id"] = selected_profile["ID"]
    st.switch_page("pages/21_Player_Search.py")

if c2.button("Open Stats Page", disabled=not (selected_profile and selected_game)):
    st.session_state["player_search_term"] = selected_profile["Username"]
    st.session_state["preselect_profile_id"] = selected_profile["ID"]
    st.session_state["selected_game_id"] = selected_game["ID"]
    st.session_state["selected_game_name"] = selected_game["Name"]
    # Change this to your actual stats page path when you have it:
    st.switch_page("pages/22_Player_Stats.py")

# ---------- Back ----------
st.divider()
if st.button("⬅ Back to Admin Home"):
    st.switch_page("pages/17_Jordan_Lee_home.py")
