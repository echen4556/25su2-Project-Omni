import os
import logging
import requests
import pandas as pd
import streamlit as st
from datetime import date
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

# ---------- Page setup ----------
st.set_page_config(layout="wide")
SideBarLinks()
st.title("Player Search")

# ---------- API roots & endpoints ----------
API_ROOT = os.getenv("API_ROOT", "http://web-api:4000").rstrip("/")

# profiles blueprint has prefix + absolute routes -> /profiles/profiles [...]
PROFILES_URL   = f"{API_ROOT}/profiles/profiles"                        # list all profiles
PROFILE_PUT    = lambda pid: f"{API_ROOT}/profiles/profiles/{pid}"      # update one
PROFILE_GAMES  = lambda pid: f"{API_ROOT}/games/profile/{pid}"          # games for profile

# playerStats is mounted at /playerstats
SUMMARY_URL    = lambda pid, gid: f"{API_ROOT}/playerstats/summary/{pid}/{gid}"
WEAPONS_URL    = lambda pid, gid: f"{API_ROOT}/playerstats/weapon/{pid}/{gid}"
MAPS_URL       = lambda pid, gid: f"{API_ROOT}/playerstats/map/{pid}/{gid}"

# gameProfiles (no prefix) — used to discover gameInstanceID
GAME_LINKS_URL = f"{API_ROOT}/gameProfiles"

# ---------- helpers: normalization ----------
def norm_profiles(raw):
    """Raw -> [{'ID','Username','Admin','Public','Premium'}]"""
    if not raw: return []
    first = raw[0]
    if isinstance(first, dict):
        return [{
            "ID":        p.get("profileID"),
            "Username":  p.get("username"),
            "Admin":     p.get("isAdmin"),
            "Public":    p.get("isPublic"),
            "Premium":   p.get("isPremium"),
        } for p in raw]
    # tuples: (profileID, username, isAdmin, isPublic, isPremium)
    out = []
    for t in raw:
        out.append({
            "ID": t[0] if len(t)>0 else None,
            "Username": t[1] if len(t)>1 else None,
            "Admin": t[2] if len(t)>2 else None,
            "Public": t[3] if len(t)>3 else None,
            "Premium": t[4] if len(t)>4 else None,
        })
    return out

def norm_games(raw):
    """Raw -> [{'ID','Name'}] from /games/profile/<pid> (gameID, name)"""
    if not raw: return []
    first = raw[0]
    if isinstance(first, dict):
        return [{"ID": g.get("gameID"), "Name": g.get("name")} for g in raw]
    return [{"ID": t[0] if len(t)>0 else None, "Name": t[1] if len(t)>1 else None} for t in raw]

def dedupe_by_id(rows, id_key="ID"):
    seen, out = set(), []
    for r in rows:
        k = r.get(id_key)
        if k in seen: continue
        seen.add(k); out.append(r)
    return out

def is_truthy(x):
    s = str(x).strip().lower()
    return s in ("1","true","t","yes","y")

# ---------- cached fetchers ----------
@st.cache_data(ttl=30)
def fetch_profiles():
    r = requests.get(PROFILES_URL, timeout=10); r.raise_for_status()
    return norm_profiles(r.json())

@st.cache_data(ttl=20)
def fetch_profile_games(pid: int):
    r = requests.get(PROFILE_GAMES(pid), timeout=10); r.raise_for_status()
    return norm_games(r.json())

@st.cache_data(ttl=20)
def fetch_summary(pid: int, gid: int):
    r = requests.get(SUMMARY_URL(pid, gid), timeout=12); r.raise_for_status()
    return r.json()

@st.cache_data(ttl=20)
def fetch_weapons(pid: int, gid: int):
    r = requests.get(WEAPONS_URL(pid, gid), timeout=12); r.raise_for_status()
    return r.json()

@st.cache_data(ttl=20)
def fetch_maps(pid: int, gid: int):
    r = requests.get(MAPS_URL(pid, gid), timeout=12); r.raise_for_status()
    return r.json()

@st.cache_data(ttl=20)
def fetch_all_game_links():
    # SELECT * FROM gamesProfiles
    r = requests.get(GAME_LINKS_URL, timeout=12); r.raise_for_status()
    return r.json()  # may be list[dict] or list[tuple]

@st.cache_data(ttl=20)
def fetch_matches(pid: int, gid: int, giid: int,
                  match_type: str|None, rank: str|None,
                  start_date: str|None, end_date: str|None):
    params = {}
    if match_type: params["matchType"] = match_type
    if rank: params["rank"] = rank
    if start_date: params["startDate"] = start_date
    if end_date: params["endDate"] = end_date

    candidates = [
        f"{API_ROOT}/matches/profile/{pid}/games/{giid}/matches",  # preferred
        f"{API_ROOT}/matches/profile/{pid}",                      # legacy (filter via query)
    ]
    errors = []
    for i, url in enumerate(candidates):
        try:
            q = params.copy()
            if i == 1:
                # send both, so backend can filter either way
                q["gameInstanceID"] = giid
                q["gameID"] = gid
            r = requests.get(url, params=q, timeout=12)
            if r.status_code == 404:
                errors.append(f"404: {r.url}")
                continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            errors.append(f"{type(e).__name__}: {e}")
    st.error("Failed to load matches:\n" + "\n".join(errors))
    raise requests.HTTPError("All match endpoints failed")


@st.cache_data(ttl=20)
def fetch_match_details(match_id: int, pid: int):
    """Try both shapes depending on how the blueprint route was declared."""
    candidates = [
        f"{API_ROOT}/matches/matches/{match_id}/{pid}",
        f"{API_ROOT}/matches/{match_id}/{pid}",
    ]
    last_err = None
    for url in candidates:
        try:
            r = requests.get(url, timeout=12)
            if r.status_code == 404:
                last_err = f"404: {r.url}"
                continue
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            last_err = f"{type(e).__name__}: {e}"
    st.error(f"Failed to load match details: {last_err}")
    raise requests.HTTPError("All match-detail endpoints failed")

def find_game_instance_id(pid: int, gid: int, summary_payload):
    """
    Prefer gameInstanceID from summary payload (playerStats.*).
    Fallback: scan /gameProfiles for (profileID, gameID) -> gameInstanceID.
    """
    try:
        if isinstance(summary_payload, dict):
            gi = summary_payload.get("gameInstanceID")
            if gi: return int(gi)
        if isinstance(summary_payload, list) and summary_payload and isinstance(summary_payload[0], dict):
            gi = summary_payload[0].get("gameInstanceID")
            if gi: return int(gi)
    except Exception:
        pass
    # Fallback via /gameProfiles
    try:
        rows = fetch_all_game_links()
        if not rows: return None
        first = rows[0]
        if isinstance(first, dict):
            for r in rows:
                if str(r.get("profileID")) == str(pid) and str(r.get("gameID")) == str(gid):
                    gi = r.get("gameInstanceID")
                    if gi is not None: return int(gi)
        else:
            # Likely order: (gameInstanceID, gameID, profileID, gameUsername, showOnDashboard)
            for t in rows:
                gi = t[0] if len(t)>0 else None
                g  = t[1] if len(t)>1 else None
                p  = t[2] if len(t)>2 else None
                if str(p) == str(pid) and str(g) == str(gid) and gi is not None:
                    return int(gi)
    except Exception:
        return None
    return None

# ---------- UI: search user ----------
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

matches, selected_profile = [], None
if term:
    with st.spinner("Searching users..."):
        try:
            allp = fetch_profiles()
            t = term.lower()
            matches = [p for p in allp if t in (p["Username"] or "").lower()]
        except requests.RequestException as e:
            st.error(f"Error contacting server: {e}")

pre_pid = st.session_state.pop("preselect_profile_id", None)
if matches:
    st.markdown("#### Matching Users")
    st.table(pd.DataFrame(matches)[["ID","Username","Premium"]].set_index("ID"))
    if pre_pid is not None:
        selected_profile = next((m for m in matches if m["ID"] == pre_pid), matches[0])
    elif len(matches) > 1:
        options = {f'{m["Username"]} (ID {m["ID"]})': m for m in matches}
        chosen = st.selectbox("Multiple matches — choose a profile:", list(options.keys()))
        selected_profile = options[chosen]
    else:
        selected_profile = matches[0]

# ---------- Game dropdown + Premium gating ----------
selected_game = None
summary_payload = None

if selected_profile:
    st.markdown("### Selected Profile")
    st.table(pd.DataFrame([selected_profile]).set_index("ID"))

    # Games for this profile
    st.markdown("### Select Game")
    try:
        games = dedupe_by_id(fetch_profile_games(selected_profile["ID"]), "ID")
        if games:
            gopts = {f'{g["Name"]} (ID {g["ID"]})': g for g in games}
            chosen_game = st.selectbox("Game", list(gopts.keys()), key="stats_game_choice")
            selected_game = gopts[chosen_game]
        else:
            st.info("This user has no linked games.")
    except requests.RequestException as e:
        st.error(f"Error loading games: {e}")

# ---------- Stats sections (load when both chosen) ----------
if selected_profile and selected_game:
    pid, gid = selected_profile["ID"], selected_game["ID"]
    username = selected_profile["Username"]; game_name = selected_game["Name"]
    st.caption(f"User: **{username}** (ID {pid})  •  Game: **{game_name}** (ID {gid})")

    # --- Summary (always visible) ---
    try:
        with st.spinner("Loading summary..."):
            summary_payload = fetch_summary(pid, gid)
    except requests.RequestException as e:
        st.error(f"Failed to load summary: {e}")
        summary_payload = None

    # Render summary
    summary_dict = summary_payload if isinstance(summary_payload, dict) else (
        summary_payload[0] if isinstance(summary_payload, list) and summary_payload and isinstance(summary_payload[0], dict) else None
    )
    st.subheader("Summary")
    if summary_dict:
        m1, m2, m3, m4 = st.columns(4)
        def val(k): return summary_dict.get(k, 0)
        m1.metric("Kills", val("kills"))
        m2.metric("Deaths", val("deaths"))
        m3.metric("Assists", val("assists"))
        m4.metric("Wins", val("totalWins"))

        # KD & HS%
        try:
            kd = (float(val("kills"))/float(val("deaths"))) if float(val("deaths"))>0 else None
        except Exception:
            kd = None
        try:
            hs_rate = (float(val("totalHeadshots"))/float(val("totalShotsHit"))) if float(val("totalShotsHit"))>0 else None
        except Exception:
            hs_rate = None

        c1, c2 = st.columns(2)
        if kd is not None: c1.metric("K/D", f"{kd:.2f}")
        if hs_rate is not None: c2.metric("Headshot %", f"{hs_rate*100:.1f}%")

        df_sum = pd.DataFrame([summary_dict]).T.reset_index()
        df_sum.columns = ["Metric", "Value"]
        st.table(df_sum.set_index("Metric"))
    elif summary_payload:
        st.table(pd.DataFrame(summary_payload))
    else:
        st.info("No summary stats found.")

    st.divider()

    # --- Premium gating ---
    is_premium = is_truthy(selected_profile.get("Premium"))

    if not is_premium:
        st.warning("Weapons, Maps, and Match History are premium features.")
        # --- Upgrade button (sets isPremium=1 via PUT /profiles/profiles/<pid>) ---
        if st.button("Upgrade to Premium"):
            try:
                body = {
                    "username": selected_profile["Username"],
                    # ensure these stay as their current values
                    "isAdmin": int(bool(selected_profile.get("Admin"))),
                    "isPublic": int(bool(selected_profile.get("Public"))),
                    "isPremium": 1
                }
                r = requests.put(PROFILE_PUT(pid), json=body, timeout=10)
                if r.status_code == 200:
                    # clear cache and refresh
                    fetch_profiles.clear()
                    st.success("Upgraded to Premium. Loading premium stats…")
                    # update local state so sections render without waiting
                    selected_profile["Premium"] = 1
                    st.experimental_rerun()
                else:
                    st.error(f"Upgrade failed: {r.status_code} {r.text}")
            except requests.RequestException as e:
                st.error(f"Upgrade error: {e}")

    else:
        # --- Weapons ---
        try:
            with st.spinner("Loading weapon stats..."):
                weapons_raw = fetch_weapons(pid, gid)
                # normalize
                weapons = weapons_raw if isinstance(weapons_raw, list) else [weapons_raw]
                if weapons and isinstance(weapons[0], dict):
                    dfw = pd.DataFrame(weapons)
                    # Rename if present
                    dfw = dfw.rename(columns={"name": "Weapon", "weaponID": "ID"})
                    sort_key = next((k for k in ("kills","totalUsageTime","accuracy","amountBought") if k in dfw.columns), None)
                    if sort_key: dfw = dfw.sort_values(by=sort_key, ascending=False)
                    if "ID" in dfw.columns: dfw = dfw.set_index("ID")
                else:
                    dfw = pd.DataFrame(weapons)
        except requests.RequestException as e:
            st.error(f"Failed to load weapon stats: {e}")
            dfw = pd.DataFrame()

        st.subheader("Weapons")
        if not dfw.empty:
            st.table(dfw)
        else:
            st.info("No weapon stats found.")
        st.divider()

        # --- Maps ---
        try:
            with st.spinner("Loading map stats..."):
                maps_raw = fetch_maps(pid, gid)
                maps_rows = maps_raw if isinstance(maps_raw, list) else [maps_raw]
                if maps_rows and isinstance(maps_rows[0], dict):
                    dfm = pd.DataFrame(maps_rows).rename(columns={"name": "Map", "mapID": "ID"})
                    sort_key = next((k for k in ("wins","kills","losses") if k in dfm.columns), None)
                    if sort_key: dfm = dfm.sort_values(by=sort_key, ascending=False)
                    if "ID" in dfm.columns: dfm = dfm.set_index("ID")
                else:
                    dfm = pd.DataFrame(maps_rows)
        except requests.RequestException as e:
            st.error(f"Failed to load map stats: {e}")
            dfm = pd.DataFrame()

        st.subheader("Maps")
        if not dfm.empty:
            st.table(dfm)
        else:
            st.info("No map stats found.")
        st.divider()

        # --- Match History (needs gameInstanceID) ---
giid = find_game_instance_id(pid, gid, summary_payload)
st.subheader("Match History")
if not giid:
    st.info("No game link found for match history.")
else:
    # Filters
    fc1, fc2, fc3, fc4 = st.columns([1,1,1,1])
    with fc1:
        match_type = st.text_input("Match Type (optional)", value="")
    with fc2:
        rank = st.text_input("Rank (optional)", value="")
    with fc3:
        start = st.date_input("Start Date (optional)", value=None, format="YYYY-MM-DD")
    with fc4:
        end = st.date_input("End Date (optional)", value=None, format="YYYY-MM-DD")

    start_s = start.strftime("%Y-%m-%d") if isinstance(start, date) else None
    end_s   = end.strftime("%Y-%m-%d") if isinstance(end, date) else None

    try:
        with st.spinner("Loading matches..."):
            matches_raw = fetch_matches(
                pid, gid, giid,
                match_type.strip() or None,
                rank.strip() or None,
                start_s, end_s
            )

        matches = matches_raw if isinstance(matches_raw, list) else [matches_raw]
        if matches and isinstance(matches[0], dict):
            dfmt = pd.DataFrame(matches)
            desired = [c for c in ("matchID","matchDate","matchType","lobbyRank","mapName") if c in dfmt.columns]
            others = [c for c in dfmt.columns if c not in desired]
            dfmt = dfmt[desired + others] if desired else dfmt
            if "matchID" in dfmt.columns:
                dfmt = dfmt.set_index("matchID")
        else:
            dfmt = pd.DataFrame(matches)
    except requests.RequestException as e:
        st.error(f"Failed to load matches: {e}")
        dfmt = pd.DataFrame()

    if not dfmt.empty:
        st.table(dfmt)
    else:
        st.info("No matches found with those filters.")

# ---------- Back ----------
st.divider()
if st.button("⬅ Back to Admin Home"):
    st.switch_page("Home.py")
