# pages/21_Player_Search.py

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

st.title("Administration Page")
st.write("\n\n")
st.write("Options")

# ---------- API location ----------
API_ROOT = os.getenv("API_ROOT", "http://web-api:4000").rstrip("/")

PROFILES_BASE = f"{API_ROOT}"
PROFILES_URL  = f"{PROFILES_BASE}/profiles"                      # list of profiles
PROFILE_URL   = lambda pid: f"{PROFILES_BASE}/profiles/{pid}"    # single profile (unused)

PROFILE_GAMES = lambda pid: f"{API_ROOT}/games/profile/{pid}"    # list games for a profile

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
    """Remove duplicate rows by ID."""
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

# ---------- UI: search + select ----------
term = st.text_input("Name of Player", value="", placeholder="Enter profile name to search").strip()

selected_profile = None
matches = []

if term:
    with st.spinner("Searching..."):
        try:
            all_profiles = fetch_all_profiles()
            t = term.lower()
            matches = [p for p in all_profiles if t in (p["Username"] or "").lower()]
        except requests.RequestException as e:
            st.error(f"Error contacting server: {e}")
        except ValueError:
            st.error("Profiles endpoint did not return JSON")

if matches:
    if len(matches) > 1:
        options = {f'{m["Username"]} (ID {m["ID"]})': m for m in matches}
        chosen = st.selectbox("Multiple matches — choose a profile:", list(options.keys()))
        selected_profile = options[chosen]
    else:
        selected_profile = matches[0]

# ---------- Display ----------
if selected_profile:
    st.subheader("Profile")
    prof_df = pd.DataFrame([selected_profile]).set_index("ID")
    st.table(prof_df)

    st.subheader("Game Profiles")
    try:
        games = fetch_profile_games(selected_profile["ID"])
        games = dedupe_by_id(games, "ID")
        if games:
            games_df = pd.DataFrame(games).set_index("ID")
            st.table(games_df)
        else:
            st.info("This user has no game profiles.")
    except requests.RequestException as e:
        st.error(f"Error loading game profiles: {e}")

elif term:
    st.info("No matching profiles found.")
else:
    st.caption("Type a name to search.")

# ---------- Back button ----------
if st.button("⬅ Back to Admin Home"):
    st.switch_page("pages/17_Jordan_Lee_home.py")
