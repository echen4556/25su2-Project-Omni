# pages/22_Player_Stats.py

import os
import logging
import json
import requests
import pandas as pd
import streamlit as st
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# ---------- Page setup ----------
st.set_page_config(layout="wide")
SideBarLinks()
st.title("Player Stats")

# ---------- API location ----------
API_ROOT = os.getenv("API_ROOT", "http://web-api:4000").rstrip("/")

# profiles blueprint has prefix + absolute routes -> /profiles/profiles [...]
PROFILES_URL  = f"{API_ROOT}/profiles/profiles"                    # list all profiles
PROFILE_GAMES = lambda pid: f"{API_ROOT}/games/profile/{pid}"      # list games for a profile

# playerStats blueprint is mounted with url_prefix="/playerstats"
SUMMARY_URL   = lambda pid, gid: f"{API_ROOT}/playerstats/summary/{pid}/{gid}"
WEAPONS_URL   = lambda pid, gid: f"{API_ROOT}/playerstats/weapon/{pid}/{gid}"
MAPS_URL      = lambda pid, gid: f"{API_ROOT}/playerstats/map/{pid}/{gid}"

# ---------- Normalizers ----------
def normalize_profiles(raw):
    """Raw rows -> [{'ID','Username',...}]"""
    if not raw: return []
    first = raw[0]
    if isinstance(first, dict):
        return [{"ID": p.get("profileID"), "Username": p.get("username")} for p in raw]
    out = []
    for p in raw:  # tuples: (profileID, username, isAdmin, isPublic, isPremium)
        pid = p[0] if len(p) > 0 else None
        uname = p[1] if len(p) > 1 else None
        out.append({"ID": pid, "Username": uname})
    return out

def normalize_games(raw):
    """Raw rows -> [{'ID','Name'}]"""
    if not raw: return []
    first = raw[0]
    if isinstance(first, dict):
        return [{"ID": g.get("gameID"), "Name": g.get("name")} for g in raw]
    out = []
    for g in raw:  # tuples: (gameID, name)
        gid  = g[0] if len(g) > 0 else None
        name = g[1] if len(g) > 1 else None
        out.append({"ID": gid, "Name": name})
    return out

def dedupe_by_id(rows, id_key="ID"):
    seen, out = set(), []
    for r in rows:
        k = r.get(id_key)
        if k in seen: continue
        seen.add(k); out.append(r)
    return out

def normalize_row_list(raw, rename=None):
    """
    Accept list[dict] or list[tuple]; return list[dict].
    Optional key rename, e.g. {'name':'Weapon','weaponID':'ID'}
    """
    if raw is None: return []
    rows = raw if isinstance(raw, list) else [raw]
    if not rows: return []
    out = []
    if isinstance(rows[0], dict):
        for d in rows:
            d2 = dict(d)
            if rename:
                for old, new in rename.items():
                    if old in d2: d2[new] = d2.pop(old)
            out.append(d2)
        return out
    width = max(len(r) for r in rows)
    cols = [f"c{i+1}" for i in range(width)]
    for r in rows:
        out.append({cols[i]: (r[i] if i < len(r) else None) for i in range(width)})
    return out

# ---------- Cached fetchers ----------
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

def safe_get_json(url: str):
    r = requests.get(url, timeout=12)
    r.raise_for_status()
    return r.json()

# ---------- UI: search + select ----------
top = st.container()
with top:
    col_q, col_clear = st.columns([3,1])
    with col_q:
        term = st.text_input(
            "Username",
            value=st.session_state.pop("player_search_term", ""),
            placeholder="Start typing a username…"
        ).strip()
    with col_clear:
        if st.button("Clear"):
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

    pre_pid = st.session_state.pop("preselect_profile_id", None)

    if matches:
        st.markdown("#### Matching Users")
        st.table(pd.DataFrame(matches)[["ID","Username"]].set_index("ID"))
        if pre_pid is not None:
            selected_profile = next((m for m in matches if m["ID"] == pre_pid), matches[0])
        elif len(matches) > 1:
            options = {f'{m["Username"]} (ID {m["ID"]})': m for m in matches}
            chosen = st.selectbox("Multiple matches — choose a profile:", list(options.keys()))
            selected_profile = options[chosen]
        else:
            selected_profile = matches[0]

# ---------- Game dropdown ----------
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
            chosen_game = st.selectbox("Game", list(gopts.keys()), key="stats_game_choice")
            selected_game = gopts[chosen_game]
        else:
            st.info("This user has no linked games.")
    except requests.RequestException as e:
        st.error(f"Error loading games: {e}")

# ---------- Stats sections (appear when both chosen) ----------
if selected_profile and selected_game:
    pid, gid = selected_profile["ID"], selected_game["ID"]
    username = selected_profile["Username"]; game_name = selected_game["Name"]
    st.caption(f"User: **{username}** (ID {pid})  •  Game: **{game_name}** (ID {gid})")

    # --- Summary ---
    try:
        with st.spinner("Loading summary..."):
            summary_raw = safe_get_json(SUMMARY_URL(pid, gid))
    except requests.RequestException as e:
        st.error(f"Failed to load summary: {e}")
        summary_raw = None

    summary_dict = summary_raw if isinstance(summary_raw, dict) else (
        summary_raw[0] if isinstance(summary_raw, list) and summary_raw and isinstance(summary_raw[0], dict) else None
    )

    st.subheader("Summary")
    if summary_dict:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Kills", int(summary_dict.get("kills", 0)) if str(summary_dict.get("kills", "")).isdigit() else summary_dict.get("kills", 0))
        m2.metric("Deaths", int(summary_dict.get("deaths", 0)) if str(summary_dict.get("deaths", "")).isdigit() else summary_dict.get("deaths", 0))
        m3.metric("Assists", int(summary_dict.get("assists", 0)) if str(summary_dict.get("assists", "")).isdigit() else summary_dict.get("assists", 0))
        m4.metric("Wins", int(summary_dict.get("totalWins", 0)) if str(summary_dict.get("totalWins", "")).isdigit() else summary_dict.get("totalWins", 0))

        # KD and Headshot %
        try:
            k = float(summary_dict.get("kills", 0)); d = float(summary_dict.get("deaths", 0))
            kd = (k / d) if d > 0 else None
        except Exception:
            kd = None
        try:
            hs = float(summary_dict.get("totalHeadshots", 0)); hits = float(summary_dict.get("totalShotsHit", 0))
            hs_rate = (hs / hits) if hits > 0 else None
        except Exception:
            hs_rate = None

        c1, c2 = st.columns(2)
        if kd is not None: c1.metric("K/D", f"{kd:.2f}")
        if hs_rate is not None: c2.metric("Headshot %", f"{hs_rate*100:.1f}%")

        df_sum = pd.DataFrame([summary_dict]).T.reset_index()
        df_sum.columns = ["Metric", "Value"]
        st.table(df_sum.set_index("Metric"))
    elif summary_raw:
        rows = normalize_row_list(summary_raw)
        st.table(pd.DataFrame(rows))
    else:
        st.info("No summary stats found.")

    st.divider()

    # --- Weapons ---
    try:
        with st.spinner("Loading weapon stats..."):
            weapons_raw = safe_get_json(WEAPONS_URL(pid, gid))
            weapons = normalize_row_list(weapons_raw, rename={"name": "Weapon", "weaponID": "ID"})
    except requests.RequestException as e:
        st.error(f"Failed to load weapon stats: {e}")
        weapons = []

    if weapons:
        dfw = pd.DataFrame(weapons)
        sort_key = next((k for k in ("kills","totalUsageTime","accuracy","amountBought") if k in dfw.columns), None)
        if sort_key: dfw = dfw.sort_values(by=sort_key, ascending=False)
        if "ID" in dfw.columns: dfw = dfw.set_index("ID")
        st.subheader("Weapons")
        st.table(dfw)
    else:
        st.info("No weapon stats found.")
    st.divider()

    # --- Maps ---
    try:
        with st.spinner("Loading map stats..."):
            maps_raw = safe_get_json(MAPS_URL(pid, gid))
            maps_list = normalize_row_list(maps_raw, rename={"name": "Map", "mapID": "ID"})
    except requests.RequestException as e:
        st.error(f"Failed to load map stats: {e}")
        maps_list = []

    if maps_list:
        dfm = pd.DataFrame(maps_list)
        sort_key = next((k for k in ("wins","kills","losses") if k in dfm.columns), None)
        if sort_key: dfm = dfm.sort_values(by=sort_key, ascending=False)
        if "ID" in dfm.columns: dfm = dfm.set_index("ID")
        st.subheader("Maps")
        st.table(dfm)
    else:
        st.info("No map stats found.")

# ---------- Back ----------
st.divider()
if st.button("⬅ Back to Home"):
    st.switch_page("Home.py")
